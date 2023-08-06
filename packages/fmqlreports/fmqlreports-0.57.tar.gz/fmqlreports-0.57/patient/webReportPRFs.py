#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent
from fmqlutils.typer.reduceTypeUtils import splitTypeDatas, checkDataPresent, singleValue
from ..webReportUtils import filteredResultIterator, TOP_MD_TEMPL, SITE_DIR_TEMPL, keyStats, roundFloat, reduce200

"""
TOFIX:
- REDO: break must be owner_site too (see if mand)
- local and national difference
- issue of distinct patient: make note that normally from "ALL" type BUT want for ACTIVE vs NOT ACTIVE and per Flag and even per flag per site

Basic PRF

Requires:
- 3_8 (All)
- 26_11 (All)
- 26_13 (Reduction)
- 26_15 (All)
- 200 (All/Indexed-reduce200)

... others to add

TODO: see other xxrepo notes <----- nix when through

TODO v1.1:
- as doing: introduce singleValue, singleValueCount on prop which enforces singletons 
- assigned are mixed with types in table and not in old reports => split out and fill in assignements ala report
- tie to docs: 8925 ... 26_14

TODO v2:
- 391_91 with sources of Patient! (Patient can have > 1 record) ... may break by 'patient'?

NEW TODO: documents tie in (see types in tables) and Treating Facility List tie in ...

> The PRF Manual says that the file, Treating Facility List, is key for designating a Patient as being owned elsewhere and that two HL7 messages are used to synchronize flags with remote systems, one triggered when a patient is added to a VistA, the other when a national flag assignment is made or edited. Both message communications are tracked in PRF HL7 log files.

... see 391.91 entries (if there).
"""
def webReportPRFs(stationNo):

    allThere, details = checkDataPresent(stationNo, [
        {"fileType": "3_8", "check": "ALL"},
        {"fileType": "26_11", "check": "ALL"},
        {"fileType": "26_13", "check": "TYPE"},
        {"fileType": "26_15", "check": "ALL"},
        {"fileType": "200", "check": "ALL"} # as indexed
    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))
                
    all26_13Data, st26_13s = splitTypeDatas(stationNo, "26_13", expectSubTypeProperty="status-flag_name-owner_site")
    stActive26_13s = [st26_13 for st26_13 in st26_13s if re.search(r':ACTIVE', st26_13["_subTypeId"])]
    activeFlagUse = dict((list(st26_13["flag_name"]["byValueCount"])[0], st26_13["_total"]) for st26_13 in stActive26_13s) 
            
    mu = """---
layout: default
title: {} Patient Record Flags
---

""".format(stationNo) 

    mu += """Patient Record Flags (PRFs) are
     
> used to alert Veterans Health Administration (VHA) medical staff and employees of patients whose behavior and characteristics may pose a threat either to their safety, the safety of other patients, themselves, or compromise the delivery of quality health care. PRFs’ assignments are displayed during the patient look-up process

Flag assignment involves document creation and maintenance, use of email and HL7 messaging.

"""

    mu += webReportAssignments(stationNo, all26_13Data, stActive26_13s)

    fmu, mailGroupUse, clsIDocTypeUse, clsIIDocTypeUse = webReportFlagTypes(stationNo, activeFlagUse)
    mu += fmu
    
    mu += webReportMailGroupUse(stationNo, mailGroupUse)
    
    mu += webReportHL7Use(stationNo)
        
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "prfs.md", "w").write(mu)
    
"""
Expand out but also decide interplay of showing assignment #'s above and this. 

TODO: remote #'s from above and just note if used or not AND off 26_14 NEW ASSIGNMENT
dates
"""
def webReportAssignments(stationNo, all26_13Data, stActive26_13s):

    cntNational = sum(st26_13["_total"] for st26_13 in stActive26_13s if re.search(r'\_15', st26_13["_subTypeId"]))
    cntLocal = sum(st26_13["_total"] for st26_13 in stActive26_13s if re.search(r'\_11', st26_13["_subTypeId"]))
    cntUniquePatients = sum(len(st26_13["patient_name"]["byValueCount"]) for st26_13 in stActive26_13s)
    
    mu = """### Flag Assignments
    
This VistA has <span class='yellowIt'>{:,}</span> active and <span class='yellowIt'>{:,}</span> inactive Patient Record Flag (PRF) assignments, <span class='yellowIt'>{:,}</span> in total. There are <span class='yellowIt'>{:,}</span> Class I (Nationally Defined) and <span class='yellowIt'>{:,}</span> Class II (Locally Defined) active flag assignments for <span class='yellowIt'>{:,}</span> patients.

""".format(all26_13Data["status"]["byValueCount"]["1:ACTIVE"], all26_13Data["status"]["byValueCount"]["0:INACTIVE"], all26_13Data["_total"], cntNational, cntLocal, cntUniquePatients)

    return mu

def webReportFlagTypes(stationNo, activeFlagUse):

    mu = "### Flag Types\n\n"

    mailGroupUse = defaultdict(list)
    
    # Nationals 
    tbl = MarkdownTable(["Flag", "Type", "Description", "Document Title", "email Group", "R/N", "Assigned"])
    resourceIter = filteredResultIterator(stationNo, "26_15")
    props = ["name", "type__03", "description", "tiu_pn_title", "review_mail_group", "review_frequency_days", "notification_days"]
    clsIDocTypeUse = defaultdict(int)
    total = 0
    for resource in resourceIter:
        fId = "{} [{}]".format(resource["label"], resource["_id"])
        if resource["status"] != "1:ACTIVE":
            raise Exception("Expected all to be active")
        if len(set(resource) - (set(["_id", "type", "label", "status"]).union(set(props)))):
            raise Exception("Unexpected property for national flag")
        row = []
        for prop in props:
            if prop == "name":
                if fId in activeFlagUse:
                    labelMU = "__{}__".format(resource["label"]) 
                    flagUseMU = activeFlagUse[fId] 
                else:
                    labelMU = resource["label"]
                    flagUseMU = ""
                row.append(labelMU)
                continue
            if prop not in resource:
                row.append("")
                continue
            if prop == "review_frequency_days":
                rnValue = resource[prop]
                continue
            if prop == "notification_days":
                rnValue += " / " + resource[prop]
                row.append(rnValue)
                continue
            if prop == "type__03":
                row.append(resource[prop]["label"][0])
                continue
            if isinstance(resource[prop], dict):
                row.append("{}".format(resource[prop]["label"]))
            elif re.search(r'\d:', resource[prop]):
                row.append(resource[prop].split(":")[1])
            elif len(row) == 0:
                row.append("__{}__".format(resource[prop]))
            else:
                row.append(re.sub(r'\n', ' ', resource[prop]))
            if prop == "review_mail_group":
                mailGroupUse[resource[prop]["id"]].append(fId)
            if prop == "tiu_pn_title":
                clsIDocTypeUse["{}".format(resource[prop]["id"])] += 1 
        row.append(flagUseMU)
        total += 1
        tbl.addRow(row)
    mu += "Every VistA Systems supports the following <span class='yellowIt'>4</span> __Class I__ (Nationally Defined) flags. The following table lists these flags along with their related document titles and mail email groups and their review and notify (R/N) times (in days) ...\n\n"
    mu += tbl.md() + "\n\n"
        
    # Locals
    tbl = MarkdownTable(["Flag", "Type", "Description", "Document Title", "email Group", "R/N", "Assigned"])
    resourceIter = filteredResultIterator(stationNo, "26_11")
    props = ["name", "type__03", "description", "tiu_pn_title", "review_mail_group", "review_frequency_days", "notification_days"]
    clsIIDocTypeUse = defaultdict(int)
    total = 0
    noAssigned = 0
    rows = []
    for resource in resourceIter:
        if len(set(resource) - (set(["_id", "type", "label", "status"]).union(set(props)))):
            raise Exception("Unexpected property for national flag")
        total += 1
        if not ("status" in resource and resource["status"] == "1:ACTIVE"):
            continue
        fId = "{} [{}]".format(resource["label"], resource["_id"])
        row = []
        for prop in props:
            if prop == "name":
                if fId in activeFlagUse:
                    labelMU = "__{}__".format(resource["label"]) 
                    flagUseMU = activeFlagUse[fId] 
                    noAssigned += 1
                else:
                    labelMU = resource["label"]
                    flagUseMU = ""
                row.append(labelMU)
                continue
            if prop not in resource:
                row.append("")
                continue
            if prop == "review_frequency_days":
                rnValue = resource[prop]
                continue
            if prop == "notification_days":
                rnValue += " / " + resource[prop]
                row.append(rnValue)
                continue
            if isinstance(resource[prop], dict):
                row.append("{}".format(resource[prop]["label"]))
            elif re.search(r'\d:', resource[prop]):
                row.append(resource[prop].split(":")[1])
            elif len(row) == 0:
                row.append("__{}__".format(resource[prop]))
            else:
                row.append(re.sub(r'\n', ' ', resource[prop]))
            if prop == "review_mail_group":
                mailGroupUse[resource[prop]["id"]].append(fId)
                continue
            if prop == "tiu_pn_title":
                clsIIDocTypeUse["{}".format(resource[prop]["id"])] += 1 
        row.append(flagUseMU)
        rows.append(row)
    for row in sorted(rows, key=lambda x: x[0]):
        tbl.addRow(row)
    mu += "This system defines <span class='yellowIt'>{:,}</span> __Class II__ (Locally Defined) flags, only <span class='yellowIt'>{:,}</span> of which are currently assignable (active) and only <span class='yellowIt'>{:,}</span> of those (in bold below) are used in active flag assignments ...\n\n".format(total, len(rows), noAssigned)    
    mu += tbl.md() + "\n\n"
    
    return mu, mailGroupUse, clsIDocTypeUse, clsIIDocTypeUse
    
"""
owner_site 

> current site that owns this patient flag assignment. Patient assignments may only be edited by the owner site. The owner site normally corresponds to the site providing primary care to the patient.

... may differ from originating_site.

TODO: 
- BUG: unique patients only works if add "owner_site" to the subTypeId
- add in state and station number for sites (need off constants) 
"""
def webReportOwnerSite(stationNo, stActive26_13s):

    totalAssignments = 0
    nationalAssignmentsByOwnerSite = Counter()
    localAssignmentsOfThisSite = 0
    uniquePatientsOfOwnerSite = defaultdict(lambda: set())
    for st26_13 in stActive26_13s:
        if not ("owner_site" in st26_13 and "byValueCount" in st26_13["owner_site"]):
            raise Exception("Expected Reduction of 26_13 to ensure owner_site is present in all actives AND the property be explicitly counted")
        if not ("patient_name" in st26_13 and "byValueCount" in st26_13["patient_name"]):
            raise Exception("Expected Reduction of 26_13 to ensure patient_name is present in all actives AND the property be explicitly counted")
        totalAssignments += st26_13["_total"]
        thisSite = ""
        for ownerSite in st26_13["owner_site"]["byValueCount"]:
            if re.search(r'\_15', st26_13["_subTypeId"]):
                nationalAssignmentsByOwnerSite[ownerSite] += st26_13["owner_site"]["byValueCount"][ownerSite]
                continue
            if thisSite:
                if thisSite != ownerSite:
                    raise Exception("Only expect one site - this one - to have class I nationals as well as local assignments")
            else:
                thisSite = ownerSite
            localAssignmentsOfThisSite += st26_13["_total"] # ie/ all to this site
            for patientName in st26_13["patient_name"]["byValueCount"]: # for now, only local
                uniquePatientsOfOwnerSite[ownerSite].add(patientName)
            
    mu = "### Owner VistAs\n\n"
    
    mu += "Including itself, <span class='yellowIt'>{:,}</span> VistAs contribute Active Flag Assignments to this VistA. The following table lists and ranks VistAs contributing 20 or more assignments or which are VistAs of interest. Not surprisingly, the local VistA contributes the most assignments ...\n\n".format(len(nationalAssignmentsByOwnerSite))
            
    tbl = MarkdownTable(["Rank", "Name", "Flag Count (Class I/ Class II)", "\%", "Unique Patients"])
    tbl.addRow([
        1,
        "__{}__".format(thisSite),
        "{:,} ({:,} / {:,})".format(
            nationalAssignmentsByOwnerSite[thisSite] + localAssignmentsOfThisSite,
            nationalAssignmentsByOwnerSite[thisSite],
            localAssignmentsOfThisSite
        ),
        reportPercent(nationalAssignmentsByOwnerSite[thisSite] + localAssignmentsOfThisSite, totalAssignments),
        len(uniquePatientsOfOwnerSite[thisSite])
    ])
    for i, ownerSite in enumerate(sorted(nationalAssignmentsByOwnerSite, key=lambda x: nationalAssignmentsByOwnerSite[x], reverse=True), 1):
        if ownerSite == thisSite:
            continue
        tbl.addRow([
            i,
            ownerSite,
            "{:,}".format(nationalAssignmentsByOwnerSite[ownerSite]),
            reportPercent(nationalAssignmentsByOwnerSite[ownerSite], totalAssignments),
            len(uniquePatientsOfOwnerSite[ownerSite])
        ])  
        
    mu += tbl.md() + "\n\n"
    
    return mu

"""
MAIL GROUPS
""" 
def webReportMailGroupUse(stationNo, mailGroupUse):   
     
    userInfoById = reduce200(stationNo)
        
    mu = "### email Groups\n\n"

    rows = []
    cols = ["Group", "Description", "Members", "Flag(s)"]
    tbl = MarkdownTable(cols)
    resourceIter = filteredResultIterator(stationNo, "3_8")
    flagsCovered = set()
    for resource in resourceIter:
        if resource["_id"] not in mailGroupUse:
            continue
        members = []
        if "member" in resource:
            for memberInfo in resource["member"]:
                memberRef = "{} [{}]".format(memberInfo["member"]["label"], memberInfo["member"]["id"])
                title = userInfoById[memberRef]["title"] if "title" in userInfoById[memberRef] else title
                members.append("{} ({})".format(memberInfo["member"]["label"], title))
        membersMU = ", ".join(sorted(members))
        row = ["__{}__".format(resource["label"]), re.sub(r'\n', ' ', resource["description"]) if "description" in resource else "", membersMU]
        # Note: by defn of 26.11/15, flag types have only one group each
        flagUsesMUs = ["{}".format(flagRef.split(" [")[0]) if re.search(r'\_11', flagRef) else "__{}__".format(flagRef.split(" [")[0]) for flagRef in sorted(mailGroupUse[resource["_id"]])]
        flagsCovered |= set(mailGroupUse[resource["_id"]])
        row.append(", ".join(flagUsesMUs))
        rows.append(row)
    for row in sorted(rows, key=lambda x: x[0]):
        tbl.addRow(row)
    mu += "<span class='yellowIt'>{:,}</span> mail groups are active for <span class='yellowIt'>{:,}</span> flags, <span class='yellowIt'>{:,}</span> of which, highlighted in bold, are Class I (National) flags ...\n\n".format(len(rows), len(flagsCovered), sum(1 for flagRef in flagsCovered if re.search(r'\_15', flagRef)))
    mu += tbl.md() + "\n\n"
    
    return mu
    
def webReportHL7Use(stationNo):

    # site_transmitted_to ... total by that!
    _17typeDatas, sts = splitTypeDatas(stationNo, "26_17", expectSubTypeProperty="")
    _19typeDatas, sts = splitTypeDatas(stationNo, "26_19", expectSubTypeProperty="")
    
    mu = "## HL7 Messaging for Class I Synchronization\n\n"
    for typeData, msgName in [(_17typeDatas[0], "Update R01"), (_19typeDatas[0], "Query R02")]:

        bvc = typeData["site_transmitted_to"]["byValueCount"]
        mdTable = MarkdownTable(["Site", "SSN", "Transmission Tos"], includeNo=False)
        sepRowIn = False
        for i, site in enumerate(sorted(bvc, key=lambda x: bvc[x], reverse=True), 1):
            if not (i < 11 or re.search(r'\-(663|640|668|442)', site)):
                if i > 10 and not sepRowIn:
                    mdTable.addSeparatorRow()
                    sepRowIn = True
                continue
            mdTable.addRow([
                i,
                site.split(" [")[0] if not re.search(r'\-(663|640|668|442)', site) else "__{}__".format(site.split(" [")[0]),
                re.search(r'\-(\d+)\]', site).group(1),
                reportAbsAndPercent(bvc[site], typeData["_total"])
            ])
        mu += "<span class='yellowIt'>{}</span> Transmissions of {} updates ...\n\n".format(typeData["_total"], msgName)
        mu += mdTable.md() + "\n\n"
        
    """
    The PRF subsystem uses two HL7 messages (Update RO1) and (Query R02) to synchronize Class I (National) flag assignments with other VistAs. Synchronization relies on VistA’s Treating Facility file. Both message types have their own logs in the system. According to this system’s logs ...
        * 6980 Update R01’s have been sent. These were triggered by updates to national flag assignments.
        * 77,446 Query R02’s have been sent. These were triggered by various types of patient registration.  
    """
    
    return mu
    
"""
Document Tie in

    In 26.14
            9. tiu_type_pn_link - POINTER - 759 (17%) - 8925_1
                1. PATIENT RECORD FLAG CATEGORY I - HIGH RISK FOR SUICIDE [8925_1-258] - 374 (49.3%)
                2. PATIENT RECORD FLAG CATEGORY II - HIGH RISK OF SUICIDE [8925_1-2113] - 370 (48.7%)
                3. PATIENT RECORD FLAG CATEGORY II - DISRUPTIVE BEHAVIOR [8925_1-2055] - 8 (1.1%)
                4. PATIENT RECORD FLAG CATEGORY I [8925_1-1402] - 7 (0.9%)
"""
    
# ################################# DRIVER #######################
               
def main():

    assert sys.version_info >= (3, 4)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO")

    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    if not os.path.isdir(userSiteDir):
        raise SystemExit("Expect User Site to already exist with its basic contents")
    
    webReportPRFs(stationNo)
                 
if __name__ == "__main__":
    main()
