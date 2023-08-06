#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent, muBVC
from fmqlutils.cacher.cacherUtils import metaOfVistA, BASE_LOCN_TEMPL
from fmqlutils.typer.reduceTypeUtils import splitTypeDatas, checkDataPresent, singleValue, combineSubTypes, muBVCOfSTProp
from fmqlreports.webReportUtils import TOP_MD_TEMPL, SITE_DIR_TEMPL, keyStats, flattenFrequencyDistribution, roundFloat, reduce200
from .userClassifier import UserClassifier

"""
TODO:
- # of days (re-adjust reduction to see)
- order by duration x so where so at least count of 1 (even if duration 0)
- treat DoD special? ie/ 200_1?
- locals how? (and mixes?)
  - also issue of 'remote' but from local station?
- turn README into Excel Header (will do a combo excel, wiki instruction for import)
"""

"""
Subset of Report - CSV different options
"""
def csvUser(stationNo, deidentify=False):

    print("Preparing to make csv for {}{} - loading data ...".format(stationNo, " [DEIDENTIFY]" if deidentify else ""))
    
    if not os.path.isdir(BASE_LOCN_TEMPL.format(stationNo)):
        raise Exception("No setup for Station {}".format(stationNo))
    def ensureLocation(locn):
        if not os.path.isdir(locn):
            os.mkdir(locn)
        return locn
    csvDirBase = BASE_LOCN_TEMPL.format(stationNo) + "CSV/"
    ensureLocation(csvDirBase)
    csvDir = csvDirBase + "Users{}/".format("" if not deidentify else "DEID")
    ensureLocation(csvDir)
        
    meta = metaOfVistA(stationNo)
    if not ("name" in meta and "cutDate" in meta):
        raise Exception("Don't expect to be here if can't know name or cut date")
    vistaName = meta["name"]
    cutDate = meta["cutDate"]
    cutDateDT = datetime.strptime(cutDate.split("T")[0], "%Y-%m-%d")
    day90DateDT = cutDateDT - relativedelta(days=90)
    onAndAfterDay = datetime.strftime(day90DateDT, "%Y-%m-%d")
    upToDay = cutDate
    lastDayDT = cutDateDT - relativedelta(days=1)
    lastDay = datetime.strftime(lastDayDT, "%Y-%m-%d")
        
    dumpREADME(csvDir, vistaName, stationNo, cutDate, onAndAfterDay, lastDay, deidentify)

    allThere, details = checkDataPresent(stationNo, [
        # Additional settings/properties:
        # - duration (in seconds) 
        # - force count on 
        #     ipv4_address, remote_station_id, remote_user_ien, duration
        {"fileType": "3_081", "check": "DAY90E"},
        {"fileType": "200", "check": "ALL"} # Index
    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    userInfoByUserRef = reduce200(stationNo) 
 
    """
    Consider: if need to break by device (ie/ segment off SSH etc? See sniff) and
    how to round out DOD USER breakdown ... are there any other 'CAPRI anyone' users
    that must be broken too ie/ not just one remote user => must break out for remote
    analysis ... 'is_remote_200_1'?
    """
    print("Loading subtypes ...")
    type3_081, st3_081ULRs = splitTypeDatas(stationNo, "3_081", reductionLabel="DAY90E", expectSubTypeProperties=["user", "level_of_assurance", "remote_app", "remote_200_user_ien", "workstation_label", "workstation_type", "remote_station_id", "device"])
    st3_081sByUserRef = defaultdict(list)
    for st in st3_081ULRs:
        userRef = singleValue(st, "user")
        st3_081sByUserRef[userRef].append(st)

    # Classify needs combo
    print("Recombining subtypes by user (backward compatible) ...")
    sts3_081Us = combineSubTypes(st3_081ULRs, ["user"], forceCountProps=["ipv4_address", "remote_station_id", "remote_user_ien", "duration"])
    print("... done")
    st3_081ByUserRef = dict((singleValue(st, "user"), st) for st in sts3_081Us if "user" in st)
    userClassifier = UserClassifier(stationNo, userInfoByUserRef, type3_081, st3_081ByUserRef)
    print("Classifying Users ...")
    classification = userClassifier.classify()
    print("... Classification complete")
        
    csvRemoteUsers(
        csvDir,
        classification["activeRemoteUserRefs"],
        userInfoByUserRef, 
        st3_081sByUserRef,
        st3_081ByUserRef,
        deidentify        
    )
    
def csvRemoteUsers(csvDir, activeRemoteUserRefs, userInfoByUserRef, st3_081sByUserRef, st3_081ByUserRef, deidentify):

    print("CSVing Remote Users ...")
    
    """
    Will move to classify
    """
    def extraEnforce(userRef, stsOfUser):
        for st in stsOfUser:
            if "remote_app" in st:
                remoteApp = singleValue(st, "remote_app")
                if re.match(r'MEDICAL DOMAIN WEB SERVICES', remoteApp) and singleValue(st, "level_of_assurance") != "1":
                    print(json.dumps(st, indent=4))
                    raise Exception("MDWS not LOA 1")
            elif singleValue(st, "level_of_assurance") != "1":
                print(json.dumps(st, indent=4))
                raise Exception("UNIDENTIFIED Remote App and LOA 2 - why remote?")
    
    remoteApps = sorted(list(set(
        singleValue(st, "remote_app") for userRef in st3_081sByUserRef for st in st3_081sByUserRef[userRef] if "remote_app" in st
    )))
    if sum(1 for userRef in st3_081sByUserRef for st in st3_081sByUserRef[userRef] if "remote_app" not in st):
        remoteApps.append("UNIDENTIFIED")
    nnRemoteApps = []
    for remoteApp in remoteApps:
        if re.match(r'MEDICAL DOMAIN WEB SERVICES', remoteApp):
            nnRemoteApp = "JLV"
        else:
            nnRemoteApp = re.sub(r'^VISTA IMAGING ', '', re.sub(r' DISPLAY$', '', remoteApp.split(" [")[0])).split("-")[0]
        nnRemoteApps.append(nnRemoteApp)
    
    cols = ["Last", "First", "SSN", "Local IEN", "Entered", "Remote Stations", "SOs", "First SO", "Last SO"]
    cols.extend(nnRemoteApps)
    
    fl = open("{}remoteUsers{}.csv".format(csvDir, "DEID" if deidentify else ""), "w")
    fl.write("{}\n".format(",".join([str(item) for item in cols])))
    
    print("Writing Remote Users ...")
    for i, userRef in enumerate(sorted(
        activeRemoteUserRefs, 
        key=lambda x: sum(st["_total"] for st in st3_081sByUserRef[x]),
        reverse=True
    )):
    
        extraEnforce(userRef, st3_081sByUserRef[userRef])
        
        userInfo = userInfoByUserRef[userRef] 
        userName = userRef.split(" [")[0]
        userNamePieces = userName.split(",")
        if len(userNamePieces) > 2:
            print("*** Only expected two pieces in names: {}".format(userName))
        lastName = userNamePieces[0]
        firstName = userNamePieces[1]
        if deidentify:
            firstName = firstName[0] + re.sub(r'[A-Za-z]', "X", firstName[1:])
            lastName = lastName[0] + re.sub(r'[A-Za-z]', "X", lastName[1:])
        userIEN = re.search(r'\-(\d+)\]', userRef).group(1)
        userEntered = userInfo["date_entered"] if "date_entered" in userInfo else ""
        userSSN = ("" if "ssn" not in userInfo else userInfo["ssn"]) if not deidentify else "XXXXXXXXX"
        row = [lastName, firstName, userSSN, userIEN, userEntered]

        remoteStationIds = sorted(list(set(remoteStationId if remoteStationId == "200CORP" else remoteStationId[0:3] for st in st3_081sByUserRef[userRef] for remoteStationId in st["remote_station_id"]["byValueCount"])))
        row.append("/".join(remoteStationIds))

        totalSignOns = sum(st["_total"] for st in st3_081sByUserRef[userRef])
        firstSignOn = sorted([st["date_time"]["firstCreateDate"].split("T")[0] for st in st3_081sByUserRef[userRef]])[0]
        lastSignOn = sorted([st["date_time"]["lastCreateDate"].split("T")[0] for st in st3_081sByUserRef[userRef]], reverse=True)[0]
        row.extend([totalSignOns, firstSignOn, lastSignOn])
        
        stByRemoteApp = dict((singleValue(st, "remote_app", ifMissingValue="UNIDENTIFIED"), st) for st in st3_081sByUserRef[userRef])
        for remoteApp in remoteApps:
            if remoteApp not in stByRemoteApp:
                row.append("")
                continue
            stRemoteApp = stByRemoteApp[remoteApp]
            if not ("duration" in stRemoteApp and "byValueCount" in stRemoteApp["duration"]):
                row.append(stRemoteApp["_total"])
                continue
            if stRemoteApp["_total"] > 1:
                kstatsDur = keyStats(
                    flattenFrequencyDistribution(stRemoteApp["duration"]["byValueCount"])
                )
                durMed = muSeconds(kstatsDur["median"])
            else:
                durMed = muSeconds(singleValue(stRemoteApp, "duration"))
            row.append("{} [{}]".format(stRemoteApp["_total"], durMed)) 
        
        fl.write("{}\n".format(",".join([str(item) for item in row])))
        
    print("... wrote {:,}".format(i))

    fl.close()
   
"""
TODO: may evolve to or do parallel CSV form so can put into cover page of an excel
""" 

README_TEMPL = """# Users from {} [{}]
{}
Data in Excel-compatible CSV about the users who logged into VistA Spokane over its latest 90 days. This VistA copy was cut on _{}_ so this user data is for the period of _{}_ through _{}_.

  * remoteUsers: users whose home VistA is elsewhere and who logged into this VistA using a range of applications from JLV to TeleReader during this 90 days. The first columns identify a user, with social security number, station number of the user's home VistA and the IEN of the user's record in this VistA's user file and the home VistA's user file. The application columns give the total number of signons for an application by a user and the median duration, day/hour/minute/second, is in square brackets. The reason JLV has such high numbers for signons and low durations is that a typical JLV session signs on 12 times into a VistA.
"""

README_DEID_QUAL = """
__Note__: "DEID" means de-identified which X's names and socials. An unredacted equivalent of this dataset is available.
"""

def dumpREADME(csvDir, vistaName, stationNo, cutDate, onAndAfterDay, lastDay, deidentify):

    README = README_TEMPL.format(
        vistaName,
        stationNo,
        
        README_DEID_QUAL if deidentify else "",
        
        cutDate,
        onAndAfterDay,
        lastDay
    )
    open(csvDir + "README_USERS{}.txt".format("_DEID" if deidentify else ""), "w").write(README)
    
# ######################### Utilities #######################
        
def muSeconds(seconds):
    seconds = int(seconds)
    (days, remainder) = divmod(seconds, 86400)
    (hours, remainder) = divmod(remainder, 3600)
    (minutes, seconds) = divmod(remainder, 60)
    if days:
        return "{} {}:{}:{}".format(
            int(days),
            int(hours),
            int(minutes),
            int(seconds)
        )
    if hours:
        return "{}:{}:{}".format(
            int(hours),
            int(minutes),
            int(seconds)
        )
    if minutes:
        return "{}:{}".format(
            int(minutes),
            int(seconds)
        )
    return int(seconds)
            
# ################################# DRIVER #######################
               
def main():

    assert sys.version_info >= (3, 6)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO [DEID]")

    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    if not os.path.isdir(userSiteDir):
        raise SystemExit("Expect User Site to already exist with its basic contents")
    
    if len(sys.argv) == 3:
        deidentify = True
    else:
        deidentify = False
    
    csvUser(stationNo, deidentify)
    
if __name__ == "__main__":
    main()
