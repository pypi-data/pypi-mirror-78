#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict
from datetime import datetime
import numpy

from fmqlutils.cacher.cacherUtils import SCHEMA_LOCN_TEMPL 
from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

from ..webReportUtils import SITE_DIR_TEMPL, TOP_MD_TEMPL, keyStats, roundFloat

"""
Basic overview of Data available in system 
"""
def webReportSubReportDataTypes(stationNo):

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
            if expectedCountByType[typ]["count"] == -1:
                continue
            expectedCountByType[typ]["rank"] = ranks.index(expectedCountByType[typ]["count"]) + 1
            if expectedCountByType[typ]["count"] == 0:
                continue
            for percThres in percentileThress:
                if expectedCountByType[typ]["count"] >= percThres[0]:
                    expectedCountByType[typ]["sizePercentile"] = percThres[1]
                    break
        return expectedCountByType
    typeInfoById = expectedTypeCounts(stationNo)

    title = "{} Data Types and Sizes".format(stationNo)
    mu = TOP_MD_TEMPL.format("Subreport Data Types and Sizes", title)
                
    # Reorganize
    labelByTypId = {}
    subReportsByTypId = defaultdict(list)
    for metaInfo in subReportInfo:
        title = metaInfo["title"]
        for typInfo in metaInfo["types"]:
            labelByTypId[typInfo["id"]] = typInfo["label"]
            subReportsByTypId[typInfo["id"]].append((title, typInfo["scope"]))
    
    mu += "## Data Types used for this Report\n\n"
    mu += "<span class='yellowIt'>{:,}</span> types of data are used in the following sections of this report ...\n\n".format(len(labelByTypId))
    
    tbl = MarkdownTable(["Rank", "Type", "Records", "Section"], includeNo=False)
    for typId in sorted(labelByTypId, key=lambda x: typeInfoById[re.sub(r'\.', '_', x)]["rank"]):
        typeInfo = typeInfoById[re.sub(r'\.', '_', typId)]
        tbl.addRow([typeInfo["rank"], "__{}__ ({})".format(labelByTypId[typId], typId), typeInfo["count"], ", ".join(["__{}__ ({})".format(sr[0], sr[1]) for sr in subReportsByTypId[typId]])]) 
    mu += tbl.md() + "\n\n"
    
    mu += "where _ALL_ means all of the records of a type are used while _SO_ means only those records created during the period for which sign on logs exist are examined.\n\n"
    
    mu += "As the report expands more types of data will be examined.\n\n"
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "subReportDataTypes.md", "w").write(mu)

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
        
    TYPES_USED_BY_SUBREPORT = json.load(open(userSiteDir + "subReportInfo.json"))

    webReportSubReportDataTypes(stationNo, TYPES_USED_BY_SUBREPORT)
                 
if __name__ == "__main__":
    main()
