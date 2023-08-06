#!/usr/bin/env python
# -*- coding: utf8 -*-

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

from ifc import muPlotRef, makePlots # TMP (go central to visualizeUtils)
from webReportFileDirectory import VISN20_VISTAS # TMP (go central to webReportUtils)
from patientDirectory import CommonPatientDirectory
from userDirectory import CommonUserDirectory

from webReportUserDirectory import csvDatesBySNO
        
"""
See note in user directory (as //)

... TODO: will split more as dive in (patient's common far less + need to make
up for lack of patient dates ... 
"""

# ###################################### Totals  ############################

PLOT_PREFIX = "visn20Patient"

def makeTotalsSection(cd, vistaNames, imageDir="Images"):
                       
    plotData = {}
                       
    mu = "## Patient Breakdown\n\n"
               
    countsFromTotal = { 
        "__entityName": "Patients",
    
        "__total": cd.total(),
        
        "> 1 VistA": cd.gt1VistACount(), # SHOULD BE IN OWN GRAPHIC
            
        "Male": cd.males(),
        "Marked Deceased": cd.deceased(),
        "Users Too": cd.usersToo(), 
    
        "FICN": cd.idPresence(CommonPatientDirectory.ENTRY_FICN_IDX), 
        "SSN": cd.idPresence(CommonPatientDirectory.ENTRY_SSN_IDX),
        "SCN": cd.idPresence(CommonPatientDirectory.ENTRY_SCN_IDX),
        "No ID": cd.noIds()
    }
    
    plotData["patientPercs"] = {
            "title": f'{countsFromTotal["__total"]} Patients',
            "plotName": f'{PLOT_PREFIX}Percs',
            "plotMethod": "plotIsHasBH",
            "specs": countsFromTotal
    }
    blurb = "The directory holds <span class='yellowIt'>{:,}</span> patients. <span class='yellowIt'>{}</span> are Male and nearly all have Integration Control Numbers (ICN) and Social Security Numbers (SSN). <span class='yellowIt'>{}</span> are marked deceased in at least one VistA holding part of their medical records. Note that <span class='yellowIt'>{}</span> of patients are also VistA users.".format(
        countsFromTotal["__total"],
        reportPercent(countsFromTotal["Male"], countsFromTotal["__total"]),
        reportPercent(countsFromTotal["Marked Deceased"], countsFromTotal["__total"]),
        reportPercent(countsFromTotal["Users Too"], countsFromTotal["__total"])
    )
    mu += "{}\n\n{}\n\n".format(
        blurb, 
        muPlotRef(plotData["patientPercs"], imageDir)
    )
        
    commonTotals = defaultdict(dict) # not picturing           
    allCnt = len(cd.vistas())
    for vistaInfo in cd.vistas():
        stationNo = vistaInfo["stationNumber"]
        stationMN = vistaNames[stationNo]
        commonCountsNos = cd.commonCounts(stationNo)
        commonCountsPer = {
            "all": commonCountsNos[allCnt],
            "some": sum(commonCountsNos[i] for i in range(2, allCnt)),
            "exclusive": commonCountsNos[1]
        }
        commonTotals[stationMN] = commonCountsPer
        
    plotData["commonByVistA"] = {
            "title": "Common Patient Count",
            "plotName": f'{PLOT_PREFIX}Common',
            "plotMethod": "plotCategoryBSV",
            "specs": commonTotals
    }
    blurb = "The graph below shows the total number of patients in each system as well as a breakdown of whether those patients are unique to that system (exclusive), in some but not every other system (some) or in every other (all) systems in the directory. Unlike the equivalent graph for user directory, this seems to show that systems big and small have similar proportions of unique and shared patients, but they don't."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["commonByVistA"], imageDir)
    )
    
    plotData["commonByVistAPerc"] = {
            "title": "Common Patient Count (Percentage)",
            "plotName": f'{PLOT_PREFIX}PercCommon',
            "plotMethod": "plotCategoryBSV",
            "specs": commonTotals,
            "kargs": { 
                "usePerc": True
            }
    }
    blurb = "The percentage view makes it clearer that smaller systems such as Walla Walla (WWW) through Roseland (ROS) have proportionately far more shared patients than their larger peers such as Puget Sound (PUG) or Portland (POR). This may be due to interfacility-consult work where a larger facility performs care for the patients of a smaller peer or because patients must go to bigger institutions for specialized care."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["commonByVistAPerc"], imageDir)
    )
        
    return plotData, mu
    
# #################################### Time Series Section ##########################

"""
Stories shown Patient:
- last two full months the patient addition is as expected, weekend and holiday drops and Puget is biggest, Walla Walla is smallest. It does show that unlike other systems, Puget does add patients, albeit at a lower number than usual, on holidays such as 1/20 and 2/17.
- pull back to yearly trends and again Puget is biggest but its gap on Portland only begins to grow in the last ten years
- monthly resamples reflect just what's expected. 
- addition very even in last five years in order expected
"""

def makeTimeSeriesSection(cd, vistaNames, imageDir="Images"):

    plotData = {}
    end = "2020-02"

    mu = "## Patient Additions over Time\n\n"
    
    dailiesDFCSV = csvDatesBySNO(cd)
            
    plotData["tsDailies"] = {
        "title": "2020/01-2020/02 Patient Addition",
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plotDailies",
        "dfcsv": dailiesDFCSV,
        "kargs": {
            "vistaNamesPlus": vistaNames,
            "start": "2020-01",
            "end": end
        }
    }
    blurb = "The following shows __Daily Patient Addition__ for the last full three months for which data is available with Mondays marked on the X-axis. As expected addition \"dances\" up on weekdays and down on weekends which show little activity. For every system but Puget (PUG), holidays (1/20, 2/17) act like weekends. In contrast with the _User Directory_, this directory's additions mirror system size - Puget exceeds Portland (POR), all the way down the smallest, Walla Walla (WWW)."
    mu += "{}\n\n{}\n\n".format(
        blurb, 
        muPlotRef(
            plotData["tsDailies"],
            imageDir
        )
    )
        
    plotData["ts365RollingMean"] = {
        "title": "Trends in Patient Addition (365 day rolling)",
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plot365RollingMean",
        "dfcsv": dailiesDFCSV,
        "kargs": {
            "vistaNamesPlus": vistaNames,
            "start": "1987-01", 
            "end": end
        }
    }
    blurb = "Here are the yearly trends using a __\"365 day rolling mean\"__ starting when the directory first gets data to the latest additions. Again, additions follow system size but first in 2000 and then in 2009, Puget and Portland jump up in volume compared to their  smaller peers with Puget's magnitude of increase exceeding Portland's. Except for Roseland, which seems to follow its own way. The reason for this - new types of care or additional clinics supported in systems? - should be investigated."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(
            plotData["ts365RollingMean"],
            imageDir
        )
    )
    
    plotData["tsMonthlyResamples"] = {
        "title": "Patients - Resampled Monthly (2018-{})".format(re.sub(r'\-', '/', end)),
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plotMonthlyResamples",
        "dfcsv": dailiesDFCSV,
        "kargs": {
            "vistaNamesPlus": vistaNames,
            "start": '2018-01', 
            "end": end
        }
    }
    blurb = "A __monthly resample__ from 2018 to the latest common date echo's the yearly trends - unlike for User Directory, there are no unpredicted peaks or troughs."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(
            plotData["tsMonthlyResamples"],
            imageDir
        )
    )
  
    plotData["tsTotalsPerYear"] = {
        "title": "Patients - Annual Additions (2015-{})".format(re.sub(r'\-', '/', end)),
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plotTotalsPerYear",
        "dfcsv": dailiesDFCSV,
        "kargs": {
            "vistaNamesPlus": vistaNames,
            "start": "2015", 
            "end": end
        }
    }
    blurb = "Finally, a simple __side by side set of totals__ for the last five years shows all systems adding similar numbers, year after year. It also reiterates that the bigger the system, the more patient additions it has - Puget adds up to <span class='yellowIt'>25,000</span> patients per year while Walla Walla adds less than <span class='yellowIt'>4,000</span>."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(
            plotData["tsTotalsPerYear"],
            imageDir
        )
    )
                                
    return plotData, mu
            
# ############################## DRIVER ################################
            
def main():

    assert sys.version_info >= (3, 6)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "PLOT":
            makePlots("Common", "Patients")
            return
        raise Exception("Only argument allowed is 'PLOT'")

    dirName = "Patient"
    cpd = CommonPatientDirectory(VISN20_VISTAS, CommonUserDirectory(VISN20_VISTAS))

    plotData = {}
    mu = f"""---
layout: default
title: VISN 20 {dirName} Directory
---

# VISN 20 {dirName} Directory

"""

    mu += """The following reports on a VISN 20 Patient Directory built from the patient file (2) of 7 VistAs: Puget Sound [663], Portland [648], Boise [531], Spokane [668], Roseburg [653], White City [692] and Walla Walla [687]. Together they hold <span class='yellowIt'>{:,}</span> distinct patients using <span class='yellowIt'>{:,}</span> patient file records.

Note: Anchorage is the missing VISN 20 system. Its information will be added once the system is made available.

""".format(
        cpd.total(),
        cpd.entryTotal()
    )
    
    ttlPlotData, ttlMU = makeTotalsSection(cpd, VISN20_VISTAS)
    mu += ttlMU
    plotData.update(ttlPlotData)
    
    tsPlotData, tsMU = makeTimeSeriesSection(cpd, VISN20_VISTAS)
    mu += tsMU
    plotData.update(tsPlotData)
        
    plotDir = f'{VISTA_DATA_BASE_DIR}Common/TmpWorking/'
    print(f'Serializing vizData to {plotDir}')
    json.dump(plotData, open(f'{plotDir}plotDataPatients.json', "w"), indent=4)
                
    siteDir = SITE_DIR_TEMPL.format("Common")
    print(f'Serializing Report to {siteDir}')
    open(f'{siteDir}visn20PatientDirectory.md', "w").write(mu) 
        
if __name__ == "__main__":
    main()
    