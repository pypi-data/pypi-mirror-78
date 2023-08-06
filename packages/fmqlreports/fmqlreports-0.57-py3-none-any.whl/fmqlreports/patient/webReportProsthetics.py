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
from ..webReportUtils import SITE_DIR_TEMPL, loadSelectTypes, reduce200, mdFilesOfDomain

"""
Prosthetics ... follow Dental, Health Factors

Requires:
- SELECT TYPEs for File Types

TO SEE:
- home ox Rx in multiple of Pros Patient

"""
def webReportProsthetics(stationNo):

    allThere, details = checkDataPresent(stationNo, [
    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    mu = """---
layout: default
title: {} Prosthetics
---

## Prosthetics

""".format(stationNo) 
    
    usedFiles = ["PROSTHETICS PATIENT"]
    mu += mdFilesOfDomain(
        stationNo, 
        "Prosthetics", 
        660, 
        670,
        usedFiles
    )
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "prosthetics.md", "w").write(mu)
        
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
    
    webReportProsthetics(stationNo)
    
if __name__ == "__main__":
    main()
