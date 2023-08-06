#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime, date

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent, muBVC
from fmqlutils.typer.reduceTypeUtils import splitTypeDatas, checkDataPresent, singleValue, combineSubTypes, muBVCOfSTProp

from ..webReportUtils import TOP_MD_TEMPL, SITE_DIR_TEMPL, ensureWebReportLocations, keyStats, flattenFrequencyDistribution, roundFloat, reduce200
from .userClassifier import UserClassifier
from .USER_CONSTANTS import SSNO_DEFINITIONS

"""
Basic User Type Summary/Overview

Unlike the stopcode centric reports (off locations), these are used and institution centered. Approach is PER USER STs and then Categorize Users (=> STs) as REMOTE
etc.

Requires:
- 3.081 (Type Reduction by User: YR1 
- 200 (All/Indexed-reduce200)
- ... Will move to require image logs too to round out

TODO: classification is work in progress - remotes from non key institution, locals
from non subordinate divisions etc.

Graph It To Emulate:
https://matplotlib.org/gallery/showcase/bachelors_degrees_by_gender.html#sphx-glr-gallery-showcase-bachelors-degrees-by-gender-py - any dimension for users over time ... types of user?
"""
def webReportUser(stationNo, deidentify=False):

    print("Preparing to make user report for {}{} - loading data ...".format(stationNo, " [DEIDENTIFY]" if deidentify else ""))

    allThere, details = checkDataPresent(stationNo, [
        # Additional settings/properties:
        # - duration (in seconds) 
        # - force count on 
        #     ipv4_address, remote_station_id, remote_user_ien, duration
        {"fileType": "3_081", "check": "YR1E"}
    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    mu = TOP_MD_TEMPL.format("{} Users".format(stationNo), "Users")

    userInfoByUserRef = reduce200(stationNo) 
 
    """
    Consider: if need to break by device (ie/ segment off SSH etc? See sniff) and
    how to round out DOD USER breakdown ... are there any other 'CAPRI anyone' users
    that must be broken too ie/ not just one remote user => must break out for remote
    analysis
    """
    print("Loading subtypes ...")
    try:
        type3_081, st3_081URLDs = splitTypeDatas(stationNo, "3_081", reductionLabel="YR1E", expectSubTypeProperties=["user", "level_of_assurance", "remote_app", "remote_200_user_ien", "workstation_label", "workstation_type", "remote_station_id", "device"])
    except:
        print("Can't split type data - exiting")
    sts3_081ByUserRef = defaultdict(list)
    for st in st3_081URLDs:
        userRef = singleValue(st, "user")
        sts3_081ByUserRef[userRef].append(st)
    
    # BACKWARD COMPATIBLE ... TODO: make work with ULRD (and only recombine down below 
    # where needed)
    print("Recombining subtypes by user (backward compatible) ...")
    sts3_081Us = combineSubTypes(st3_081URLDs, ["user"], forceCountProps=["ipv4_address", "remote_station_id", "remote_user_ien", "duration"])
    print("... done")
    st3_081ByUserRef = dict((singleValue(st, "user"), st) for st in sts3_081Us if "user" in st)
    userClassifier = UserClassifier(stationNo, userInfoByUserRef, type3_081, st3_081ByUserRef)
    print("Classifying Users ...")
    classification = userClassifier.classify()
    print("... Classification complete")

    if "_createDateProp" not in type3_081:
        raise Exception("YR1 3.081's must have create date prop")
    createDatePropInfo = type3_081[type3_081["_createDateProp"]]
    overallFirstSODate = createDatePropInfo["firstCreateDate"].split("T")[0]
    overallLastSODate = createDatePropInfo["lastCreateDate"].split("T")[0]
        
    BLURB_TEMPL = """Of the <span class='yellowIt'>{:,}</span> users known to the system, a minority <span class='yellowIt'>{}</span> ("__Active Users__") signed in between {} and {}, {}.

Most Active Users are real people but there are "__Machine Users__" for specialized VA batch applications or applications which manage end users themselves.

"""

    mu += BLURB_TEMPL.format(
        len(userInfoByUserRef),
        reportAbsAndPercent(len(classification["activeUserRefs"]), len(userInfoByUserRef)),
        overallFirstSODate, 
        overallLastSODate,
        "the most recent year for which data is available"
    )  
    
    if deidentify:
        mu += "__DE-IDENTIFIED__: the names and national identifiers of real (Non-Machine) end users have been scrubbed from this report. VistA-specific IENs are left to identify such users for those with access to the system.\n\n"
            
    tbl = MarkdownTable([":Type", "Users", "SignOns"], includeNo=False)
    tbl.addRow([
        "Total Users (200 entries)", 
        len(userInfoByUserRef),
        ""
    ])
    tbl.addRow([
        "Active Users (3.081s for period)", 
        reportAbsAndPercent(len(classification["activeUserRefs"]), len(userInfoByUserRef)),
        type3_081["_total"]
    ])
    tbl.addRow([
        "DoD User",
        re.search(r'\[200\-([^\]]+)', classification["dodUserRef"]).group(1),
        reportAbsAndPercent(
            st3_081ByUserRef[classification["dodUserRef"]]["_total"],
            type3_081["_total"]
        )
    ])
    tbl.addRow([
        "Postmaster",
        muUserRef(classification["postmasterUserRef"]),
        reportAbsAndPercent(
            st3_081ByUserRef[classification["postmasterUserRef"]]["_total"],
            type3_081["_total"]
        )
    ])
    tbl.addRow([
        "Active __Proxy Users__", 
        len(classification["activeProxyUserRefs"]),
        reportAbsAndPercent(
            sum(st3_081ByUserRef[userRef]["_total"] for userRef
 in classification["activeProxyUserRefs"]),
            type3_081["_total"]
        )
    ])  
    tbl.addRow([
        "Active __(Non Proxy) Machine Users__", 
        len(classification["activeNonProxyMachineUserRefs"]),
        reportAbsAndPercent(
            sum(st3_081ByUserRef[userRef]["_total"] for userRef
 in classification["activeNonProxyMachineUserRefs"]),
            type3_081["_total"]
        )
    ])
    for usrCls, label in [
        ("activeRemoteUserRefs", "Active __Remote Users__"),
        ("activeLocalUserRefs", "Active __Local Users__"),
        ("activeNotCategorizedUserRefs", "Active __Uncategorized__")
    ]:
        if len(classification[usrCls]):
            tbl.addRow([
                label, 
                reportAbsAndPercent(len(classification[usrCls]), len(classification["activeUserRefs"])),
                reportAbsAndPercent(
                    sum(st3_081ByUserRef[userRef]["_total"] for userRef
 in classification[usrCls]),
                    type3_081["_total"]
                )
            ])
    
    mu += "User type signon summary ...\n\n"
    mu += tbl.md() + "\n\n"
    
    mu += "Signon by week day ...\n\n"
    mu += tblByWeekDay(type3_081) + "\n\n"
    
    mu += webReportPostmaster(
        classification["postmasterUserRef"],
        userInfoByUserRef[classification["postmasterUserRef"]],
        type3_081["_total"],
        st3_081ByUserRef[classification["postmasterUserRef"]],
        classification["warningsByUserRef"][classification["postmasterUserRef"]] if classification["postmasterUserRef"] in classification["warningsByUserRef"] else []
    )
    
    mu += webReportDoDUser(
        classification["dodUserRef"],
        userInfoByUserRef[classification["dodUserRef"]],
        type3_081["_total"],
        st3_081ByUserRef[classification["dodUserRef"]],
        classification["warningsByUserRef"][classification["dodUserRef"]] if classification["dodUserRef"] in classification["warningsByUserRef"] else [],
        deidentify
    )
    
    # Beside's the special 2, 4 classes of User
    
    mu += webReportProxyUsers(
        classification["activeProxyUserRefs"], 
        classification["warningsByUserRef"],
        userInfoByUserRef,
        st3_081ByUserRef,
        type3_081["_total"],
        keyColsOnly=deidentify
    )

    mu += webReportNonProxyMachineUsers(
        classification["activeNonProxyMachineUserRefs"], 
        classification["warningsByUserRef"],
        userInfoByUserRef,
        type3_081["_total"],
        st3_081ByUserRef,
        keyColsOnly = deidentify
    )

    mu += webReportRemoteUsers(
        classification["activeRemoteUserRefs"],
        classification["warningsByUserRef"],
        len(classification["activeUserRefs"]), 
        userInfoByUserRef, 
        type3_081["_total"], 
        st3_081ByUserRef,
        classification["remoteExcludeReasonCount"], 
        deidentify,
        keyColsOnly = deidentify
    )
        
    # NOTE: far too crude now - need breaks
    mu += webReportLocalUsers(
        classification["activeLocalUserRefs"], 
        classification["warningsByUserRef"],
        len(classification["activeUserRefs"]), 
        userInfoByUserRef, 
        type3_081["_total"], 
        st3_081ByUserRef,
        deidentify,
        keyColsOnly = deidentify
    )
    
    mu += webReportUnclassifiedUsers(
        classification["activeNotCategorizedUserRefs"], 
        classification["warningsByUserRef"],
        len(classification["activeUserRefs"]), 
        userInfoByUserRef, 
        type3_081["_total"], 
        st3_081ByUserRef,
        deidentify,
        keyColsOnly = deidentify
    )    

    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    reportFile = userSiteDir + ("user.md" if not deidentify else "userDeId.md")
    print("Writing report {}".format(reportFile))
    open(reportFile, "w").write(mu)

"""
Proxy Users

Classifier enforces CONNECTOR PROXY, AV presence and LOA 2

TO ADD:
- workstation_name pattern (ie/ form of TCP Connect)
- forced_close on SO %

Refs: <----- TODO: make explicit in report
https://github.com/vistadataproject/RPCDefinitionToolkit/issues/44
- EDIS - Emergency Department Integration Software (EDIS) https://www.va.gov/vdl/documents/Clinical/Emergency_Dept_Integration_Software/edp_2_1_1_tm.pdf (SPOK: CONNECTOR,EDIS?)
- AVS may be After Visit Summary
- The VistALink Connector Proxy User is an entry on your VistA NEW PERSON file that the PATS application and other web-based applications use to connect to your VistA site. For the PATS application, there will be one data center located in Falling Waters, VA and a second fail-over data center in Hines, IL. A VistALink connector proxy user needs to be set up on your VistA server for the Falling Waters data center and also for the Hines data center.
  (SPOK: VISTALINK,EMC HINES)
- RTLS: "application proxy user 'VIAASERVICE,RTLS APPLICATION PROXY' will be created automatically."
- VPS: 
  (SPOK: CONNECT,VPS)
- Fee Basis Claims System (FBCS) application
- CPGATEWAY,USER: The CP Gateway Service is composed of two subsystems ... via the RPC Broker to retrieve the HL7 message ... Vendor CIS for Clinical Procedures and VistA

Note: tied up with vistalink and two step of connector (with station number
lookup) and then switch to local user <------------ see if two step means two sign ons?
"""
def webReportProxyUsers(activeProxyUserRefs, warningsByUserRef, userInfoByUserRef, st3_081ByUserRef, totalSignOns, keyColsOnly=False):

    totalProxySignOnCount = sum(st3_081ByUserRef[userRef]["_total"] for userRef
 in activeProxyUserRefs)
    mu = """## Proxy Users
    
There are <span class='yellowIt'>{:,}</span> active __Proxy Machine Users__ (user_class is \"CONNECTOR PROXY\") with <span class='yellowIt'>{}</span> signons. All user records have _access_, _verify_ and lack a social while their signons have _LOA_ 2 and don't have \"remote_...\" properties (ie/ CPRS-like combo). These signons probably happen over __VistALink__ and not the plain RPC Broker ...\n\n""".format(len(activeProxyUserRefs), reportAbsAndPercent(totalProxySignOnCount, totalSignOns))
    cols = [":Name [IEN]", "Entered", "SignOns", "Period", "\# IPs"] if keyColsOnly else [":Name [IEN]", "Entered", ":PMO", ":SMOs", ":Keys", "SignOns", "Period", "\# IPs", "Duration", ":Unexpected"] 
    tbl = MarkdownTable(cols)
    allSTs = []
    for userRef in sorted(activeProxyUserRefs, key=lambda x: st3_081ByUserRef[x]["_total"], reverse=True):
        userInfo = userInfoByUserRef[userRef] 
        st = st3_081ByUserRef[userRef]
        allSTs.append(st)
        pmoMU, smosMU, keysMU = muOptionsNKeys(userInfo)
        if "duration" in st and "byValueCount" in st["duration"]: # TODO: remove and FORCE all to have duration once redo E
            if st["_total"] > 1:
                kstatsDur = keyStats(
                    flattenFrequencyDistribution(st["duration"]["byValueCount"])
                )
                durMU = "{}/{}/{}".format(muSeconds(kstatsDur["median"]), muSeconds(kstatsDur["min"]), muSeconds(kstatsDur["max"]))
            else:
                durMU = muSeconds(singleValue(st, "duration"))
        else:
            durMU = ""
        unexpectedMU = "" if userRef not in warningsByUserRef else "/ ".join(warningsByUserRef[userRef])
        if keyColsOnly:
            row = [
                muUserRef(userRef),
                userInfo["date_entered"] if "date_entered" in userInfo else "", 
                reportAbsAndPercent(st["_total"], totalProxySignOnCount),
                muSignOnPeriod(st),
                muBVC(st["ipv4_address"]["byValueCount"], countOnlyIfOver=5) 
            ]
        else:           
            row = [
                muUserRef(userRef),
                userInfo["date_entered"] if "date_entered" in userInfo else "", 
                pmoMU,
                smosMU,
                keysMU,
                reportAbsAndPercent(st["_total"], totalProxySignOnCount),
                muSignOnPeriod(st),
                muBVC(st["ipv4_address"]["byValueCount"], countOnlyIfOver=5),
                durMU,
                unexpectedMU
            ]
        tbl.addRow(row)
    mu += tbl.md() + "\n\n"
            
    return mu
    
"""
Off Key Words BUT Not the DoD User (| Postmaster) 

Expects: machine SSN, visited_from, NO remote_app, LOA 2 (usually), no PMO or keys

Note:
- no PMO or Keys as none specified (in VCB)
- not enforcing LOA 2 as see 200, 2001 combos where first is 1 and then move to 2
- showing remote_user_ien as apparently fixed
- NOT enforcing no remote_app as one CVIX has VISTAWEB login in VCB

CVIX remote_user_ien seems to have a fixed IEN
CVIX_MHVUSER_SSNIEN = "200:412864" # expect 2001 too and 2006_95's >> sign ons
CVIX_USER_SSNIEN = "200:217122" # expect 2001 too; 2006_95 << sign ons 
...
and fixed IP and LOA 1 usually
"""
def webReportNonProxyMachineUsers(activeNonProxyMachineUserRefs, warningsByUserRef, userInfoByUserRef, totalSignOns, st3_081ByUserRef, keyColsOnly=False):

    totalNonProxyMachineSignOnCount = sum(st3_081ByUserRef[userRef]["_total"] for userRef in activeNonProxyMachineUserRefs)
    mu = """## (Non Proxy) Machine Users
    
Besides the _DoD User_, there are <span class='yellowIt'>{:,}</span> active __Non-Proxy Machine Users__ with <span class='yellowIt'>{}</span> signons. These users appear in most VistAs under fabricated social security numbers ...\n\n""".format(
        len(activeNonProxyMachineUserRefs), 
        reportAbsAndPercent(totalNonProxyMachineSignOnCount, totalSignOns)
    )

    # To add: workstation_name - take first part? ipv4_address    
    cols = [":Name [IEN]", "Entered", "SSN", "SignOns", "Period", "Remote Station Id(s)", "Remote IEN(s)", ":IPs"] if keyColsOnly else [":Name [IEN]", "Entered", "SSN", ":SMOs", "SignOns", "Period", "Remote Station Id(s)", "Remote IEN(s)", ":IPs", "Duration", ":Unexpected"]
    tbl = MarkdownTable(cols)
    for userRef in sorted(activeNonProxyMachineUserRefs, key=lambda x: st3_081ByUserRef[x]["_total"], reverse=True):
        userInfo = userInfoByUserRef[userRef]
        st = st3_081ByUserRef[userRef]
        pmoMU, smosMU, keysMU = muOptionsNKeys(userInfo)
        unexpectedMU = "" if userRef not in warningsByUserRef else "/ ".join(warningsByUserRef[userRef])
        if "remote_user_ien" in st:
            if len(st["remote_user_ien"]["byValueCount"]) > 5:
                remoteIENsMU = "_#{:,}_".format(len(st["remote_user_ien"]["byValueCount"]))
            else:
                remoteIENsMU = "/".join(st["remote_user_ien"]["byValueCount"])
        else:
            remoteIENsMU = ""
        if "duration" in st and "byValueCount" in st["duration"]: # TODO: remove
            if st["_total"] > 1:
                kstatsDur = keyStats(
                    flattenFrequencyDistribution(st["duration"]["byValueCount"])
                )
                durMU = "{}/{}/{}".format(muSeconds(kstatsDur["median"]), muSeconds(kstatsDur["min"]), muSeconds(kstatsDur["max"]))
            else:
                durMU = muSeconds(singleValue(st, "duration"))
        else:
            durMU = ""
        if keyColsOnly:
            row = [
                muUserRef(userRef),
                userInfo["date_entered"] if "date_entered" in userInfo else "",
                "__{}__".format(userInfo["ssn"]) if "ssn" in userInfo else "",
                reportAbsAndPercent(st["_total"], totalNonProxyMachineSignOnCount),
                muSignOnPeriod(st),
                # NO remote app?
                "/".join(st["remote_station_id"]["byValueCount"].keys()) if "remote_station_id" in st else "",
                remoteIENsMU,
                muBVC(st["ipv4_address"]["byValueCount"], countOnlyIfOver=5)            
            ]
        else:
            row = [
                muUserRef(userRef),
                userInfo["date_entered"] if "date_entered" in userInfo else "",
                "__{}__".format(userInfo["ssn"]) if "ssn" in userInfo else "",
                smosMU,
                reportAbsAndPercent(st["_total"], totalNonProxyMachineSignOnCount),
                muSignOnPeriod(st),
                # NO remote app?
                "/".join(st["remote_station_id"]["byValueCount"].keys()) if "remote_station_id" in st else "",
                remoteIENsMU,
                muBVC(st["ipv4_address"]["byValueCount"], countOnlyIfOver=5),
                durMU,
                unexpectedMU      
            ]
        tbl.addRow(row)
    mu += tbl.md() + "\n\n"
        
    return mu
    
"""
FIRST: exceed and nix
- https://github.com/vistadataproject/RPCDefinitionToolkit/blob/master/Reporters/Users/reportRemoteUsersE.py
- bseEntries = [entry for entry in entries if "remote_app" in entry] etc in
https://github.com/vistadataproject/DataExtractNSync/blob/master/RPCSessionTests/reportUsersAndLogins.py

TODO: needs more
- JLV vs other - see IPs in fmrepo's util
  ... JLV with DoD Ids
  ie/ DoD JLV
  ie/ may show REAL dod ids => de-identify
- non station id/ien combo (need from custom run on SO!) ie/ X:1 in particular
"""
def webReportDoDUser(userRef, userInfo, totalSignons, st, warnings, deidentify):
        
    mu = """## \"DoD User\"
    
One special non proxy, machine user, the __\"DoD User\"__ is used for JLV DoD access and for access by a number of other applications ...\n\n"""
    
    tbl = MarkdownTable([":Property", ":Value"], includeNo=False)
    
    tbl.addRow(["IEN", re.search(r'\[200\-([^\]]+)', userRef).group(1)])
    tbl.addRow(["Date Entered", userInfo["date_entered"] if "date_entered" in userInfo else ""])
    tbl.addRow(["SSN", "__{}__".format(userInfo["ssn"])])
    pmoMU, smosMU, keysMU = muOptionsNKeys(userInfo)
    tbl.addRow(["SMOs", smosMU])
    tbl.addRow(["Sign ons", reportAbsAndPercent(st["_total"], totalSignons)])
    tbl.addRow(["Sign on period", muSignOnPeriod(st)])
    wdCntr = expandByWeekDay(st)
    tbl.addRow(["Days", ", ".join(["{} [{}]".format("__{}__".format(day) if i < 5 else day, wdCntr[day]) for i, day in enumerate(wdCntr)])])
    noRemoteStationIds = len(st["remote_station_id"]["byValueCount"])
    tbl.addRow(["Station Ids", noRemoteStationIds])
    def topRemoteStationIds(st):
        orderedTopCounts = {} 
        for i, rsid in enumerate(sorted(st["remote_station_id"]["byValueCount"], key=lambda x: st["remote_station_id"]["byValueCount"][x], reverse=True), 1):
            if i > 5:
                break
            orderedTopCounts[rsid] = st["remote_station_id"]["byValueCount"][rsid]
        return orderedTopCounts
    tbl.addRow(["Top Station Ids", muBVC(topRemoteStationIds(st))])
    fiveOrMoreRemoteStationIds = sum(1 for rsid in st["remote_station_id"]["byValueCount"] if re.match(r'\d\d\d\d\d', rsid))
    tbl.addRow(["5 digit plus Station Ids (DoD?)", fiveOrMoreRemoteStationIds])
    threeAlphaRemoteStationIds = dict((rsid, st["remote_station_id"]["byValueCount"][rsid]) for rsid in st["remote_station_id"]["byValueCount"] if re.match(r'\d\d\d\d?[A-Z]*[A-Z]*$', rsid))
    tbl.addRow(["3 digit [2 alpha] Station Ids (VA)", muBVC(threeAlphaRemoteStationIds, countOnlyIfOver=10)])
    tbl.addRow(["IPs", len(st["ipv4_address"]["byValueCount"])])
    tbl.addRow(["Divisions", muBVC(st["division"]["byValueCount"])])
    if len(warnings):
        tbl.addRow(["Unexpected", "/ ".join(warnings)])
        
    mu += tbl.md() + "\n\n"
    return mu
        
def webReportPostmaster(userRef, userInfo, totalSignons, st, warnings):

    mu = """## Postmaster

Every VistA has __Postmaster__, (one of) the first user in the system ...

"""
    
    tbl = MarkdownTable([":Property", ":Value"], includeNo=False)
    
    tbl.addRow(["Name \[IEN\]", muUserRef(userRef)])
    tbl.addRow(["Date Entered", userInfo["date_entered"] if "date_entered" in userInfo else ""])
    pmoMU, smosMU, keysMU = muOptionsNKeys(userInfo)
    if pmoMU:
        tbl.addRow(["PMO", pmoMU])
    if smosMU:
        tbl.addRow(["SMOs", smosMU])
    if keysMU:
        tbl.addRow(["Keys", keysMU])
    # Division is hardly ever set and then to main site - ignoring
    
    tbl.addRow(["Sign ons", reportAbsAndPercent(st["_total"], totalSignons)])
    tbl.addRow(["Sign on period", muSignOnPeriod(st)])
    
    if len(warnings):
        tbl.addRow(["Unexpected", "/ ".join(warnings)])
    
    mu += tbl.md() + "\n\n"
    return mu
    
"""
REM: the dynamic sniffing of a session would yield much of this (user from certain IPs, remote station id, context chosen is VPR or , workstation 10 etc)

TODO: (review the issues in TK too)
- should add DIVISION restriction (only def div) to REMOTE CHECK
- JLV subset (add to classifier)
  - workstation 10 ie/ the JLV Sub
  - more on VPR SMO ... split em out
    ie mu += "{:,} VPR Remote Users; {:,} no remote_app remote users; {:,} both; {:,} VPR only; {:,} no remote_app only
    "ipv4_addresses": set(JLV_INVA_IPS).union(set(JLV_INVA_EXTRA_IPS)),
            "level_of_assurance": "1",
            "workstation_name": "10"
    and CC JLV
    (besides DoD JLV)
        ipt = IPTracker(defn["name"])
            for so in sos:
                ipt.processSignOn(so)
                globalIPTracker.processSignOn(so) # overalls!
  <-------- VPR subset and tie to JLV IPs too
- REMOTE APP SPEC => BSE subset 
- by APP ie/ CAPRI et al + ENFORCE [classifier] on loa 1/2 (3 for local?) ie/ break JLV vs others in separate tables (fuller report)
- manilla called out; 200 too?
fmrepo/user/catag (move over)
"""
def webReportRemoteUsers(activeRemoteUserRefs, warningsByUserRef, totalActiveUsers, userInfoByUserRef, totalSignOns, st3_081ByUserRef, remoteExcludeReasonCount, deidentify, keyColsOnly=False):

    if len(activeRemoteUserRefs) == 0:
        return ""

    remoteSignOnCountsByUserRef = dict((userRef, st3_081ByUserRef[userRef]["_total"]) for userRef in activeRemoteUserRefs)
    totalRemoteSignOns = sum(remoteSignOnCountsByUserRef[userRef] for userRef in remoteSignOnCountsByUserRef)
    kstats = keyStats(list(remoteSignOnCountsByUserRef.values()))

    print("About to combine lot's of remote sts (takes time) ...")
    comboST = combineSubTypes([st3_081ByUserRef[userRef] for userRef in activeRemoteUserRefs], forceCountProps=["remote_station_id", "remote_app", "division"])[0]
    print("... end combo'ing")
    
    mu = """## Remote Users
    
Remote users dominate in every VistA - <span class='yellowIt'>{}</span> - but account for less sign ons - <span class='yellowIt'>{}</span> - than their numbers suggest. The median number of sign ons per remote user is <span class='yellowIt'>{:,}</span>. 
 
""".format(
        reportAbsAndPercent(len(activeRemoteUserRefs), totalActiveUsers),
        reportAbsAndPercent(totalRemoteSignOns, totalSignOns),
        roundFloat(kstats["median"])
    )
    
    remoteStationBVC = comboST["remote_station_id"]["byValueCount"]
    mu += "Remote sign on comes from <span class='yellowIt'>{:,}</span> Remote Stations or <span class='yellowIt'>{:,}</span> three digit stations. The top 10 are ...\n\n".format(
        len(remoteStationBVC),
        len(set(stId[0:3] for stId in remoteStationBVC))
    )    
    tbl = MarkdownTable([":Remote Station Id", ":Count of Remote SignOns"], includeNo=False)
    for i, stationId in enumerate(sorted(remoteStationBVC, key=lambda x: remoteStationBVC[x], reverse=True), 1):
        if i > 10:
            break
        stationMU = "__{}__".format(stationId)
        if stationId in SSNO_DEFINITIONS:
            stationMU = "__{} [{}]__".format(stationId, SSNO_DEFINITIONS[stationId])
        tbl.addRow([
            stationMU, 
            reportAbsAndPercent(remoteStationBVC[stationId], totalRemoteSignOns)
        ])
    mu += tbl.md() + "\n\n"
    
    mu += "Remote signon by week day ...\n\n"
    mu += tblByWeekDay(comboST) + "\n\n"
            
    def muRemoteIds(st): # points to need for custom combine of sno:ien
        stationIdVC = st["remote_station_id"]["byValueCount"]
        # Could happen but ? ... TODO: force IEN count 
        if "byValueCount" not in st["remote_user_ien"]:
            return ""
        ienVC = st["remote_user_ien"]["byValueCount"]
        def muTripler(sid):
            if sid == "459":
                return "__459__"
            return sid 
        if len(stationIdVC) == 1:
            return "{}:{}".format(
                muTripler(list(stationIdVC)[0]), 
                list(ienVC)[0]
            )
        if len(ienVC) == 1:
            return "{}:{}".format(
                "/".join([muTripler(sid) for sid in stationIdVC]), 
                list(ienVC)[0]
            )
        # TODO: match counts in both to assemble id
        return ""
    mu += "The following shows the top 50 Remote Users ...\n\n"
    cols = [":Name [IEN]", "Entry", "Remote Id(s)", "SignOns", "Period", "Days", ":Remote Apps"] if keyColsOnly else [":Name [IEN]", "Entry", "Remote Id(s)", "SignOns", "Period", "Days", ":Remote Apps", ":Options", "Duration", ":Unexpected"]   
    tbl = MarkdownTable(cols)
    for i, userRef in enumerate(sorted(activeRemoteUserRefs, key=lambda x: st3_081ByUserRef[x]["_total"], reverse=True), 1):
        if i > 50:
            break
        userInfo = userInfoByUserRef[userRef] 
        st = st3_081ByUserRef[userRef]
        # May put VPR in bold later as JLV indicator
        pmoMU, smosMU, keysMU = muOptionsNKeys(userInfo)
        remote_app_count = st["remote_app"]["byValueCount"] if "remote_app" in st else {}
        no_remote_app_count = st["_total"] if "remote_app" not in st else st["_total"] - st["remote_app"]["count"]
        if no_remote_app_count:
            remote_app_count["UNIDENTIFIED"] = no_remote_app_count
        remoteAppMU = ", ".join(["{} ({})".format(remote_app.split(" [")[0], remote_app_count[remote_app]) for remote_app in sorted(remote_app_count, key=lambda x: remote_app_count[x], reverse=True)])
        wdCntr = expandByWeekDay(st)
        if "duration" in st and "byValueCount" in st["duration"]:
            if st["_total"] > 1:
                kstatsDur = keyStats(
                    flattenFrequencyDistribution(st["duration"]["byValueCount"])
                )
                durMU = "{}/{}/{}".format(muSeconds(kstatsDur["median"]), muSeconds(kstatsDur["min"]), muSeconds(kstatsDur["max"]))
            else:
                durMU = muSeconds(singleValue(st, "duration"))
        else:
            durMU = ""
        if keyColsOnly:
            row = [ 
                muUserRef(userRef, ssn="NO SSN" if "ssn" not in userInfo else userInfo["ssn"], deidentify=deidentify),
                userInfo["date_entered"] if "date_entered" in userInfo else "",
                muRemoteIds(st),
                reportAbsAndPercent(st["_total"], totalRemoteSignOns),
                muSignOnPeriod(st),
            ", ".join(["{} [{}]".format("__{}__".format(day) if i < 5 else day, wdCntr[day]) for i, day in enumerate(wdCntr)]),
                remoteAppMU            
            ]
        else:
            row = [
                muUserRef(userRef, ssn="NO SSN" if "ssn" not in userInfo else userInfo["ssn"], deidentify=deidentify),
                userInfo["date_entered"] if "date_entered" in userInfo else "",
                muRemoteIds(st),
                reportAbsAndPercent(st["_total"], totalRemoteSignOns),
                muSignOnPeriod(st),
            ", ".join(["{} [{}]".format("__{}__".format(day) if i < 5 else day, wdCntr[day]) for i, day in enumerate(wdCntr)]),
                remoteAppMU,
                smosMU,
                durMU,
                "" if userRef not in warningsByUserRef else "/ ".join(warningsByUserRef[userRef])
            ]
        tbl.addRow(row)
    mu += tbl.md() + "\n\n"
        
    return mu
    
"""
TODO: 
- broad: FAR TOO catch all -- why does PUG have so many more in Pug than ALake? 
  - and device: ssh vs other
- exclude from remote on MAND_PROPS and ALLOWED_PROPS as opposed to 0's ie/ 0's in here PLUS station_no in locals
"""
def webReportLocalUsers(activeLocalUserRefs, warningsByUserRef, totalActiveUsers, userInfoByUserRef, totalSignOns, st3_081ByUserRef, deidentify, keyColsOnly=False):

    if len(activeLocalUserRefs) == 0:
        return ""

    totalLocalSignOns = sum(st3_081ByUserRef[userRef]["_total"] for userRef in activeLocalUserRefs)
    mu = """## Local Users
    
There are <span class='yellowIt'>{}</span> active Local Users with <span class='yellowIt'>{}</span> signons.\n\n""".format(reportAbsAndPercent(len(activeLocalUserRefs), totalActiveUsers), reportAbsAndPercent(totalLocalSignOns, totalSignOns))

    comboST = combineSubTypes([st3_081ByUserRef[userRef] for userRef in activeLocalUserRefs], forceCountProps=["division"])[0]
    mu += "Local users select <span class='yellowIt'>{:,}</span> divisions (SHOULD RESTRICT THIS SET) ...\n\n".format(len(comboST["division"]["byValueCount"]))
    tbl = MarkdownTable([":Division", ":Count %"])
    for divisionRef in sorted(comboST["division"]["byValueCount"], key=lambda x: comboST["division"]["byValueCount"][x], reverse=True):
        tbl.addRow([
            "__{}__".format(re.sub(r'4\-', '', divisionRef)), 
            reportAbsAndPercent(comboST["division"]["byValueCount"][divisionRef], totalLocalSignOns)
        ])
    mu += tbl.md() + "\n\n"
    
    mu += "And don't just sign on through device 0 ...\n\n"
    tbl = MarkdownTable([":Device", "Count %"], includeNo=False)
    for device in sorted(comboST["device"]["byValueCount"], key=lambda x: comboST["device"]["byValueCount"][x], reverse=True):
        tbl.addRow([
            "__{}__".format(device), 
            reportAbsAndPercent(comboST["device"]["byValueCount"][device], comboST["_total"])
        ])
    mu += tbl.md() + "\n\n"
    
    # TODO: will break on these 
    mu += "And have multiple levels of assurance ...\n\n"
    tbl = MarkdownTable([":LOA", "Count %"], includeNo=False)
    for loa in sorted(comboST["level_of_assurance"]["byValueCount"], key=lambda x: comboST["level_of_assurance"]["byValueCount"][x], reverse=True):
        tbl.addRow([
            "__{}__".format(device), 
            reportAbsAndPercent(comboST["level_of_assurance"]["byValueCount"][device], comboST["_total"])
        ])
    mu += tbl.md() + "\n\n"
    
    SUPERUSER_KEYS = ["XUMGR"] # removing XUPROG
    superUserRefs = set(userRef for userRef in activeLocalUserRefs if "keys" in userInfoByUserRef[userRef] and len(set(SUPERUSER_KEYS).intersection(set(userInfoByUserRef[userRef]["keys"]))))
    mu += "<span class='yellowIt'>{:,}</span> Local Users are __Superusers__ (those with key {}) ...\n\n".format(len(superUserRefs), "|".join(SUPERUSER_KEYS))
    cols = [":Name [IEN]", "Entry", ":Title", "SignOns", "Period", "Days"] if keyColsOnly else [":Name [IEN]", "Entry", ":Title", "SignOns", "Period", "Days", ":PMO", ":SMOs", ":Keys", ":Unexpected"]
    tbl = MarkdownTable(cols)
    for userRef in sorted(superUserRefs, key=lambda x: st3_081ByUserRef[x]["_total"], reverse=True):
        userInfo = userInfoByUserRef[userRef]
        st = st3_081ByUserRef[userRef]
        pmoMU, smosMU, keysMU = muOptionsNKeys(userInfo)
        wdCntr = expandByWeekDay(st)
        if keyColsOnly:
            row = [
                muUserRef(userRef, ssn="NO SSN" if "ssn" not in userInfo else userInfo["ssn"], deidentify=deidentify),
                userInfo["date_entered"] if "date_entered" in userInfo else "",
                userInfo["title"] if "title" in userInfo else "",
                reportAbsAndPercent(st["_total"], totalLocalSignOns),
                muSignOnPeriod(st),
                ", ".join(["{} [{}]".format("__{}__".format(day) if i < 5 else day, wdCntr[day]) for i, day in enumerate(wdCntr)])            
            ]
        else:
            row = [
                muUserRef(userRef, ssn="NO SSN" if "ssn" not in userInfo else userInfo["ssn"], deidentify=deidentify),
                userInfo["date_entered"] if "date_entered" in userInfo else "",
                userInfo["title"] if "title" in userInfo else "",
                reportAbsAndPercent(st["_total"], totalLocalSignOns),
                muSignOnPeriod(st),
                ", ".join(["{} [{}]".format("__{}__".format(day) if i < 5 else day, wdCntr[day]) for i, day in enumerate(wdCntr)]),
                pmoMU,
                smosMU,
                keysMU,
                "" if userRef not in warningsByUserRef else "/ ".join(warningsByUserRef[userRef])
            ]
        tbl.addRow(row)
    mu += tbl.md() + "\n\n"
        
    return mu
    
def webReportUnclassifiedUsers(activeNotCategorizedUserRefs, warningsByUserRef, totalActiveUsers, userInfoByUserRef, totalSignOns, st3_081ByUserRef, deidentify, keyColsOnly=False):

    if len(activeNotCategorizedUserRefs) == 0:
        return ""

    totalUnclassfiedSignOns = sum(st3_081ByUserRef[userRef]["_total"] for userRef in activeNotCategorizedUserRefs)
    mu = """## Unclassified Users
    
There are <span class='yellowIt'>{}</span> active unclassified Users with <span class='yellowIt'>{}</span> signons.\n\n""".format(reportAbsAndPercent(len(activeNotCategorizedUserRefs), totalActiveUsers), reportAbsAndPercent(totalUnclassfiedSignOns, totalSignOns))

    return mu
       
# TODO: change to calc length formally in case of gaps 
def muSignOnPeriod(st):
    if len(st["date_time"]["byValueCount"]) == 13:
        soPeriodMU = "EVERY MONTH"
    elif st["date_time"]["firstCreateDate"].split("T")[0] == st["date_time"]["lastCreateDate"].split("T")[0]:
        soPeriodMU = st["date_time"]["lastCreateDate"].split("T")[0]
    elif re.search(r'\-', list(st["date_time"]["byValueCount"])[0]): # months
        soPeriodMU = "{} - {} ({})".format(st["date_time"]["firstCreateDate"].split("T")[0], st["date_time"]["lastCreateDate"].split("T")[0], len(st["date_time"]["byValueCount"]))
    else:      
        soPeriodMU = "{} - {}".format(st["date_time"]["firstCreateDate"].split("T")[0], st["date_time"]["lastCreateDate"].split("T")[0])
    return soPeriodMU
    
"""
TODO: change -- move to reducing non RPC options 
"""
def muOptionsNKeys(userInfo):
    # rosByLabel = dict((res["label"], res) for res in rpcOptions(stationNo))
    pmoMU = ""
    if "primary_menu_option" in userInfo:
        pmoMU = userInfo["primary_menu_option"]
        # if userInfo["primary_menu_option"] not in rosByLabel:
        #    pmoMU += " [NOT RPC]"
    smosMU = ""
    if "secondary_menu_options" in userInfo:
        # smosMU = ", ".join(sorted([smo if smo in rosByLabel else "{} [NOT RPC]".format(smo) for smo in userInfo["secondary_menu_options"]]))
        if len(userInfo["secondary_menu_options"]) <= 5:
            smosMU = ", ".join(sorted(userInfo["secondary_menu_options"])[0:5])
        else:
            smosMU = "_{:,}_".format(len(userInfo["secondary_menu_options"]))
    keysMU = ""
    if "keys" in userInfo:
        if len(userInfo["keys"]) <= 5:
            keysMU = ", ".join([key for key in sorted(userInfo["keys"])[0:5]])
        else:
            keysMU = "_{:,}_".format(len(userInfo["keys"]))
    return pmoMU, smosMU, keysMU
    
def muUserRef(userRef, ssn=None, deidentify=False):
    name = userRef.split(" [200-")[0]
    if deidentify:
        name = re.sub(r'[A-Za-z]', "X", name)
        if ssn:
            ssn = "XXXXXXXXX"
    ien = userRef.split("[200-")[1][:-1]
    return "__{}__ [{}]".format(
            name,
            "{}/{}".format(ien, ssn) if ssn != None else ien
    )
    
def tblByWeekDay(st):
    ocntr = expandByWeekDay(st, fullDays=True)
    tbl = MarkdownTable([":Day", "Total", "Average"], includeNo=False)
    for i, day in enumerate(ocntr):
        avg = ocntr[day].split("/")[1]
        avgMU = "" if avg == "0" else avg
        tbl.addRow([
            "__{}__".format(day) if i < 5 else day,
            ocntr[day].split("/")[0],
            avgMU
        ])              
    return tbl.md() 
    
"""
Want average as well as total for period - but note that average may be bad
indicator if median is low. Best st can offer.
"""
def expandByWeekDay(st, fullDays=False): 
    def countDaysInPeriod(s, e):
        d1 = datetime.strptime(s.split("T")[0], "%Y-%m-%d")
        d2 = datetime.strptime(e.split("T")[0], "%Y-%m-%d")
        cnter = Counter()
        for d_ord in range(d1.toordinal(), d2.toordinal() + 1):
            d = date.fromordinal(d_ord)
            cnter[d.weekday()] += 1
        return cnter
    createDatePropInfo = st[st["_createDateProp"]]
    dayCnter = countDaysInPeriod(createDatePropInfo["firstCreateDate"], createDatePropInfo["lastCreateDate"])
    weekdays=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] if fullDays else ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
    cntr = {}
    byWeekDay = st["date_time"]["byWeekDay"]
    for wd in sorted(byWeekDay, key=lambda x: int(x)):
        if wd not in byWeekDay:
            continue
        avg = int(round(float(byWeekDay[wd])/ float(dayCnter[int(wd)])))
        val = "{:,}/{:,}".format(byWeekDay[wd], avg)
        cntr[weekdays[int(wd)]] = val
    return cntr
    
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

    ensureWebReportLocations(stationNo)
    
    if len(sys.argv) == 3:
        deidentify = True
    else:
        deidentify = False
    
    webReportUser(stationNo, deidentify)
    
if __name__ == "__main__":
    main()
