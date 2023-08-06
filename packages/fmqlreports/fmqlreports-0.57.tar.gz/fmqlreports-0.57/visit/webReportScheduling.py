#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent, muBVC
from fmqlutils.cacher.cacherUtils import metaOfVistA
from fmqlutils.typer.reduceTypeUtils import splitTypeDatas, combineSubTypes, checkDataPresent, singleValue, muBVCOfSTProp

from ..webReportUtils import filteredResultIterator, reduce200, reduce4, reduce44, TOP_MD_TEMPL, SITE_DIR_TEMPL, ensureWebReportLocations, keyStats, roundFloat

"""
Overall: Scheduling w/VSE focus

TODO: [1] match webReportEncounter's nuance of noshow(VSE only)/cancelled/active break
for appts and carry it through into tables ie/ can index triple ST by workload and instit 
in detailed report below. [2] prelude to showing % of each type with matching enc - mainly/only active with some active's still being left as orphans. [3] Also can show legacy to VSE matchups where not all legacy has a VSE and vica versa including workload
type.
+
by institution and its stationNo -- seems to take that of first st by institution, st broken by Hospital Location. If locn is wrongly allocated then will end up with wrong station no for Instit in table?

per institution (has station number), showing scheduling based on stop codes. Additional nuance provided by normalized physical location names and, if many locations, forms/templates of locations. Handles case where only legacy (effectively) is working
ie/ VSE little or none for recent 3 month period (ex/ Columbus)

Most obvious missing: link from Appointment (non cancelled) to [Scheduled] Visit
and the normalization of visits (often > 1 resource made) into clean Encounters.

Context: one of the "DSS-based" (https://github.com/vistadataproject/workload/issues/27) reports as Location is key. Part of a flow from Appointment through [Scheduled] Visit (which anchors clinical activity): [1] DSS gathers [2] Appointments and [3] Scheduled Encounters which gather [4] Clinical Activity (record updates for our purposes). Ultimately appropriate, normalized RF data versions should make such reports easy to do.

Short cut: taking DSS from Location, something that changes yearly. Acceptable as only
doing last three months though if that period spans a year, there can be miscues. See
if can trace the "DSS per Location by Year/Period" so accurate.

Two VSE PDFs:
- https://www.va.gov/vdl/documents/Clinical/Scheduling/VSE_GUI_1_5_Technical_Manual.pdf and https://usermanual.wiki/Pdf/VSEGUI15UserGuide.1029341778/view
and
- https://www.va.gov/vdl/documents/Clinical/Scheduling/VSE_GUI_1_4_User_Guide.pdf
"""
def reportAppointmentsVSE(stationNo, vistaName, cutDate):

    allThere, details = checkDataPresent(stationNo, [

        {"fileType": "4", "check": "ALL"},
        {"fileType": "44", "check": "ALL"}, # from ALLRF (temporary)
        
        {"fileType": "409_84", "check": "TYPE"},
        {"fileType": "409_84", "check": "DAY90"},

        {"fileType": "409_831", "check": "ALL"},
        {"fileType": "409_833", "check": "ALL"}

    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))
            
    _all, sts = splitTypeDatas(stationNo, "409_84") # SDEC Appointments
    
    # expect YR-MTH for starttime but allow for older Year only too
    allSortedStartTime = sorted([(startTime, _all["starttime"]["byValueCount"][startTime]) for startTime in _all["starttime"]["byValueCount"]], key=lambda x: x[0]) 
    sigSortedStartTime = [sv[0] for sv in allSortedStartTime if sv[1] > 500]
    firstSignificantDate = re.sub(r'\-', '/', sigSortedStartTime[0])
    lastSignificantDate = re.sub(r'\-', '/', sigSortedStartTime[-1])
        
    # IMPORTANT: 'expectNotEfficientWalked' important as "starttime" is not ien order
    allDAY90, stsDAY90 = splitTypeDatas(stationNo, "409_84", reductionLabel="DAY90", expectSubTypeProperties=["resource", "#cancel_datetime", "#noshow_datetime"], expectNotEfficientWalked=True) 
    
    # Checking for Columbus and others where VSE may be off (or never on?)
    day90Fraction = float(allDAY90["_total"])/float(_all["_total"])
    if _all["_total"] < 10000 or day90Fraction < .01:
        print("Can't work as either total VSE {:,} too small (< 10K) or the fraction of VSE in last three months has dropped to tiny levels - {}. Exiting VPE Reporting".format(_all["_total"], day90Fraction))
        return
    
    # TODO: move to three way pass down reporting No Show, Cancel, Active
    # ... will fit with Legacy which has two of these three breakdowns.
    stsDAY90Active = [st for st in stsDAY90 if not ("noshow_datetime" in st or "cancel_datetime" in st)]
    # Cancel and not marked noshow
    stsDAY90Cancelled = [st for st in stsDAY90 if "cancel_datetime" in st and "noshow_datetime" not in st] # Cancel only
    # Allows cancel too but noshow takes precedent
    stsDAY90NoShowed = [st for st in stsDAY90 if "noshow_datetime" in st]
    stsDAY90 = combineSubTypes(stsDAY90, ["resource"], forceCountAllProps=True)
    
    institInfosByIEN = reduce4(stationNo)
    hlInfosByIEN = reduce44(stationNo, useRF=False)
    resourceInfosByIEN = reduce409_831(stationNo)
                
    # ENFORCE/SEPARATE: Making a statement that only doing Location resources - enforce it
    def enforceResourcesAllLocation(stsDAY90):
        nstsDAY90 = []
        for st in stsDAY90:
            try:
                resourceRef = singleValue(st, "resource")
            except:
                # in 663, say NOVALUE meant 'note' set to CX IN ERROR
                print("** Warning: expected st's of 409_84 to have resource set but {} with {:,} appointments didn't.".format(st["_subTypeId"], st["_total"]))
                continue
            resourceIEN = re.search(r'\-(\d+)\]', resourceRef).group(1)
            resourceInfo = resourceInfosByIEN[resourceIEN]
            if resourceInfo["source_resource_class"] != "LOCATION":
                raise Exception("Expect all resources with appointments to be LOCATION")
            nstsDAY90.append(st)
        return nstsDAY90
    stsDAY90 = enforceResourcesAllLocation(stsDAY90)
        
    # Make explicit the hospital location from the Location Resource 
    for st in stsDAY90:
        resourceRef = singleValue(st, "resource")
        resourceIEN = re.search(r'\-(\d+)\]', resourceRef).group(1)
        resourceInfo = resourceInfosByIEN[resourceIEN]
        st["_hospital_location"] = resourceInfo["hospital_location"]   
    stsDAY90 = enhanceHLocSTsByLOC(institInfosByIEN, hlInfosByIEN, stsDAY90)
                
    # TMP: for now, keeping separate from norm of 44 so can work incrementally     
    try:
        PLOCMAP = json.load(open("MetaPerStation/{}/physicalLocationsNorm.json".format(stationNo)))["map"]
    except:
        PLOCMAP = None        
                
    # ############################ MU REPORT ################################
            
    mu = """VistA Scheduling Enhancements (VSE) is the package used for appointment creation and tracking. Despite the word \"Enhancements\", VSE is a new package that superceeds an older scheduling package.
    
"""
    
    muProviderTotal = "Only <span class='yellowIt'>{}</span> of these _Location Appointments_ specify a provider".format(reportAbsAndPercent(allDAY90["provider"]["count"], allDAY90["_total"])) if "provider" in allDAY90 else "No appointments specify a provider"
    
    # REM: three month scheduled == occur in this period ie/ not made in it but meant to
    # take place.
    mu += """{} records <span class='yellowIt'>{:,}</span> VSE appointments, the first in significant numbers in {}, the latest in {}. 
    
For the 90 days before this VistA copy was cut (_{}_), the System shows <span class='yellowIt'>{}</span> appointments were scheduled for <span class='yellowIt'>{:,}</span> patients and <span class='yellowIt'>{:,}</span> \"Resources\". <span class='yellowIt'>{}</span> of these appointments were active, <span class='yellowIt'>{}</span> were formally cancelled and <span class='yellowIt'>{}</span> were \"no shows\".
    
The software allows a \"Resource\" to be a provider or a location but in this system, all resources with appointments from 2019 are locations - in other words, appointments are only made for locations (\"Location Appointment\"). {}.

""".format(
        "__{} [{}]__".format(vistaName, stationNo),
        _all["_total"],
        firstSignificantDate,
        lastSignificantDate,
        
        cutDate,
        reportAbsAndPercent(allDAY90["_total"], _all["_total"]),
        allDAY90["patient"]["rangeCount"],
        allDAY90["resource"]["rangeCount"],
        reportAbsAndPercent(
            sum(st["_total"] for st in stsDAY90Active),
            allDAY90["_total"]
        ),
        reportAbsAndPercent(
            sum(st["_total"] for st in stsDAY90Cancelled),
            allDAY90["_total"]
        ),
        reportAbsAndPercent(
            sum(st["_total"] for st in stsDAY90NoShowed),
            allDAY90["_total"]
        ),
        
        muProviderTotal # very unlikely: say in Columbus as moved on from VSE
    )
            
    mu += muByInstitutions(allDAY90, stsDAY90, plocMap=PLOCMAP)
    
    mu += muAboutWorkLocation() 
    
    """
    TODO: markup or check "length of appt" and see date appt made vs
    split on appt time ie/ where one is == or < or ... (same for 44_003 below)
    
    Also appointment_type (which was removed from generic)
    """
    propsPresenceToCount=["checkin", "checkout", "noshow", "consult_link", "provider", "cancel_datetime"]
    mu += muByStopCodes(stationNo, stsDAY90, plocMap=PLOCMAP, propsPresenceToCount=propsPresenceToCount)
                    
    # #################### FINAL WRITE OUT ###########################
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print("Serializing VSE Appointment Report to {}".format(userSiteDir))
    if not os.path.isdir(userSiteDir):
        raise Exception("Expect User Site to already exist with its basic contents")
    title = "VSE Appointments {}".format(stationNo)
    mu = TOP_MD_TEMPL.format(title, "VSE Appointments") + mu
    open(userSiteDir + "appointmentsVSE.md", "w").write(mu)
    
# ############################## Legacy Form Appointments 44_003 #######################

"""
In form, this follows VPE (409_84) reports except where Legacy 44.003 has its own
properties (consult ref)

TODO: add from type of 44_003 here ala for 409_84 above
"""
def reportAppointmentsLegacy44(stationNo, vistaName, cutDate):

    allThere, details = checkDataPresent(stationNo, [

        {"fileType": "4", "check": "ALL"},
        {"fileType": "44", "check": "ALLRF"},
        {"fileType": "44_003", "check": "TYPE"},
        {"fileType": "44_003", "check": "DAY90"}

    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    institInfosByIEN = reduce4(stationNo)
    hlInfosByIEN = reduce44(stationNo)

    LOCN_PROP = "appointment_container_"

    _all, sts = splitTypeDatas(stationNo, "44_003")
        
    # expect YR-MTH for starttime but allow for older Year only too
    allSortedADT = sorted([(adt, _all["appointment_date_time"]["byValueCount"][adt]) for adt in _all["appointment_date_time"]["byValueCount"]], key=lambda x: x[0]) 
    sigSortedADT = [sv[0] for sv in allSortedADT if sv[1] > 500]
    firstSignificantDate = re.sub(r'\-', '/', sigSortedADT[0])
    lastSignificantDate = re.sub(r'\-', '/', sigSortedADT[-1])

    allDAY90, stsDAY90 = splitTypeDatas(stationNo, "44_003", reductionLabel="DAY90", expectSubTypeProperties=["appointment_container_", "#appointment_cancelled"], expectNotEfficientWalked=True)     
    stsDAY90Active = [st for st in stsDAY90 if re.search(r'ABSENT', st["_subTypeId"])]
    # TODO: eventually will only do non cancelled as cuts out ZZ's too
    stsDAY90Cancelled = [st for st in stsDAY90 if re.search(r'PRESENT', st["_subTypeId"])]
    # TMP: for now, only want resource based sts
    stsDAY90 = combineSubTypes(stsDAY90, ["appointment_container_"], forceCountAllProps=True)
    
    # TMP: for now, keeping separate from norm of 44 so can work incrementally     
    try:
        PLOCMAP = json.load(open("MetaPerStation/{}/physicalLocationsNorm.json".format(stationNo)))["map"]
    except:
        PLOCMAP = None  
        
    for st in stsDAY90:
        if LOCN_PROP not in st:
            continue
        hlRef = singleValue(st, LOCN_PROP)
        st["_hospital_location"] = hlRef
        # Note: not enforce all locs have stop_code (warned below)
        hlInfo = hlInfosByIEN[re.search(r'(\d+)\]', hlRef).group(1)]
    stsDAY90 = enhanceHLocSTsByLOC(institInfosByIEN, hlInfosByIEN, stsDAY90)
    
    # ############################ MU REPORT ################################
            
    mu = "VistA Scheduling (Legacy) was the only mechanism used for managing appointments in VistA before VistA Scheduling Enhancements (VSE).\n\n"   
    
    mu += """{} records <span class='yellowIt'>{:,}</span> legacy appointments, the first in significant numbers in {}, the latest in {}. 
    
For the 90 days before this VistA copy was cut (_{}_), the System shows <span class='yellowIt'>{}</span> appointments were scheduled for <span class='yellowIt'>{:,}</span> patients and <span class='yellowIt'>{:,}</span> \"Locations\". <span class='yellowIt'>{}</span> of these appointments were active, <span class='yellowIt'>{}</span> were formally cancelled.

""".format(
        "__{} [{}]__".format(vistaName, stationNo),
        _all["_total"],
        firstSignificantDate,
        lastSignificantDate,
        
        cutDate,
        reportAbsAndPercent(allDAY90["_total"], _all["_total"]),
        allDAY90["patient"]["rangeCount"],
        allDAY90[LOCN_PROP]["rangeCount"],
        reportAbsAndPercent(
            sum(st["_total"] for st in stsDAY90Active),
            allDAY90["_total"]
        ),
        reportAbsAndPercent(
            sum(st["_total"] for st in stsDAY90Cancelled),
            allDAY90["_total"]
        )
    )
            
    mu += muByInstitutions(allDAY90, stsDAY90, plocMap=PLOCMAP)
    
    mu += muAboutWorkLocation() 
    
    """
    TODO: markup or check "length of app't" and see date_appointment_made vs
    split on appointment_date_time ie/ where one is == or < or ...
    """
    propsPresenceToCount=["checked-in", "checked_out", "appointment_cancelled", "consult_link"]
    mu += muByStopCodes(stationNo, stsDAY90, plocMap=PLOCMAP, propsPresenceToCount=propsPresenceToCount)
            
    # #################### FINAL WRITE OUT ###########################
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print("Serializing Legacy Appointment Report to {}".format(userSiteDir))
    if not os.path.isdir(userSiteDir):
        raise Exception("Expect User Site to already exist with its basic contents")
    title = "Legacy Appointments {}".format(stationNo)
    mu = TOP_MD_TEMPL.format(title, "Legacy Appointments") + mu
    open(userSiteDir + "appointmentsLegacy.md", "w").write(mu)

# ################################# Common MU's/ HL Enhance ###################

"""
Focus is [1] per institution and [2] stop codes as [3] work locations are combination concepts. Need to report on both [A] VPE and [B] Legacy 44.003 (and maybe per patient too)
"""
def muAboutWorkLocation(): # background blurb shared
    
    mu = "In VistA, location (\"Work Location\") represents the combination of [i] a type of work in [ii] a specific institution performed by [iii] a particular provider, group of providers or class of provider. Appointments and Visits are organized around these Work Locations.\n\n"
    
    mu += "The work type of each Work Location is formally specified with a VA-custom \"stop code number\", the key designator for VA's _Decision Support System_ (DSS) ...\n\n"
    
    # "DSS calculates the actual cost to provide patientcare services"
    mu += "> VHA collects workload data that supports the continuity of patient care, resource allocation, performance measurement, quality management, and third-party collections. Decision Support System (DSS) Identifiers assist VA medical centers in defining workload, which is critical for costing purposes. DSS Identifiers are used to identify workload for all outpatient encounters, inpatient appointments in outpatient clinics, and inpatient billable professional services. They also serve as guides to select DSS outpatient department structures.\n\n"
    
    mu += "This approach downplays physical location as one physical location may host many Work Locations. Even when specified in the system, physical location is a freeform text string that varies greatly in form and quality - it has been somewhat normalized in the tables below.\n\n"
    
    mu += "The use of Work Locations for appointments makes _stop code_ the best mechanism for describing and typing appointments.\n\n"
    
    return mu
    
"""
By Institution summary 

Expects: _institution, _stop_code_number added to st's
"""
def muByInstitutions(_all, sts, plocMap=None): # TODO: map ploc ala sc mu below

    _allTotal = sum(st["_total"] for st in sts) # have _all too for patient range total but TODO, will move off that.
    stsByInstitution = defaultdict(list)
    stsNoInstitution = [] # again
    stByPhyLocByInstit = defaultdict(lambda: defaultdict(list))
    patientsByInstitution = defaultdict(set)
    apptCountByInstitution = Counter()
    apptTypeCountByInstitution = defaultdict(lambda: Counter()) # only 409_84
    for st in sts:
        if "_institution" not in st:
            stsNoInstitution.append(st)
            continue
        instit = st["_institution"]
        stsByInstitution[st["_institution"]].append(st)
        apptCountByInstitution[instit] += st["_total"]
        if "byValueCount" not in st["patient"]:
            raise Exception("Reduction of st didn't enforce count 'patient' so no byValueCount")
        patientsByInstitution[st["_institution"]] |= set(st["patient"]["byValueCount"])
        if "_physical_location" in st:
            pl = st["_physical_location"].upper()
            stByPhyLocByInstit[instit][pl].append(st)
        if "appointment_type" in st: # 409_84 only
            bvc = st["appointment_type"]["byValueCount"]
            for v in bvc:
                apptTypeCountByInstitution[instit][v] += bvc[v] 
                
    def weekdayWeekendCounts(st, wdweCounts):
        if not ("_createDateProp" in st and st["_createDateProp"] in st):
            return wdweCounts
        createDatePropInfo = st[st["_createDateProp"]]
        if "byWeekDay" not in createDatePropInfo:
            return wdweCounts
        wdweCounts["WD"] += sum(createDatePropInfo["byWeekDay"][wd] for wd in createDatePropInfo["byWeekDay"] if int(wd) < 5)
        wdweCounts["WE"] += sum(createDatePropInfo["byWeekDay"][wd] for wd in createDatePropInfo["byWeekDay"] if int(wd) > 4)
        return wdweCounts

    cols = [":Institution", "Locns", ":Locn Prefixes", "Phy Locns", "Stop Codes", "PTs", "Appts", "Weekend"]
    if len(apptTypeCountByInstitution):
        cols.append(":Appointment Types")
    tbl = MarkdownTable(cols)
    for instit in sorted(apptCountByInstitution, key=lambda x: apptCountByInstitution[x], reverse=True):
        name = re.sub(r' +$', '', instit.split(" [")[0])
        nameMU = "__{}__ [{}]".format(name, st["_station_number"]) if "_station_number" in st else "__{}__".format(name)
        byStopCodeCount = Counter()
        hlocPrefixes = Counter()
        wdweCounts = Counter()
        for st in stsByInstitution[instit]:
            if "_stop_code_number" not in st:
                continue
            byStopCodeCount[st["_stop_code_number"]] += 1
            hlocPrefixes[st["_prefix"] if "_prefix" in st else "NO PREFIX"] += 1
            wdweCounts = weekdayWeekendCounts(st, wdweCounts)
        weekendMU = reportPercent(wdweCounts["WE"], apptCountByInstitution[instit]) if wdweCounts["WE"] != 0 else ""
        row = [
            nameMU,
            len(stsByInstitution[instit]),
            muBVC(hlocPrefixes, totalOver=7), # may cut down (more a QA)
            len(stByPhyLocByInstit[instit]) if instit in stByPhyLocByInstit else "",
            len(byStopCodeCount),
            reportAbsAndPercent(len(patientsByInstitution[instit]), _all["patient"]["rangeCount"]),
            reportAbsAndPercent(apptCountByInstitution[instit], _allTotal),
            weekendMU
        ]
        if len(apptTypeCountByInstitution):
            row.append(muBVC(apptTypeCountByInstitution[instit]))
        tbl.addRow(row)
    mu = "<span class=\"yellowIt\">{:,}</span> \"Institutions\" supported by this system have Appointments spread over <span class=\"yellowIt\">{:,}</span> locations with <span class=\"yellowIt\">{:,}</span> stop codes ...\n\n".format(
        len(apptCountByInstitution),
        sum(len(stsByInstitution[instit]) for instit in stsByInstitution),
        len(set(st["_stop_code_number"] for st in sts if "_stop_code_number" in st))
    )
    mu += tbl.md() + "\n\n"
    
    # IMPORTANT: rare rare not to have stop code. Usually won't have _institution.
    if len(stsNoInstitution):
        mu += "__Note__: <span class=\"yellowIt\">{:,}</span> location(s) with <span class=\"yellowIt\">{:,}</span> appointments either don't specify an institution or one can't be derived from its name. <span class=\"yellowIt\">{}</span> of these are deleted locations, ones whose names begin with _ZZ_.\n\n".format(
            len(stsNoInstitution),
            sum(st["_total"] for st in stsNoInstitution),
            reportAbsAndPercent(
                sum(1 for st in stsNoInstitution if "_hospital_location" in st and re.match(r'ZZ', st["_hospital_location"])),
                len(stsNoInstitution)
            ) 
        )
    
    return mu
    
"""
Stop Code as Anchor - [1] separate out the non 'in person' appts from [2] TELEPHONE 
etc for the primary institutions and then all others.
    
See: https://www.va.gov/vdl/documents/Financial_Admin/Decision_Supp_Sys_(DSS)/dss_ug.pdf, http://vistadataproject.info/demo2/ and http://vistadataproject.info/demo2/location (need to rework these)

NOTE: no institution (and rarer no stop_code) sts are passed in and used to count the
total. There are counted in the Note about ("appointments either don't specify an institution or one can't be derived from its name"). It is not worth counting them again.
    
TODO Structure:
- ala webReportEncounter, distinguish cancelled, no show, active (=> will need noshow in 409_84 breakdown; Legacy doesn't do noshow)
    
TODO Overall:
- more on those others (TELEPHONE etc)
- TELEHEALTH -- go beyond stops
- PRIMARY CARE broken out as secondaries won't do anything ... need more
- GROUPs of Stop Codes    
"""
def muByStopCodes(stationNo, sts, plocMap=None, propsPresenceToCount=[]):

    # FUTURE: consider grouping stop codes together
    SC_GROUPS = [
        ["ORTHO JOINT SURG", "PODIATRY"], # Building 1e SPECIALITY for this
        ["OPHTHALMOLOGY", "OPTOMETRY"], # Building 40 ... expect SPO EYE for first twos
        ["BROS (BLIND REHAB O P SPEC)", "PHYSICAL THERAPY", "CHIROPRACTIC CARE", "OCCUPATIONAL THERAPY", "WHEELCHAIR & ADVAN MOBILITY", "RECREATION THERAPY SERVICE", "PROSTHETICS ORTHOTICS"], # Building 31
        ["MH INTGRTD CARE GRP", "MH INTGRTD CARE IND"], # group these but not others?
        ["PSYCHOLOGICAL TESTING", "MH INTGRTD CARE IND", "PTSD - INDIVIDUAL"], # B40, BHS (not SUBSTANCE USE DISORDER IND)
        ["SUBSTANCE USE DISORDER IND", "SUBSTANCE USE DISORDR GRP"],
        
        ["MENTAL HEALTH CLINIC - IND", "MENTAL HEALTH CLINIC-GROUP", "MH INTGRTD CARE IND", "MH TEAM CASE MANAGEMENT", "PSYCHOLOGICAL TESTING", "PTSD - GROUP", "PTSD - INDIVIDUAL", "SUBSTANCE USE DISORDR GRP"]
    ]
    
    # FUTURE: more expansion for Workload Location names
    MED_ACRONYMS = {
    
        "DI": "DIAGNOSTIC IMAGING",
        "BHS": "BEHAVIORAL HEALTH SERVICES"
        
    }
                                
    def muAppointmentsOfStopCodes(instit, stsOfSC, plocMap=None, propsPresenceToCount=[], showLocations=False):
        def dashNBVC(sts, prop, valMap=None):
            cntr = Counter()
            for st in stsOfSC[sc]:
                if prop not in st:
                    val = "*NOT SET*"
                elif re.match(r'\_', prop):
                    val = re.sub(r' +$', '', st[prop].upper())
                    if valMap and val in valMap:
                        val = valMap[val]
                    cntr[val] += st["_total"]
                else:
                    for val in st[prop]["byValueCount"]:
                        cntr[val.split(" [")[0]] += st[prop]["byValueCount"][val]
            return cntr 
        def bvcSTSs(sts, prop):
            cntr = Counter()
            for st in sts:
                for val in st[prop]["byValueCount"]:
                    cntr[val.split(" [")[0]] += st[prop]["byValueCount"][val]
            return cntr
        def bvcPropsPresence(sts, props):
            cntr = Counter()
            for st in sts:
                for prop in props:
                    if prop not in st:
                        continue
                    cntr[prop] += st[prop]["count"]
            return cntr
        def countLocnPrefixes(sts):
            cntrAppear = Counter()
            entries = []
            for st in sts:
                locn = re.sub(r'^ +', '', re.sub(r' +$', '', st["_hospital_location"].split(" [")[0]))
                pieces = locn.split(" ")
                entry = [[], st["_total"]]
                for i in range(1, len(pieces) + 1):
                    k = " ".join(pieces[0:i])
                    cntrAppear[k] += 1
                    entry[0].append(k)
                entries.append(entry)
            cntr = Counter()
            for entry in entries: # reduce entries and count 
                ks = entry[0]
                if len(ks) >= 3 and cntrAppear[ks[2]] > 1 and not re.search(r' (\d+|[A-Z])$', ks[2]):
                    cntr[ks[2]] += entry[1]
                    continue
                if len(ks) >= 2 and cntrAppear[ks[1]] > 1:
                    cntr[ks[1]] += entry[1]
                    continue
                cntr[ks[-1]] += entry[1] 
            return cntr
        tbl = MarkdownTable([":Stop Code", "Locns", ":Location [Roots]", ":Physical Location(s)", "PTs", "Appts", ":Props"])
        scs = sorted(stsOfSC, key=lambda x: sum(st["_total"] for st in stsOfSC[x]), reverse=True)
        rplocMap = {}
        if plocMap:
            for ploc in plocMap:
                for rploc in plocMap[ploc]:
                    rplocMap[rploc] = ploc
        for sc in scs:
            locns = set(st["_hospital_location"] for st in stsOfSC[sc]) 
            phyLocCntr = dashNBVC(stsOfSC[sc], "_physical_location", rplocMap)     
            tbl.addRow([
                "__{}__".format(re.sub(r'\_', ' ', sc.split(" [")[0])),
                muBVC(dashNBVC(stsOfSC[sc], "_hospital_location")) if showLocations else len(locns),
                muBVC(countLocnPrefixes(stsOfSC[sc])),
                muBVC(phyLocCntr) if len(phyLocCntr) else "",
                len(bvcSTSs(stsOfSC[sc], "patient")),
                reportAbsAndPercent( # % of these appts (not total overall instits)
                    sum(st["_total"] for st in stsOfSC[sc]),
                    sum(st["_total"] for sc in scs for st in stsOfSC[sc])
                ),
                re.sub(r'\_', ' ', muBVC(bvcPropsPresence(stsOfSC[sc], propsPresenceToCount)))
            ])
        return tbl.md() + "\n\n"
        
    _allTotal = sum(st["_total"] for st in sts)
    
    stsWSC = [st for st in sts if "_stop_code_number" in st and "_institution" in st]
    
    # Note: for now, not explicitly noting these are noted above in Note with
    # 'appointments either don't specify an institution or one can't be derived ...'
    # ... may reconsider whether _allTotal should have them or not but not worth excluding
    # now as [1] small in # and [2] only showing in-person appointments in tables so
    # they are a subset anyhow
    notCountedTotal = sum(st["_total"] for st in sts if not ("_stop_code_number" in st and "_institution" in st))
    def catagST(st):
        for mtch, catag in [
            (r'(TELEPHONE|PHONE)', "TELEPHONE"),
            (r'(COMMUNITY CARE CONSULT)', "CC"),
            (r'(ADMIN PAT ACTIVTIES)', "ADMIN"),
            (r'(HOME)', "HOME")
        ]:
            if re.match(mtch, st["_stop_code_number"]):
                return catag
        return ""
    stsByCategory = defaultdict(list)
    for st in stsWSC:
        catag = catagST(st)
        if catag:
            stsByCategory[catag].append(st)
            continue
        """
        TODO: doesn't take them ALL -- if TELEHEALTH in physical_location takes
        others w/o a secondary code
        """
        if "_credit_stop_code" in st and re.search(r' TH ', st["_credit_stop_code"]):
            stsByCategory["TELEHEALTH"].append(st)
            continue
        stsByCategory["INPERSON"].append(st)

    mu = "## By Stop Code\n\n"
    # May add: The range of states transitioned by appointments from checkin to checkout seems to vary with work type.
    mu += """The system holds <span class='yellowIt'>{}</span> in-person, clinical appointments. There are also <span class='yellowIt'>{}</span> _TELEPHONE_, <span class='yellowIt'>{}</span> _COMMUNITY CARE_, <span class='yellowIt'>{}</span> _in home care_, <span class='yellowIt'>{}</span> _Telehealth_ and <span class='yellowIt'>{}</span> _administrative appointments_.
    
The tables below break down appointments by institution. _Location_ counts the root or base of location names as the number of individual locations in larger institutions get unmanageable for a table and _Physical Location_ shows the free text names given for buildings and rooms. _Props_ count how many appointments have defining properties such as _"cancel datetime"_ or _checked out_. 
    
""".format(
        reportAbsAndPercent(
            sum(st["_total"] for st in stsByCategory["INPERSON"]),
            _allTotal
        ),
        reportAbsAndPercent(
            sum(st["_total"] for st in stsByCategory["TELEPHONE"]),
            _allTotal
        ),
        reportAbsAndPercent(   
            sum(st["_total"] for st in stsByCategory["CC"]),
            _allTotal
        ),
        reportAbsAndPercent(   
            sum(st["_total"] for st in stsByCategory["HOME"]),
            _allTotal
        ),
        # Undercounted as secondary not enough to break out and NO PRIMARY code
        # ... could use physical location matches but didn't for now
        reportAbsAndPercent(   
            sum(st["_total"] for st in stsByCategory["TELEHEALTH"]),
            _allTotal
        ),
        reportAbsAndPercent(   
            sum(st["_total"] for st in stsByCategory["ADMIN"]),
            _allTotal
        )
    )
    inPersonSTsByInstitBySC = defaultdict(lambda: defaultdict(list))
    stationNumberOfInstit = {}
    for st in stsByCategory["INPERSON"]:
        instit = st["_institution"]
        inPersonSTsByInstitBySC[instit][st["_stop_code_number"]].append(st)
        stationNumberOfInstit[instit] = st["_station_number"] if "_station_number" in st else ""
    for instit in sorted(inPersonSTsByInstitBySC, key=lambda x: sum(st["_total"] for sc in inPersonSTsByInstitBySC[x] for st in inPersonSTsByInstitBySC[x][sc]), reverse=True):
        mu += """Institution _{} [{}]_ uses <span class='yellowIt'>{:,}</span> stop codes for <span class='yellowIt'>{}</span> in-person appointments. Where there are many Work Locations, only the root (first pieces) of those locations are shown,  ...
        
""".format(
            re.sub(r' +$', '', instit.split(" [")[0]), 
            stationNumberOfInstit[instit],
            len(inPersonSTsByInstitBySC[instit]),
            reportAbsAndPercent(sum(st["_total"] for sc in inPersonSTsByInstitBySC[instit] for st in inPersonSTsByInstitBySC[instit][sc]), _allTotal)
        )
        mu += muAppointmentsOfStopCodes(instit, inPersonSTsByInstitBySC[instit], plocMap, propsPresenceToCount)
        
    # TODO: more on Telehealth etc + break that out more as still inside as codes aren't enough
    
    return mu
    
"""
Pattern: enhance sts with _ props from HLOC and Instit

Expect: _hospital_location to be in st
Copies key HLOC props into st along with station_number of Institution for ease of 
mu - makes sure same props for both 409_84 and 44_003 reductions (and more).
"""
def enhanceHLocSTsByLOC(institInfosByIEN, hlInfosByIEN, sts, locationProp="_hospital_location"):
    def addHLPropsToApptST(st, hlInfo):
        pieces = re.split(r'[ \-\/]', hlInfo["label"])
        if len(pieces) > 1:
            st["_prefix"] = pieces[0]
        for prop in ["stop_code_number", "credit_stop_code", "physical_location", "patient_friendly_name", "abbreviation", "provider", "institution"]:
            if prop in hlInfo:
                st["_" + prop] = hlInfo[prop]
        return st
    for st in sts:
        if locationProp not in st:
            continue
        hlIEN = re.search(r'(\d+)\]', st[locationProp]).group(1)
        try:
            hlInfo = hlInfosByIEN[hlIEN]
        except:
            print("Couldn't find {} for {} - probably hl red is incomplete".format(hlIEN, locationProp))
            raise
        addHLPropsToApptST(st, hlInfo)
        if "institution" not in hlInfo:
            continue
        # 541 has . IENs for institution pointer
        institIEN = re.search(r'([\d\.]+)\]$', hlInfo["institution"]).group(1)
        try:
            institInfo = institInfosByIEN[institIEN]
        except:
            raise
        if "station_number" in institInfo:
            st["_station_number"] = institInfo["station_number"]
    return sts

# ################################# Reduce/Lookup #################

"""
Break Resource 409_831 - VPE has indirection for NEW PERSON (200) and
HOSPITAL LOCATION (44) appointments.
"""
def reduce409_831(stationNo):
    from fmqlutils.cacher.cacherUtils import TMPWORKING_LOCN_TEMPL
    jsnFl = TMPWORKING_LOCN_TEMPL.format(stationNo) + "vpeResourceReduction.json"
    try:
        infosByIEN = json.load(open(jsnFl))
    except:
        pass
    else:
        return infosByIEN
    infosByIEN = {}
    for resource in filteredResultIterator(stationNo, "409_831"):
        missingMands = set(["entered_by_user", "date_time_entered", "resource_type"]) - set(resource)
        if len(missingMands):
            raise Exception("Resource 409_831 missing mandatory properties - {}".format(missingMands))
        red = {"_ien": resource["_id"].split("-")[1]}
        infosByIEN[resource["_id"].split("-")[1]] = red
        for prop in resource:
            if re.match(r'_', prop) or prop in ["label", "type"]:
                continue
            if prop == "resource_type": # VPTR to lead to two
                red["source_resource"] = "{} [{}]".format(resource[prop]["label"], resource[prop]["id"]) # no split as VPTR
                trt = resource[prop]["id"].split("-")[0] 
                # Note: perhaps ??? TODO 200's do too?
                if trt == "44" and "hospital_location" not in resource:
                    raise Exception("Expected resource 44's to have hospital location")
                if trt == "44":
                    red["source_resource_class"] = "LOCATION" 
                elif trt == "200":
                    red["source_resource_class"] = "USER"
                else: 
                    red["source_resource_class"] = "SDEC ADDITIONAL" # none in SPOKANE
                continue
            if isinstance(resource[prop], dict):
                if "value" in resource[prop]:
                    red[prop] = resource[prop]["value"]
                    continue
                if "id" in resource[prop]:
                    red[prop] = "{} [{}]".format(resource[prop]["label"], resource[prop]["id"].split("-")[1]) 
                    continue
                raise Exception("Dict Valued Prop not date or ref")
            red[prop] = resource[prop]        
    print("Dumping 409_831 reduction for first time - {:,} LOCATION's, {:,} USER's, {:,} SDEC ADDITIONALs".format(
        sum(1 for ien in infosByIEN if infosByIEN[ien]["source_resource_class"] == "LOCATION"),
        sum(1 for ien in infosByIEN if infosByIEN[ien]["source_resource_class"] == "USER"),            
        sum(1 for ien in infosByIEN if infosByIEN[ien]["source_resource_class"] == "SDEC ADDITIONAL")            
    ))
    json.dump(infosByIEN, open(jsnFl, "w"), indent=4)
    return infosByIEN
        
# ################################# DRIVER #######################

def main():

    assert sys.version_info >= (3, 6)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO")

    ensureWebReportLocations(stationNo)
    
    meta = metaOfVistA(stationNo)
    vistaName = "VistA" if "name" not in meta else meta["name"]
    cutDate = meta["cutDate"]

    reportAppointmentsVSE(stationNo, vistaName, cutDate)
    reportAppointmentsLegacy44(stationNo, vistaName, cutDate)

if __name__ == "__main__":
    main()

