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
from ..webReportUtils import ensureWebReportLocations, SITE_DIR_TEMPL, loadSelectTypes, reduce200, mdFilesOfDomain

"""
Dental with tie ins to Documents, Images, User (permissions) and Workload

Requires:
- 220_5 (Reduction) DENTAL PROVIDER
- 228_1 (SOReduction) DENTAL HISTORY ("dental encounter")
- 8925 (SOReduction)
- SELECT TYPEs for Dental File Types

TODO v1.1: notes and RPCs
- blurb ala PRF and others ie/ start with blurb
- Add 221: note that 221 is OLD ie/ last date of it? (being downloaded)
  > This file (228_1) is a new dental activity file. It is not meant to replace the official DAS at this time. Data stored in this file will be different from that in the DAS file (221)
- classes for dental notes?
- see others who use dental notes ie/ beyond providers identified
  > The dentists can do their Progress Note in the DSS-GUI which will download it to the VistA TIU package
- dental RPCs (key tie in to User Permissions) ... for DSS-GUI

TODO v2: introduce graph of activity per month + locns for Workload/PCE
- 228_1 SO ... show # per month over year, may break by type and consider per User breakdown (ala other types)
- 228_1 ... see locations (would tie to workload?): schema says locn for PCE!
  > at the same time, it will create PCE workload entries (ie/ auto created when putting in 228_1 with DSS-GUI

TODO v3: add to dental encounter ie/ activity file with this nuance
- Add 228_2: 
  - note always (100%) refers to 221 (less of them) => 221's group ie/ nuance
    ... pointer of 'dental encounter' ... may rename and use this phrase for 228_1 below?
  - Can use 228.3 to categorize? Most "type of care" is just transaction; visit_date break? 

TODO v4:
- tie in to imaging

ie/ doc, imaging, workload tie in and all dental done by end

TODO: see other xxrepo notes <---- nix once crossed
"""

"""
TODO MORE NUANCE: Orders/TIU

# From V PROVIDER of DENTAL Visits

vast majority of Dental Visits have one provider with

  PERSON CLASS: Dental Providers
  P:PRIMARY
  DATA SOURCE: DENTV DSS GUI, PACKAGE: DENTAL

but few are

  DATA SOURCE: TIU ..., PACKAGE: ORDER ...

==> came from orders but orders for what?
"""

def webReportDental(stationNo):

    ensureWebReportLocations(stationNo)

    allThere, details = checkDataPresent(stationNo, [
        {"fileType": "220_5", "check": "TYPE"}, # want Dental Providers 
        {"fileType": "228_1", "check": "TYPESO"}, # no split
        {"fileType": "8925", "check": "TYPESO"},
        {"fileType": "200", "check": "ALL"} # Index
    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    mu = """---
layout: default
title: {} Dental
---

## Dental Package

""".format(stationNo) 

    # Practice of Care    
    type220_5, subs = splitTypeDatas(stationNo, "220_5", expectSubTypeProperty="")
    userInfoByUserRef = reduce200(stationNo)
    allDentalProviders = set(userRef for userRef in type220_5["name"]["byValueCount"])
    # Forcing use of SO signon ie/ last year only
    type3_081, st3_081 = splitTypeDatas(stationNo, "3_081", reductionLabel="YR1", expectSubTypeProperty="user")
        
    allUserSignOnCounts = dict((singleValue(st, "user"), st["user"]["count"]) for st in st3_081)
    currentDentalProviders = set(userRef for userRef in allDentalProviders if userRef in allUserSignOnCounts)
    # Dental History (228.1) == Dental Activity
    typeSO228_1, subs = splitTypeDatas(stationNo, "228_1", reductionLabel="YR1", expectSubTypeProperty="")
    allDentalRecordCreators = set(typeSO228_1["creator"]["byValueCount"])
    if len(allDentalRecordCreators - currentDentalProviders):
        raise Exception("Expected all dental record creators to be Current Dental Providers")
    
    # Note: this system doesn't use 220_2 in 220_5 ... dental classification -- so
    # fall back on titles.
    # ... TODO: more on Dental Activity Records (and related 228.2) for type of activity
    if "byValueCount" not in typeSO228_1["creator"]:
        raise Exception("Expect full byValueCount for {}".format("creator"))
    if "byValueCount" not in typeSO228_1["patient"]:
        raise Exception("Expect full byValueCount for {}".format("patient"))
    mu += """The system identifies <span class="yellowIt">{:,}</span> Dental Providers but only <span class='yellowIt'>{}</span> are current users, meaning they signed on to the system between _{}_ and _{}_, the most recent year for which data is available. There are <span class="yellowIt">{:,}</span> Dental Activity Records (\"Dental History\") for this period for <span class="yellowIt">{:,}</span> distinct patients treated by <span class="yellowIt">{:,}</span> of the dental providers (\"Dental Activity Providers\"). <span class="yellowIt">{:,}</span> were outpatient records, <span class="yellowIt">{:,}</span> in-patient.
    
""".format(
        len(allDentalProviders),
        reportAbsAndPercent(len(currentDentalProviders), len(allDentalProviders)),
        type3_081["user"]["firstCreateDate"].split("T")[0],
        type3_081["user"]["lastCreateDate"].split("T")[0],

        typeSO228_1["_total"],
        len(typeSO228_1["patient"]["byValueCount"]),
        len(typeSO228_1["creator"]["byValueCount"]),

        typeSO228_1["patient_type"]["byValueCount"]["O:outpatient"],
        typeSO228_1["patient_type"]["byValueCount"]["I:inpatient"]
    )
    
    # Now let's do a document break down [1] record providers, [2] others
    all8925, subTypes8925 = splitTypeDatas(stationNo, "8925", reductionLabel="YR1", expectSubTypeProperty="document_type")
    countByDocTypeByDentalProvider = defaultdict(lambda: Counter())
    parentTypeByDocumentType = {}
    for subTypeInfo in subTypes8925:
        if re.search(r'(8925_1\-0|ADDENDUM|ERRONEOUS)', subTypeInfo["_subTypeId"]):
            continue
        matched = False
        docType = singleValue(subTypeInfo, "document_type")
        parentDocType = singleValue(subTypeInfo, "parent_document_type")
        for pProp in ["expected_signer", "entered_by"]:
            if pProp not in subTypeInfo: # one in 668 (so rare!)
                continue
            pPropVC = subTypeInfo[pProp]["byValueCount"]
            matchedUserRefs = set(userRef for userRef in pPropVC if userRef in allDentalProviders)
            if len(matchedUserRefs):
                for userRef in matchedUserRefs:
                    countByDocTypeByDentalProvider[userRef][docType] = pPropVC[userRef]
                parentTypeByDocumentType[docType] = parentDocType
                break # only need one matcher - if not entered_by then expected_signer
   
    def tableDentalProviders(providers):
        count = 0
        tbl = MarkdownTable(["Provider", "Title", "Sign on \#", "Document \#s"])
        for userRef in sorted(countByDocTypeByDentalProvider, key=lambda x: sum(countByDocTypeByDentalProvider[x][y] for y in countByDocTypeByDentalProvider[x]), reverse=True):
            if userRef not in providers:
                continue # for other providers which may not write documents
            count += 1
            dtDetailsMU = ", ".join(["{} ({:,})".format(docType.split(" [")[0], countByDocTypeByDentalProvider[userRef][docType]) for docType in sorted(countByDocTypeByDentalProvider[userRef], key=lambda x: countByDocTypeByDentalProvider[userRef][x], reverse=True)])
            tbl.addRow([ 
                "__{}__".format(userRef.split(" [")[0]), 
                userInfoByUserRef[userRef]["title"] if "title" in userInfoByUserRef[userRef] else "",
                allUserSignOnCounts[userRef],
                dtDetailsMU
            ])
        return tbl, count
                
    mu += """Dental Providers write documents (\"TIU Notes\"). The most significant are written by the <span class="yellowIt">{:,}</span> _Dental Activity Providers_, those who create _Dental Histories_ (228.1) ...
    
""".format(len(allDentalRecordCreators))
    tbl, count = tableDentalProviders(allDentalRecordCreators)
    mu += tbl.md() + "\n\n"  
    
    tbl, count = tableDentalProviders(currentDentalProviders - allDentalRecordCreators)
    mu += """The remaining <span class="yellowIt">{:,}</span> Dental Providers with documents are a mix of _MSAs_ and other assistants who enter acknowledgements and consents not all of which may be about dental services ...
    
""".format(count)
    mu += tbl.md() + "\n\n"
    
    usedFiles = ["DENTAL PROVIDER", "DENTAL HISTORY", "DENTAL PATIENT"]
    mu += mdFilesOfDomain(
        stationNo, 
        "Dental Package", 
        220, 
        230,
        usedFiles
    )
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "dental.md", "w").write(mu)
        
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
    
    webReportDental(stationNo)
    
if __name__ == "__main__":
    main()
