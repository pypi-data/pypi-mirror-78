#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict
from datetime import datetime
import numpy

from fmqlutils.cacher.cacherUtils import SCHEMA_LOCN_TEMPL, metaOfVistA
from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

from ..webReportUtils import ensureWebReportLocations, SITE_DIR_TEMPL, TOP_MD_TEMPL, keyStats

"""
Basic overview of Data available in system (suits a PDF/ all is for Web)
"""
def webReportDataTypesSummary(stationNo, typeInfoById=None):
       
    if typeInfoById == None:
        typeInfoById = expectedTypeCounts(stationNo)
    noRecords = sum(typeInfoById[typId]["count"] for typId in typeInfoById)

    title = "{} Data Types Summary".format(stationNo)
    mu = TOP_MD_TEMPL.format("Data Types Summary", title)
        
    mu += muIntroduction(stationNo, typeInfoById)
    
    mu += "The top 15 types are a mixture of patient record and system log and configuration data ...\n\n"
    
    top15 = set()
    tbl = MarkdownTable(["Rank", ":Type", "Records", "Share"], includeNo=False)
    for i, typId in enumerate(sorted(typeInfoById, key=lambda x: typeInfoById[x]["count"], reverse=True), 1):
        top15.add(typId)
        fid = re.sub(r'\_', '.', typId)
        cntMU = typeInfoById[typId]["count"] if typeInfoById[typId]["count"] != -1 else "UNTRACKED"
        percMU = reportPercent(typeInfoById[typId]["count"], noRecords) if typeInfoById[typId]["count"] > 0 else ""
        tbl.addRow([typeInfoById[typId]["rank"], "__{}__ ({})".format(typeInfoById[typId]["label"], fid), cntMU, percMU])
        if i == 15:
            break
    mu += tbl.md() + "\n\n"
    
    # In case not in the top 15
    OTHER_SIGNIFICANT_FILES = set([
        "3_081",
        "2", # PATIENT
        "9_4", # PACKAGE
        "44", # HOSPITAL LOCATION
        "200", # NEW PERSON
        "409_84", # SDEC APPOINTMENT
        "627_8", # DIAGNOSTIC RESULTS - MENTAL HEALTH 
        "631", # H... Patient
        "665", # Prosthetic Patient
        "790", # WV Patient
        "2005", # IMAGE
        "8925", # TIU DOCUMENT
        "8925_1", # TIU DOCUMENT DEFINITION
        "8994", # REMOTE PROCEDURE
    ])
        
    mu += "Other less populated but significant files include ...\n\n"
    
    tbl = MarkdownTable(["Rank", ":Type", "Records", "Share"], includeNo=False)
    for i, typId in enumerate(sorted(typeInfoById, key=lambda x: typeInfoById[x]["count"], reverse=True), 1):
        if typId not in OTHER_SIGNIFICANT_FILES:
            continue
        if typId in top15:
            continue
        fid = re.sub(r'\_', '.', typId)
        cntMU = typeInfoById[typId]["count"] if typeInfoById[typId]["count"] != -1 else "UNTRACKED"
        percMU = reportPercent(typeInfoById[typId]["count"], noRecords) if typeInfoById[typId]["count"] > 0 else ""
        tbl.addRow([typeInfoById[typId]["rank"], "__{}__ ({})".format(typeInfoById[typId]["label"], fid), cntMU, percMU])
    mu += tbl.md() + "\n\n"
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "dataTypesSummary.md", "w").write(mu)

"""
Full enumeration of available data (web suitable - summary suits a PDF)
"""    
def webReportDataTypesAll(stationNo, typeInfoById=None):

    if typeInfoById == None:
        typeInfoById = expectedTypeCounts(stationNo)
    noRecords = sum(typeInfoById[typId]["count"] for typId in typeInfoById)

    title = "{} Data Types".format(stationNo)
    mu = TOP_MD_TEMPL.format("Data Types", title)
    
    mu += muIntroduction(stationNo, typeInfoById)
    
    currentPercentile = -1
    tbl = None
    for i, typId in enumerate(sorted(typeInfoById, key=lambda x: typeInfoById[x]["count"], reverse=True), 1):
        fid = re.sub(r'\_', '.', typId)
        cntMU = typeInfoById[typId]["count"] if typeInfoById[typId]["count"] != -1 else "UNTRACKED"
        percMU = reportPercent(typeInfoById[typId]["count"], noRecords) if typeInfoById[typId]["count"] > 0 else ""
        sizePercentile = typeInfoById[typId]["sizePercentile"] if "sizePercentile" in typeInfoById[typId] else ""
        if sizePercentile != currentPercentile:
            currentPercentile = sizePercentile
            if tbl:
                mu += tbl.md() + "\n\n"
            mu += "{} Percentile ...\n\n".format(currentPercentile)
            tbl = MarkdownTable(["\#", ":Type", "Records", "Share"], includeNo=False)
            j = 1
        else:
            j += 1
        if typeInfoById[typId]["count"] == -1:
            if currentPercentile != -1:
                currentPercentile = -1
                tbl.addSeparatorRow()
            tbl.addRow(["{}/{}".format(j, i), "__{}__ ({})".format(typeInfoById[typId]["label"], fid), "", "", ""])    
            continue 
        tbl.addRow([i, "__{}__ ({})".format(typeInfoById[typId]["label"], fid), cntMU, percMU])
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "dataTypes.md", "w").write(mu)
    
"""
Basic summary shared by ALL and Summary reports
"""
def muIntroduction(stationNo, typeInfoById):

    noEmptyTypes = sum(1 for typId in typeInfoById if typeInfoById[typId]["count"] == 0)
    # untrack is -1
    noUntrackedTypes = sum(1 for typId in typeInfoById if typeInfoById[typId]["count"] == -1)
    noRecords = sum(typeInfoById[typId]["count"] for typId in typeInfoById)
    
    cnts = [typeInfoById[typId]["count"] for typId in typeInfoById if typeInfoById[typId]["count"] > 1]
    singletonCnts = sum(1 for typId in typeInfoById if typeInfoById[typId]["count"] == 1)
    kstats = keyStats(cnts)
    median = int(round(kstats["median"]))
    recordCntBiggest = sorted(cnts, reverse=True)[0]
    
    # 'fails' gracefully on meta and perhaps run BEFORE any but schema exist
    meta = metaOfVistA(stationNo)
    mu = "__{} [{}]__ was cut on _{}_ and reports <span class='yellowIt'>{:,}</span> types of data (\"File Types\"), <span class='yellowIt'>{}</span> of which are singletons (have only one record), <span class='yellowIt'>{}</span> are empty and <span class='yellowIt'>{:,}</span> are untracked. The system has a total of <span class='yellowIt'>{:,}</span> records. While the biggest type has <span class='yellowIt'>{:,}</span> records, the median number of records for types with more than one record is a lowly <span class='yellowIt'>{:,}</span>.\n\n".format(
        meta.get("name", "VistA"), 
        stationNo, 
        meta["cutDate"],
        len(typeInfoById), 
        reportAbsAndPercent(singletonCnts, len(typeInfoById)), 
        reportAbsAndPercent(noEmptyTypes, len(typeInfoById)), 
        noUntrackedTypes, 
        noRecords, 
        recordCntBiggest, 
        median
    )
    
    return mu
    
"""
Utility that using SELECT TYPES to rank files by count and give them
a size percentile

TODO: if full and SO for types then may add date summary ie/ first entry etc
"""
def expectedTypeCounts(stationNo):
    try:
        selectTypes = json.load(open(SCHEMA_LOCN_TEMPL.format(stationNo) + "SELECT_TYPES.json"))
    except:
        raise Exception("Can't load SELECT_TYPE.json from {}".format(SCHEMA_LOCN_TEMPL.format(stationNo)))
    expectedCountByType = {}
    ranks = set()
    cnts = []
    for result in selectTypes["results"]:
        if "parent" in result:
            continue
        typ = re.sub(r'\.', '_', result["number"])
        if "count" not in result:
            cnt = 0
        elif re.search(r'\-', result["count"]):
            cnt = -1
        else:
            cnt = int(result["count"]) 
            cnts.append(cnt)
        if cnt not in ranks:
            ranks.add(cnt)
        expectedCountByType[typ] = {"label": result["name"], "count": cnt}
    ranks = sorted(list(ranks), reverse=True)
    percentileThress = []
    for ptile in range(90, 0, -10):
        thres = numpy.percentile(cnts, ptile)
        percentileThress.append((int(thres), ptile))
    for typ in expectedCountByType:
        if expectedCountByType[typ]["count"] == -1: # no rank given
            continue
        expectedCountByType[typ]["rank"] = ranks.index(expectedCountByType[typ]["count"]) + 1
        if expectedCountByType[typ]["count"] == 0:
            continue
        for percThres in percentileThress:
            if expectedCountByType[typ]["count"] >= percThres[0]:
                expectedCountByType[typ]["sizePercentile"] = percThres[1]
                break
    return expectedCountByType

# ################################# DRIVER #######################
               
def main():

    assert sys.version_info >= (3, 4)
    
    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO")
        
    ensureWebReportLocations(stationNo)

    webReportDataTypesSummary(stationNo)
                 
    webReportDataTypesAll(stationNo)
    
if __name__ == "__main__":
    main()
