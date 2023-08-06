#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from fmqlutils import VISTA_DATA_BASE_DIR
from fmqlutils.cacher.cacherUtils import FMQLReplyStore, FilteredResultIterator, metaOfVistA
from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent, muBVC
from fmqlutils.typer.reduceTypeUtils import splitTypeDatas, checkDataPresent, singleValue, combineSubTypes, muBVCOfSTProp, refsOfST

from fmqlreports.webReportUtils import TOP_MD_TEMPL, SITE_DIR_TEMPL, ensureWebReportLocations, keyStats, flattenFrequencyDistribution, roundFloat, reduce4, flattenPropValues 

"""
NEXT ON CONTENT (not on visuals):

- Filler breakdown ala Placer (no mixing for now)
- may only do completed ie/ nix discontinued/cancelled for now
- expose remote site service name for placers? ie/ to link em up?
    ifc_remote_service_name (pair with local services so see if 1 remote for > 1 local?)
- visn named (not just other visns)
- filler only patients (delay reg?) ... what?
- WILL START with COMPLETED vs OTHER for all CONSULTs and then just do COMPLETED in rest of report.
- locations:
    from/... location 44 (no pattern seen per see but do they all have similar workloads?)
    ordering_facility (is precise to clinic)

Portland vs Pug as big (can do TeleMental as part of filler breaks):
... TODO:
    - TeleMental highlight for POR from all four others?
    - setup BOI for Pharmacy the same
- portland has more filler only services
- portland has more placer consults
- pug has more filler only patients (because proportionately more FILLER IFCs ie/ few placers)
- their user proportions are remarkedly similar
- common placers (50% PUG, 76% POR)
- spec placers (20 PUG, 5 POR)
  - for PUG, POR dominates, for POR, BOISE dominates
  - PUG to POR is for TELEMENTAL/ TELE NEURO! WWW does this the most for POR too and SPO has it too [TELEMENTAL is POR's second highest FILLER after TELER ie/ POR specializes in this]
  - POR to BOI (smaller amount) is Pharmacy! [NEED TO SEE HOW MUCH PHARMACY and not just TELER that BOI does]
  - lessor spec placees differ:
    - CANCER TEAM from PUG (expected!) but not POR
  - few other VISNs ... no real pattern
  
FORMATTING IMPROVEMENTS <--- key for going forward
- 1. MOVE all calcs to "Data Prep/Frame Phase" ... also key stats (vs so many details) out
- 2. Consider plots separate ie/ can gen first and then write blurbs ... could cut down on data needed for actual text/paragraphs ... could do tables in this phase too ie/ table of DF vs Graph of DF ... plot from frames/table from frames
- 3. Better struct for md ... add section, add header, add paragraph, add table ...
"""

"""
Next week should be last on IFCs (for now): it'll add Puget and flesh out the findings for the other three VistAs (the intra and inter VISN aspects as well as the Filler as opposed to the Placers of IFCs).
            	+
Consider how to see range of test consults in B1930 [ie how to feed into that]
"""

""" 
TODO NEXT: for basic, do filler 
<----- goal is finish IFC in three pushes along with TeleR (into 2 of 3) ... deliver mid Aug
- travel: break to VISN out and shorten table
- filler:
  - VIRS, DISCHARGE FOLLOW UP, TRAVELLING VETERAN, OTHER (do simply for now to parallel)
  ... then try PUG ... and will flip FILLER/PLACER on Volume
- ? DISCHARGE follow up in FILLER -- what is it on the other end? as not obvious
  ... add note TODO now
- OTHER Q: if high # local -- is there a type of things ALWAYS DONE LOCALLY?
- go to DF (before doing services more break etc) ... typerDFPlay
- break out other services
  - one reason for so many placer services is 'embeds destination' => for any consult type, need where as well (any exs of 'type for x', 'type for y'? ex/ ENDOCRINOLOGY (visit and non visit) ... POR and SEATTLE ... UROLOGY is another example ... with many many. see if can unify using formal meta? ie disciplines, smaller is PODIATRY but still over three centers
  <------- break out other services
  - Break out VIRs 
  - IVR is "intra VistA Req" (sic) ... what is it text-wise (123 look)
- do graph per weekday as have it for each (more/new Py code below)
  - redo reduction for per month (or per day?) to get time series
  <------ chance to use per weekday <------- gets into time series too
- get into Filer side for PUG etc ie/ WANT MORE ON FILER SIDE (may be week three of IFC?)
- more on if Consult has images or not (teler beyond on image bearing consults?)
- user and patient discrepancies ... a/c for them <---- make top bars relevant
- OTHER DATA: TIU, Image, Appts - any connection to consults (IFCs) ie/ anything else made? [will tie to images and encounters] ... also want to see if any have img or doc assoc? [123 has TIU link! and assoc results ie/ PROCESSED IN TELEREADING (do this in there first ie/ any image etc ref from doc?]
- VISN 20 dynamic! ie/ lookup for any system
- clean TODO PASS 2 below

USE AS EXCUSE FOR:
> images and encounters (We are trying to determine the encounter relationships with the images at the VA. Hoping the data you have could help us. Could you provide how many images have encounter relationships for the IOC Sites with the Cache database you have?
Justin Cook; Botzum,Ed <Ed.Botzum@cerner.com>: Also, could we get a sense of what percent of the total that is. I.E. 72% of all images are associated with encounters.)
         ... work back from Docs and Visits? or? <---- put into a report
"""
    
"""
All Consults - IFC Consults with TeleRead as Subset

Bonus: enforces that all routing is to or from primary station #'s/4's and
not (sub) clinics. ie/ are VistA and not subfacility stations and ids.

Relies on: prepareMeta for 4 (may go native on it when move)

TODO PASS 2:
- 123_5:
  - and its stop code ... bring stop code in here
  - Service Remote name (is in 123_5 too) for IFC placer ... ie/ these are my PLACER five ... probably worth doing [true for more than TeleReading?]
- BIG: 2005, 8925 tie ins + PATIENT timing (longest time gap? ... need enhanceResource 123)
  ... may be through 2006.84/5 in 2005 itself or from 123_5 (indexed in VistA Imaging)
  ... but is the link "manual"? how link to document? (may need extra q)
- Locations (Clinics) ie/ precise ones
- More on Users and Roles and particularly default (programmed) users (fill accepted?)
- COMPLETE has result always as essential? Why not -- go back to mand/opt

TO WORK FILLER SEPARATION:
- PORTLAND
    DIABETIC TELERETINAL IMAGING (PORTLAND) IFC - MANN-GRANDSTAFF VAMC [689], ROSEBURG VA MEDICAL CENTER [372], ANCHORAGE VA MEDICAL CENTER [326], BOISE VA MEDICAL CENTER [279], JONATHAN M. WAINWRIGHT VAMC [108], WHITE CITY VA MEDICAL CENTER [35]
    ie/ see SPO, ROSE, ANC, BOISE, WWW, WHITE CITY
  [in simil now, would only get SPO and WWW]
  [NOTE: 60% of SPO go to PORT, others go to BOISE]
- PUGET 
    TELEDERMATOLOGY IFC (PUGET SOUND) - SOUTHERN ARIZONA VA HCS [2,886], ROSEBURG VA MEDICAL CENTER [2,641], PHOENIX VAMC [2,108], BILOXI VA MEDICAL CENTER [1,746], JONATHAN M. WAINWRIGHT VAMC [1,194], MANN-GRANDSTAFF VAMC [1,192], WHITE CITY VA MEDICAL CENTER [545], BOISE VA MEDICAL CENTER [284], VA HEARTLAND - WEST, VISN 15 [188], ANCHORAGE VA MEDICAL CENTER [55], PORTLAND VA MEDICAL CENTER [2]
    DIABETIC TELERETINAL IMAGING IFC (PUGET SOUND) - BOISE VA MEDICAL CENTER [3], MANN-GRANDSTAFF VAMC [1] (prob no longer used - and see in SPO ... do date stamp to remove?)
- [Missing BOISE end of 40% SPO EYE]

<----------- [1] come back here and to [2] 2005 rep for below (XRAY GROUP == group of any etc) before going back + [3] We're going to add the edge case to our simulation data: spec/proc to two readers and see that both see work for the other. Mike saw that the TeleReader displays the "unintended" in a particular way. More on that next week.
"""
def webReportIFC(stationNo, stationName, onAndAfterDay, upToDay, imageDir="Images", doDAD=False):

    type123YR1, sts123YR1All = splitTypeDatas(stationNo, "123", reductionLabel="YR1", expectSubTypeProperties=["cprs_status", "routing_facility", "to_service"])
    sts123YR1 = []
    for st in sts123YR1All:
        try:
            singleValue(st, "to_service")
        except:
            print("** No service for {} ({:,}) so skipping".format(st["_subTypeId"], st["_total"])) # one in POR
            continue
        sts123YR1.append(st)
                
    institByIEN = reduce4(stationNo)
            
    # WRF - with routing facility => IFC ie/ wrf <=> ifc
    stWRF = [st for st in sts123YR1 if "routing_facility" in st]
    placerServicesCheck = set()
    # If routing_facility => ifc_role and vica_versa
    if sum(1 for st in stWRF if "ifc_role" not in st and "routing_facility" in st) or sum(1 for st in sts123YR1 if "ifc_role" in st and "routing_facility" not in st):
        raise Exception("Where routing facility expect role and where role, expect routing facility")
    try: # either placer or filler within st gathered by service, routing_facility
        for st in stWRF:
            ifcRole = singleValue(st, "ifc_role")
            # bonus - record placer service for below
            if ifcRole == "P:PLACER":
                placerServicesCheck.add(singleValue(st, "to_service"))
    except:
        print(json.dumps(st, indent=4))
        raise Exception("> 1 ifc_role in routing_facility'ed ST. Unexpected")
    byServiceWRF = defaultdict(list)
    for st in stWRF: # note: for filler/local overlaps will only gather the filler st's
        service = singleValue(st, "to_service")
        byServiceWRF[service].append(st)

    # Service overlap with RF may happen due to filler being used in RF 
    # and WORF consults
    #
    # REVISIT: handles case where Placer service DOES not get reused in WORF
    # (enforced below) BUT Portland has DISCONTINUED case where this happens.
    # ... perhaps discontinued happens before IFC info added to a Consult? 
    # ... TODO: follow up as not counting this now!
    # 
    stWORF = [st for st in sts123YR1 if not ("routing_facility" in st or singleValue(st, "to_service") in placerServicesCheck)]  
    # Just for tracing -- the WORF Placers
    # ... PENDING is fine (but rare); DISCONTINUED seems to be too and then WCO has
    # an Active that has no further action beyond CPRS submit and just sits there.
    stWORFPlacer = [st for st in sts123YR1 if "routing_facility" not in st and singleValue(st, "to_service") in placerServicesCheck]
    if len(stWORFPlacer):
        for st in stWORFPlacer: # POR (DISCONTINUED), PUG (PENDING)
            stat = singleValue(st, "cprs_status")
            if not re.search(r'(ACTIVE|DISCONTINUED|PENDING)', stat):
                print(json.dumps(st, indent=4))
                raise Exception("If a Placer Service ST lacks Route Info, expect it to be (quickly?) discontinued or to be pending")
        print("** Warning: {:,} consults were routeless to Placer Services.".format(
            sum(st["_total"] for st in stWORFPlacer)
        ))
    worfTTL = sum(st["_total"] for st in stWORF)
    worfServices = set(singleValue(st, "to_service") for st in stWORF)
    worfUsers = set(user for st in stWORF for user in refsOfST(st, "200"))
    worfPatients = set(patient for st in stWORF for patient in refsOfST(st, "2"))
    
    # if WORF removed a placer, must a/c for that so only doing ALL here.
    stAll = stWORF + stWRF 
    allTTL = sum(st["_total"] for st in stAll)
    allServices = set(singleValue(st, "to_service") for st in stAll)
    allUsers = set()
    allPatients = set()
    for st in stAll:
        allUsers |= refsOfST(st, "200")
        allPatients |= refsOfST(st, "2")
                
    # Big: one role per service ie/ placer or filer in practice
    wrfTTL = 0
    wrfUsers = set()
    wrfPatients = set()
    placerTTL = 0
    placerServices = set()
    placerUsers = set()
    placerPatients = set()
    fillerTTL = 0
    fillerServices = set()
    fillerUsers = set()
    fillerPatients = set()
    for service in byServiceWRF:
        serviceUsers = set()
        servicePatients = set()
        serviceTTL = 0
        for st in byServiceWRF[service]:
            serviceTTL += st["_total"]
            serviceUsers |= refsOfST(st, "200")
            servicePatients |= refsOfST(st, "2")
            # Enforce that a routing facility is PRIMARY ie/ placed to or
            # filled from a first class, VistA naming station
            rf = singleValue(st, "routing_facility")
            rfIEN = re.search(r'4\-([^\]]+)', rf).group(1)
            if rfIEN not in institByIEN:
                raise Exception("RF is for 4 entry with no Station No")
            if not re.match(r'\d{3}$', institByIEN[rfIEN]["station_number"]):
                print("{} - {}".format(rf, institByIEN[rfIEN]["station_number"]))
                raise Exception("RF points to 4 with non primary station number")
        wrfTTL += serviceTTL
        wrfUsers |= serviceUsers
        wrfPatients |= servicePatients
        roles = set(role for st in byServiceWRF[service] for role in st["ifc_role"]["byValueCount"])
        if len(roles) != 1:
            raise Exception("Only expect one role for a service ie/ placer or filer")
        if list(roles)[0] == "F:FILLER":
            fillerServices.add(service)
            fillerUsers |= serviceUsers
            fillerPatients |= servicePatients
            fillerTTL += serviceTTL
        else:
            placerServices.add(service)
            placerUsers |= serviceUsers
            placerPatients |= servicePatients
            placerTTL += serviceTTL
            if len(set(rf for st in byServiceWRF[service] for rf in st["routing_facility"]["byValueCount"])) > 1:
                # ie/ Service --> Place Routed to if Placer. Filler may take from
                # multiple places.
                raise Exception("Expected one and only one RF for Placer Services")
                
    if placerServices != placerServicesCheck:
        print(len(placerServices))
        print(len(placerServicesCheck))
        raise Exception("Placers analyzed before to avoid WORF problems above - make sure in Sync") # TMP til tackle the DISCONTINUED
    if (placerTTL + fillerTTL + worfTTL) != allTTL:
        raise Exception("Totalling mistake - consult totals are exclusive")
    # ONLY for no overlap placer and WORF ... filler may be reused so there can be
    # overlap (ie/ remote VistA reuses a locally used consult service)
    if len(worfServices.intersection(placerServices)):
        print(worfServices.intersection(set(placerServices)))
        raise Exception("Expect Placer to be exclusive from Local Services")
    fillerAndLocalServices = worfServices.intersection(fillerServices)
    if len(allServices) != len(placerServices) + (len(fillerServices) - len(fillerAndLocalServices)) + len(worfServices): # overlap only counted in worfServices
        raise Exception("Expected overlap of filler and local to be easy to a/c for in allTotal") 
        
    # Tele SubSet definitively leveraging 2006_5849 USE!    
    type2006_5849YR1E, sts2006_5849YR1E = splitTypeDatas(stationNo, "2006_5849", reductionLabel="YR1E", expectSubTypeProperties=["reader_duz_at_acquisition_site", "image_index_for_specialty", "consult_service", "status", "#reading_start"])
    # DFNOTE: would be derived column (ie/ placer service type: TELER | TRAVEL | OTHER)
    telerAcServicesUsed = set(singleValue(st, "consult_service") for st in sts2006_5849YR1E)
    
    # DFNOTE: other to break further -- NEUROSURGERY X, (gather all) -- see if any subtyping done formally?
    # ... DOMICIALLARY REFERRAL (https://www.visn2.va.gov/VISN2/bh/inpatient.asp)
    # ... TELEDERMATOLOGY ... why not in TELE... top one WWW to PUG
    # ... granularity of subcategory advised ... how to group so can assign?
    # ... do as part of typer upgrade for categories as types => limited # (can
    # include PTERs!) ... want reduction (proportion?)
                
    # Cache data on Image
    meta = metaOfVistA(stationNo)
    
    dad = DumpAndAnalyzeData(stationNo, meta["cutDate"]) if doDAD else None
                        
    # ######################## MU Consults Per ####################
    
    plotData = {}
         
    mu = TOP_MD_TEMPL.format("{} IFCs".format(stationNo))
         
    mu += "# Interfacility Consults (IFCs) {} [{}]\n\n".format(meta["name"], stationNo)
    
    mu += "The following describes Consults, specifically Interfacility Consults (IFC), for the most recent year of _{}_ VistA cut on {}.\n\n".format(meta["name"], meta["cutDate"])  
    
    # Blurb
    blurb = """_Local consults_ - those ordered and fulfilled within this VistA - represent fully <span class='yellowIt'>{}</span> of the consults created in this VistA during the last full year for which data is available. """.format(
        reportAbsAndPercent(
            worfTTL,
            allTTL
        )
    )
    if placerTTL > fillerTTL:
        blurb += """Of the IFCs, there are more _Placer_ consults (\"placed\" elsewhere) <span class='yellowIt'>{}</span> than _Filler_ consults (fulfilled by this VistA for another) <span class='yellowIt'>{}</span>. In terms of IFCs, this is a __Placer VistA__ ...
    
""".format(
        reportAbsAndPercent(
            placerTTL,
            allTTL,
        ),
        reportAbsAndPercent(
            fillerTTL,
            allTTL
        )
    )
    else:
        blurb += """Of the IFCs, there are more _Filler_ consults (fulfilled by this VistA for another) <span class='yellowIt'>{}</span> than _Placer_ consults (\"placed\" elsewhere) <span class='yellowIt'>{}</span>. In terms of IFCs, this is a __Filler VistA__ ...
    
""".format(
        reportAbsAndPercent(
            fillerTTL,
            type123YR1["_total"]
        ),
        reportAbsAndPercent(
            placerTTL,
            type123YR1["_total"]
        )
    )
        
    # Plot: Consults Vs Services
    plotData["allConsults"] = {
        "title": "All Consults",
        "plotName": "ifcAllConsults",
        "plotMethod": "plotCategoryBH",
        "rows": ["consults"],
        "columns": ["local", "placer", "filler"],
        "data": [
            (
                worfTTL, 
                placerTTL, 
                fillerTTL
            ), # consults
        ]
    }
    plotRef = muPlotRef(
        plotData["allConsults"],
        imageDir
    )
    
    # MU - Blurb + Plot: Consults Vs Services
    mu += "{}\n\n{}\n\n".format(
        blurb,
        plotRef
    )
    
    blurb = """VistA Consults are ordered using consult types called _services_. Local consults use <span class='yellowIt'>{}</span> of the services used in this system, less than their proportion of consults. In other words, more services are employed for ordering IFCs than their numbers would suggest. Notice also that some services used for local consults - <span class='yellowIt'>{}</span> - are also used for IFC fulfillment. While services used for placement are exclusively for IFCs, the same is not true for fulfillment.
    
""".format(
        reportAbsAndPercent(
            len(worfServices),
            len(allServices)
        ),
        reportAbsAndPercent(
            len(fillerAndLocalServices),
            len(allServices)
        )
    )
    
    plotData["allServices"] = {
        "title": "All Consult Services",
        "plotName": "ifcAllServices",
        "plotMethod": "plotCategoryBH",
        "rows": ["services"],
        "columns": ["local only", "placer only", "filler only", "local+filler"],
        "data": [
            (
                len(worfServices) - len(fillerAndLocalServices), 
                len(placerServices), 
                len(fillerServices) - len(fillerAndLocalServices),
                len(fillerAndLocalServices)
            ) # services 
        ]           
    }
    plotRef = muPlotRef(
        plotData["allServices"],
        imageDir
    )
    
    mu += "{}\n\n{}\n\n".format(
        blurb,
        plotRef
    )
    
    # This one differs between Placer and Filler VistAs
    plotData["patientsAndUsers"] = {
        "title": "Users and Patients",
        "plotName": "ifcPatientsAndUsers",
        "plotMethod": "plotCategoryBH",
        "rows": ["users", "patients"],
        "columns": ["local only", "placer only", "filler only", "mixed"],
        "data": [
            (
                len(worfUsers - wrfUsers), 
                len(placerUsers - (worfUsers | fillerUsers)), 
                len(fillerUsers - (worfUsers | placerUsers)), 
                len(worfUsers.intersection(wrfUsers))
            ),
            (
                len(worfPatients - wrfPatients), 
                len(placerPatients - (worfPatients | fillerPatients)), 
                len(fillerPatients - (worfPatients | placerPatients)), 
                len(worfPatients.intersection(wrfPatients))
            )
        ]            
    }
    plotRef = muPlotRef(
        plotData["patientsAndUsers"],
        imageDir
    )
    blurb = """As seen below, most patients with consults only have local consults and the majority of the balance have both local consults and IFCs (\"mixed\").
    
"""
    if placerTTL > fillerTTL:
        blurb += """A small minority of patients have only fulfilled consults. With fulfilled consults, a patient's home record is typically elsewhere so you would expect to see more such patients and less mixed patients. The lower number of such \"remote-only patients\" should be examined further. 

As for users, a smaller proportion are only involved in local consults. While no users only fulfill consults submitted from elsewhere, a relatively large set only place consults elsewhere. This set of \"placer only users\" needs further examination.

"""
    else:
        blurb += """As a larger _Filler VistA_, a large number of its patients only have filled IFCs - the patient's home VistA is elsewhere. 
        
As for users, most tend to only local consults or to a mix of local and filled consults.

"""       

    mu += "{}\n\n{}\n\n".format(
        blurb,
        plotRef,
    )
    
    # ################################ Placer ######################
            
    # {"ANCHORAGE VA MEDICAL CENTER [363]", "BOISE VA MEDICAL CENTER [531]", "MANN-GRANDSTAFF VAMC [668]", "PORTLAND VA MEDICAL CENTER [648]", "ROSEBURG VA MEDICAL CENTER [653]", "SEATTLE VA MEDICAL CENTER [663]", "WHITE CITY VA MEDICAL CENTER [692]"}
    VISN20s = {"363": "ANC", "531": "BOI", "687": "WWW", "668": "SPO", "648": "POR", "653": "ROS", "663": "PUG", "692": "WCO"}
    placerServicesFacilities = Counter()
    telerTBL = MarkdownTable([":Placer Service", ":To Facility", "\#", "Status'"])
    placerServicesTeleR = set()
    travelTBL = MarkdownTable([":Placer Service", ":To Facility", "\#", "Status'"])
    placerServicesTravel = set()
    commonTBL = MarkdownTable([":Placer Service", ":To Facility", "\#", "Status'"])
    placerServicesCommon = set()
    spclzedTBL = MarkdownTable([":Placer Service", ":To Facility", "\#", "Status'"])
    placerServicesSpclzed = set()
    """
    Enforced here as grouping done here -- TODO: move grouping of placers up to data
    organization and not in mix of presentation.
    
    Of WRF's, only TELER has a local result (2 places for it - as a doc and in generic
    associated_results). But it is a disappointing reference (in SPO -- TODO: check
    more and wider by keeping all 8925 refs when typing) ala 
    
        >  "Please refer to Inter-facility Consult for results.\n\nA
utomatically generated note - signature not required.\n \n  Electronically Filed
: {DAY}\n                    by: {author-dictator}\n
 ",
    """
    def enforceOnlyTelerHasARnDoc(st):
        if "associated results" in st:
            raise Exception("WRF: TELER is only one expected to have local associated results")
        if "tiu_result_narrative" in st:
            raise Exception("WRF: TELER is only one expected to have local tiu - equivalent to associated resutls")
    for i, service in enumerate(sorted(placerServices, key=lambda x: sum(st["_total"] for st in byServiceWRF[x]), reverse=True), 1):
        tttl = sum(st["_total"] for st in byServiceWRF[service])
        rf = singleValue(byServiceWRF[service][0], "routing_facility")
        placerServicesFacilities[rf] += tttl
        if service in telerAcServicesUsed:
            groupLabel = "TELER"
            placerServicesTeleR.add(service)
            tblToUse = telerTBL
        elif re.search(r'(?i)travel', service):
            groupLabel = "TRAVEL"
            placerServicesTravel.add(service)
            tblToUse = travelTBL
        # follow-up is PUG, f/u is POR and these DISCHARGE FOLLOW UPs are only from big 
        # (POR/PUG) to small and not vica-versa
        elif re.search(r'(?i)(discharge f\/u|discharge follow\-up|virs |domiciliary|clinic f\/u|lodging)', service):
            groupLabel = "COMMON"
            placerServicesCommon.add(service)
            tblToUse = commonTBL
        else: 
            groupLabel = "SPECIALIZED"
            placerServicesSpclzed.add(service)
            tblToUse = spclzedTBL
        rfcntr = Counter()
        scntr = Counter()
        # Note: for Placer, only status varies (RF and by Defn, service is one)
        for st in byServiceWRF[service]:
            if groupLabel != "TELER":
                enforceOnlyTelerHasARnDoc(st)
            scntr[re.sub(r'100_01\-', '', singleValue(st, "cprs_status"))] += st["cprs_status"]["byValueCount"][singleValue(st, "cprs_status")]
            if dad:
                dad.dumpDocsOfST(groupLabel, st)
        serviceName = re.sub(r' +$', '', service.split(" [")[0]) 
        facMU = re.sub(r'4\-', '', rf)
        facMU = f'__{facMU}__' if re.search(r'\-(\d+)\]', rf).group(1) in VISN20s else facMU 
        tblToUse.addRow([
            # "__{}__".format(serviceName) if tttl/placerTTL > 0.1 else serviceName,
            serviceName,
            facMU,
            tttl,
            muBVC(scntr)
        ])
        
    if dad:
        dad.finish()
        
    mu += "## Placer\n\n"
    
    def summarizePlacerFacilities(services, groupLabel):
        serviceFacilityCount = defaultdict(lambda: Counter())
        facilityCount = Counter()
        ssttl = 0
        for service in services:
            sttl = sum(st["_total"] for st in byServiceWRF[service])
            ssttl += sttl
            facility = singleValue(byServiceWRF[service][0], "routing_facility")
            serviceFacilityCount[facility][service.split(" [")[0]] = sttl
            facilityCount[facility] += sttl
        cols = [":Facility", ":Service", "Consults"]
        if sum(1 for facility in serviceFacilityCount if len(serviceFacilityCount[facility]) > 1): 
            cols = [":Facility", "Consults", ":Services"]
        tbl = MarkdownTable(cols)
        visnValues = []
        otherTTL = 0
        for facility in sorted(facilityCount, key=lambda x: facilityCount[x], reverse=True):
            facSNO = re.search(r'\-(\d+)\]', facility).group(1)
            if facSNO in VISN20s:
                visnValues.append((facilityCount[facility], VISN20s[facSNO]))
            else:
                otherTTL += facilityCount[facility]
            facMU = re.sub(r'4\-', '', facility)
            # serviceNameMU = "__{}__".format(serviceName) if facilityCount[facility]/ssttl > 0.01 else serviceName
            facMU = f'__{facMU}__' if facSNO in VISN20s else facMU 
            if cols[1] == ":Service":
                row = [
                    facMU,
                    list(serviceFacilityCount[facility])[0],
                    reportAbsAndPercent(facilityCount[facility], ssttl)
                ]
            else:
                row = [
                    facMU,
                    reportAbsAndPercent(facilityCount[facility], ssttl),
                    muBVC(serviceFacilityCount[facility])
                ]
            tbl.addRow(row)
        sankeyVIZData = {
            "title": f'{groupLabel} Placers', 
            "plotName": f'ifc{re.sub(" ", "", groupLabel)}', 
            "plotMethod": "plotOutOtherSankey",
            "specs": {
                "outValues": visnValues,
                "toOtherTTL": otherTTL,
                "fromLabel": "SOURCE" 
            }
        }   
        plotData[f'placer{groupLabel}'] = sankeyVIZData    
        plotRef = muPlotRef(
            sankeyVIZData,
            imageDir
        )
        return tbl, set(facilityCount), ssttl, plotRef
        
    # Break into three.
    pbdmu = "" # placer breakdown mu
    tttlTeleR = tttlTravel = tttlCommon = tttlSpclzed = 0
    
    """
    TODO: may put these down with specialized ... ie/ after travel and common ie/
    part of specialized breakdowns and need to do others so IFCs covered in general.
    """
    if len(placerServicesTeleR):
        ftbl, facilities, tttlTeleR, plotRef = summarizePlacerFacilities(placerServicesTeleR, "TeleReading")
        pbdmu += "<span class='yellowIt'>{}</span> of the Placer Services are for __TeleReading__ to <span class='yellowIt'>{:,}</span> facilities ...\n\n".format(
            len(placerServicesTeleR), 
            len(facilities) 
        )
        pbdmu += plotRef + "\n\n"
        pbdmu += "Service by Service ...\n\n"
        pbdmu += telerTBL.md() + "\n\n"

    # For Travel, just use the facility table as 1-1 for most but PORT breaks that
    # ... also note broken from "common" as not just within VISN!
    # TODO: 
    # - consider change to have toVISNs ... ie/ show all except lowest numbers
    # including this VISN ... sunnier VISNs comment
    # - ... also travel coincides with summer/holidays?
    # - also who making these (docs or others?) 
    if len(placerServicesTravel):
        ftbl, facilities, tttlTravel, plotRef = summarizePlacerFacilities(placerServicesTravel, "Travel") 
        pbdmu += "<span class='yellowIt'>{}</span> of the Placer Services denote __travel__ to remote facilities and represent <span class='yellowIt'>{}</span> of placed consults. These prove to be the exception to the rule that a VistA places most IFCs within its own VISN.\n\n".format(
            len(placerServicesTravel), 
            reportPercent(tttlTravel, placerTTL)
        )
        pbdmu += plotRef + "\n\n"
        pbdmu += "By Facility ...\n\n"
        pbdmu += ftbl.md() + "\n\n"

    """
    A range of common "admin" (VIRS ...) and regular services (F/Us, lodging requests)
    sent between systems of any size, whether they are fillers or placers.
    
    Discharge F/U ; VIRS ; Domiciliary ; Clinic F/U; LODGING ... -i
    
    Ex/ VIRS Coordinator - IFC Spokane [53], Spokane Clinic F/U - IFC [48], Discharge F/U - Spokane IFC [6]
    
    The fillers (see below) of Smaller VistAs are dominated by such requests. For larger
    clinics, these common requests are proportionately less important.
    """
    if len(placerServicesCommon):
        ftbl, facilities, tttlCommon, plotRef = summarizePlacerFacilities(placerServicesCommon, "Common") 
        # All such consults stay within the VistA's VISN.
        # ADD: if Placer VistA -- Note that as the filler section below shows, services like these dominate the list of consults filled by a Placer VistA such as this one.
        pbdmu += """<span class='yellowIt'>{}</span> are \"Common\" Placer Services sent between both filler and placer VistAs. They represent a range of typical administrative (_\"VIRS\"_, _Lodging_, _Domiciliary_) and care requests to remote facilities (Follow ups). In this VistA, such requests represent <span class='yellowIt'>{}</span> of placed consults.
  
Note that equivalent services are filled by this VistA. Those are detailed in the _Filler Section_ below.      
        
""".format(
            len(placerServicesCommon), 
            reportPercent(tttlCommon, placerTTL)
        )
        pbdmu += plotRef + "\n\n"
        pbdmu += "By Facility ...\n\n"
        pbdmu += ftbl.md() + "\n\n"

    # TODO: Portland etc -- very very few compared to WWW ie/ here fillers take the lot
    # ... makes sense to group filler and placed specialized ... few if any for POR, all 
    # Fill!
    if len(placerServicesSpclzed):
        ftbl, facilities, tttlSpclzed, plotRef = summarizePlacerFacilities(placerServicesSpclzed, "Specialized")        
        # TODO: add later -- Placer VistA has many (relatively); a Filler has few - this is reversed in the Filler section    
        pbdmu += "The balance, <span class='yellowIt'>{}</span>, of the Placer Services to <span class='yellowIt'>{:,}</span> facilities, are mainly for specialized clinical services and represent <span class='yellowIt'>{}</span> of placed consults. Once again, the vast majority go to other VISN 20 facilities but the flow is mainly from smaller facilities to larger with the small placing with the large.\n\n".format(
            len(placerServicesSpclzed), 
            len(facilities), 
            reportPercent(tttlSpclzed, placerTTL)
        )
        pbdmu += plotRef + "\n\n"
        pbdmu += "By Facility ...\n\n"
        pbdmu += ftbl.md() + "\n\n"
    
    """
    TODO PLOT: move to a horizontal once more categories with % and totals and overall #
        teler -----------xx
        travel -xx
        common -------xx
        spec -------------------xxx 
    """
    plotData["placerConsultsNServices"] = {
        "title": "Placed Consults and Services",
        "plotName": "ifcConsultsNServicesPlaced",
        "plotMethod": "plotCategoryBH",
        "rows": ["consults", "services"],
        "columns": ["telereading", "travel", "common", "specialized"],
        "data": [
            (
                tttlTeleR,
                tttlTravel,
                tttlCommon,
                tttlSpclzed
            ),
            (
                len(placerServicesTeleR),
                len(placerServicesTravel),
                len(placerServicesCommon),
                len(placerServicesSpclzed)
            ), # placed services 
        ]           
    }
    plotRef = muPlotRef(
        plotData["placerConsultsNServices"],
        imageDir
    )
    
    # May break out 'VISN 20 CANCER CARE NAVIGATION TEAM IFC' -- another common, peer to
    # peer service (all do placer and filler)
    blurb = "There are <span class='yellowIt'>{:,}</span> __Placer Services__ - services that route/place consults __to__ <span class='yellowIt'>{:,}</span> other facilities. In VistA, a Placer Service identifies a specific remote (routing) facility which is always the main, default facility of a remote VistA. In this VistA, <span class='yellowIt'>{}</span> of the IFC Consults are \"Placed\" and the vast majority go __to other VISN 20 facilities__, facilities highlighted in bold in the tables below. Placer consults can be broken into four broad classes ...\n\n".format(
        len(placerServices), 
        len(placerServicesFacilities), 
        reportPercent(placerTTL, wrfTTL)
    )
    mu += "{}\n\n{}\n\n".format(
        blurb,
        plotRef
    )
    mu += pbdmu # placer breakdown mu
    
    # ############################# Filler ###########################
    
    """
    TODO: when break down
    - Break into TeleR/Travel (out of VISN!)/Common/Specialized
      ... or isn't TeleR just another form of specialized?
    - consider NOT counting ANY discontinued except at the top => ie/ in summary => smaller tables
    """

    tbl = MarkdownTable([":Filler Service", ":From Facilities", "\#", "Status'"])
    filledCntByPlacer = Counter()
    for i, service in enumerate(sorted(fillerServices, key=lambda x: sum(st["_total"] for st in byServiceWRF[x]), reverse=True), 1):
        tttl = sum(st["_total"] for st in byServiceWRF[service])
        rfcntr = Counter()
        scntr = Counter()
        for st in byServiceWRF[service]:
            placer = re.sub(r'4\-', '', singleValue(st, "routing_facility"))
            cnt = st["routing_facility"]["byValueCount"][singleValue(st, "routing_facility")]
            filledCntByPlacer[placer] += cnt
            rfcntr[placer] += cnt
            scntr[re.sub(r'100_01\-', '', singleValue(st, "cprs_status"))] += st["cprs_status"]["byValueCount"][singleValue(st, "cprs_status")]
        serviceName = re.sub(r' +$', '', service.split(" [")[0]) 
        # TODO: from facilities don't appear to be ordered
        tbl.addRow([
            serviceName,
            ", ".join(["{} [{:,}]".format(rf.split(" [")[0] if re.search(r'\[(\d+)\]', rf).group(1) not in VISN20s else f'__{rf.split(" [")[0]}__', rfcntr[rf]) for rf in rfcntr]),
            reportAbsAndPercent(tttl, fillerTTL),
            muBVC(scntr)
        ])
    
    mu += "## Filler\n\n"
    mu += "There are <span class='yellowIt'>{:,}</span> __Filler Services__ - services that accept/fill consults __from__ other facilities. In VistA, a single Filler Service may be employed by more than one remote facility and may also be used for purely local consults. In this VistA, <span class='yellowIt'>{}</span> of the IFC consults are \"filled\", mostly from VistAs in the same VISN ...\n\n".format(len(fillerServices), reportPercent(fillerTTL, wrfTTL))
    mu += tbl.md() + "\n\n"   
    
    # dump plotData for use
    plotDir = f'{VISTA_DATA_BASE_DIR}{stationNo}/TmpWorking/'
    print(f'Serializing vizData to {plotDir}')
    json.dump(plotData, open(f'{plotDir}plotDataIFC.json', "w"), indent=4)
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print(f'Serializing Report to {userSiteDir}')
    open(f'{userSiteDir}ifcs.md', "w").write(mu) 

# ##################### Plot Creation #########################
        
"""
TMP -- will move to webReportUtils when happy

Plot creation is separate --- may move into Visualize so common

ex/ plotDataFile = "plotDataIFC.json" ie/ plotDataFileSuffix="IFC"

TODO:
- ifcPlTravelVISNSankey (from Travel PlacersVISNSankey) -- .md change too
- all consult services categ ... -> ifcAllConsultsCategory 
- remove 0 ie/ NO OTHER!
- map SEA -> PUG, MAN -> SPO

"""

def makePlots(stationNo, plotDataFileSuffix):   

    import io
    import pandas as pd

    from visualize import Visualize
    imageDir = f'{VISTA_DATA_BASE_DIR}{stationNo}/ReportSite/Images'
    if not os.path.isdir(imageDir):
        os.mkdir(imageDir)
    viz = Visualize(imageDir)
    plotData =  json.load(open(f'{VISTA_DATA_BASE_DIR}{stationNo}/TmpWorking/plotData{plotDataFileSuffix}.json'))
    for plotDataName in plotData:
        plotDataInfo = plotData[plotDataName]
        print(f'Remaking {plotDataInfo["title"]}')
        method = getattr(viz, plotDataInfo["plotMethod"])
        if "rows" in plotDataInfo:
            arg = viz.makeDF(
                data=plotDataInfo["data"],
                columns=plotDataInfo["columns"],
                rows=plotDataInfo["rows"]
            )
        elif "specs" in plotDataInfo:
            arg = plotDataInfo["specs"]
        elif "dfcsv" in plotDataInfo:
            dfcsv = plotDataInfo["dfcsv"]
            df = pd.read_csv(
                io.StringIO("\n".join(dfcsv)),
                index_col=0, 
                parse_dates=True
            )
            arg = df
        else:
            raise Exception("Expect plot data for DF or as 'specs'")
        kargs = plotDataInfo.get("kargs", {})
        plotRef = method(arg, plotDataInfo["title"], plotDataInfo["plotName"], **kargs)
        print(f'\texpect reference to {plotRef} in report')
        
def muPlotRef(plotInfo, flushToDirectory):
    """
    # Want separate from visualize for now BUT possible break
    # as separate from Visualize naming impl
    
    ex/ ![ifcTravelVISNSankey](Images/ifcTravelVISNSankeyBGW.svg)
    """
    def svgPlotFile(plotName, plotMethodName, plotKArgs, flushToDirectory):
        """
        So don't have to make the plot but can know its name as making md
        Compatible with Visualize.__flushPlot's naming of SVG's
        """
        coreMethodName = re.sub("plot", "", plotMethodName)
        coreMethodNameU = coreMethodName[0].upper() + coreMethodName[1:]
        plotFilePrefix = f'{plotName}{coreMethodNameU}'
        if plotKArgs:
            if "start" in plotKArgs:
                plotFilePrefix += plotKArgs["start"]
            if "end" in plotKArgs:
                plotFilePrefix += "-{}".format(plotKArgs["end"])
        plotFile = f'{flushToDirectory}/{plotFilePrefix}BGW.svg'
        return plotFile, plotFilePrefix
    plotFile, plotFilePrefix = svgPlotFile(plotInfo["plotName"], plotInfo["plotMethod"], plotInfo["kargs"] if "kargs" in plotInfo else None, flushToDirectory)
    return "![{}]({})".format(plotFilePrefix, plotFile)
    
"""
TMP HERE - move to IFCRawDataAnalysis.py for raw data analysis of IFC pieces
... not part of .md flow per se

Want to see:
- [ ] consult report_text (vs doc)
  ... does filler get report_text off placer for its consult or its doc?
- [I] documents on Placer and Filler side

For Placer side first, dump documents of travel, telereading and common ... as
traverse st's, can get docs dumped. Different groups possible ex/ Travel
and TeleReading etc. and from Placer or Filler sides

So Far:
- for fraction of TELER with small number notes => will see a narrative ...

        "report_text": "Please refer to Inter-facility Consult for results.\n\nA
utomatically generated note - signature not required.\n \n  Electronically Filed
: {DAY}\n                    by: {author-dictator}\n
 ",

ie/ only TELER has document ref and then 

TODO:
- "reason_for_request" ... does this have initial VIRS etc text? [same remotely?] ie/ just a "text copy"?
"""
import shelve
from fmqlutils.cacher.cacherUtils import FMQLReplyStore, FilteredResultIterator
class DumpAndAnalyzeData:
    def __init__(self, stationNo, cutDate):
        self.__docsByGroupLabel = defaultdict(list)
        
        cutDateDT = datetime.strptime(cutDate.split("T")[0], "%Y-%m-%d")
        yrBeforeDateDT = cutDateDT - relativedelta(years=1)
        yrBeforeDate = datetime.strftime(yrBeforeDateDT, "%Y-%m-%d")
        onAndAfterDay = yrBeforeDate
        print(f'Calculated year before date is {yrBeforeDate}')
        
        tmpWorkingDir = f'{VISTA_DATA_BASE_DIR}{stationNo}/TmpWorking/'
        all8925ByIENDBFL = f'{tmpWorkingDir}all8925ByIEN{onAndAfterDay}.db'
        if os.path.isfile(all8925ByIENDBFL):
            print(f'8925 Types DB reduction in {all8925ByIENDBFL} done already')
            self.__8925ByIEN = shelve.open(all8925ByIENDBFL, flag='r')
            return
        dataLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/Data/'
        if not os.path.isfile(dataLocn + "8925-0.zip"):
            raise Exception("8925 not available for reduction")
        print(f'No 8925 Reduction for {onAndAfterDay} on so making')
        store = FMQLReplyStore(dataLocn)
        startAtReply = store.firstReplyFileOnOrAfterCreateDay("8925", "entry_date_time", onAndAfterDay)
        if startAtReply == "":
            raise Exception("Can't find a start at reply for {}".format("8925"))
        print("Starting with reply {}".format(startAtReply))
        resourceIter = FilteredResultIterator(dataLocn, "8925", startAtReply=startAtReply)
        all8925ByIEN = shelve.open(all8925ByIENDBFL)
        for i, resource in enumerate(resourceIter, 1):
            if i % 100000 == 0:
                print("Another 100K to {:,}".format(i))
            all8925ByIEN[str(resource["_id"].split("-")[1])] = resource
        all8925ByIEN.close()    
        self.__8925ByIEN = shelve.open(all8925ByIENDBFL, flag='r')

    """
    Ex/ dumpDocsOfST('placerTeleR', st)
    
    Only TELER has tiu_result_narrative (and associated_results)
    See limited # of TELER where doc has 'see elsewhere' text but where?
    - associated_results <=> tiu_result_narritive
    - remote_results == VPTR for 8925's remotely [ie/ doc not transferred]
    
    No Document Locally: VIRS, Travel etc - all have remote doc refs
    
    OTHER:
    - note the "from" 44's in sts ... need these for all service types or see it in patient_location
    """
    def dumpDocsOfST(self, groupLabel, st):
        if "tiu_result_narrative" not in st:
            return
        if "associated_results" not in st:
            raise Exception("Expected 'associated_results' if 'tiu_result_narrative'")
        if "byValueCount" not in st["tiu_result_narrative"]:
            return
        for ref in st["tiu_result_narrative"]["byValueCount"]:
            tiuIEN = str(re.search(r'\[8925-(\d+)\]', ref).group(1))
            self.__docsByGroupLabel[groupLabel].append(self.__8925ByIEN[tiuIEN])
            # print(json.dumps(st, indent=4))
        
    def finish(self):
        for groupLabel in self.__docsByGroupLabel:
            json.dump(self.__docsByGroupLabel[groupLabel], open(f'{groupLabel}.json', "w"), indent=4)
            print(f'Look in {groupLabel}.json for documents of {groupLabel}')
    
"""
> https://hackingandslacking.com/using-hierarchical-indexes-with-pandas-38057cf1d7e
... call multikeys a hierarchy ... order of it

[can even do on columns ie/ subtypeid and then can group cols (props) by another prop
=> of individual user if not in primary breakdown]

[pivottable needed]

Typer has multiple indexes (subtypeid) and then value ranges for all properties (ie/ not individual rows).

TODO: replicate in DF ...
- type123YR1, sts123YR1All = splitTypeDatas(stationNo, "123", reductionLabel="YR1", expectSubTypeProperties=["cprs_status", "routing_facility", "to_service"])
... comparing size and lookup effectiveness

And note, no need to flatten back out ...
- lastSeasonDF = nhlDF.xs(20182019, level='season')  # Group by last season

OTHER: encapsulate DF version in a typer class with setitem/getitem and static props
 X.prop etc. => can put behind as migrate?
"""
def typerToDFPlay(stationNo):

    """
    Walk one year 123 to DF
    """
    pass
        
# ################################# DRIVER #######################
               
# try argparse vs other cli
def main():
    """
    Specify only Station No if want .md and plot DATA made
    Specify 'PLOT' too if want to generate plots from pre-generated plot data
    """
    
    assert sys.version_info >= (3, 6)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO [PLOT]")

    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    if not os.path.isdir(userSiteDir):
        raise SystemExit("Expect User Site to already exist with its basic contents")
        
    if len(sys.argv) > 2:
        if sys.argv[2] == "PLOT":
            makePlots(stationNo, "IFC")
            return
        raise Exception("Only argument allowed is 'PLOT'")

    # <=> YR1 (fits with YR1E of 3.081)
    meta = metaOfVistA(stationNo)
    vistaName = "VistA" if "name" not in meta else meta["name"]
    cutDate = meta["cutDate"]
    cutDateDT = datetime.strptime(cutDate.split("T")[0], "%Y-%m-%d")
    yrBeforeDateDT = cutDateDT - relativedelta(years=1)
    yrBeforeDate = datetime.strftime(yrBeforeDateDT, "%Y-%m-%d")
    onAndAfterDay = yrBeforeDate
    upToDay = cutDate
    print("Reporting IFCs for YR1 (from {} to {})".format(onAndAfterDay, upToDay))

    webReportIFC(stationNo, meta.get("name", "VistA"), onAndAfterDay, upToDay)
        
if __name__ == "__main__":
    main()
