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

from fmqlreports.webReportUtils import SITE_DIR_TEMPL

"""
Basic Patient

   - # total
   - # alive, dead
   - longevity median
   - median age of those alive
   - veteran y or n for alive
   - period of service for all
   (ie/ quick go)
"""
def webReportPatient(stationNo):

    allThere, details = checkDataPresent(stationNo, [
        {"fileType": "2", "check": "TYPE"}
    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    mu = """---
layout: default
title: {} Patient
---

## Patient Basics

""".format(stationNo) 

    # Practice of Care    
    type2, subs = splitTypeDatas(stationNo, "2", expectSubTypeProperty="date_of_death")
    
    print("Total known {}".format(type2["_total"]))
    print("Alive {}".format(type2["_total"] - type2["date_of_death"]["count"]))
    longevity = Counter()
    for sub in subs:
        if "date_of_death" not in sub:
            aliveSub = sub
            continue
        deathDate = int(singleValue(sub, "date_of_death"))
        for dob in sub["date_of_birth"]["byValueCount"]:
            ageAtDeath = deathDate - int(dob)
            longevity[ageAtDeath] += 1
    print(longevity)
        
    print(aliveSub["period_of_service"])
    print()
    return
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "patient.md", "w").write(mu)

"""
Criteria: if has entry for ANY of vitals, ... in last three years.

Required: SO 3 Years for key clinical data

TODO: move to webReportPatientUtils.py and may write to TMP
"""    
def lastThreeYearsPatients(stationNo):
    pass
        
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
    
    webReportPatient(stationNo)
    
if __name__ == "__main__":
    main()
