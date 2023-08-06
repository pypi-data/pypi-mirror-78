#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent, muBVC
from fmqlutils.cacher.cacherUtils import metaOfVistA, TMPWORKING_LOCN_TEMPL, FMQLReplyStore, FilteredResultIterator, DATA_LOCN_TEMPL 
from fmqlutils.typer.reduceTypeUtils import checkDataPresent, muBVCOfSTProp

from ..webReportUtils import TOP_MD_TEMPL, SITE_DIR_TEMPL, ensureWebReportLocations, keyStats, roundFloat, reduce44, filteredResultIterator, flattenPropValues
        
"""  
Encounter (1 or more visits) matched to Appointment => Scheduled Encounter; Appointment matched to Encounter. [1] How well does the system do it? [2] And what's the institution and stop code breakdown. 

TODO/Evolve: [1] break down between two roles - [a] matching by system (how good?) and [b] then of the matched, the institution/stop code breakdown ie/ data problems and clean
data reporting (** there are encounters from cancelled and no show appts - can you tell from the visit?; are some non scheduled encounters really just same day extensions of scheduled encounters?**) [2] move to simpler indexes (apptN to Enc etc) for use in reportScheduling
and in a rewrite of the below to use typer. [3] for each work type broadly (DENTAL etc), do narrow report

TODO: Weekdays only n Nature of Clinics
- ex/ YAKIMA CBOC [687] - 687HA in FOIA - M-F (https://www.va.gov/directory/guide/facility.asp?id=5319)  
  < The clinic provides primary medical and mental health care with full-time staff.  The clinic contracts locally in the community and surrounding area for emergent laboratory, x-ray and pharmacy services.
- ex/ Coeur d' Alene
(https://www.va.gov/directory/guide/facility.asp?id=5674)

ISSUE/BUG: 541 - too big in first reduction so removed _06 pass. Could break this pass into four.

NICETY TODO: PIE chart the Instit table ie/ those columns into obvious visual break outs

End Goal: explicit RF'ed data makes Appointment --> Encounter --> Activity clear
where locations too are clear. ie/ where, when, what type of work and scheduled
or not and get away from fact systems making rawer data are not properly synced
even where these (sub)systems are modules of VistA (VPE to IHS Visits etc)
ie/ MVDM (Encounter, Appointment) from VDM (Visit, 409_84, 44_003, V PROVIDER)

cgfmr/issues:114 [CONTEXT: need to get to replay]
- rerun gatherEncounterDataByDay for 668 and 663 (663 no child visits -- why?)
"""
    
"""
webReportEncounters (appts and encounters, scheduled or not)

Mixes QA (mismatch and match of enc and appt in system and by it) with per site
and worktype breakdowns. TODO: make this distinction clearer
"""
def webReportEncounters(stationNo, vistaName, indexedDayTimeLocationPatient, cutDate, onAndAfterDay, upToDay, printOnly=True):

    byCatag = Counter()
    noneApptOnlyDetails = Counter()
    matchedDetails = {"encounterTypes": Counter(), "apptTypeByCatag": defaultdict(lambda: Counter())}
    matchedDetails2ByCatag = defaultdict(lambda: Counter())
    visitCreateBorAStart = defaultdict(lambda: Counter())
            
    """
    TODO: move to custom + typer and off the embedded below
        
    For analysis, custom gathers and adds new props to visit
    
    New/Moved Props:
        - apptCatag 
        - _children (move)
        - secondary credit stop
        - _isNoShow
        - _isCancelled
        - _isWalkin
        (ie/ some from visit gather/process, some from appt prop transfer)
        
    Config typer, can make all these =>  
        - cross: ALL
        - byInstit
        - byInstit, dssRef
        - byInstit, createOption
        - byInstit, location
        => break by all four (built in so fine)
        
    Note: tried service_category, encounter_type, #parent_visit_link where expect
    et=CREDIT STOP to be for parent_visit_link only (subset of them)
    """ 
    
    totalInfos = 0 # ie/ d/t/l/p
    totalSlots = 0
    totalMatchedAppts = 0
    catagedEncounters = [] # post 'custom' so have props
    unmatchedAppts = [] # pick out the active one
    
    hlInfosByIEN = reduce44(stationNo) # to get instit of locn for unmatched appts
    hlInfosByLabel = defaultdict(list)
    for ien in hlInfosByIEN:
        hlInfo = hlInfosByIEN[ien]
        label = hlInfo["label"]
        hlInfosByLabel[label].append(hlInfo)
    # Let apptN superceed
    def matchOperativeAppointment(info):
        for defn in [
            ("apptN", "", "active"), 
            ("apptNCancelled", "_isCancelled", "cancelled"), 
            ("apptNNoShow", "_isNoShow", "noShow"), 
            ("apptL", "", "active"),
            ("apptLC", "_isCancelled", "cancelled")
        ]:
            if defn[0] in info:
                return defn, info[defn[0]][0]
        raise Exception("Expect to match some operative appointment")
    for day in indexedDayTimeLocationPatient:
        for tm in indexedDayTimeLocationPatient[day]:
            totalSlots += 1
            for locn in indexedDayTimeLocationPatient[day][tm]:
                for patient in indexedDayTimeLocationPatient[day][tm][locn]:
                    info = indexedDayTimeLocationPatient[day][tm][locn][patient]
                    totalInfos += 1
                    try:
                        catag = categorizeVisitAppts(info, noneApptOnlyDetails, matchedDetails, matchedDetails2ByCatag, visitCreateBorAStart)            
                    except:
                        raise
                    byCatag[catag] += 1
                    if catag == "NONE_PCEONLY":
                        visitNS = info["visitNS"][0]
                        visitNS["_apptCatag"] = catag
                        catagedEncounters.append(visitNS)
                        continue
                    # No appts
                    if catag == "NONE_SCHEDONLY":
                        visit = info["visit"][0]
                        visit["_apptCatag"] = catag
                        catagedEncounters.append(visit)  
                        continue                      
                    if re.match(r'SCHED', catag):
                        visit = info["visit"][0]
                        visit["_apptCatag"] = catag
                        catagedEncounters.append(visit)
                        totalMatchedAppts += 1
                        apptSpec, appt = matchOperativeAppointment(info)
                        if apptSpec[1]:
                            visit[apptSpec[1]] = True
                        continue
                    if re.match(r'PCE', catag):
                        visitNS = info["visitNS"][0]
                        visitNS["_apptCatag"] = catag
                        catagedEncounters.append(visitNS)
                        totalMatchedAppts += 1
                        apptSpec, appt = matchOperativeAppointment(info)
                        if apptSpec[1]:
                            visitNS[apptSpec[1]] = True
                        continue
                    if catag == "NONE_NOTMATCHABLE":
                        if not ("ehVisit" in info and len(info) == 1): 
                            raise Exception("HUH on NONE")
                        """ 
                        # COME BACK
                        if "visit" in info:
                            visit = info["visit"][0]
                        else:
                            visit = info["visitNS"][0]
                        visit["_apptCatag"] = catag
                        catagedEncounters.append(visit)
                        """
                        continue
                    # NONE_APPTONLY - only one NOT visit based (most cancelled)
                    if catag == "NONE_APPTONLY":
                        apptSpec, appt = matchOperativeAppointment(info)
                        appt["_location"] = locn
                        if locn in hlInfosByLabel:
                            hlInfos = hlInfosByLabel[locn]
                            if len(hlInfos) > 1:
                                for hlInfo in hlInfos:
                                    if "institution" in hlInfo:
                                        break
                                print("** Warning - ambig label {} for locations. Just taking institution from first".format(locn))
                            else:
                                hlInfo = hlInfos[0]
                            if "institution" in hlInfo:
                                appt["_institution"] = hlInfo["institution"]
                        if apptSpec[1]:
                            appt[apptSpec[1]] = True
                        unmatchedAppts.append(appt)
                        continue
                    raise Exception("Unexpected catag: {}".format(catag))
                    
    # Will use catagedEncounters, unmatchedAppts below
    print("Post Walk of {:,} Slots in {:,} D/T/L/P's, have {:,} cataged visits, {:,} matched appts and {:,} unmatched appts. Specifically {} unmatched appts are cancelled, {} are noshows.".format(
        totalSlots,
        totalInfos,
        len(catagedEncounters),
        totalMatchedAppts,
        len(unmatchedAppts),
        
        reportAbsAndPercent(sum(1 for appt in unmatchedAppts if "_isCancelled" in appt), len(unmatchedAppts)),
        reportAbsAndPercent(sum(1 for appt in unmatchedAppts if "_isNoShow" in appt), len(unmatchedAppts))
    ))
        
    # Expect vast majority to be cancelled
    def summarizeUnmatchedAppts(appts):
        
        summ = {
            "id": "unmatchedAppts",
            "total": 0,
            "patients": set(),
            "locns": set(),
            "active": 0,
            "cancel": 0,
            "noShow": 0
        }
        summByInstit = {}
        for appt in appts:
            if "_institution" not in appt: # skipping if couldn't work out above!
                continue
            instit = appt["_institution"].split(" [")[0]
            if instit not in summByInstit:
                byInstit = {
                    "id": "unmatchedAppts{}".format(instit),
                    "total": 0,
                    "patients": set(),
                    "locns": set(),
                    "active": 0,
                    "cancel": 0,
                    "noShow": 0
                }
                summByInstit[instit] = byInstit
            else:
                byInstit = summByInstit[instit]
            for s in [summ, byInstit]:
                s["total"] += 1
                s["patients"].add(re.search(r'\-(\d+)', appt["patient"]).group(1))
                s["locns"].add(re.sub(r'\_', '/', appt["_location"]))
                if "_isCancelled" in appt:
                    s["cancel"] += 1
                elif "_isNoShow" in appt:
                    s["noShow"] += 1
                else:
                    s["active"] += 1 
        return summ, summByInstit
                    
    """
    TODO: replace with typer 4 as it will count appropriately.
    """            
    def summarizeAllEncounters(visits):    
                  
        # add to utils with makeSummary          
        def summarizeEncounters(visits, totalersAndAdders=[]):
        
            # TMP: TODO move into visit to encounter reduction code
            # WARNING in 541: location WMIC, WSIC only - seems to be all IN patient, TIU
            # from CPRS ie/ part of long stay. But not common.
            def enforceChild(visit): # bonus - move this
                if "_child_visits" in visit:
                    for cvisit in visit["_child_visits"]:
                        if cvisit["service_category"] not in ["E:EVENT (HISTORICAL)", "D:DAILY HOSPITALIZATION DATA", "X:ANCILLARY PACKAGE DAILY DATA"]: 
                            print("** WARNING: Children only expected to be EH or D:DAILY or X:ANCILL - {} is service_category of child with location {} and status {}".format(cvisit["service_category"], cvisit["hospital_location"].split(" [")[0] if "hospital_location" in cvisit else "", cvisit["patient_status_in_out"] if "patient_status_in_out" in cvisit else ""))
        
            for visit in visits:
            
                enforceChild(visit)
                
                if visit["_apptCatag"] == "NONE_NOTMATCHABLE":
                    if "service_category" in visit and re.match(r'E:EVENT', visit["service_category"]):
                        taa["ehVisit"] += 1 # DEBUG as not working
                    continue
            
                for taa in totalersAndAdders:

                    taa["total"] += 1

                    taa["patients"].add(re.search(r'\-(\d+)', visit["patient_name"]).group(1))
                                        
                    if "_child_visits" in visit:
                        taa["haveChildren"] += 1
                        taa["totalChildren"] += 1
                    
                    # TODO? not accounting for no locn
                    if "hospital_location" in visit:
                        taa["locns"].add(re.sub(r'\_', '/', visit["hospital_location"].split(" [")[0]))
                        
                    if "createdBys" in taa:
                        userRef = visit["created_by_user"] if "created_by_user" in visit else "*NOT SPECIFIED*"
                        taa["createdBys"].add(userRef)
                                                
                    if visit["patient_status_in_out"] == "1:IN":
                        taa["noIns"] += 1
                        """
                        REMOVING as mainly true but not always
                        if not ("service_category" in visit and visit["service_category"] in ["D:DAILY HOSPITALIZATION DATA", "I:IN HOSPITAL"]):
                            print(json.dumps(visit, indent=4))
                            raise Exception("Expected sc to be hosp related for in patient visit")
                        """

                    if "byServiceCategory" in taa:
                        sc = visit["service_category"] if "service_category" in visit else "*NOT SPECIFIED*"
                        et = visit["encounter_type"] if "encounter_type" in visit else "*NOT SPECIFIED*"
                        oc = visit["option_used_to_create"] if "option_used_to_create" in visit else "*NOT SPECIFIED*"
                        taa["byServiceCategory"][sc] += 1
                        taa["byEncounterType"][et] += 1
                        taa["byOptionCreateUsed"][oc] += 1
                            
                    if re.match(r'SCHED', visit["_apptCatag"]):
                        taa["schedAuto"] += 1
                        if "_isCancelled" in visit:
                            taa["schedAutoCancel"] += 1
                        elif "_isNoShow" in visit:
                            taa["schedAutoNoShow"] += 1
                        else:
                            taa["schedAutoActive"] += 1
                        continue
                    if re.match(r'PCE', visit["_apptCatag"]):
                        taa["schedManual"] += 1
                        if "_isCancelled" in visit:
                            taa["schedManualCancel"] += 1  
                        elif "_isNoShow" in visit:
                            taa["schedManualNoShow"] += 1
                        else:
                            taa["schedManualActive"] += 1
                        continue
                    if visit["_apptCatag"] == "NONE_PCEONLY":
                        taa["pceOnly"] += 1
                        continue
                    if visit["_apptCatag"] != "NONE_SCHEDONLY":
                        raise Exception("Expected NONE SCHED ONLY: {}".format(visit["_apptCatag"]))
                    taa["schedOnly"] += 1
        
        """
        TODO TYPER REPLACE THESE SUMMARIES:
        - <=> ["dss_id", "loc_of_encounter"] BUT what if loc_of_encounter missing
        
        - cross <=> all with locations, patients forced to keep
        - summByInstit <=> stInstitByInstit
        - dssSummsByInstit <=> stDSSInstitByInstit ie/ broken into DSS's
        """  
        encountersByInstit = defaultdict(list)
        for visit in visits:
            if "loc_of_encounter" not in visit:
                raise Exception("Expected all Encounter visits to have location of encounter specified")
            instit = visit["loc_of_encounter"].split(" [")[0]
            encountersByInstit[instit].append(visit)
            
        """
        Note: no walkin and that's available for apptN. Could add later (would subset actives)
        """
        def makeSummary(id):
            return {
                "id": id,
                    
                "locns": set(),
                "patients": set(),
                "createdBys": set(), # PREP for machine users or not
            
                "total": 0,
                "noIns": 0,
                
                "haveChildren": 0,
                "totalChildren": 0,
                    
                "schedAuto": 0,
                "schedAutoActive": 0, # ie/ active non walkin
                "schedAutoNoShow": 0,
                "schedAutoCancel": 0,
                "schedManual": 0,
                "schedManualActive": 0,
                "schedManualNoShow": 0,
                "schedManualCancel": 0,
                "schedOnly": 0,
                
                "pceOnly": 0,
                    
                "ehVisit": 0, # NOTE: NOT INCLUDED IN TOTALS ABOVE including 'total' ... stand alone for later. See "COM_CARE" in Cleveland so TODO undercounting
                    
                # Want these for non event hist only
                "byServiceCategory": Counter(),
                "byEncounterType": Counter(),
                "byOptionCreateUsed": Counter()   
            }
                          
        cross = makeSummary("cross")
        
        summByInstit = {}
        dssSummsByInstit = defaultdict(list)
        createOptionSummsByInstit = defaultdict(list)
        
        noOptionCreateBy = Counter()
                
        for instit in encountersByInstit:
                                    
            byInstit = makeSummary(instit)
            summByInstit[instit] = byInstit
            
            summarizeEncounters(encountersByInstit[instit], [byInstit, cross])

            visitsByDSSRef = defaultdict(list)
            visitsByCreateOption = defaultdict(list)
            for visit in encountersByInstit[instit]:
                if "dss_id" not in visit:
                    dssRef = "*NOT SPECIFIED*"
                else:
                    dssRef = visit["dss_id"]
                visitsByDSSRef[dssRef].append(visit)
                if "option_used_to_create" not in visit:
                    createOptionRef = "*NOT SPECIFIED*"
                else:
                    createOptionRef = visit["option_used_to_create"]
                visitsByCreateOption[createOptionRef].append(visit)

            for dssRef in visitsByDSSRef:
             
                byDSS = makeSummary(dssRef)
                
                dssSummsByInstit[instit].append(byDSS)

                summarizeEncounters(visitsByDSSRef[dssRef], [byDSS])
                
            for createOption in visitsByCreateOption:
             
                byCreateOption = makeSummary(createOption)
                
                createOptionSummsByInstit[instit].append(byCreateOption)

                summarizeEncounters(visitsByCreateOption[createOption], [byCreateOption])
                
            # TODO: visits by location to just focus on that in detail if need be
                
        return cross, summByInstit, dssSummsByInstit, createOptionSummsByInstit
        
    unmatchedApptsSumm, unmatchedApptsSummByInstit = summarizeUnmatchedAppts(unmatchedAppts)
        
    # Will all go to different typer passes/summary reductions
    cross, summByInstit, dssSummsByInstit, createOptionSummsByInstit = summarizeAllEncounters(catagedEncounters)
    
    # Appt or Encounter 
    allPatients = cross["patients"].union(unmatchedApptsSumm["patients"])
    print("** Warning: unmatched appointments introduce {:,} novel patients".format(len(unmatchedApptsSumm["patients"] - cross["patients"])))
    allLocns = cross["locns"].union(unmatchedApptsSumm["locns"])
    print("** Warning: unmatched appointments introduce {:,} novel locations".format(len(unmatchedApptsSumm["locns"] - cross["locns"])))
    
    # ############################ MU .md #####################################
    # TODO: add MU excel
                 
    def percentBreakdownMU(counts, contextTotal=-1, bold=True): 
        total = sum(cnt for cnt in counts)
        if total == 0:
            return "-"
        if contextTotal == -1:
            contextTotal = total
        percents = [re.sub(r'^0$', '-', re.sub(r'\.0$', '', re.sub(r'\%', '', reportPercent(cnt, contextTotal)))) for cnt in counts]
        mu = "/".join(percents)
        return "__{}__".format(mu) if bold and float(total)/float(contextTotal) > 0.5 else mu
                 
    def muByInstit(cross, summByInstit, unmatchedApptsSumm, unmatchedApptsSummByInstit):
        mu = """The following quantifies both appointments and encounters by institution.
  * _Encounters_ shows the quantity and percentage of encounters in each institution for this period. Note that this number does not include dependent (\"child\") or historical encounters. 
  * _Sched_ quantifies encounters with matching appointments (\"Scheduled Encounters\").  The _AU/M/O%_ breakdown shows how many of these are _AUtomatically_ entered into VistA as a result of appointment creation, how many were _Manually_ entered, prompted by an appointment and how many are marked as scheduled by VistA but which lack an appointment. The latter reflect synchronization bugs in the system. Its entry is in _Bold_ below when  _Scheduled Encounters_ are in the majority.
  * _NoSched_ quantifies encounters without appointments (\"Non Scheduled Encounters\"). Its entry is in _Bold_ below when _Non Scheduled Encounters_ are in the majority. This proportion reflects how much a site doesn't schedule activity.
  * _No Enc Appts_ shows appointments that lack encounters. The _A/NS/C%_ breakdown shows how many of these \"orphan appointments\" are Active, NoShow and Cancelled. In a VistA running VistA Scheduling (_VSE_), cancelled appointments account for the vast majority of the orphans with noshows making up the majority of the balance. Active orphans may reflect a failure of a system synchronization or cleanup task.
  * _Pts_ and _Locns_ show the total number of unique patients and locations involved
        
"""
        gotInP = True if sum(1 for instit in summByInstit if summByInstit[instit]["noIns"]) else False 
        cols = [":Institution", "Encounters"]
        if gotInP:
            noteMU = ""
        else:
            noteMU = "__Note__: no institution in this VistA has in-patient encounters.\n\n" 
        cols.extend(["Sched (AU/M/O)%", "Non Sched %", "No Enc Appts (A/NS/C%)"])
        cols.extend(["Pts", "Locns"])
        tbl = MarkdownTable(cols)
        for instit in sorted(summByInstit, key=lambda x: summByInstit[x]["total"], reverse=True):
            
            institSumm = summByInstit[instit]
            schedAuto = institSumm["schedAutoActive"] + institSumm["schedAutoNoShow"] + institSumm["schedAutoCancel"]
            schedManual = institSumm["schedManualActive"] + institSumm["schedManualNoShow"] + institSumm["schedManualCancel"]
            schedMU = percentBreakdownMU([schedAuto, schedManual, institSumm["schedOnly"]], institSumm["total"])
            nonSchedMU = percentBreakdownMU([institSumm["pceOnly"]], institSumm["total"])
            
            patients = institSumm["patients"].union(summByInstit[instit]["patients"])
            locns = institSumm["locns"].union(summByInstit[instit]["locns"])
            if instit in unmatchedApptsSummByInstit:
                unmatchedApptsSummI = unmatchedApptsSummByInstit[instit]
                unmatchedApptsBDMU = percentBreakdownMU([unmatchedApptsSummI["active"], unmatchedApptsSummI["noShow"], unmatchedApptsSummI["cancel"]], unmatchedApptsSummI["total"], bold=False)
                patients |= unmatchedApptsSummI["patients"]
                locns |= unmatchedApptsSummI["locns"]
                unmatchedApptsMU = "{:,} ({}%)".format(unmatchedApptsSummI["total"], unmatchedApptsBDMU)
            else:
                unmatchedApptsMU = ""
            
            row = [
                "__[{}](#{})__".format(instit, re.sub(r'[ \(\)\.]', '_', instit.lower())),
                reportAbsAndPercent(institSumm["total"], cross["total"])
            ]
            row.extend([
                schedMU,
                nonSchedMU,
                unmatchedApptsMU
            ])
            row.extend([
                reportAbsAndPercent(len(patients), len(allPatients)),   
                reportAbsAndPercent(len(locns), len(allLocns))
            ])
            tbl.addRow(row)
        mu += noteMU + tbl.md() + "\n\n"
        return mu
                           
    def muByInstitByDSSnCreateOption(index, instit, institSumm, dssSummsOfInstit, createOptionSummsOfInstit, printOnly=True):  
        
        imu = "## {}. {} {{#{}}}\n\n".format(index, instit, re.sub(r'[ \(\)\.]', '_', instit.lower()))
        
        # TODO: encounters with cancelled appointments are 'strange', the other
        # side of 'active' appointments with no encounters. These "mis-alignments"
        # need further investigation.
        imu += "This Institution has <span class='countHigh'>{:,}</span> encounters assigned to <span class='countHigh'>{:,}</span> work types (\"stop codes\") for <span class='countHigh'>{:,}</span> patients at <span class='countHigh'>{:,}</span> \"locations\". Of these encounters, <span class='countHigh'>{}</span> are automatically created from appointments (\"Sched Auto\"), <span class='countHigh'>{}</span> are manually created from appointments (\"Sched Manual\"), <span class='countHigh'>{}</span> are marked as scheduled but lack a matching appointment (\"Sched Only\"), while the balance, <span class='countHigh'>{}</span>, are not scheduled (\"Non Sched\"). Both types of scheduled encounter are further broken down into Active (A), NoShow (NS) and Cancelled (C) with the vast majority being active.\n\n".format(
                institSumm["total"],
                len(dssSummsOfInstit),
                len(institSumm["patients"]),     
                len(institSumm["locns"]),
                   
                reportAbsAndPercent(institSumm["schedAuto"], institSumm["total"]),
                reportAbsAndPercent(institSumm["schedManual"], institSumm["total"]),
                reportAbsAndPercent(institSumm["schedOnly"], institSumm["total"]),
                reportAbsAndPercent(institSumm["pceOnly"], institSumm["total"])
            )  
                
        # ################## Do a summary by create option #####################
        
        # TODO: add in some marker on Roll and Scroll or GUI (or not create option => machine user?)
        cotbl = MarkdownTable([":Created By", "Count", "Sched Auto (A/NS/C)%", "Sched Manual (A/NS/C)%", "Sched Only %", "Non Sched %"])
        for createOptionSumm in sorted(createOptionSummsOfInstit, key=lambda x: x["total"], reverse=True):
            # ie/ automatic, manual, orphan (sched only); not scheduled
            totalSched = createOptionSumm["schedAuto"] + createOptionSumm["schedManual"] + createOptionSumm["schedOnly"]
            schedAutoMU = percentBreakdownMU([createOptionSumm["schedAutoActive"], createOptionSumm["schedAutoNoShow"], createOptionSumm["schedAutoCancel"]], createOptionSumm["total"]) 
            schedManualMU = percentBreakdownMU([createOptionSumm["schedManualActive"], createOptionSumm["schedManualNoShow"], createOptionSumm["schedManualCancel"]], createOptionSumm["total"]) 
            schedOnlyMU = percentBreakdownMU([createOptionSumm["schedOnly"]], createOptionSumm["total"]) 
            nonSchedMU = percentBreakdownMU([createOptionSumm["pceOnly"]], createOptionSumm["total"])
            label = createOptionSumm["id"].split(" [")[0]
            if float(totalSched)/float(createOptionSumm["total"]) > 0.5:
                label = "__{}__".format(label)
            cotbl.addRow([
                label,
                createOptionSumm["total"],
                schedAutoMU,
                schedManualMU,
                schedOnlyMU, 
                nonSchedMU
            ])
        imu += "<span class='countHigh'>{:,}</span> options (application types) created encounters for this institution. Options names are __in bold__ where most of the encounters they create are scheduled.\n\n".format(len(createOptionSummsOfInstit))
        imu += cotbl.md() + "\n\n"
    
        # ################# Break stop code down/dominant based grouping ######
        dssSummsByDominantSC = defaultdict(list)

        for dssSumm in dssSummsOfInstit:
                        
            dominantSC = sorted(dssSumm["byServiceCategory"], key=lambda x: dssSumm["byServiceCategory"][x], reverse=True)[0]

            if dominantSC in ["A:AMBULATORY", "X:ANCILLARY PACKAGE DAILY DATA", "T:TELECOMMUNICATIONS"]:
                dssSummsByDominantSC[dominantSC].append(dssSumm)
            else: # include not specified
                dssSummsByDominantSC["O:OTHER"].append(dssSumm)           

        # Allowing no showSC to fit into print 
        def muDSSSummsOfDominantSC(dominantSC, dssSumms, printOnly=True):
        
            cols = [":Stop Code", "Total"]
            if sum(dssSumm["noIns"] for dssSumm in dssSumms):
                cols.append("In Patient")
                showIP = True
            else:
                showIP = False
            cols.extend(["Sched Auto (A/NS/C)%", "Sched Manual (A/NS/C)%", "Sched Only %", "Non Sched %", "Pts", "Locns"]) # Creators removed as too wide
            
            scs = set(sc for dssSumm in dssSumms for sc in dssSumm["byServiceCategory"])
            if printOnly == False:
                cols.append("Options")
                showCreateOption = True
                if len(scs) > 1:
                    cols.append(":Service Categories")
                    showSC = True
                else:
                    showSC = False
            else:
                showCreateOption = False
                showSC = False
                
            tbl = MarkdownTable(cols)
    
            # TODO: pie it with instit overall
            
            for dssSumm in sorted(dssSumms, key=lambda x: x["total"], reverse=True):
                
                totalSched = dssSumm["schedAuto"] + dssSumm["schedManual"] + dssSumm["schedOnly"]
                schedAutoMU = percentBreakdownMU([dssSumm["schedAutoActive"], dssSumm["schedAutoNoShow"], dssSumm["schedAutoCancel"]], dssSumm["total"]) 
                schedManualMU = percentBreakdownMU([dssSumm["schedManualActive"], dssSumm["schedManualNoShow"], dssSumm["schedManualCancel"]], dssSumm["total"]) 
                schedOnlyMU = percentBreakdownMU([dssSumm["schedOnly"]], dssSumm["total"]) 
                nonSchedMU = percentBreakdownMU([dssSumm["pceOnly"]], dssSumm["total"])       
                    
                label = re.sub(r'\_', '/ ', dssSumm["id"].split(" [")[0])
                if float(totalSched)/float(dssSumm["total"]) > 0.5:
                    label = "__{}__".format(label)
                    
                row = [
                    label,
                    dssSumm["total"]
                ]
                if showIP:
                    row.append(dssSumm["noIns"] if dssSumm["noIns"] > 0 else "")
                row.extend([
                    schedAutoMU,
                    schedManualMU,
                    schedOnlyMU,
                    nonSchedMU,
                    
                    len(dssSumm["patients"]),
                    len(dssSumm["locns"])
                    # len(dssSumm["createdBys"]) as too wide
                ])
                if showCreateOption:
                    row.append(muBVC(dssSumm["byOptionCreateUsed"]))
                if showSC:
                    row.append(muBVC(dssSumm["byServiceCategory"]))
                
                tbl.addRow(row)  
                  
            # TODO: add a statement on scheduled/non scheduled for both OR A PIE CHART?
            if len(scs) == 1:
                tmu = "For <span class='countHigh'>{:,}</span> stop codes, there is only __{}__ activity. The names of stop codes with a majority of scheduled encounters are in __bold__ ...\n\n".format(
                    len(dssSumms),
                    dominantSC.split(":")[1]
                )
            elif dominantSC == "O:OTHER":
                tmu = "For <span class='countHigh'>{:,}</span> stop codes, other types of activity dominate. The names of stop codes with a majority of scheduled encounters are in __bold__ ...\n\n".format(
                    len(dssSumms)
                )
            else:
                tmu = "For <span class='countHigh'>{:,}</span> stop codes, __{}__ activity dominates. The names of stop codes with a majority of scheduled encounters are in __bold__ ...\n\n".format(
                    len(dssSumms),
                    dominantSC.split(":")[1]                    
                )            

            tmu += tbl.md() + "\n\n"
                
            return tmu
            
        for dominantSC in sorted(dssSummsByDominantSC, key=lambda x: len(dssSummsByDominantSC[x]), reverse=True):
            imu += muDSSSummsOfDominantSC(dominantSC, dssSummsByDominantSC[dominantSC], printOnly=printOnly)                                    
            
        return """<section>
        
{}</section>

""".format(imu) 
    
    # Encounters means 'direct' ie/ not child or EH encounters. TODO more on them.
    mu = """
    
A copy of VistA __{} [{}]__ was cut on _{}_. For its final 90 full days, starting on _{}_, the system had <span class='countHigh'>{:,}</span> appointments in <span class='countHigh'>{:,}</span> time slots and <span class='countHigh'>{:,}</span> encounters. These involved <span class='countHigh'>{:,}</span> patients at <span class='countHigh'>{:,}</span> institutions with <span class='countHigh'>{:,}</span> \"locations\".

""".format(
        vistaName,
        stationNo,
        cutDate,

        onAndAfterDay,
        totalMatchedAppts + len(unmatchedAppts),
        totalSlots,
        cross["total"], # of encounters
        
        len(allPatients), # cross appt and encounters
        len(summByInstit),
        len(allLocns), # cross appt and encounters
    )
    
    mu += muByInstit(cross, summByInstit, unmatchedApptsSumm, unmatchedApptsSummByInstit)
        
    for i, instit in enumerate(sorted(summByInstit, key=lambda x: summByInstit[x]["total"], reverse=True), 1):
        mu += muByInstitByDSSnCreateOption(i, instit, summByInstit[instit], dssSummsByInstit[instit], createOptionSummsByInstit[instit], printOnly=printOnly)
                
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print("Serializing Report to {}".format(userSiteDir))
    if not os.path.isdir(userSiteDir):
        raise Exception("Expect User Site to already exist with its basic contents")
    title = "Encounters {}".format(stationNo)
    mu = TOP_MD_TEMPL.format(title, "Encounters") + mu
    open(userSiteDir + "encounters.md", "w").write(mu)
    
# ################################# Reductions/Utils #########################

"""
Overall: want match of apptN, apptL, visit (as encounter) with embedded v provider.
Must include option used to create the encounter so can match that to auto or
manual creation (some created manually after seeing a scheduled appt?). 

TODO: evolve to smaller indexes so can go from appointment perspective indexing
encounter component by apptN or apptL.
"""

"""
Indexing by day of visits, appts (legacy and VSE) and V providers for an 
Encounter Period (onAndAfter, upTo). This enables linking.

Flattened and extraneous properties removed (ie/ work off pter refs/LABEL [ID] vs
full dicts.

TODO:
- credit stop qual -- put in and enforce form (is it added afterwards?)
- child visit date spread (may analyze above)
- BIG: consult tie in or other data_source ref ... 
- make sure enough data for 668, 757 alignments ie/ all leg, all vpe aligned in 668
including WHEN/WHY VISIT or APPT are deleted.
- cover all of https://github.com/vistadataproject/workload/blob/master/prodcloneAnalyze/createWorkDetailMVDM.py includes 409_73 (ie/ counted) and pull of V CPT and V POV
- add Patient Appt
"""
def gatherEncounterDataByDay(stationNo, onAndAfterDay, upToDay):

    jsnFl = TMPWORKING_LOCN_TEMPL.format(stationNo) + "legNvpeApptsNVisits.json"
    try:
        gatheredByDay = json.load(open(jsnFl))
    except:
        print("Appt source data not yet gathered by day - organizing relevant 44_003, 409_84, 9000010_06 and 9000010 ...")
    else:
        return gatheredByDay

    # Used for filtering out - same as typer
    def getResourceDay(resource, createProp, onAndAfterDay, upToDay):
        if createProp not in resource:
            return ""
        dtValue = resource[createProp]["value"] if "value" in resource[createProp] else resource[createProp]["label"]
        dayValue = dtValue.split("T")[0]
        if dayValue < onAndAfterDay:
            return ""
        if dayValue >= upToDay:
            return ""
        return dayValue

    """
    9000010: 'date_visit_created' used to decide how far
    back to go (1 year back from onAndAfter) in walk. Unlike appointments, 
    there are so many 9000010's that won't just walk them all to pick
    out those with the matchable appointment/visit time ("visit_admit_datetime")
    in the onAndAfter and until range.
    """
    def gatherVisitsByDay(stationNo, onAndAfterDay, upToDay):
        jsnFl = TMPWORKING_LOCN_TEMPL.format(stationNo) + "byDay9000010_{}_{}".format(onAndAfterDay, upToDay)
        try:
            visitsByDay = json.load(open(jsnFl))
        except:
            print("9000010 not yet gathered by day for {} to {} ...".format(onAndAfterDay, upToDay))
        else:
            return visitsByDay

        visitStartDate = (datetime.strptime(onAndAfterDay, "%Y-%m-%d") - relativedelta(years=1)).strftime("%Y-%m-%d") # one year back
        print("Organizing 9000010 starting at {}, one year back from onAndAfter {} ...".format(visitStartDate, onAndAfterDay))
        visitsByDay = defaultdict(list)
        visitsByIEN = {} # for provider and parent linking
        parentIENByChildIEN = {} # for checking below
        unattachedChildVisits = 0
        cntEncountersInDateRange = 0
        cntQualCreditStopVisitsSkipped = 0
        cntTopLevelEncounters = 0
        cntByPackage = Counter()
        createProp = "visit_admit_datetime"   
        startProp = "date_visit_created"
        dataLocn = DATA_LOCN_TEMPL.format(stationNo)     
        store = FMQLReplyStore(dataLocn)
        # Go back one year from onAndAfter which should get all visits created for encounters
        # falling in the onAndAfter/upTo window.
        startAtReply = store.firstReplyFileOnOrAfterCreateDay("9000010", startProp, visitStartDate) 
        if startAtReply == "":
            raise Exception("Can't find 9000010 start reply")
        resourceIter = FilteredResultIterator(dataLocn, "9000010", startAtReply=startAtReply)
        print("... starting at reply {}".format(startAtReply))
        for i, resource in enumerate(resourceIter, 1):
            if i == 1:
                print("\tFirst resource seen {}".format(
                    resource[startProp]["value"] if startProp in resource else "?"
                ))
            if i % 50000 == 0:
                print("\tAnother 50K to {:,}, {:,} taken, {:,} credit stop visit's skipped, last resource day {} - 50K resource create date {}".format(i, cntEncountersInDateRange, cntQualCreditStopVisitsSkipped, resourceDay, resource[startProp]["value"] if startProp in resource else "?"))
            # issue in one of 648
            if "service_category" not in resource:
                print("** Skipping Visit as no setting for 'service_category'")
                continue
            # Keeps it in the window of onAndAfterDay and upToDay
            resourceDay = getResourceDay(resource, createProp, onAndAfterDay, upToDay)
            if resourceDay == "":
                continue # as can't rely on create/ien order == createProp order
            # CREDIT STOP -- qual [SCHED] child
            if "package" in resource and re.match(r'SCHEDULING', resource["package"]["label"]) and "encounter_type" in resource and resource["encounter_type"] == "C:CREDIT STOP":
                cntQualCreditStopVisitsSkipped += 1
                continue
            cntEncountersInDateRange += 1
            resource["_ien"] = resource["_id"].split("-")[1]
            for prop in list(resource):
                if prop in ["_id", "type", "label"]:
                    del resource[prop]
                    continue
                if re.search(r'(flag|cancer|connected|sexual|veteran|112|asia|exposure)', prop):
                    del resource[prop]
                    continue
            flattenPropValues(resource)
            visitsByIEN[resource["_ien"]] = resource
            if "parent_visit_link" in resource:
                parentIEN = re.search(r' \[9000010\-(\d+)', resource["parent_visit_link"]).group(1)
                if parentIEN in visitsByIEN:
                    pvisit = visitsByIEN[parentIEN]
                    if "_child_visits" not in pvisit:
                        pvisit["_child_visits"] = []
                    pvisit["_child_visits"].append(resource)
                    parentIENByChildIEN[resource["_ien"]] = parentIEN
                else:
                    unattachedChildVisits += 1 # should only occur at year start
                continue
            cntTopLevelEncounters += 1
            visitsByDay[resourceDay].append(resource)
            
        print("... finished taking {:,} encounters in date range ({}-{}), {:,} are top level, {:,} children, {:,} in range child visits unattached and dropped".format(
            cntEncountersInDateRange, 
            visitStartDate,
            upToDay,
            cntTopLevelEncounters,
            len(parentIENByChildIEN),
            unattachedChildVisits
        ))
    
        json.dump(visitsByDay, open(jsnFl, "w"))
    
        return visitsByDay
    
    visitsByDay = gatherVisitsByDay(stationNo, onAndAfterDay, upToDay)
        
    """    
    2. V PROVIDER - make subordinate to their referenced visits. Will only do V PROVIDERs
    for visits with admit time in the onAndAfter/upTo range. This can also QA
    if the go-back-a-year visit walk above catches all expected. 

    def gatherVProviderByVisitIEN(stationNo, onAndAfterDay, upToDay, topVisitIENs, childVisitIENs):
    
        print("Organizing 9000010_06 under visits starting at {}, the on and after date ...".format(onAndAfterDay))

    """
        
    def gatherOldApptsByDay(stationNo, onAndAfterDay, upToDay):
    
        jsnFl = TMPWORKING_LOCN_TEMPL.format(stationNo) + "byDay44_003_{}_{}".format(onAndAfterDay, upToDay)
        try:
            oldApptsByDay = json.load(open(jsnFl))
        except:
            print("44_003 not yet gathered by day for {} to {} ...".format(onAndAfterDay, upToDay))
        else:
            return oldApptsByDay

        print("Organizing 44_003 (walking all) ...")
        oldApptsByDay = defaultdict(list)
        createProp = "appointment_date_time"
        taken = 0
        for i, resource in enumerate(filteredResultIterator(stationNo, "44_003", useRF=True), 1):
            if i % 50000 == 0:
                print("\tAnother 50K to {:,}, {:,} taken".format(i, taken))
            resourceDay = getResourceDay(resource, createProp, onAndAfterDay, upToDay)
            # filter to window
            if resourceDay == "":
                continue
            taken += 1
            resource["_ien"] = resource["_id"].split("-")[1]
            for prop in ["_id", "patient_container_", "label", "type"]:
                if prop in resource:
                    del resource[prop]
            flattenPropValues(resource)
            oldApptsByDay[resourceDay].append(resource)
        print("... finished processing {:,} 44_003's, {:,} taken".format(i, taken))

        json.dump(oldApptsByDay, open(jsnFl, "w"))
    
        return oldApptsByDay
    
    oldApptsByDay = gatherOldApptsByDay(stationNo, onAndAfterDay, upToDay)

    def gatherNewApptsByDay(stationNo, onAndAfterDay, upToDay):
    
        jsnFl = TMPWORKING_LOCN_TEMPL.format(stationNo) + "byDay409_84_{}_{}".format(onAndAfterDay, upToDay)
        try:
            newApptsByDay = json.load(open(jsnFl))
        except:
            print("409_84 not yet gathered by day for {} to {} ...".format(onAndAfterDay, upToDay))
        else:
            return newApptsByDay
        
        print("Organizing 409_84 (walking all, filtering to window) ...")
        newApptsByDay = defaultdict(list)
        createProp = "starttime"
        taken = 0
        for i, resource in enumerate(filteredResultIterator(stationNo, "409_84"), 1):
            if i % 50000 == 0:
                print("\tAnother 50K to {:,}, {:,} taken".format(i, taken))
            resourceDay = getResourceDay(resource, createProp, onAndAfterDay, upToDay)
            # filter to window
            if resourceDay == "":
                continue
            taken += 1
            resource["_ien"] = resource["_id"].split("-")[1]
            for prop in ["_id", "label", "type"]:
                if prop in resource:
                    del resource[prop]
            flattenPropValues(resource) 
            newApptsByDay[resourceDay].append(resource)
        print("... finished processing {:,} 409_84, {:,} taken".format(i, taken))
        
        json.dump(newApptsByDay, open(jsnFl, "w"))

        return newApptsByDay

    newApptsByDay = gatherNewApptsByDay(stationNo, onAndAfterDay, upToDay)
                    
    print("Returning Organized Data")     
    return visitsByDay, oldApptsByDay, newApptsByDay
        
"""
Post gathering by day, hone down matches by location/patient too
"""               
def indexEncounterDataByDateLocationPatient(stationNo, visitsByDay, oldApptsByDay, newApptsByDay):

    # ######### Organize Appts + Encounters into Time/Locn/Patient Hierarchy #######
    # ... TODO: may move this into the Reducer ie/ make the reducer do this
    
    # A/C for older _ sub'ed for / in locn and if locnRef is delegate with different
    # id but same label ie/ reduce to a / using label
    def toLocnLabel(locnRef):
        return re.sub(r'\_', '/', locnRef.split(" [")[0])
    
    matchesDayTimeLocationPatient = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list)))))
    # from union of old and new appts (not visit only days)
    days = set(oldApptsByDay).union(set(newApptsByDay))
    for day in days:
        if day not in oldApptsByDay:
            continue
        for res in oldApptsByDay[day]:
            if not ("appointment_container_" in res and "appointment_date_time" in res and "patient" in res):
                print("** Warning - bad old appt missing expected props")
                continue
            tm = res["appointment_date_time"].split("T")[1]
            locnLabel = toLocnLabel(res["appointment_container_"])
            patient = res["patient"]
            if "appointment_cancelled" in res:
                typ = "apptLC"
            else:
                typ = "apptL"
            matchesDayTimeLocationPatient[day][tm][
            locnLabel][patient][typ].append(res)  
    for day in days:
        if day not in newApptsByDay:
            continue
        for res in newApptsByDay[day]:
            if not ("resource" in res and "starttime" in res and "patient" in res):
                print("** Warning - bad new appt missing expected props, resource | starttime | patient")
                continue
            tm = res["starttime"].split("T")[1]
            locnLabel = toLocnLabel(res["resource"])
            patient = re.sub(r'9000001', '2', res["patient"])
            if "cancel_datetime" in res:
                typ = "apptNCancelled"
            elif "noshow" in res:
                typ = "apptNNoShow"
            else:
                typ = "apptN"
            matchesDayTimeLocationPatient[day][tm][
            locnLabel][patient][typ].append(res)
    # REM: reduction doesn't have credit stop only ([SCHED]/parent) visits
    # ... TOP SCHED, TOP PCE, child PCE (under either top) as never have a child
    # SCHED 'encounter'
    # CHANGE COMING: may exclude EH visits from RED
    totalMatchableTopEncounters = 0
    totalMatchableEncounters = 0
    noTimeVisitsByPackage = Counter() # + double check typer that pkg mand in 757 too
    noHospitalLocationVisitsByPackage = Counter()
    excludedVisitsAsMissingProps = 0
    excludedScheduledVisitsAsMissingProps = 0
    countExcludedVisitsAsMissingPropsSC = Counter()
    totalVisitsEH = 0
    totalChildren = 0
    totalNoTimeTops = 0
    for day in days:
        if day not in visitsByDay:
            continue
        for res in visitsByDay[day]:
            if not ("hospital_location" in res and "visit_admit_datetime" in res and "patient_name" in res):
                if res["service_category"] != "E:EVENT (HISTORICAL)":
                    raise Exception("Expect key props in all PCE and SCHED visits - only EH excluded for missing props")
                continue
            # Can exclude as key props will all agree with parent
            if "parent_visit_link" in res:
                if re.match(r'SCHEDULING', res["package"]): # extra - no SCHED is a child
                    raise Exception("Scheduling with parent!")
                totalChildren += 1
                continue # let's just have top
            # note: visit_admit_date_time must support tm
            if not re.search(r'T', res["visit_admit_datetime"]):
                noTimeVisitsByPackage[res["package"]] += 1
                totalNoTimeTops += 1
                continue
            tm = res["visit_admit_datetime"].split("T")[1]
            if "hospital_location" not in res:
                noHospitalLocationVisitsByPackage[res["package"]] += 1
                continue
            locnLabel = toLocnLabel(res["hospital_location"])
            # TODO: BUT perhaps exclude res's w/o it (saw in 648)
            if res["service_category"] == "E:EVENT (HISTORICAL)": # some have all keys props so exclude em all
                if "package" in res and re.match(r'SCHEDULING', res["package"]):
                    raise Exception("Dont expect EVENT HISTORICAL service_category with package SCHEDULING")
                totalVisitsEH += 1
                # doing as EH Visit to avoid 
                matchesDayTimeLocationPatient[day][tm][
            locnLabel][patient]["ehVisit"].append(res) 
                continue
            # Exclude no locn, no admit
            totalMatchableEncounters += 1
            patient = re.sub(r'9000001', '2', res["patient_name"])
            if "package" in res and re.match(r'SCHEDULING', res["package"]):
                matchesDayTimeLocationPatient[day][tm][
            locnLabel][patient]["visit"].append(res) 
                continue
            # ie/ non schedule appts - inc with no package!
            matchesDayTimeLocationPatient[day][tm][
            locnLabel][patient]["visitNS"].append(res)
    print("Summary of Visits: total matchable encounters {:,} - {:,} children, {:,} top EHs and {:,} no time tops are not in matcheable categories".format(totalMatchableEncounters, totalChildren, totalVisitsEH, totalNoTimeTops))
    if len(noTimeVisitsByPackage):
        print("** WARNING: no time in visit_admit_time by pkg {}".format(noTimeVisitsByPackage))
    if len(noHospitalLocationVisitsByPackage):
        print("** WARNING: no location by pkg: {}".format(noHospitalLocationVisitsByPackage))
        
    return matchesDayTimeLocationPatient
    
def categorizeVisitAppts(info, noneApptOnlyDetails=None, matchedDetails=None, matchedDetails2ByCatag=None, visitCreateBorAStart=None):

    # Reduce to singular of a type if can        
    def oneAppt(info, apptPrefix="apptN"):
        apptProps = [prop for prop in info if re.match(apptPrefix, prop)]
        if len(apptProps) == 0:
            return None
        # Strict for apptN - looser (need apptL) for apptL (TODO: tighten)
        if len(apptProps) > 1:
            if apptPrefix == "apptN" or apptPrefix not in info:  
                # USED TO BE AN EXCEPTION BUT ISSUE FOR POR 663 TODO
                print("*** Ambiguous multiple {} matches".format(apptPrefix, json.dumps(apptProps)))
            # apptProp = apptPrefix
            apptProp = apptPrefix if apptPrefix in apptProps else apptProps[0]
        else:
            apptProp = apptProps[0]
        # Strict for apptN - looser - pick bigger for apptL (TODO: tighten)
        if len(info[apptProp]) > 1:
            if apptPrefix == "apptN": # Warning for apptN (weakened exp for 663)
                print("** Ambiguous multiple {}s at same time".format(apptPrefix))
            ressBySize = sorted(info[apptProp], key=lambda x: len(x), reverse=True)
            appt = ressBySize[0] # ie/ with checkout etc     
        else:
            appt = info[apptProp][0]
        return appt
        
    """
    Matching appt and visit DT props to get nearest time when visit created. Is
    it created when appt is or at checkin or at checkout or ?
    
    EXTRA: Events would create, checkout, cancel etc. ie/ a state table.
    ... fill in this and other pattern notes
        apptL:
        - date_appointment_made == visit:date_visit_created
        - appointment_date_time = visit:visit_admit_datetime
        - data_entry_clerk == visit:created_by_user
        - checked_out=apptN:checkout
        apptN:
        - starttime = visit:visit_admit_datetime (and apptL)
        and maybe visit:date_last_modified == checked
    """
    def matchCreationDateTimes(apptN, apptL, visit):

        # Should be day after 0:50
        # ? what option used in appt create here? ie/ what app? Why all CC 
        # like this?
        if re.match(r'SDAM BACKGROUND', visit["option_used_to_create"]):
            return None

        # Issue that no match time as vista can be out by seconds - when
        # out indicates code sequential using NOW as opposed to just cloning (apptN-SCHED)
        def squeezeTimes(dtTimeCollection):
            dtMap = {}
            dts = [dt for dt in dtTimeCollection if re.search(r'\dZ', dt)]
            # within 60 seconds => take lower
            mappedDTs = {}
            cnt = 0
            for i, dt in enumerate(sorted(dts), 1):
                try:
                    dtDT = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
                except:
                    print("** PROBLEM BAD DATE TIME: {}".format(dt))
                    continue
                cnt += 1
                if cnt == 1:
                    prevDT = dtDT
                    prevdt = dt
                    continue
                if dtDT - prevDT < timedelta(seconds=60):
                    mappedDTs[dt] = prevdt
                    dtTimeCollection[prevdt].extend(dtTimeCollection[dt])
                    del dtTimeCollection[dt]
                    continue
                prevDT = dtDT
                prevdt = dt
            return dtTimeCollection 
           
        # For two and three 
        def isstr(s):
            try:
                return isinstance(s, basestring)
            except NameError:
                return isinstance(s, str)

        appt = apptN if apptN else apptL
        typedDTPropsByDT = defaultdict(list)
        for prop in appt:
            # know not relevant
            if prop == "desired_date_of_appointment":
                continue 
            # walkin can be bool
            if not isstr(appt[prop]):
                continue
            if re.search(r'\dZ$', appt[prop]):
                typedDTPropsByDT[appt[prop]].append("appt:" + prop)
                continue
            if re.match(r'\d\d\d\d\-\d\d\-\d\d$', appt[prop]):
                typedDTPropsByDT[appt[prop]].append("appt:" + prop + "_day")
        visitDtPropsByDT = defaultdict(list)
        for prop in visit:
            if not isstr(visit[prop]):
                continue
            if re.search(r'\dZ$', visit[prop]):
                typedDTPropsByDT[visit[prop]].append("visit:" + prop)
                if prop == "date_visit_created": 
                    dayOnlyDT = visit[prop].split("T")[0]
                    typedDTPropsByDT[dayOnlyDT].append("visit:" + prop + "_day")
                continue
            if re.match(r'\d\d\d\d\-\d\d\-\d\d$', visit[prop]):
                typedDTPropsByDT[visit[prop]].append("visit:" + prop + "_day")
        typedDTPropsByDT = squeezeTimes(typedDTPropsByDT)
        # Stick to matchable props
        mtch = None
        for dt in typedDTPropsByDT:
            apptProps = [prop.split(":")[1] for prop in typedDTPropsByDT[dt] if re.match(r'appt:', prop) if re.search(r'(\_made|check)', prop.split(":")[1])]
            if len(apptProps) == 0:
                continue
            if "visit:date_visit_created" in typedDTPropsByDT[dt]:
                mtch = ("date_visit_created", "/".join(sorted(apptProps)))
            elif "visit:date_visit_created_day" in typedDTPropsByDT[dt]:
                mtch = ("date_visit_created_day", "/".join(sorted(apptProps)))
        return mtch
        
    # TODO: just make this and logic at end func be the func ie/ no need
    # for explicit enum of SchedVisit and its options etc. That was just for
    # dev
    def categorizeMatch(visitType, visit, apptType, apptN, apptL):
        if "option_used_to_create" not in visit: 
            catag = "{}_NOOPTION".format(visitType)  
            matchedDetails["apptTypeByCatag"][catag][apptType] += 1 
            return catag
        optionUsedToCreateLabel = visit["option_used_to_create"].split(" [")[0]
        catag  = "{}_{}".format(visitType, optionUsedToCreateLabel)     

        matchedDetails["apptTypeByCatag"][catag][apptType] += 1

        if matchedDetails2ByCatag != None:
            mtch = matchCreationDateTimes(apptN, apptL, visit)
            if mtch == None:
                apptVisitCreationMatch = "NONE"
            else:
                apptVisitCreationMatch = mtch[1]
            matchedDetails2ByCatag[catag][apptVisitCreationMatch] += 1
            
        return catag
        
    # Matching is from Visit back to Appts
    def matchScheduledVisit(info, apptType, apptN, apptL):
            
        if len(info["visit"]) != 1:
            """
            Saw where second visit as if first appt at exact time was deleted
            and the older visit created lingered. 
            """
            return "SCHED_AMBIG_VISIT"
                
        visit = info["visit"][0] 
                                
        """
        TODO: O:OCCASION OF SERVICE for MRI etc and for that service_category is
        X:ANCILL. O:OCC's are NON COUNT
        """
        if not ("encounter_type" in visit and visit["encounter_type"] in ["P:PRIMARY", "O:OCCASION OF SERVICE"]):
            raise Exception("Expected SCHED Visit match to have encounter type P:PRIMARY or O:OCCASION OF SERVICE")
                                            
        if "option_used_to_create" not in visit: 
            catag = "SCHED_NOOPTION"  
            matchedDetails["apptTypeByCatag"][catag][apptType] += 1 
            return catag
                                
        optionUsedToCreateLabel = visit["option_used_to_create"].split(" [")[0]
        catag  = "SCHED_{}".format(optionUsedToCreateLabel)     
                
        # Know there is an APPTN
        matchedDetails["apptTypeByCatag"][catag][apptType] += 1

        if matchedDetails2ByCatag != None:
            mtch = matchCreationDateTimes(apptN, apptL, visit)
            if mtch == None:
                apptVisitCreationMatch = "NONE"
            else:
                apptVisitCreationMatch = mtch[1]
            matchedDetails2ByCatag[catag][apptVisitCreationMatch] += 1
            
        """
        KEY: NOT AS TELLING AS MAYBE CREATE APPT AFTER VISIT TIME TOO
        .. ie/ hence SDECRPC which aligns APPT and VISIT will have 'surprising'
        AFTER
        """
        if visitCreateBorAStart != None:
            visitCreate = visit["date_visit_created"] 
            visitStart = visit["visit_admit_datetime"]
            if not re.search(r'T', visitCreate):
                visitStart = visitStart.split("T")[0]
            ordr = "BEFORE" if visitCreate <= visitStart else "AFTER"
            visitCreateBorAStart[catag][ordr] += 1
                    
        # TODO: can reduce the following to comment of most frequent (ie/ move from
        # above comment with comparison!!! 
        
        # Important -- the following catag breakdown are placeholders to highlight main
        # catags and allow checks in the future -- effectively the code just returns
        # 'catag' now                   
                        
        """
        Pattern TODO: removed for now
        
        data_entry_clerk == created_by_user but apptN code messes up as 
        no separate slots for various other setters.
            
        # Appears that last changer updates 'entry clerk' ie/ original lost
        if not ("checkin" in apptN or "noshow_by_user" in apptN or "cancelled_by_user" in apptN or "walkin" in apptN) and apptN["data_entry_clerk"] != visit["created_by_user"]:
            raise Exception("Expected SCHEDULED creator to match in appt and visit if no checkin or other mods")        
        """
            
        """
        In general, there is apptN-apptL-visit matching when using SDECRPC
        (SPO 65986 of 68307 of SDECRPC do have apptL)
        
        ApptL there or not
        - NOT: in general (1661 vs 74), apptN cancelled, date before appt start then 
        none (deleted?)
        - THERE: in general (1517 vs 8), apptN noshow, then apptL still there ie/ 
        not removed
        - ... misc others but low # 650+ and could just be quirks -- can't see pattern
        
        TODO Pattern fill in:
        - aligning create times
          - time create apptN is effected by checkin, checkout
          - time apptL less so ie/ still matches visit create time but not all the time
        - why O:OCCASION OF SERVICE (LAB-X etc?) -- plays into CATSCAN etc X:ANCIL, O:OCC
        - consult_links: appt_request_type is to 123, explicit in apptL etc.
        - a/c for misc non apptL others ... lowish # but can't see pattern 
        (based on locn? See typer)
        """
        if re.match(r'SDECRPC', visit["option_used_to_create"]):
                
            return catag
        
        """
        BG: generally no apptL - just apptN; run next day after midnight.
        (SPO only 608 have apptL, 9493 not) 
        
        ? is what created the appointment? Unlike SDECRPC, don't know per se. Presumably
        this a/cs for exceptions on apptL.
        
        TODO: WHY BG needed - due to options NOT making visits? -- is its lack of
        apptLs <=> orphan apptL #'s ie/ different matching? appt date slightly out
        in apptLs in the option create.
        
        KEY CONFIG: only one created_by_user -- setup in option
        """        
        if re.match(r'SDAM BACKGROUND', visit["option_used_to_create"]):

            if not re.search(r'T0[0123]', visit["date_visit_created"]):
                raise Exception("Expected SDAM BG job to run in the three hours after midnight (the next day)")    
                                    
            return catag # doesn't say what made the appt -> encounter as diff time
                
        """
        Roll and Scroll (see users) ala CPRS with Manual Creation? 
                
        See CC visits created with checkout=starttime and 10 minute duration. 
        The appt and visit are created AFTER the appt time => manual process 
        (SUBCATEGORY?)
                
        Some have protocol: 'SDCO APPT CHECK OUT' in visit (ie/ triggered?)
        [an option 101 for 'checking out an appt']
                
        TODO: see CC appts created like this with 10 min duration, entered
        AFTER appt time, source is consult and ApptN only (not ApptL)
        """
        if re.match(r'SDAM APPT MGT', visit["option_used_to_create"]):
                                                                
            return catag
                
        """
        Few, no apptL
        """
        if re.match(r'SDM \[', visit["option_used_to_create"]):
                                                
            return catag
                
        """
        Few, all apptL
        """
        if re.match(r'SDMULTIBOOK', visit["option_used_to_create"]):    
                
            return catag
                
        """
        Mainly INP and dss of ADMIN but more nuance there.
        
        Few ApptL - 668 had none, 663 had DG ADMIT PATIENT
                
        TODO: in hosp care => appt may pre-exist but no checkin/out and match
        is made in an in hospital option earlier in the day of start.
        ... do more when do in hospital care more.
                           
                DG DISCHARGE PATIENT is one: straight apptN (no L) and 1 dep visit w/o
        a checkin/out or other stateful changes
        """
        if re.match(r'DG ', visit["option_used_to_create"]):
        
            if apptL:
                # 663 has DG ADMIT PATIENT but 668 doesn't
                print("** Don't expect SCHED DG ({}) to have ApptL".format(visit["option_used_to_create"]))         
                    
            return catag # actually a set of DG's possibly
                
        """
        PXCE ENCOUNTER ENTRY ...
        ... a series of options. Roll and Scroll. Says allow V related files 
        to be updated.
        
        Tiny - 2 apptL, 1 w/o 
                
        Note: dss probably ADMIN 
        """
        if re.match(r'PXCE ENCOUNTER', visit["option_used_to_create"]):         
                
            return catag
                
        return catag # SHOULD BREAK DOWN
        
    """
    Much less likely - where an app is used to (or roll and scroll) to fill in a
    PCE visit to match an appt
    """
    def matchPCEVisit(info, apptType, apptN, apptL):
                                     
        """
        NON SCHED (PCE) Encounter for Scheduled Appt
        
        Notes:
        - protocol rare (hardly ever) and PXCE SDAM UPDATE ENCOUNTER
        - encounter_type (all as CREDIT STOP out): P:PRIMARY, O:OCCASION, A:ANCILLARY, 
        """
        if not ("visitNS" in info and len(info["visitNS"]) == 1): 
            return "PCE_AMBIG_VISIT"
        visitNS = info["visitNS"][0]
                            
        """
        We see PXCE SDAM ... w/o encounter_type
        
        Interplay with service_category: X:ANCILL with O:OCC and plays into non count
        and MRI, CAT SCAN etc.
        """
        if "encounter_type" in visitNS and visitNS["encounter_type"] not in ["P:PRIMARY", "O:OCCASION OF SERVICE", "A:ANCILLARY"]:
            raise Exception("Expected Non SCHED Visit (NS) match to have encounter type P:PRIMARY or O:OCCASION OF SERVICE or A:ANCILLARY ")    
                    
        if "option_used_to_create" not in visitNS:
            catag = "PCE_NOOPTION"
            matchedDetails["apptTypeByCatag"][catag][apptType] += 1
            return catag  
            
        optionUsedToCreateLabel = visitNS["option_used_to_create"].split(" [")[0]
        catag  = "PCE_{}".format(optionUsedToCreateLabel)     
                
        # Know there is an APPTN
        matchedDetails["apptTypeByCatag"][catag][apptType] += 1 
            
        if matchedDetails2ByCatag != None:
            mtch = matchCreationDateTimes(apptN, apptL, visitNS)
            if mtch == None:
                apptVisitCreationMatch = "NONE"
            else:
                apptVisitCreationMatch = mtch[1]
            matchedDetails2ByCatag[catag][apptVisitCreationMatch] += 1
            
        if visitCreateBorAStart != None:
            visitCreate = visitNS["date_visit_created"] 
            visitStart = visitNS["visit_admit_datetime"]
            if not re.search(r'T', visitCreate):
                visitStart = visitStart.split("T")[0]
            ordr = "BEFORE" if visitCreate <= visitStart else "AFTER"
            visitCreateBorAStart[catag][ordr] += 1
            
        # Important -- the following catag breakdown are placeholders to highlight main
        # catags and allow checks in the future -- effectively the code just returns
        # 'catag' now                                      
        
        """
        Vast Majority of PCE matches
        
        Most lack apptL (11789 vs 1723; of none, 928 cancelled and 186 noshow)
        
        # Add many of the same as DSS
        """
        if re.match(r'OR CPRS GUI CHART', optionUsedToCreateLabel):
                       
            return catag
        
        """
        apptL usually there: 12 has; 12 cancelled => would be deleted; 1 missing
        
        ie/ if check for "cancelled_by_user" in apptN. Also shows that most dental
        don't come this route at all. Perhaps cancelling resets option in visit too?
        """
        if re.match(r'DENTV DSS DRM GUI', optionUsedToCreateLabel):
                                
            # alternative: "noshow_by_user" and note that time then of visit
            # create doesn't seem to match even the noshow recording ie/ seems
            # to be situation where VISIT setup manually by DSS GUI so comments
            # could be made on noshow!
            # ... ie/ not really a match per se. checkout could be the same ie/
            # commenting on a visit that may never have happened even if didn't
            # note a noshow.  
                    
            return catag
                
        # ED TRACKING SYSTEM - got RPCs (calling out as RPCs)
        if re.match(r'EDPF TRACKING SYSTEM', optionUsedToCreateLabel):                
                
            return catag
                
        """
        # EC GUI CONTEXT - Event Capture GUI option
        # ... note that checkout is present
        
        noApptL (11 to 1 ie/ only 1 has it)
        """
        if re.match(r'EC GUI CONTEXT', optionUsedToCreateLabel):
            
            if visitNS["encounter_type"] != "A:ANCILLARY":
                raise Exception("Expected scheduled visit from EC GUI to be Ancillary")           
            
            return catag
                
        """
        Never apptL
        """
        if re.match(r'DVBA CAPRI GUI', optionUsedToCreateLabel):               
            
            return catag
                
        """
        Never apptL
        """
        if re.match(r'DSIU MENTAL HEALTH SUITE', optionUsedToCreateLabel):              
                
            return catag
                
        return catag
                           
    if len(info) == 0:
        return "NONE_EMPTY"
                                      
    """
    Remove child PCEs, EH PCEs and PCEs if no appts
    """    
    def pruneNS(info): 
        # Cleanup visitNS - exclude E:EVENT, children
        if "visitNS" in info:
            visitNSR = [visitNS for visitNS in info["visitNS"] if not re.match(r'E:EVENT', visitNS["service_category"])]
            visitNSR = [visitNS for visitNS in visitNSR if "parent_visit_link" not in visitNS]
            if len(visitNSR):
                info["visitNS"] = visitNSR
            else:
                del info["visitNS"]
        return info
    info = pruneNS(info)
    
    # In case others in info for calcs ... using 'visit' and not ehVisit means EH won't count
    keys = set([key for key in info if re.match(r'(appt|visit)', key)])
    
    if len(keys) == 0:
        return "NONE_NOTMATCHABLE" # include EH only! TODO
    
    if keys == set(["visitNS"]):
        return "NONE_PCEONLY"
        
    if keys == set(["visit"]):
        return "NONE_SCHEDONLY"
        
    """
    No Match as missing either encs or appts to match
    ... may remove as should only work if both appt and enc
    """               
    if sum(1 for k in keys if re.match(r'visit', k)) == 0:
        if noneApptOnlyDetails != None:
            noneApptOnlyDetails["/".join(sorted(info))] += 1
        return "NONE_APPTONLY"
    
    apptTypes = []             
    apptN = oneAppt(info, "apptN")
    if apptN:
        apptTypes.append("apptN")
    apptL = oneAppt(info, "apptL") 
    if apptL:
        apptTypes.append("apptL")
    apptType = "/".join(apptTypes)
    
    if apptType == "" or sum(1 for k in keys if re.match(r'visit', k)) == 0:
        raise Exception("Expect to be matchable at this stage")
                
    if "visit" in info: # visit == visitS
        return matchScheduledVisit(info, apptType, apptN, apptL)
    return matchPCEVisit(info, apptType, apptN, apptL)

# ###################### Per 9000010 Enforce #####################

"""
Note: may move to a general enforcer category/ sub type

Quad of: PCE | SCHED, CHILD | TOP
where Child SCHED under either is credit stop qual and it is NOT an Encounter.

... using Typer red as it should

In order of importance: PCE/TOP, SCHEDULE/TOP and then (ignore qualifying SCHED-CHILD DSS) a small number of real children most of which are E:HIST.

TODO MORE: beyond called for below (reproduce visits from rawer data)
- BIG: DSS report and Locn -- see that visit dss (inc [SCHED] child qual) from locn DSS's
  ... will need to work dates there.
- outside_location and see where it appears (use hosp_locn and in_out breaks)
- If matched with cancelled or noshow appt, is there any form? ie/ would it be an auto-created that can't be deleted?
  ... part of ability to recreate VDM (visit, 409_84 etc) from MVDM of Encounter, Appt

NOTE: move to pure Encounter setup or WL as beyond Scheduled Encounters (SCHED/TOP)
"""
def enforce9000010Quad(stationNo):

    """
    - Basic is package (for x 4) and parent_package_label/#parent_visit_link (combo as can't work out package for some) 
    - hospital_location adds For DSS + Behavior and interplays with patient_status_in_out
    - type__003 allows VA or OTHER and outside_location stuff (bonus) 
    ie/ lot's of options for different combos
    """
    _all, sts = splitTypeDatas(stationNo, "9000010", reductionLabel="2019ToCutE", expectSubTypeProperties=["package", "#parent_visit_link", "parent_package_label", "hospital_location", "type__3", "patient_status_in_out"]) 
    
    """
    'Fake visit' child - just CREDIT STOP, acting as a stop qualifier
    ... this is NOT an encounter and should be excluded during encounter matching
    
    Other properties will be copies of its parent (identical loc_of_encounter, hospital_location, identical type__03, identical eligibility)
    
    Dates not enforced here but checked in manual walk
    - visit_admit_date_time same
    - date_last_modified == date_visit_created if full or == day of visit_created
      ... sometimes only day set for modified
    
    Key: why package set to SCHEDULING. Many seem to be caused by PCE parent/CPRS
    using 
    
    - option_used_to_create
      - for SCHED parent: SCHED options
      - for PCE parent: mainly CPRS
    - service_category: mainly X:ANCILL for both
    
    IMPORTANT: for PCE Parent, most have the optional protocol property set to SDAM PCE EVENT which must be triggers during create of CPRS (and others?) and it must set PACKAGE to SCHEDULING. ie/ fake package setting, almost a bug == quirk.
    """
    def enforceScheduleChild(st, parentPackageLabel):
    
        if singleValue(st, "encounter_type") != "C:CREDIT STOP":
            raise Exception("SCHILD: expect CREDIT STOP only ET")
            
        # TODO: is this 409_68?
        if singleValue(st, "dependent_entry_count") != "1":
            raise Exception("SCHILD: expect only 1 dependent entry")
                    
        # Key of fake setting of SCHEDULING as package - other package calls into a protocol of SCHEDULING
        if "protocol" in st and parentPackageLabel != "SCHEDULING":
            print("** INFO: protocol set for {} Sched Child under {} - {}".format(
                parentPackageLabel,
                reportAbsAndPercent(st["protocol"]["count"], st["_total"]),
                muBVC(st["protocol"]["byValueCount"])
            ))
                    
    """
    'Real' child and relatively simple/few patterns
    - under PCE: in-hospital, telephony and E:HIST (low ANCILL too?)
    - under SCHED: all E:HIST <------- only used for E:HIST under scheduled
        
    Note: very little used as E:HIST usually stands alone (PCE/TOP)
    """
    def enforcePCEChild(st, parentPackageLabel):
    
        if "C:CREDIT STOP" in st["encounter_type"]["byValueCount"]:
            raise Exception("PCHILD: CREDIT STOP not expected in ET")
            
        if not re.match(r'OR CPRS GUI CHART', singleValue(st, "option_used_to_create")):
            raise Exception("PCHILD: only expect option used of CPRS")
            
        # AND only one in 668 when parent is SCHED
        if "E:EVENT (HISTORICAL)" not in st["service_category"]["byValueCount"]:
            print("** WARNING: expected E:HIST service_category to be in PCE Child options")
        
    """
    - option_used_to_create: SCHED options (and DG) but NO HL7 etc 
      ... todo: small rogue CPRS
    - encounter_type: PRIMARY dominates and some OCCASION OF SERVICE (TODO more)
    - service_category: AMB, TELECOM, HOSP stuff (but some X:ANCILL too) ... note no E:HIST
    Note: very low use of 'protocol' so ignoring for now
    Note: very few outside_location but follow up on em
    """
    def enforceScheduleTop(st):

        if "C:CREDIT STOP" in st["encounter_type"]["byValueCount"]:
            raise Exception("S/-: CREDIT STOP not expected in ET")
            
        if "E:EVENT (HISTORICAL)" in st["service_category"]["byValueCount"]:
            raise Exception("S/-: don't expect service_category of E:HIST")
    
        if "outside_location" in st:
            raise Exception("S/-: don't expect outside locations for Scheduled (TOP) encounters")
    
        if set(st["encounter_type"]["byValueCount"]) != set(["P:PRIMARY", "O:OCCASION OF SERVICE"]):
            print("** WARNING: expect only Primary and OOS encounter type for Schedule Top")
                                                
    """
    - option_used_to_create: many but CPRS dominates (and then a big drop to LRVR ... and alot more) ie/ THIS IS WHERE variety kicks in for various apps
    - service_category: E:HIST, A:AMB (but some ANCILL too) ...
    - very low use of protocol so ignoring
    
    ... large variety and would need more breakdown itself but note a lot of E:HIST ie
    presumably many added in.
    
    Note: only one with full outside_location (very few) but follow up
    """
    def enforcePCETop(st):

        if "C:CREDIT STOP" in st["encounter_type"]["byValueCount"]:
            raise Exception("P/-: CREDIT STOP not expected in ET")
                            
    # Important: custom can't map all parent links to a parent for its package =>
    # link is superset and for processing we will exclude st's where there is a link
    # but no label.
    stsPP = combineSubTypes(sts, subTypePropsSubset=["package", "#parent_visit_link", "parent_package_label"])
    typeCounts = Counter()
    for st in stsPP:
        pkg = singleValue(st, "package")
        if "parent_visit_link" in st:
            # ignore st if parent pkg label missing when there is a link
            if "parent_package_label" not in st:
                continue 
            ppkg = singleValue(st, "parent_package_label")
            # Not real visit - lazy qual credit stop
            if re.search(r'SCHEDULING', pkg):
                enforceScheduleChild(st, ppkg)
                typeCounts["ChildSched" + ppkg[0]] = st["_total"]
            else:
                enforcePCEChild(st, ppkg)
                typeCounts["ChildPCE" + ppkg[0]] = st["_total"]
            continue
        if re.search(r'SCHEDULING', pkg):
            enforceScheduleTop(st)
            typeCounts["Sched"] = st["_total"]
            continue
        enforcePCETop(st)
        typeCounts["PCE"] = st["_total"]
        
    totalEncs = typeCounts["PCE"] + typeCounts["Sched"] + typeCounts["ChildPCES"] + typeCounts["ChildPCEP"]
    totalTopEncs = typeCounts["PCE"] + typeCounts["Sched"]
    print("## Summary Totals")
    print("... note doesn't count the visits who parent visit link couldn't be resolved")
    print("Total Encounters (not SCHED CHILD/DSS quals): {:,}".format(totalEncs))
    print("Total Encounters Top: {}".format(
        reportAbsAndPercent(totalTopEncs, totalEncs)
    ))
    print("Children as % of Top PCE: {}".format(
        reportAbsAndPercent(typeCounts["ChildPCEP"], typeCounts["PCE"])
    ))
    print("Children as % of Top Sched: {}".format(
        reportAbsAndPercent(typeCounts["ChildPCES"], typeCounts["Sched"])
    ))
    print("Qualifying Visits as % of Top PCE: {}".format(
        reportAbsAndPercent(typeCounts["ChildSchedP"], typeCounts["PCE"])
    ))
    print("Qualifying Visits as % of Top Sched: {}".format(
        reportAbsAndPercent(typeCounts["ChildSchedS"], typeCounts["Sched"])
    ))
    
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
    cutDateDT = datetime.strptime(cutDate.split("T")[0], "%Y-%m-%d")
    day90DateDT = cutDateDT - relativedelta(days=90)
    day90Date = datetime.strftime(day90DateDT, "%Y-%m-%d")
    print("For {}, cutdate {} is upTo and 90 day back, {}, is on or after".format(stationNo, cutDate, day90Date))
    onAndAfterDay = day90Date
    upToDay = cutDate
    
    # Here until whole report moves to typer and E
    allThere, details = checkDataPresent(stationNo, [

        {"fileType": "9000010", "check": "ALL"},
        {"fileType": "9000010_06", "check": "ALL"},
        {"fileType": "409_84", "check": "ALL"},
        {"fileType": "44_003", "check": "ALLRF"}

    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))
        
    # expectations of 9000010 enforced - TODO: change to merge into DataByDay's 9000010 
    # walk
    # enforce9000010Quad(stationNo)

    print("Gather | Load encounter data by day ...")
    visitsByDay, oldApptsByDay, newApptsByDay = gatherEncounterDataByDay(stationNo, onAndAfterDay, upToDay) 
    print("... loaded")
    print("Index encounter data (appts and visits) using location, patient, time ...")
    indexedDayTimeLocationPatient = indexEncounterDataByDateLocationPatient(stationNo, visitsByDay, oldApptsByDay, newApptsByDay)
    print("... indexed")
    
    webReportEncounters(stationNo, vistaName, indexedDayTimeLocationPatient, cutDate, onAndAfterDay, upToDay)

if __name__ == "__main__":
    main()
