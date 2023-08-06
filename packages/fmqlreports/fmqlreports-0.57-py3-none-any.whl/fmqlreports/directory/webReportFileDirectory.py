#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime

from fmqlutils import VISTA_DATA_BASE_DIR
from fmqlutils.cacher.cacherUtils import SCHEMA_LOCN_TEMPL 
from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

from fmqlreports.webReportUtils import SITE_DIR_TEMPL, TOP_MD_TEMPL, keyStats, roundFloat

from ifc import muPlotRef, makePlots # TMP - go to visualizeUtils etc
from fileDirectory import VISN20_VISTAS # TMP (go central to webReportUtils)
from fileDirectory import CommonFileDirectory

"""
To get to a "Core" VistA and "Exclusive" VistAs for all VISN sites. 

TODO: 
--------------------- SPECIFIC CONTENT ---------------------------
- burrow more into Exclusives (particularly in Puget) <------ BIG ONE
- 'some' files -- do SPO and POR have populated overlaps as only two to jump out for common in last graph
- verify empties can be ignored
--------------------- GENERIC/CACHE RELATED ----------------------
- consider singleton (at most one where appears ie/ can be 0 too but at most one) descriptions as these are configs?
- bands of file sizes -- # of files in bands of size ... [part of Caching]
- mult #'s ie/ # contained ... indication that doc, not rec?
- old count of pter vs ... ie/ get into quantities of props
- CACHED sizes (est vs real) [message: much variety but not big size]
"""

def webReportFileDirectory(stationNoMap, imageDir="Images"):
    
    cfd = CommonFileDirectory(stationNoMap)
    allFLs = cfd.fileIds()
    ttlRecords = cfd.totalRecords()

    mu = TOP_MD_TEMPL.format("VISN 20 File Directory")
        
    mu += """# VISN 20 File Directory
    
_FileMan_ is VistA's proprietary database. It holds not only clinical data but also nearly all the configurations, audit logs and financial information of the system. Having all this data in one location is a boon for VistA system analysis and the centrality of FileMan effectively turns VistA analysis into FileMan content analysis. 

In _FileMan_, data is gathered into \"files\" which are structured by \"data dictionaries\" or schemas. 
    
The following reports on a VISN 20 File Directory built from the data dictionaries of 7 VistAs: Puget Sound [663], Portland [648], Boise [531], Spokane [668], Roseburg [653], White City [692] and Walla Walla [687]. Together the systems hold <span class='yellowIt'>{:,}</span> distinct files containing <span class='yellowIt'>{:,}</span> records.

Note: Anchorage is the missing VISN 20 system. Its information will be added once the system is made available.
    
""".format(
        len(allFLs),
        ttlRecords
    )

    plotData = {}
    
    # ######################## Summary Criteria ############################
    # 
    # ... exclusives, singletons, all's, empties ... 
    #
    
    commonCount = cfd.commonCounts()            
    allCnt = max(commonCount)
    plotData["fileTypes"] = {
            "title": "All File Types",
            "plotName": "visn20AllFileTypes",
            "plotMethod": "plotIsHasBH",
            "specs": {
                "__entityName": "Files",
                "__total": len(allFLs),
                "all": commonCount[allCnt],
                "some": sum(commonCount[i] for i in range(2, allCnt)),
                "exclusive": commonCount[1] # rem 1-# of VistAs
            }
    }
    blurb = "Files can be grouped into those in every VistA (\"all\"), those in more than one but not all (\"some\") and those only in one (\"exclusive\"). The files in every VistA represent the __core of a VA VistA__, that portion of FileMan common to production systems ..."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["fileTypes"], imageDir)
    )

    emptiesInAll = set(cfd.filesOfCount(count=0))
    singletons = set(cfd.filesOfCount(count=1))
    plotData["fileTypesEmptySingleton"] = {
            "title": "File Types in Use",
            "plotName": "visn20FilesTypesInUse",
            "plotMethod": "plotIsHasBH",
            "specs": {
                "__entityName": "Files",
                "__total": len(allFLs),
                "empty in all": len(emptiesInAll),
                "singleton in all": len(singletons)
            }
    }
    # TODO: could make singleton == 0 or at most 1?
    # TODO: retired => last record from 5 plus years ago?
    blurb = "Files can also be grouped on whether they are \"empty\" or have only one record (\"singletons\") whereever they appear. The _empties_ usually represent retired parts of VistA and can be put aside ..."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["fileTypesEmptySingleton"], imageDir)
    )
    
    # ####################### Overall Proportions less Empty ###################
    
    commonCountNoEmpties = cfd.commonCounts(excludeFLs=emptiesInAll)
    alls = set(cfd.commonFiles())
    exclFiles = cfd.commonFiles(count=1) # only appear in one
    allFlsByGroup = {}
    for fl in allFLs:
            if fl in emptiesInAll:
                continue
            if fl in exclFiles:
                allFlsByGroup[fl] = "exclusive"
                continue
            if fl in alls:
                allFlsByGroup[fl] = "all"
                continue
            allFlsByGroup[fl] = "some"
    totalsByGroup = cfd.totalRecords(groupOfFile=allFlsByGroup)
    
    grpColumns = ["all", "some", "exclusive"]
    plotData["filesNRecordsByFileCategory"] = {
            "title": "File and Record Counts by File Category",
            "plotName": "visn20FileNRecordCountsByFileType",
            "plotMethod": "plotCategoryBH",
            "rows": ["files", "records"],
            "columns": grpColumns,
            "data": [
                (
                    commonCountNoEmpties[allCnt],
                    sum(commonCountNoEmpties[i] for i in range(2, allCnt)),
                    commonCountNoEmpties[1]
                ),
                (
                    totalsByGroup["all"],
                    totalsByGroup["some"],
                    totalsByGroup["exclusive"]
                )
            ]
    }
    blurb = "Putting aside the empty files puts focus on the active parts of the VISN 20 VistAs. See the contrast between common or core files and the proportion of records in those files - while only <span class='yellowIt'>{}</span> files are common to all systems, those common files contain <span class='yellowIt'>{}</span> of the records in these systems. In other words, the core of a VistA FileMan holds most of the records ...".format(
        reportAbsAndPercent(
            plotData["filesNRecordsByFileCategory"]["data"][0][0],
            sum(commonCountNoEmpties[i] for i in range(0, allCnt+1))
        ),
        reportPercent(
            plotData["filesNRecordsByFileCategory"]["data"][1][0],
            sum(totalsByGroup[c] for c in totalsByGroup)
        )
    )
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["filesNRecordsByFileCategory"], imageDir)
    )
    
    # ####################### By VistA (4) Common Details ###################

    commonByVistA = defaultdict(dict) # not picturing           
    commonNoEmptiesByVistA = defaultdict(dict)
    totalsByGroupByVistA = {}
    for vistaInfo in cfd.vistas():
            stationNo = vistaInfo["stationNumber"]
            stationMN = stationNoMap[stationNo]
            commonCount = cfd.commonCounts(stationNo)
            commonByVistA[stationMN] = {
                "all": commonCount[allCnt],
                "some": sum(commonCount[i] for i in range(2, allCnt)),
                "exclusive": commonCount[1]
            }
            commonCountNoEmpties = cfd.commonCounts(stationNo, emptiesInAll)
            commonNoEmptiesByVistA[stationMN] = {
                "all": commonCountNoEmpties[allCnt],
                "some": sum(commonCountNoEmpties[i] for i in range(2, allCnt)),
                "exclusive": commonCountNoEmpties[1]
            }
            mnTotal = cfd.totalRecords(stationNo, groupOfFile=allFlsByGroup)
            totalsByGroupByVistA[stationMN] = dict((grp, mnTotal.get(grp, 0)) for grp in grpColumns)

    # may have "flip perc" as option
    plotData["commonNoEmptiesByVistA"] = {
            "title": "VISN 20 VistAs - File Types Compared (No Empties)",
            "plotName": "visn20SideBySideCommonCountsNoEmpties",
            "plotMethod": "plotCategoryBSV",
            "specs": commonNoEmptiesByVistA
    }
    blurb = "Put side by side, you see that systems big and small have very similar numbers of files but that larger systems like Portland (\"POR\") have proportionately more exclusive files ..."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["commonNoEmptiesByVistA"], imageDir)
    )
    
    plotData["totalRecordsByCommonByVistA"] = {
            "title": "VISN 20 VistAs - Records",
            "plotName": "visn20SideBySideByCommonRecordCounts",
            "plotMethod": "plotCategoryBSV",
            "specs": totalsByGroupByVistA
    }
    blurb = "Record numbers, side by side tell a different story. The biggest system is Puget - not as file count indicates, Portland - and Puget is responsible for most of the populated exclusive files. In other words, though all systems have some exclusive files, they are of most (only of?) importance in Puget ..."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["totalRecordsByCommonByVistA"], imageDir)
    )
    
    # ###################### Save Plot Data and .md #####################
        
    plotDir = f'{VISTA_DATA_BASE_DIR}Common/TmpWorking/'
    print(f'Serializing vizData to {plotDir}')
    json.dump(plotData, open(f'{plotDir}plotDataFiles.json', "w"), indent=4)
    
    siteDir = SITE_DIR_TEMPL.format("Common")
    print(f'Serializing Report to {siteDir}')
    open(f'{siteDir}visn20FileDirectory.md', "w").write(mu) 

# ################################# DRIVER #######################
               
def main():

    assert sys.version_info >= (3, 4)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "PLOT":
            makePlots("Common", "Files")
            return
        raise Exception("Only argument allowed is 'PLOT'")

    webReportFileDirectory(VISN20_VISTAS)    
                 
if __name__ == "__main__":
    main()