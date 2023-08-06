#!/usr/bin/env python
# -*- coding: utf8 -*-

#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import io
import json
from collections import defaultdict, Counter
from datetime import datetime

import pandas as pd

from fmqlutils import VISTA_DATA_BASE_DIR
from fmqlutils.cacher.cacherUtils import SCHEMA_LOCN_TEMPL 
from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent
from fmqlreports.webReportUtils import SITE_DIR_TEMPL, TOP_MD_TEMPL, keyStats, roundFloat

from ifc import muPlotRef, makePlots # TMP (go central to visualizeUtils)
from webReportFileDirectory import VISN20_VISTAS # TMP (go central to webReportUtils)
from userDirectory import CommonUserDirectory
        
"""
QUICK TODO: 
- reorder the render of user totals in time series (last graph) so biggest appears first ie/ key has PUG, POR ... vistaNamesPlus needs to be ordered

Goal for directories in general - user ala patient with one, move id checks there but
first need to see what's there now. Federated Directory => mismatch possible, dup,
possible

REM: want ALL User (and Patient?) fixed up and cleaned up (individ and dir) by Labor Day
[one of three key areas inc IFC/TeleR + Data Shape/Sizes]

TODO: and in parallel, improve and make visuals generic
- [ ] make clear the time span of the individual vista (ie/ cut date!) --- want one cut date for directory ie/ cut off all to time of oldest VistA
- [ ] remote vs local user! KEY! --- feeds WWW etc mostly elsewhere (all 4!)
  ... correlate with patients in all? get into 'scatters?'
  (want the "user gone by Labor day")
- [ ] secid growing user (new dups etc) ... "SECID-use" issue! ... 
- [ ] term/demise (user and patient (more))
- [ ] FIX to end date of earliest for data ... as don't want SPO (with extra month) over POR etc in 2020. Leave start date as is.
- [ ] look on graphs -- | black on X and Y axes so clearer
- [ ] Link VISN 20 (VISN 20 https://www.va.gov/directory/guide/region.asp?ID=1020) Directories -- shared care across hospitals and clinics ie/ can treat as unit! ... ALSO may find some are more stand-alone (anchrorage doesn't matter? ... gotta see visits froms)
- New Plot
  - [ ] Scatter Plot use ---> Demise vs Patients added per month ie/ two tracked
  - [ ] Patient age at addition -- does this vary? [age of live patients at cut time]
  (see scatter: https://towardsdatascience.com/5-amazing-tips-for-data-visualization-990fdb19c396)
- [I] time series left
  - "ALL" total ie/ first date of any user
    ... change to serialize CSV at same time in directory using 
  <----- doing user/ seems to make sense but make sure ... main place is totals (NEED TO LOOK INTO IF TRULY NEW ETC ... ie/ DO THE TELEREADER ONLY DIRECTORY USER REPORT and then get back to this)
- [ ] go back to two first months of year for dir as three doesn't stand out right ???
- [ ] BIG And KEY -- HOME PATIENT, HOME USER <---- tell how ... do a pass alg ie/ user => created explicitly
- [user only] no creator vs creator [Auto Entry Addition] ... telling on 2006 or 2019? --- interplay with TERMINATION (a lot a lot in Portland ie/ show contrast)
- [user + patient] 'term' and 'demise' ...
- missing date fill in ie/ evens (got in Patient, add to User and must graph records w/o - extrapolate by surroundings? ie/ guessed date) ---- really only a Patient Problem (seems mainly ok for user)
- automate start-end off VistA image start end (and better doc in md) ie/ automate the ranges (put into dir entries?) ... fix rogues?
  REM: por, www oldest at 3/25 => why do feb back ... cut time series back to there too
  [means for report can handle rolling start-end]
- Variation: Registration Time Delay for studies ie/ 1 patients registered due to studies and two, delay! [studyId, studyDay, patient create day acq, patient create day read] ie/ gets to Patient being in > 1 system and how they get there!

[Context: want fuller Sankey for IFC, TeleR completed in this time frame too]

TODO  NEXT: bigger
- BETTER SPLIT of PATIENT/ USER vs records with fan out of patient, user (first created somewhere) to various systems. ie/ pitch is normalized with (in case of user) 'wasteful'
VistA copies. IE/ FEDERATED DIRECTORIES have issues ... - records flow to ... first
user or patient.
- patient and why ... for IFC? for appt? ie/ what's the trigger?
- feed directory reports back into individual system reports
"""

# ###################################### Totals  ############################

# ... put in line about USER, PATIENT total as a stand out ala NYT graph ie/ all
# lines but that line are greyed
# ... blurb on Directory => Users may have > 1 record in a VistA (misplaced duplication will be a section) ... lifecycle management too (with last logins from anywhere?)
# GOAL: centralize user mgmt to ease migration and management [ 1 of a # for dec]

PLOT_PREFIX = "visn20User"

def makeTotalsSection(cd, vistaNames, imageDir="Images"):
                       
    plotData = {}
                       
    mu = "## User Breakdown\n\n"
               
    countsFromTotal = {
        "__entityName": "Users",
    
        "__total": cd.total(),
        
        "> 1 VistA": cd.gt1VistACount(), # SHOULD BE IN OWN GRAPHIC
    
        "SSN": cd.idPresence(CommonUserDirectory.ENTRY_SSN_IDX),
        "SECID": cd.idPresence(CommonUserDirectory.ENTRY_SECID_IDX),
        "NWNM": cd.idPresence(CommonUserDirectory.ENTRY_NWNM_IDX),
        "DUID": cd.idPresence(CommonUserDirectory.ENTRY_DUID_IDX)
    }
    plotData["userPercs"] = {
            "title": f'{countsFromTotal["__total"]} Users',
            "plotName": f'{PLOT_PREFIX}Percs',
            "plotMethod": "plotIsHasBH",
            "specs": countsFromTotal
    }
    blurb = "The directory holds <span class='yellowIt'>{:,}</span> Users. The majority are in greater than one VistA. Most have a social security number (SSN) while a much smaller number have VA's own \"security id\" (secid).".format(countsFromTotal["__total"])
    mu += "{}\n\n{}\n\n".format(
        blurb, 
        muPlotRef(plotData["userPercs"], imageDir)
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
            "title": "Common User Count",
            "plotName": f'{PLOT_PREFIX}Common',
            "plotMethod": "plotCategoryBSV",
            "specs": commonTotals
    }
    blurb = "The graph below shows the total number of users in each system as well as a breakdown of whether those users are unique to that system (exclusive), in some but not all systems (some) or in every (all) other systems in the directory. It's striking how few of the users in the smaller systems - Walla Walla (WWW) and Spokane (SPO) - are unique to them. Indeed, for WWW, most of its users appear in some or every other system."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["commonByVistA"], imageDir)
    )
    
    plotData["commonByVistAPerc"] = {
            "title": "Common User Count (Percentage)",
            "plotName": f'{PLOT_PREFIX}PercCommon',
            "plotMethod": "plotCategoryBSV",
            "specs": commonTotals,
            "kargs": { 
                "usePerc": True
            }
    }
    blurb = "The following shows the same information but instead of totals, each system's representation distinguishes the percentage of its users that are unique from those that also appear elsewhere. Puget Sound, the biggest system, has the highest proportion of unique users. Clearly most users in smaller VistAs also use or have some impact on other VistAs."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["commonByVistAPerc"], imageDir)
    )
        
    return plotData, mu
    
# #################################### Time Series Section ##########################

"""
Stories shown User:
- last three full months across all four systems, 12/19-2/20, shows evenness, holiday and weekend dips and Puget adding more users than other systems. All 'marching along' inside Puget, Portland trying to reach up.
- pull back and look at yearly trends, there are four main changes to such evenness, in 
- last five years, monthly means highlights how different 2019 was. Portland's additions exceed Pugets and both these VistAs and Spokane add far more users than normal. But note (and TODO: follow up), the mid peek of POR and SPO seems to pre-existing users.
- last five years annual totals show how different 2019 was, both in volume for all systems except Walla Walla and, for once, Portland adds more users than Puget
"""

def makeTimeSeriesSection(cd, vistaNames, imageDir="Images"):

    plotData = {}
    
    end = "2020-02" # so common for all (make dynamic going forward)

    mu = "## User Additions over Time\n\n"
    
    dailiesDFCSV = csvDatesBySNO(cd)
        
    vistaNamesPlus = vistaNames.copy()
    vistaNamesPlus["USER"] = "New" # new users
    
    plotData["tsDailies"] = {
        "title": "2020/01-{} User Addition".format(re.sub(r'\-', '/', end)),
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plotDailies",
        "dfcsv": dailiesDFCSV,
        "kargs": {
            "vistaNamesPlus": vistaNamesPlus,
            "start": "2020-01",
            "end": end
        }
    }
    blurb = "The following shows __Daily User Addition__ for the last full three months for which data is available with Mondays marked on the X-axis. As expected addition mainly happens on weekdays with holidays (1/1, 1/20 and 2/17) and weekends showing little activity. December shows less activity than the following months with a steady decline through the end of the month. As expected, Puget (PUG) adds the most users but given the disparity in system size - something that shows up in the Patient Directory Report - it is surprising how close the numbers for all systems are. _This needs examination_."
    mu += "{}\n\n{}\n\n".format(
        blurb, 
        muPlotRef(
            plotData["tsDailies"],
            imageDir
        )
    )
        
    plotData["ts365RollingMean"] = {
        "title": "Trends in User Addition (365 day rolling)",
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plot365RollingMean",
        "dfcsv": dailiesDFCSV,
        "kargs": {
            "vistaNamesPlus": vistaNamesPlus,
            "start": "1987-01", 
            "end": end
        }
    }
    blurb = "Here are the yearly trends using a __\"365 day rolling mean\"__ starting when the directory first gets data to the latest additions. In general, additions follow system size (Puget, Portland, Spokane, Walla Walla) but there's an exception in 2019 where four of the seven have a large spike in additions and Portland exceeds Puget's total. This is one of four times where the rate of addition changes - the others are 2002, 2006 and 2009. _All need examination_ - they must reflect the addition of or changes to VistA applications and use."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(
            plotData["ts365RollingMean"],
            imageDir
        )
    )
    
    plotData["tsMonthlyResamples"] = {
        "title": "Users - Resampled Monthly (2018 - {})".format(re.sub(r'\-', '/', end)),
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plotMonthlyResamples",
        "dfcsv": dailiesDFCSV,
        "kargs": {
            "vistaNamesPlus": vistaNamesPlus,
            "start": '2018-01', 
            "end": end
        }
    }
    blurb = "When the data is __resampled by month__, it shows three subpeaks for the 2019 leap in additions. The reason for Portland's leap above Puget also shows more clearly - though Puget has one large spike in April 2019, Portland has two, one in July and one in September. Note that the lack of any spike mirrors the flat line for smaller systems during this period in the yearly trends above.\n\nThis graph also shows - in purple - the running total of new users added. As seen above, users added to VistAs sometimes already pre-exist in other VistAs. While the new user line shadows Puget's peak in April and Portland's in September, it is markedly lower than the spikes for Portland and Spokane in July - this indicates that much of those spikes are existing (Puget?) users being added to these systems. _This needs examination_."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(
            plotData["tsMonthlyResamples"],
            imageDir
        )
    )
  
    plotData["tsTotalsPerYear"] = {
        "title": "Users - Annual Additions (2015 - {})".format(re.sub(r'\-', '/', end)),
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plotTotalsPerYear",
        "dfcsv": dailiesDFCSV,
        "kargs": {
            "vistaNamesPlus": vistaNamesPlus,
            "start": "2015", 
            "end": end
        }
    }
    # TODO: calc these #'s - dangerous to just put here
    blurb = "Finally, a simple __side by side set of totals__ for the last five years echo's the graphs above with Portland jumping ahead of Puget in 2019. That year, Portland added <span class='yellowIt'>60,000</span> users, twice the number of a \"normal\" year. Spokane, too nearly doubled its numbers while Walla Walla stayed steady with under <span class='yellowIt'>20,000</span> additions. The years prior to 2019 share the same steady pattern of addition."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(
            plotData["tsTotalsPerYear"],
            imageDir
        )
    )
                                    
    return plotData, mu
    
# ######################### Utils used by Patient Too ######################
    
"""
DF Start
(will move to own utils)

A FOLLOW DIRECTLY: https://medium.com/li-ting-liao-tiffany/solving-real-world-business-questions-with-pandas-70ef8ef02675
... see all the techniques and trade offs 
ie/ cleaning, grouping etc and then compare to Typer

Basic DF to Typer:
- col per subTypeId (fixed value) + one other col with variable values
  ie/ <=> groupby?
  ... many individually grouped by
=> N DF's based on # of props + extra for create as "dayOfWeekCreated" etc.
(do first on Placer Consults -- see notes)

DF for all data exercise (perhaps enum -> C: only, timestamp down?, )
- Basic DF exercise --- how big would a straight up loading of rows get? (count of mults)
  ... load all
  ... ts.memory_usage(deep=True)
  ... idea of "store as a categorical!" ie/ enum of values elsewhere and ref with int ... may be better ... ie/ often "object" -> "category" ts2['name'].astype('category')
see: https://pandas.pydata.org/pandas-docs/stable/user_guide/scale.html

DF default reports and plotting <----------- KEY
  
Typer Improve Goals too:
... rem: context is byType grouping that doesn't loose granularity ie/ it's already
a pre-grouping. When going to pandas, gotta work out what I want to see in pandas.
ex/ if all by service of IFC => one service value and could see range of that etc ...
- byValueCount --- just put straight ie/ {}
- use __ for all meta including __count etc
- date inline too and all others?
- byHour option to go with byDay, byMonth, byYear + Day of Week (sample rate)
- option to reference off to labels for pters => if used in subtypes over all over!
      ... 200 ref efficiency ie/ label out ... may do just for it for now (and can expand those types) ... ie/ only 200 at start as others could balloon ... then do others if # lvalues << # asserts ... do comparison 
        ... will need big code change! ie/ do see 200- and then ...
        ... also need a convert new to old type if need be ... [util so no need to regen all]
... _ _count ala _subTypeId
- want the setup options (date time granularty etc to be obvious up front (and drive pandas?) and have a separate .info option?
- import to pandas option (and can see pandas data usage using nvy_df.info)

Takes result of directory.dumpTimeSeriesData() into a DataFrame

https://medium.com/sfu-cspmp/advanced-visualization-for-data-scientists-with-matplotlib-15c28863c41c (see techniques)

FIRST:
======
ie/ df aggregation into a column ala when I combine sts ... if I do a column per criteria and have their vals (subtypeid) and then row each for values 
... then can recombine

> df = df[['PID', 'YEAR_BUILT']].groupby('YEAR_BUILT', as_index = False).count().astype('int').rename(columns = {'PID':'No_of_properties_built'})

and

> df = df[(df['YEAR_BUILT'] >= 1900) & (df['YEAR_BUILT'] <= 2018)]

Look into https://stackoverflow.com/questions/34193862/pandas-pivot-table-list-of-aggfunc
with aggfunc for stats and the pivottable (explained!)

SECOND:
=======
- typer to df 
https://medium.com/well-red/cleaning-a-messy-dataset-using-python-7d7ab0bf199b
... along with subtype id to rows as flatten into rows ... also will drop optionals? as typing not strict OR must populate a default or "N:NONE" for catags
- use other cleans like normalize catag names USA, united states unify ... ie/ df.py (do my own df utils (mainly tips til get routines)

Could have used JSON ...

df = pd.DataFrame({'Date': [day1, day2 ...],
                   '668': [cnt day 1, cnt day2, ...],
                   '663' ...
                   })

or DataFrame({...}, [dates as index])                   

vs CSV form

    Date,668,663,648,687
    1979-02-13,0,0,1,0
    ...
    
https://hackingandslacking.com/plotting-data-with-seaborn-and-pandas-d2499fdf6f01 <---- good on "cleanup CSV pandas" and objects [if doing own typing]
    
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_markdown.html includes markdown serialization

TODO: 
- https://towardsdatascience.com/pyviz-simplifying-the-data-visualisation-process-in-python-1b6d2cb728f1 <------ pandas built in "visuals" ... max/min etc. ie/ just working the
dataframes before going to deeper graphs
- https://towardsdatascience.com/handling-pandas-groupby-and-its-multi-indexes-efae3e6b788c with various grouping etc techniques
- https://tryolabs.com/blog/2017/03/16/pandas-seaborn-a-guide-to-handle-visualize-data-elegantly/ ... see groups columns etc

Other options to look at: (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html)
- if no names are passed the behavior is identical to header=0 and column names are inferred from the first line of the file
- squeeze: If the parsed data only contains one column then return a Series. (TODO: using a series)

Note: if want CSV inline then use StringIO
    pd.read_csv(io.StringIO(data))
where data is string CSV

Can just make a DF with explicit Index (column) and other columns ...

speed = [0.1, 17.5, 40, 48, 52, 69, 88]
lifespan = [2, 8, 70, 1.5, 25, 12, 28]
index = ['snail', 'pig', 'elephant',
         'rabbit', 'giraffe', 'coyote', 'horse']
df = pd.DataFrame({'speed': speed,
                   'lifespan': lifespan}, index=index)
                   
In Dailies:
    index = dates (col 0 of csv)
    data = {"COLNAME": [...] ie/ "668": [...] etc.
    where COLNAME appears in legend

MORE:
- https://levelup.gitconnected.com/pandas-dataframe-python-10-useful-tricks-b4beae91df3d ... filtering, combining, renaming in frames ie/ all frame operations to try
- https://medium.com/@rrfd/cleaning-and-prepping-data-with-python-for-data-science-best-practices-and-helpful-packages-af1edfbe2a3 <---- includes 'fillna'
"""
def csvDatesBySNO(cd):
        datesBySNO = cd.entryDatesBySNO()
        snosOrdered = sorted(datesBySNO, key=lambda x: len(datesBySNO[x]), reverse=True)
        byDateBySNO = defaultdict(Counter)
        for sno in datesBySNO:
            for dt in datesBySNO[sno]:
                byDateBySNO[dt][sno] += 1
        csvLines = []
        for dt in sorted(byDateBySNO):
            ln = [str(byDateBySNO[dt][sno]) if sno in byDateBySNO[dt] else "0" for sno in snosOrdered]
            ln.insert(0, dt)
            csvLine = ",".join(ln)
            csvLines.append(csvLine)
        cols = snosOrdered
        cols.insert(0, "Date")
        csvLines.insert(0, ",".join(cols))
        return csvLines
                    
# ############################## DRIVER ################################
            
def main():

    assert sys.version_info >= (3, 6)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "PLOT":
            makePlots("Common", "Users")
            return
        raise Exception("Only argument allowed is 'PLOT'")

    dirName = "User"
    cud = CommonUserDirectory(VISN20_VISTAS)

    plotData = {}
    mu = f"""---
layout: default
title: VISN 20 {dirName} Directory
---

# VISN 20 {dirName} Directory

"""

    mu += """The following reports on a VISN 20 User Directory built from the user file (200) of 7 VistAs: Puget Sound [663], Portland [648], Boise [531], Spokane [668], Roseburg [653], White City [692] and Walla Walla [687]. Together they hold <span class='yellowIt'>{:,}</span> distinct users using <span class='yellowIt'>{:,}</span> user file records.

Note: Anchorage is the missing VISN 20 system. Its information will be added once the system is made available.

""".format(
        cud.total(),
        cud.entryTotal()
    )
    
    ttlPlotData, ttlMU = makeTotalsSection(cud, VISN20_VISTAS)
    mu += ttlMU
    plotData.update(ttlPlotData)
    
    tsPlotData, tsMU = makeTimeSeriesSection(cud, VISN20_VISTAS)
    mu += tsMU
    plotData.update(tsPlotData)
        
    plotDir = f'{VISTA_DATA_BASE_DIR}Common/TmpWorking/'
    print(f'Serializing vizData to {plotDir}')
    json.dump(plotData, open(f'{plotDir}plotDataUsers.json', "w"), indent=4)
                
    siteDir = SITE_DIR_TEMPL.format("Common")
    print(f'Serializing Report to {siteDir}')
    open(f'{siteDir}visn20UserDirectory.md', "w").write(mu) 
        
if __name__ == "__main__":
    main()
    