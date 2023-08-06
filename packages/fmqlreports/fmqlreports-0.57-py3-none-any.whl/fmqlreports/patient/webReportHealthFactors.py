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
from ..webReportUtils import filteredResultIterator, TOP_MD_TEMPL, SITE_DIR_TEMPL, keyStats, roundFloat

"""
Health Factors Basic

Examine categories types more (http://www.cbo.gov/sites/default/files/cbofiles/ftpdocs/88xx/doc8892/maintext.3.1.shtml, 

Requires:
- 9999999_64 ALL (Filtered Walk)
- 9000010_23 (SOReduction/health_factor)

TODO v1.1: 
- 9000010_23 SPO has few but still present invalid visit dates of YR-MTH-00 so excluded (filtered) by typer
- put in last signon for everyone mentioned (do same for Dental)

And note that in PCE

    Patient Care Encounter (PCE) helps sites collect, manage, and display outpatient
    encounter data (including providers, procedure codes, and diagnostic codes) in
    compliance with the 10/1/96 Ambulatory Care Data Capture mandate from the
    Undersecretary of Health.     (https://www.va.gov/vdl/documents/Clinical/Patient_Care_Encounter_(PCE)/pxtm.pdf)

TODO: see other xxrepo notes
"""
def webReportHealthFactors(stationNo):
        
    allThere, details = checkDataPresent(stationNo, [
        {"fileType": "9999999_64", "check": "ALL"},
        {"fileType": "9000010_23", "check": "TYPESO"} # subtype prop checked below
    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))
        
    mu = """---
layout: default
title: {} Health Factors
--- 

""".format(stationNo) 

    # Definitions
    resourceIter = filteredResultIterator(stationNo, "9999999_64")
    redByRef = {}
    for resource in resourceIter: 
        # Not ideal - SPO has beyond ASCII - fix in Python 3
        label = resource["label"].encode('ascii', 'ignore').decode('ascii')
        resRef = "{} [{}]".format(re.sub(r'\_', '/', label), resource["_id"])
        red = {"ref": resRef}
        if "category" in resource:
            if resource["category"]["id"] == resource["_id"]:
                red["is_category_self"] = True
            else:
                categoryRef = "{} [{}]".format(re.sub(r'\_', '/', resource["category"]["label"]), resource["category"]["id"])
                red["category"] = categoryRef
        if "inactive_flag" in resource:
            red["is_inactive"] = True
        if "display_on_health_summary" in resource and resource["display_on_health_summary"]:
            red["is_display_on_health_summary"] = True
        if resource["entry_type"] == "F:FACTOR":
            red["is_factor"] = True
        redByRef[red["ref"]] = red
    factors = set(ref for ref in redByRef if "is_factor" in redByRef[ref])
    categories = set(ref for ref in redByRef if "is_factor" not in redByRef[ref])
    inactives = set(ref for ref in redByRef if "is_inactive" in redByRef[ref])
    actives = set(ref for ref in redByRef if "is_inactive" not in redByRef[ref])

    # Assignments
    all9000010_23Data, st9000010_23s = splitTypeDatas(stationNo, "9000010_23", reductionLabel="YR1", expectSubTypeProperty="health_factor")        
    usedFactors = set(re.sub(r'\_', '/', list(subTypeInfo["health_factor"]["byValueCount"])[0].split(" [")[0]) + " [" + list(subTypeInfo["health_factor"]["byValueCount"])[0].split(" [")[1] for subTypeInfo in st9000010_23s)
    subTypeInfoById = dict((re.sub(r'\_', '/', list(subTypeInfo["health_factor"]["byValueCount"])[0].split(" [")[0]) + " [" + list(subTypeInfo["health_factor"]["byValueCount"])[0].split(" [")[1], subTypeInfo) for subTypeInfo in st9000010_23s)
    usedFactorCounts = dict((factorRef, subTypeInfoById[factorRef]["_total"]) for factorRef in subTypeInfoById)
    usedCategoryCounts = Counter()
    usedFactorByCategoryCounts = defaultdict(lambda: Counter())
    factorsByCategory = defaultdict(list)
    for ref in redByRef:
        red = redByRef[ref]
        if "category" in red:
            factorsByCategory[red["category"]].append(ref)
    for factorRef in subTypeInfoById:
        red = redByRef[factorRef]
        if "category" in red:
            categoryRef = red["category"] 
        elif "is_factor" not in red:
            categoryRef = factorRef
        else:
            categoryRef = "** NO CATEGORY **"
        usedCategoryCounts[categoryRef] += subTypeInfoById[factorRef]["_total"]
        usedFactorByCategoryCounts[categoryRef][factorRef] = subTypeInfoById[factorRef]["_total"]

    overallFirstCreateDate = all9000010_23Data["_firstCreateDate"].split("T")[0]
    overallLastCreateDate = all9000010_23Data["_lastCreateDate"].split("T")[0]

    kstatsCategories = keyStats(usedCategoryCounts.values())
    maxCategoryLabel = sorted(usedCategoryCounts, key=lambda x: usedCategoryCounts[x], reverse=True)[0].split(" [")[0]
    kstatsFactors = keyStats([subTypeInfo["_total"] for subTypeInfo in st9000010_23s])
    maxFactorLabel = sorted(usedFactorCounts), key=lambda x: usedFactorCounts[x], reverse=True)[0].split(" [")[0]
    unassignedActiveFactors = factors - set(usedFactorCounts)
    unassignedActiveCategories = categories - set(usedCategoryCounts)
            
    mu += """<span class='yellowIt'>{:,}</span> health factor assignments were made in this VistA from {} through {}, the last full year for which data is available. The assignments cover <span class='yellowIt'>{:,}</span> health factors, grouped into <span class='yellowIt'>{:,}</span> categories for <span class='yellowIt'>{:,}</span> patients.
 Most nominally active factors - <span class='yellowIt'>{}</span> - and categories -  <span class='yellowIt'>{}</span> - are not assigned to a patient. They go _Unused_.
    
The median number of assignments per factor is <span class='yellowIt'>{:,}</span>, while the maximum is <span class='yellowIt'>{:,}</span> for factor _{}_. The median number per category is <span class='yellowIt'>{:,}</span>, while the maximum is <span class='yellowIt'>{:,}</span> for category _{}_.    
        
""".format(
        all9000010_23Data["_total"], 
        overallFirstCreateDate, 
        overallLastCreateDate,
        len(st9000010_23s), 
        len(usedCategoryCounts), 
        all9000010_23Data["patient_name"]["rangeCount"],
        
        reportAbsAndPercent(len(unassignedActiveFactors), len(factors.intersection(actives))), 
        reportAbsAndPercent(len(unassignedActiveCategories), len(categories.intersection(actives))), 
        
        roundFloat(kstatsFactors["median"]), 
        kstatsFactors["max"], 
        maxFactorLabel, 
        roundFloat( kstatsCategories["median"]), 
        kstatsCategories["max"], 
        maxCategoryLabel
    )
    
    categoriesAssigned = usedFactors.intersection(categories)
    if len(categoriesAssigned):
        mu += """__Note__: patients are typically assigned specific health factors, but in this system <span class='yellowIt'>{:,}</span> categories are assigned directly to patients.
        
""".format(len(categoriesAssigned))

    tbl = MarkdownTable(["Category", "Assignments", "Used Factors", "Unused Factors"])
    assignmentCount = 0
    for i, categoryRef in enumerate(sorted(usedCategoryCounts, key=lambda x: usedCategoryCounts[x], reverse=True), 1): 
        if i > 20:
            break
        unusedActiveFactors = set(factorsByCategory[categoryRef]).intersection(actives) - set(usedFactorByCategoryCounts[categoryRef])
        row = [
            "__{}__".format(categoryRef.split(" [")[0]), 
            reportAbsAndPercent(usedCategoryCounts[categoryRef], 
            all9000010_23Data["_total"]), 
            len(usedFactorByCategoryCounts[categoryRef]), 
            len(unusedActiveFactors)
        ]
        tbl.addRow(row)
        assignmentCount += usedCategoryCounts[categoryRef]
    mu += """The following shows the top 20 (out of <span class='yellowIt'>{:,}</span>) categories used for assigning health factors to patients. Collectively they account for <span class='yellowIt'>{}</span> of the system's assignments during this period. The table also shows how many of the factors of a category are used and how many go unused.
    
{}

""".format(
        len(usedCategoryCounts), 
        reportAbsAndPercent(assignmentCount, all9000010_23Data["_total"]), 
        tbl.md()
    )

    tbl = MarkdownTable(["Factor", "Category", "Assignments"])
    assignmentCount = 0
    for i, factorRef in enumerate(sorted(usedFactorCounts, key=lambda x: usedFactorCounts[x], reverse=True), 1): 
        if i > 20:
            break    
        red = redByRef[factorRef]
        factorLabel = factorRef.split(" [")[0]
        categoryMU = "__{}__".format(factorLabel) if "is_factor" not in red else red["category"].split(" [")[0]
        row = [
            "__{}__".format(factorLabel),
            categoryMU,
            reportAbsAndPercent(usedFactorCounts[factorRef], all9000010_23Data["_total"]) 
        ]
        tbl.addRow(row)
        assignmentCount += usedFactorCounts[factorRef]
    mu += """The following shows the top 20 (out of <span class='yellowIt'>{:,}</span>) health factors assigned to patients. Collectively they account for <span class='yellowIt'>{}</span> of the system's assignments. 
    
{}

""".format(
        len(usedFactorCounts), 
        reportAbsAndPercent(assignmentCount, all9000010_23Data["_total"]), 
        tbl.md()
    )
    
    mu += """__More to Analyze__:
    
  * __Clinical Reminders__ leverage Health Factors - hence the prevalence of _REMINDER FACTORS_. This needs to be fully examined.
  * Break out the Reminder Categories by broad topics to see just how much VA employs these factors for quite different activities - remind to educate, note homelessness, note an advance directive is refused.
  * The management of Health Factor and Category Definitions seems haphazard. Most go unused and the way they are marked inactive - make a factor inactive OR make its category inactive - seems inconsistent. This needs further examination.
  * The tie between documents (TIU Notes) and factors needs to be explored - in this system 99.8% of factors have TIU Notes as their data source.
  * Direct assignment of categories happens but it is unusual - is this because an individual factor type was turned into a category after assignment or because categories can be directly assigned.
  * Neither the definitions nor the assignments of this system have been standardized - standard codes go unused and factor definitions are not marked LOCAL or NATIONAL. A more recent system needs to be examined to see how far VA has gone with __Factor Standardization__. There are factors named VA- and these need to be examined further.
  

"""
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "healthFactors.md", "w").write(mu)
    
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

    webReportHealthFactors(stationNo)
                 
if __name__ == "__main__":
    main()
