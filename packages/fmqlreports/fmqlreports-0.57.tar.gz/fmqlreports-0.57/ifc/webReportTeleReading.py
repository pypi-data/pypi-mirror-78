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
from fmqlutils.typer.reduceTypeUtils import splitTypeDatas, checkDataPresent, singleValue, combineSubTypes, muBVCOfSTProp

from fmqlreports.webReportUtils import TOP_MD_TEMPL, SITE_DIR_TEMPL, ensureWebReportLocations, keyStats, flattenFrequencyDistribution, roundFloat, reduce200, reduce4, flattenPropValues

"""
TODO FIRST:
- reader side report (incoming IFC ie/ filer) ... will tie in with documents <-- big for 663 and 648
- [2006.5831](http://localhost:9100/schema#2006_5831)
- may put queue trigger back in if the behavior is significant
- note if activity (ie/ if active in last year) is used in config section

Report TeleReading and the supporting IFCs, documents and images. Very particular IFC.
Cover [1] both Acquisition and Reader sides (including when they are the same VistA) and
[2] the configuration (files) used in all cases.

ADD BACK NOTE

The client __[Telereader Configurator](https://www.va.gov/vdl/documents/Clinical/Vista_Imaging_Sys/mag_telereader_configuration.pdf)__ sets up the following configuration files that determine how Telereading operates in a VistA. It configures both the __Acquisition Role__ and the __Reader Role__.

BETTER INTERP/CONFIG SETUPs (not even clear to me!):
- what's with Boise stuff? 
- remote service name vs local? ie/ one portland 'remote' "BETIC TELERETINAL IMAGING (PORTL" / 2006.5841 has many local 123.5 service types (where one each per local site like Yakama) 
     ie/ local, per instit service name [many] - global (note remote) service name
<--------- ie need to combine the configs tables ie/ local name (instit + local service name) ------> one service based remote name (per remote VistA as a whole)
- ex/ seems like 2006... Queue only uses more global sounding local service DIABETIC TELERETINAL IMAGING IFC (PORTLAND) for eye care and not all the individual per instit services supported in the system
  <------------ ie/ what does the queue use!!!
  BUT the little EYE of YAK TELE-EYE SCREENING (BOI) IFC is used ... ie/ 
- WANT TO SEE 'unused configs'!!!!!
- BIGGIE: split of 1/2/3 (local:local not IFC) ++ what's the no procedure about 
ie/ CONSISTENT configs to go with other stuff

> A (placer) consult created with the Service name (2005.5841->123.5) results in a (filler) consult with the service name Remote Name in the Remote Reading Site ... 2005.5841 also decides how entry is triggered. 

============================= TODO: Content =====================

TODO: [1] fin ac [2] finish Reader Side (align consults) + [3] HL7 vs RPC + [4] neaten/finish final rep form <------ gives new template
- the biggie is FILLER: extrapolate a list as if there is a config file for "filler reading services" ... => 
- need PUG [only internal]
- combine table better ie/ see 2006.5841 ac service -- bring in its Remote Reading Site ie/ show combination.
- RPCs/HL7 attribution and code paths (static report/table) ... see below ie/ BEYOND what data shows unless there is HL7 logs?
  - telereader use lower in SPO (only Eye) but COS consistent with all remote using it!
  - MAY REWORK USER TABLE into 'roles' based on transitions AND not the one summary in queue (who is a reader? responsible? no? ...)
- [FINAL FORM] <-------------- when done beyond freps mv, note IFC in general context + TYPER use rework as neater (not lot's of random types.) MAY DO TYPER explicitly within here ie/ don't run through front end => no need to do custom there ... build in reframe to report.

TODO WORK comments RPCs and HL7 attribution (see code etc comments in reportIFC)
  > Clinical Capture provides the capability to acquire dermatology images that can be
remotely read using Inter-Facility Consults (IFCs) and TeleReader. To support this
capability, a new association has been added to Clinical Capture called “TeleReader
Consult”. JPEG and TIFF dermatology images saved to VistA using this new association
will be converted into DICOM format before storing in VistA Imaging. The images will
then be viewable in Clinical Display.
ie/ dermatology special [and there are a bunch of them]
   ---
   > - TIU Note File – this is used to automatically create a TIU note for a set of images
when the consult request is remotely completed via an Inter-facility Consult.
ie/ TIU creation from remote IFC completion.
   > MAG3 TELEREADER READ/UNRD ADD - adds a consult and image pointers to the
UNREAD/READ LIST file (#2006.5849) and DICOM GMRC TEMP LIST file
(#2006.5839)
<------------ important: 'assoociation' of clinical capture -- find

"""

def webReportTeleReading(stationNo, stationName, onAndAfterDay, upToDay):

    allThere, details = checkDataPresent(stationNo, [

        # [ACQ] T. Q (See comment in ACQ below)
        {"fileType": "2006_5849", "check": "YR1E"},              
        # [ACQ] T. ACQUISITION SERVICE, a 'bridge' configuration file between world 
        # of 123's and VA-wide telereading. Also determines when Q entry made from 123
        # and document type used for result
        {"fileType": "2006_5841",  "check": "ALL"}, 
        
        # [READ] T. ACQUISITION SITE
        {"fileType": "2006_5842", "check": "ALL"}, 
        # [READ] T. READER 
        {"fileType": "2006_5843", "check": "ALL"}, 
        
        # REQUEST/CONSULTATION for T. Q YR1E - complication of local-only Telereading
        {"fileType": "123", "check": "YR1"}, 
        # REQUEST SERVICES (local terms mapped to VA-wide in 2006_5841)
        {"fileType": "123_5", "check": "ALL"},

        # For User Identification
        # 200 - reduce200 will enforce need for 200
        {"fileType": "3_081", "check": "YR1E"}
        
    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    mu = TOP_MD_TEMPL.format("{} TeleReader".format(stationNo))

    mu += """# Telereader
   
The following describes _Telereading_ in VistA _{}_ [{}]. VistA can both acquire studies (\"Acquisition\") and read studies (\"Reading\"). Where one VistA acquires a study and another reads that study, Telereading builds upon VistA's general-purpose Inter-facility Consult (IFC) feature.

    
""".format(stationName, stationNo)

    mu += webReportAcquisition(stationNo, stationName, onAndAfterDay, upToDay)
    
    mu += webReportReading(stationNo, stationName, onAndAfterDay, upToDay)
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print("Serializing Report to {}".format(userSiteDir))
    open(userSiteDir + "telereader.md", "w").write(mu)
    
# ######################## Acquisition ######################
    
def webReportAcquisition(stationNo, stationName, onAndAfterDay, upToDay):
    mu = "## Acquisition\n\n" 
    mu += webReportAcquisitionConfiguration(stationNo, stationName)
    mu += webReportAcquisitionActivity(stationNo, onAndAfterDay, upToDay)
    return mu
    
"""
Acquisition Service is effectively a combination of information from 123.5 and 2006_5841

TODO:
- consider a synthesized name of SPEC PROC ABBREVS (SNO AC/SNO READ VISTA)
"""
def webReportAcquisitionConfiguration(stationNo, stationName):

    dataLocn = "{}{}/Data/".format(VISTA_DATA_BASE_DIR, stationNo)   
    ifcServiceIndex = dict((cs["_id"], cs) for cs in FilteredResultIterator(dataLocn, "123_5") if "ifc_routing_site" in cs)
    institByIEN = reduce4(stationNo)
    snoByNationalInstitId = dict(("4-" + ien, institByIEN[ien]["station_number"]) for ien in institByIEN if "isNational" in institByIEN[ien] and "station_number" in institByIEN[ien])
    
    asResourceIter = FilteredResultIterator(dataLocn, "2006_5841")
    serviceCount = 0
    byRoutingSite = defaultdict(list)
    locals = []
    for resource in asResourceIter:
        serviceCount += 1
        row = [
            "__{}__".format(resource["name"]["label"]),
            "{} [{}]".format( # 2006.5841
                re.sub(r'( VAMC| VA CLINIC| CBOC| VA MEDICAL CENTER)', '', resource["acquisition_site"]["label"]),
                snoByNationalInstitId[resource["acquisition_site"]["id"]]
            ),
            "{} [{}]".format( # 2006.5841
                resource["specialty_index"]["label"],
                resource["specialty_index"]["id"].split("-")[1]
            ),
            "{} [{}]".format( # 2006.5841
                resource["procedure_index"]["label"],
                resource["procedure_index"]["id"].split("-")[1]
            )
        ]
        tiuNoteFile = resource["tiu_note_file"]["label"] if "tiu_note_file" in resource else ""
        row.append(tiuNoteFile)
        # If not just LOCAL
        if resource["name"]["id"] in ifcServiceIndex: # 123.5
            ifcService = ifcServiceIndex[resource["name"]["id"]]
            row.append(ifcService["ifc_remote_name"])
            routingSite = ifcService["ifc_routing_site"]
            remoteSiteRef = "{} [{}]".format(
                routingSite["label"],
                snoByNationalInstitId[routingSite["id"]]
            )
            byRoutingSite[remoteSiteRef].append(row)
            # NOT DOING ASSOCIATED STOP CODE as many don't have it
        else:
            locals.append(row)
        # IGNORING FOR NOW (as doesn't effect quantifying per se
        # trigger = resource["unread_list_creation_trigger"]

    mu = "### Configuration\n\n"
    mu += "This VistA has <span class='countHigh'>{:,}</span> consult services for Telereading by <span class='countHigh'>{:,}</span> remote VistAs.{}\n\n".format(
        serviceCount,
        len(byRoutingSite),
        " In addition, <span class='countHigh'>{:,}</span> services are for local reading.".format(len(locals)) if len(locals) else ""
    )
    basicCols = [
            ":Service",
            ":Acquisition Site",
            ":Specialty",
            ":Procedure",
            ":Acquisition Note"
    ]
    for rs in sorted(byRoutingSite):
        # "All map to one service in Boise
        acSites = set(row[1] for row in byRoutingSite[rs])
        remoteServices = set(row[-1] for row in byRoutingSite[rs])
        cols = basicCols[:]
        if len(remoteServices) > 1:
            cols.append(":Remote Service")
        tbl = MarkdownTable(cols)
        for row in sorted(byRoutingSite[rs], key=lambda x: x[1]): # group by ac site
            if len(remoteServices) == 1:
                row.pop()
            tbl.addRow(row)
        if len(acSites) > 1:
            mu += "__{}__ receives <span class='countHigh'>{:,}</span> types of consult service from <span class='countHigh'>{:,}</span> acquisition sites{} ...\n\n".format(
                rs, 
                len(byRoutingSite[rs]), 
                len(acSites),
                ", all sent to one remote service _{}_".format(list(remoteServices)[0]) if len(remoteServices) == 1 else "" 
            )
        else:
            mu += "__{}__ receives <span class='countHigh'>{:,}</span> services ...\n\n".format(rs, len(byRoutingSite[rs]))
        mu += tbl.md() + "\n\n"
    if len(locals):
        tbl = MarkdownTable(basicCols)
        mu += "The <span class='countHigh'>{:,}</span> locally read (non interfacility consult) services are ...\n\n".format(len(locals))
        for row in sorted(locals, key=lambda x: x[0]):
            tbl.addRow(row)
        mu += tbl.md() + "\n\n"
    
    return mu

"""
Acquisition Activity - local acquisition and either remote or local telereading

Different breaks of Enhanced 2006_5849 (with a little addition from 3.081's
app breakdown)

TODO:
- more on time between consult creation (audit etc) and queue times ie/ want to get to ONE audit trail for simulation) <--------- ********
- more on local telereading (ie/ no ifc consult) <------ not in scope but ... would expect
Reading config user to be active one! [IE/ ENFORCE HERE]

The key file is Telereader List (TELEREADER READ/UNREAD LIST (2006.5849)) pre-enhanced by Placer 123's audit trail and service assertion. 

It summarized from the following perspectives and these summaries are reported on:
1. By Specialty (image_index_for_specialty)
2. By (Consult) Service (E added from 123)
3. By Status
4. By Reader (in Acquisition System's 200)

In addition, there should be a broad summary of consults as key consult props embedded
in the queue element by E.
a. consult_service_tiu_note_type (itself put into 123 from ...): would expect one as one per Consult Service
b. consult_audit_trail: into transitions mu so one value of all transitions
c. is_consult_ifc (not there if consult is local): rem E enforces that consult is 
always PLACER if ifc
e. for service: tiu note type (ie/ one or none)

number_of_images -- print it
"""
def webReportAcquisitionActivity(stationNo, onAndAfterDay, upToDay):

    # 123 and 2006_5849 reductions
    type123YR1, sts123YR1 = splitTypeDatas(stationNo, "123", reductionLabel="YR1", )
    type2006_5849YR1E, sts2006_5849YR1E = splitTypeDatas(stationNo, "2006_5849", reductionLabel="YR1E", expectSubTypeProperties=["reader_duz_at_acquisition_site", "image_index_for_specialty", "consult_service", "status", "#reading_start"])
    
    # Group per User (and don't want the one possible, no user specified)
    st2006_5849Us = [st for st in combineSubTypes(sts2006_5849YR1E, ["reader_duz_at_acquisition_site"], forceCountProps=["consult_service"]) if "reader_duz_at_acquisition_site" in st]
    readersPerAcVistA = set(singleValue(st, "reader_duz_at_acquisition_site") for st in st2006_5849Us) 
    
    # ? users == just name. What if overlap?                
    def sosOfUsers(stationNo, users):
        print("Loading 3.081 YR1E ...")
        type3_081, st3_081s = splitTypeDatas(stationNo, "3_081", reductionLabel="YR1E")    
        st3_081Us = combineSubTypes(st3_081s, ["user"], forceCountProps=["ipv4_address", "remote_station_id", "remote_user_ien", "duration"])
        st3_081ByUserRef = dict((singleValue(st, "user"), st) for st in st3_081Us if singleValue(st, "user") in readersPerAcVistA)
        print("\tLoaded and processed for {:,}".format(len(users)))
        return st3_081ByUserRef
    st3_081ByUserRef = sosOfUsers(stationNo, readersPerAcVistA) 
    
    # ? readers == just name. What if overlap?
    def autoCreatedReaders(readers):
        print("Loading user information (200 Reduction) ...")
        userInfoByUserRef = reduce200(stationNo, coreOnly=True)   
        # V1.1 and V10 compatible as creator only shows if != 200-0 for v1.1
        readersAutoCreated = set(userRef for userRef in userInfoByUserRef if userRef in readers and "creator" not in userInfoByUserRef[userRef])
        print("\tLoaded and processed {:,} users, {:,} readers to see {:,} are auto created".format(len(userInfoByUserRef), len(readers), len(readersAutoCreated)))
        return readersAutoCreated
    readersAutoCreated = autoCreatedReaders(readersPerAcVistA)
                            
    mu = "### Activity\n\n"             

    """
    Overall summary uses:
    - 123 YR1 Red for total consults
    - 2006_5849 YR1E Red for total queue entries: all have unique consult and
    with E embedding consult properties, can describe the consult of queue entries
    from the queue reduction

    # Placer Total Consults if want to use these.
        reportAbsAndPercent(
            type123YR1["ifc_role"]["byValueCount"]["P:Placer"],
            type123YR1["_total"]
        ) if "ifc_role" in type2006_5849YR1E else 0,
    """
    consultIFCCount = type2006_5849YR1E["is_consult_ifc"]["count"] if "is_consult_ifc" in type2006_5849YR1E else 0
    if consultIFCCount < type2006_5849YR1E["_total"]:
        mixedOrNotMU = "<span class='countHigh'>{}</span> of these are interfacility consults (IFCs), where another facility performs the consult while the balance, <span class='countHigh'>{}</span>, are performed locally".format(
            reportAbsAndPercent(
                consultIFCCount, 
                type2006_5849YR1E["_total"]
            ),
            reportAbsAndPercent(
                type2006_5849YR1E["_total"] - consultIFCCount, 
                type2006_5849YR1E["_total"]
            )
        )
    else:
        mixedOrNotMU = "all of which are interfacility consults (IFCs) - no locally acquired studies are read locally"
    mu += """An _Acquisition site_ imports images and submits them for telereading \"consults\". These are tracked in _TELEREADER READ/UNREAD LIST (2006.5849) [\"Acquisition List\"]_. In this site, there are <span class='countHigh'>{:,}</span> total consults between {} and {}. Of these, <span class='countHigh'>{}</span> are in the Acquisition List, {}.
    
""".format(
        type123YR1["_total"],
        onAndAfterDay, 
        upToDay,
        # count of queue consults == count of queue entries as 1-1
        reportAbsAndPercent(type2006_5849YR1E["_total"], type123YR1["_total"]), 
        mixedOrNotMU
    ) 

    """
    Specialty, Service and Status
    """
    mu += """The entries have <span class='countHigh'>{:,}</span> states, {} and <span class='countHigh'>{:,}</span> specialties, {} covering <span class='countHigh'>{:,}</span> services.
    
""".format(
        len(type2006_5849YR1E["status"]["byValueCount"]), 
        muBVC(type2006_5849YR1E["status"]["byValueCount"]), 
        len(type2006_5849YR1E["image_index_for_specialty"]["byValueCount"]), 
        muBVC(type2006_5849YR1E["image_index_for_specialty"]["byValueCount"]), 
        len(type2006_5849YR1E["consult_service"]["byValueCount"])
    )
    st2006_5849SpecialtyNService = combineSubTypes(sts2006_5849YR1E, ["image_index_for_specialty", "consult_service"], forceCountProps=["reader_duz_at_acquisition_site"]) 
    ifcServiceByIEN = reduce123_5ForIFC(stationNo)
    specialitiesTotals = Counter()
    stsBySpecialty = defaultdict(list)
    for st in st2006_5849SpecialtyNService:
        specialty = singleValue(st, "image_index_for_specialty")
        stsBySpecialty[specialty].append(st)
    for specialty in sorted(stsBySpecialty, key=lambda x: sum(st["_total"] for st in stsBySpecialty[x]), reverse=True):
        mu += "Specialty _{}_ ...\n\n".format(re.split(r' +\[', specialty)[0])
        tbl = MarkdownTable([":Service", ":Remote Reader", "Count", ":Status"])
        for stService in sorted(stsBySpecialty[specialty], key=lambda x: x["_total"], reverse=True):
            service = singleValue(stService, "consult_service")
            serviceIEN = re.search(r'\-(\d+)', service).group(1)
            name = re.split(r' +\[', service)[0]
            ifcRoutingSiteMU = re.sub(r'4\-', '', ifcServiceByIEN[serviceIEN]["ifc_routing_site"]) if serviceIEN in ifcServiceByIEN and "ifc_routing_site" in ifcServiceByIEN[serviceIEN] else ""
            tbl.addRow([
                "__{}__".format(name) if ifcRoutingSiteMU else name,
                ifcRoutingSiteMU,
                stService["_total"], 
                muBVC(stService["status"]["byValueCount"])
            ])
        mu += tbl.md() + "\n\n"
    
    """
    Status of the Queue Entries - show transition combinations for the status'. Comes
    from E on Queue [1] fabricating a consult_audit_trail_transitions property for the
    reduction and [2] having status in the breakdown.
    """
    st2006_5849Status = combineSubTypes(sts2006_5849YR1E, ["status"], forceCountProps=["consult_audit_trail_transitions"]) 
    st2006_5849ByStatus = defaultdict(list)
    for st in st2006_5849Status:
        status = singleValue(st, "status")
        st2006_5849ByStatus[status].append(st)
    # , ":Added Comments"
    tbl = MarkdownTable([":Status", ":Transitions", "Count", ":Reading Site"], includeNo=False)
    currentStatus = ""
    for status in ["W:Waiting", "U:Unread", "C:Cancelled", "L:Locked", "D:Deleted", "R:Read"]:
        if status not in st2006_5849ByStatus:
            continue
        for st in sorted(st2006_5849ByStatus[status], key=lambda x: x["_total"], reverse=True):
            # POR has this for DELETED - TODO, examine
            if "consult_audit_trail_transitions" not in st:
                continue
            for trans in sorted(st["consult_audit_trail_transitions"]["byValueCount"], key=lambda x: st["consult_audit_trail_transitions"]["byValueCount"][x], reverse=True):
                if status != currentStatus:
                    currentStatus = status
                    row = ["__{}__".format(status.split(":")[1])]
                else:
                    row = [""]
                row.extend([trans, st["consult_audit_trail_transitions"]["byValueCount"][trans]])
                if "reader_site" in st:
                    row.append(muBVC(st["reader_site"]["byValueCount"]))
                else:
                    row.append("")
                """
                ADDED COMMENT isn't in transitions - local or remote of it is
                in consult_audit_trail_comment_{} counters of local or 
                remote comments added.
                
                Would need to add 'consult_audit_trail_transitions' to typer
                and then total LOCAL or REMOTEs across a transition typer ie/
                     consult_audit_trail_comment_local - 4: 2, 5:7 ... etc  
                """
                tbl.addRow(row)
    mu += """List entries go through one or more transitions, starting with a _CPRS RELEASED ORDER_ when the entry is first added right after its consult is created. The most common sequence moves on to _RECEIVED_ (reader site received the consult) through _COMPLETE UPDATE_ (reader site has read the image and created a document) and ends with _NEW NOTE ADDED_ (an equivalent document was created in the \"local\"/acquisition site). 
    
The following shows transitions by Acquisition List entry status. The last column shows how _ADDED COMMENT_ actions accompany a specific transition. These actions may be local or remote and allow users to annotate a consult. Transitions in __bold__ represent remote reader activity ...

"""
    mu += tbl.md() + "\n\n"
    
    """
    Per Reader (User) summaries: st2006_5849Us - will distinguish remote and local 
    ... on the acquisition side ie for the 'Acquisition List'
    
    TODO: ala older report
    - network_name (so portable for common view)
    - WHERE IS THE REMOTE ID FOR ALL OF THEM!!!!
    - consider LOA as well as app count to be sure (need break!)
    
    Note: nixed roles (ie/ enterer remote or local) and remote or local tiu refs
    per user. Will return when work specific document types.
    """
    tbl = MarkdownTable([":Reader Name", "Spec(s)", "\#", ":Remote Reader", ":Applications (SOs)"])
    noLocal = 0
    for i, st in enumerate(sorted(st2006_5849Us, key=lambda x: x["_total"], reverse=True), 1):
        userRef = singleValue(st, "reader_duz_at_acquisition_site")
        readerIENPerAcVistA = re.search(r'\-(\d+)', userRef).group(1)
        appsMU = ""     
        if userRef in st3_081ByUserRef:
            st3_081 = st3_081ByUserRef[userRef]
            byAppCount = Counter() if "remote_app" not in st3_081 else st3_081["remote_app"]["byValueCount"]
            # UNSET's probably CPRS
            if st3_081["_total"] > sum(byAppCount[app] for app in byAppCount):
                byAppCount["UNSET"] = st3_081["_total"] - sum(byAppCount[app] for app in byAppCount)   
            appsMU = muBVC(byAppCount)
            for f, t in [("VISTA IMAGING TELEREADER", "__TELEREADER__"), ("MEDICAL DOMAIN WEB SERVICES", "JLV"), ("VISTAWEB-PROD", "WEB"), ("VISTA IMAGING", "IMG"), ("DISPLAY", "DISP"), ("UNSET", "_UNSET_")]:
                appsMU = re.sub(f, t, appsMU)
                
        # Note: can differ from mandatory "full_name_of_reader" (which is last reader?)
        # ... must note these going forward; readers_initials agrees with         
        # full_name_of_reader
        nameMU = "{} [{}]".format(re.sub(r'\,', ', ', userRef.split(" [")[0]), readerIENPerAcVistA)
        # Local iff one reader_duz_at_reading_site AND same as IEN at this 
        # acquisition site. Very minority thing to have (why? - see audit)
        isLocalReader = True if ("reader_duz_at_reading_site" in st and len(st["reader_duz_at_reading_site"]["byValueCount"]) == 1 and readerIENPerAcVistA == singleValue(st, "reader_duz_at_reading_site")) else False
        if isLocalReader:
            noLocal += 1
            remoteMU = ""
            if "is_consult_ifc" in st:
                print("** Don't expect Local Readers to have IFC Consults for their TeleReading")
        else:
            nameMU = "__{}__".format(nameMU)
            remoteMU = re.sub(r'VA MEDICAL CENTER', 'VAMC', muBVC(st["reader_site"]["byValueCount"], forceShowCount=False)) if "reader_site" in st else ""
            if "reader_duz_at_reading_site" in st:
                if len(st["reader_duz_at_reading_site"]["byValueCount"]) != 1:
                    remoteMU += " [AMBIG>1]"
                else:
                    remoteMU += " [{}]".format(list(st["reader_duz_at_reading_site"]["byValueCount"])[0])
        if userRef not in readersAutoCreated:
            nameMU = re.sub(r'\]', '*]', nameMU)
        tbl.addRow([
            nameMU,
            re.sub(r'(ATOLOGY| CARE)', '', muBVC(st["image_index_for_specialty"]["byValueCount"])),
            st["_total"],
            remoteMU,
            appsMU
        ])
    mu += """For the period considered here, the Acquisition List has <span class='countHigh'>{:,}</span> Readers, <span class='countHigh'>{}</span> of which are local. The names of Readers from remote sites (_\"Remote Readers\"_) are in __bold__.
    
""".format(
        len(st2006_5849Us), 
        reportAbsAndPercent(noLocal, len(st2006_5849Us))
    )
    mu += """<span class='countHigh'>{}</span> of the following Readers were added automatically to this VistA - those added explicitly are marked with a _*_. \"Applications (Signons)\" gives the number of sign ons a user makes with different applications for the period under consideration. _UNSET_ means the application doesn't identify itself - _CPRS_ is the chief example of this. Note that _TeleReader_ is used by remote users.
    
""".format(
        reportAbsAndPercent(
            len(readersAutoCreated),
            len(st2006_5849Us)
        )
    )
    mu += tbl.md() + "\n\n"
        
    return mu  
        
# ################## Configuration (Reader and Acquisition Roles) ###############
    
def webReportReading(stationNo, stationName, onAndAfterDay, upToDay):
    mu = "## Reading\n\n" 
    mu += webReportReadingConfiguration(stationNo, stationName)
    # mu += webReportReadingActivity(stationNo, onAndAfterDay, upToDay)
    return mu
    
def webReportReadingConfiguration(stationNo, stationName):
        
    # > The TELEREADER ACQUISITION SITE file (#2006.5842) contains the list of the
    # Acquisition Sites for each Reading Site. This list must also include the Reading     
    # Site itself if it is to perform image acquisition as well.
    # > ...
    def mu2006_5842(dataLocn):

        propMap = [("name", "Name", "DROP"), ("primary_site", "Primary Site", "IEN"), ("lock_timeout_in_minutes", "Lock Timeout")] # dropped status
        
        resourceIter = FilteredResultIterator(dataLocn, "2006_5842")
        tbl = MarkdownTable([":{}".format(pmap[1]) for pmap in propMap])
        includesItselfMU = ""
        for i, resource in enumerate(sorted(resourceIter, key=lambda x: x["primary_site"]["label"], reverse=True), 1):
            resource["name"]["label"] = re.sub(r'( VAMC| CBOC| VA CLINIC| VA MEDICAL CENTER)', "", resource["name"]["label"])
            flattenPropValues(resource)
            if re.search(stationNo, resource["primary_site"]):
                includesItselfMU = ", including itself"
            tbl.addRow(rowUp(resource, propMap, True, suppress=["status"]))

        fmu = """Despite the name, _TELEREADER ACQUISITION SITE [2006.5842]_ configures a VistA for __Reading__, not acquisition. It lists __the sites a VistA can read from__. This list will include the Reading Site itself if it reads images acquired locally. In this VistA, it has <span class='countHigh'>{:,}</span> entries{} ... 

""".format(i, includesItselfMU)
        fmu += tbl.md() + "\n\n"
        return fmu
        
    # Add more 200 details ie/ created explicitly or not? Presume so
    # Add -- should tie into FILLER Consults?
    def mu2006_5843(dataLocn):
    
        propMap = [("reader", "Reader"), ("acquisition_site", "Acquisition Site", "", "acquisition_site")]
        
        resourceIter = FilteredResultIterator(dataLocn, "2006_5843")
        tbl = MarkdownTable([":{}".format(pmap[1]) for pmap in propMap])
        for i, resource in enumerate(resourceIter, 1):
            flattenPropValues(resource)
            tbl.addRow(rowUp(resource, propMap, True))
    
        fmu = """_TELEREADER READER [2006.5843]_ adds information about individual users for __Reading__. It [1] identifies readers using their User file entry (200), [2] lists the  one or more _TELEREADER ACQUISITION SITE [2006.5842]_ the user can read from and [3] designates the clinical specialties a user has. In this VistA, it has <span class='countHigh'>{:,}</span> entries ... 

""".format(i)
        fmu += tbl.md() + "\n\n"
        return fmu
        
    dataLocn = "{}{}/Data/".format(VISTA_DATA_BASE_DIR, stationNo)   

    mu = "### Configuration\n\n"
    mu += mu2006_5842(dataLocn)
    mu += mu2006_5843(dataLocn)
    
    return mu
        
# ################################# Utils #############################
    
def rowUp(resource, propMap, enforceMapAll=True, suppress=[]):
    propsDontSee = ["type", "_id", "label"]
    propsDontSee.extend(suppress)
    propsSeen = set(k for k in resource if k not in propsDontSee)
    propsMapped = set(suppress)
    row = []
    for i, pMap in enumerate(propMap, 1):
        if pMap[0] in resource:
            propsMapped.add(pMap[0])
            if len(pMap) > 3 and pMap[3]:
                valMU = ", ".join(sorted([re.sub(r' +\[[\d\_]+\-', ' [', v[pMap[3]]) for v in resource[pMap[0]]]))
                row.append(valMU)
                continue
            val = resource[pMap[0]]
            if len(pMap) == 3:
                if pMap[2] == "IEN":
                    val = re.sub(r' +\[[\d\_]+\-', ' [', val)
                elif pMap[2] == "DROP":
                    val = re.split(r' +\[', val)[0]
            valMU = "__{}__".format(re.sub(r'\s+$', '', val)) if i == 1 else val
            row.append(valMU)
        else:
            row.append("")
    if enforceMapAll and len(propsSeen - propsMapped):
        raise Exception("Not all resource props expected were mapped")
    return row
    
# ############### Reducer/Reframer to nix for Typers #############
    
"""
TODO: part of 123 E, accounting for 2006_5849. REM: each 2006_5849 has one and only
one 2006_5849 => can use consult totals to tell how many missing.

REWORK COMPLETELY to do typer in MU of 123.

Consults have a service (123_5). If a service appears in TELEREADER ACQUISITION SERVICE (2006_5841) then it is used for Acquisition. However, some consults DO NOT APPEAR in
the Queue. This isolates them.

TODO: part of IFC in general and part of 123E walk in general.

Note: this is the direction from Consult to Queue. This COULD become type based where
123 E to feature whether it is in 2006.5849. See db123DetailsByIEN


    TODO: will need 123 reduction where its #'s exceed those of 2006_5849.
    
    Report this misconfiguration of the Acquisition Service List
    ie/ consults expected to be in Queue are not there (rightly so). The Acquisition 
    Service List is wrong. Two reasons seen:
    - Service is actually for reading for a remote site
    - Service is a Procedure (and therefore won't go in TeleReading?)
    - 668 has two others, dental, may be turned on for experiment and deleted?
    
    isolateMissingConsults <---- replace with MU direct of 123E where 123E
    has more explicit markers to count the missing's.

    if "missingFromQueue" in trqConsultSummary:
        # This means service SHOULD NOT be defined for Acquisition as it 
        # is used by a remote site to send consults to this site for Reading!
        missingMU = "Acquisition configuration predicts <span class='countHigh'>{:,}</span> consults should be on the LIST but are not.".format(trqConsultSummary["missingFromQueue"])
        if "missingFromQueueFillers" in trqConsultSummary:
            missingMU += " <span class='countHigh'>{:,}</span> belong to service(s) _{}_ that are Readers for remote VistAs.".format(
                trqConsultSummary["missingFromQueueFillers"],
                ", ".join(trqConsultSummary["missingFromQueueFillersServices"])
            )
        if "missingFromQueueProcedure" in trqConsultSummary:
            missingMU += " <span class='countHigh'>{:,}</span> belong to service(s) _{}_ which involve procedures.".format(
                trqConsultSummary["missingFromQueueProcedure"],
                ", ".join(trqConsultSummary["missingFromQueueProcedureServices"])
            )           
        if "missingFromQueueLocalDiscontinue2" in trqConsultSummary:
            missingMU += " <span class='countHigh'>{:,}</span> are discontinued before they reach the queue.".format(
                trqConsultSummary["missingFromQueueLocalDiscontinue2"]
            )           
        if "otherMissing" in trqConsultSummary:
            missingMU += " <span class='countHigh'>{:,}</span> are absent for other reasons.".format(
                trqConsultSummary["otherMissing"]
            )
"""
def isolateMissingConsults(stationNo): # TMP - move to use typer in mu

    csJSNFl = "{}{}/TmpWorking/".format(VISTA_DATA_BASE_DIR, stationNo) + "telereaderQueueConsultSummary.json"
    try:
        trqConsultSummary = json.load(open(csJSNFl))
    except:
        pass
    else:
        return trqConsultSummary
        
    raise Exception("TODO: need queueConsultIds and consultRedById")

    # TODO: replace consultRedById with walk of 123's in time period 
    trqConsultSummary = {
        "total": len(consultRedById),
    }        
    acquisitionServiceIds = set(id for id in consultRedById if "is_service_for_acquisition" in consultRedById[id])
    missingFromQueue = acquisitionServiceIds - queueConsultIds
    if len(missingFromQueue):
        trqConsultSummary["missingFromQueue"] = len(missingFromQueue)
        missingFromQueueFillers = set(consultId for consultId in missingFromQueue if "ifc_role" in consultRedById[consultId] and consultRedById[consultId]["ifc_role"] == "F:FILLER")
        if len(missingFromQueueFillers):
            trqConsultSummary["missingFromQueueFillers"] = len(missingFromQueueFillers)
            missingFromQueueFillersServices = set(consultRedById[consultId]["to_service"] for consultId in missingFromQueueFillers)
            trqConsultSummary["missingFromQueueFillersServices"] = sorted(list(missingFromQueueFillersServices))
        missingFromQueueProcedure = set(consultId for consultId in missingFromQueue if "is_acquisition_service_procedure" in consultRedById[consultId])
        if len(missingFromQueueProcedure):
            trqConsultSummary["missingFromQueueProcedure"] = len(missingFromQueueProcedure)
            missingFromQueueProcedureServices = set(consultRedById[consultId]["to_service"] for consultId in missingFromQueueProcedure) 
            trqConsultSummary["missingFromQueueProcedureServices"] = sorted(list(missingFromQueueProcedureServices))         
        missingFromQueueLocalDiscontinue2 = set(consultId for consultId in missingFromQueue if "ifc_role" in consultRedById[consultId] and consultRedById[consultId]["ifc_role"] == "P:PLACER" and re.match(r'DISCONTINUED', consultRedById[consultId]["cprs_status"]))
        if len(missingFromQueueLocalDiscontinue2):
            trqConsultSummary["missingFromQueueLocalDiscontinue2"] = len(missingFromQueueLocalDiscontinue2)
        otherMissing = missingFromQueue - ((missingFromQueueFillers.union(missingFromQueueProcedure)).union(missingFromQueueLocalDiscontinue2))
        if len(otherMissing):
            trqConsultSummary["otherMissing"] = len(otherMissing)
    json.dump(trqConsultSummary, open(csJSNFl, "w"))        
    return trqConsultSummary
        
"""            
    Combination of 123.5 (has or hasn't 'Remote Reading Site') and 2006.5841 
    (identifies specifically as telereader acquisition service) identifies telereading
    location and the shape of Consults. 
    
    For all telereader acquistion services (in 2006.5841) ...
    
            Read     123.5 Has 'Remote Reading Site'    123 Role
            ----        -------------------            ----------
            LOCAL               NO                        NONE
            IFC/REMOTE          YES                     P:PLACER
            
    but there's room for error in configuration. In 757, one LOCAL site
    (acquire and read on-site locally) is never used for local reading of
    local acquisitions (ifc_role NONE). All of its consults have ifc_role
    F:FILLER which points to it being a remote reader for another site, one
    that should NOT be in 2006.5841. This can only be known by examining the
    consults of a service and excluding services from acquisition that are
    F:FILLER.
    
    Note that so far, don't see any mixed situations ie/ remote site treats
    a Local Service as its remote Reader AND the site does so itself too ie.
    2006.5841 is valid but the service is doing double duty.
"""
def reduce123_5ForIFC(stationNo):
    
    jsnFl = "{}{}/TmpWorking/".format(VISTA_DATA_BASE_DIR, stationNo) + "ifcServiceByIEN.json"
    try:
        ifcServiceByIEN = json.load(open(jsnFl))
    except:
        pass
    else:
        return ifcServiceByIEN
    
    dataLocn = "{}{}/Data/".format(VISTA_DATA_BASE_DIR, stationNo)   
    resourceIter = FilteredResultIterator(dataLocn, "123_5")
    ifcServiceByIEN = {}
    for i, resource in enumerate(resourceIter, 1):
        ien = resource["_id"].split("-")[1]
        if not ("ifc_remote_name" in resource or "ifc_routing_site" in resource):
            continue
        flattenPropValues(resource)
        ifcServiceByIEN[ien] = {"service_name": resource["service_name"]}
        if "ifc_remote_name" in resource:
            ifcServiceByIEN[ien]["ifc_remote_name"] = resource["ifc_remote_name"]
        if "ifc_routing_site" in resource:
            ifcServiceByIEN[ien]["ifc_routing_site"] = resource["ifc_routing_site"]
        if "associated_stop_code" in resource:
            ifcServiceByIEN[ien]["associated_stop_code"] = list(set(sr["associated_stop_code"] for sr in resource["associated_stop_code"]))
        
    json.dump(ifcServiceByIEN, open(jsnFl, "w"))
        
    return ifcServiceByIEN  
                        
# ################################# DRIVER #######################
               
def main():

    assert sys.version_info >= (3, 6)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO")

    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    if not os.path.isdir(userSiteDir):
        raise SystemExit("Expect User Site to already exist with its basic contents")

    # <=> YR1 (fits with YR1E of 3.081)
    meta = metaOfVistA(stationNo)
    vistaName = "VistA" if "name" not in meta else meta["name"]
    cutDate = meta["cutDate"]
    cutDateDT = datetime.strptime(cutDate.split("T")[0], "%Y-%m-%d")
    yrBeforeDateDT = cutDateDT - relativedelta(years=1)
    yrBeforeDate = datetime.strftime(yrBeforeDateDT, "%Y-%m-%d")
    onAndAfterDay = yrBeforeDate
    upToDay = cutDate
    print("Reporting TeleReading for YR1 (from {} to {})".format(onAndAfterDay, upToDay))

    webReportTeleReading(stationNo, meta.get("name", "VistA"), onAndAfterDay, upToDay)
        
if __name__ == "__main__":
    main()
