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
from ..webReportUtils import filteredResultIterator, reduce200, TOP_MD_TEMPL, SITE_DIR_TEMPL, keyStats, roundFloat

"""
Images types, references (TIU, Radiology), Acquisition Devices, Users ...

TODO:
- bug: dicom in last table's orphans
- add in more on typing using docs and patient #'s (see GOAL)

Note: may aspects of images will appear in other more specific reports and some of the
breakdowns below (TODO) may become functions to enable that reporting ex/ Image-centric documents etc.

GOAL: move towards patient centric view of images and using reference typing to type images as native form not good enough (expand on this theme). Also expand on user access to images. Overall, WANT TO FOLLOW SAME PATTERNS as other data types. 
"""
    
def webReportImaging(stationNo):

    # Too many here - part of plus
    allThere, details = checkDataPresent(stationNo, [
    
        {"fileType": "702_09", "check": "ALL"}, # in 2005RF too
        {"fileType": "2005", "check": "YR1"}, # object_type-pdf-capture_application (off 2005RF)
        {"fileType": "2005_02", "check": "TYPE"},
        {"fileType": "2005_03", "check": "ALL"},
        {"fileType": "2006_04", "check": "ALL"},
        {"fileType": "2006_532", "check": "ALL"}, # SOP ids - get labels
        {"fileType": "2006_82", "check": "YR1"}, # workstation (used for 2005RF too)
        {"fileType": "8925", "check": "YR1"}, # document_type (used for 2005RF too)

        # Just for 2005 RF
        {"fileType": "74", "check": "ALL"}, # will index in a shelve
        {"fileType": "8925_1", "check": "ALL"},
        {"fileType": "8925_91", "check": "ALL"} # shelve to have doc by img and vica versa

    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    # ###################### Preparation/ Preprocessing #########################
          
    allTypeData, subTypeDatas = splitTypeDatas(stationNo, "2005", reductionLabel="YR1", expectSubTypeProperty="object_type-pdf-capture_application")
    totalAll = allTypeData["_total"]
        
    """
    Enforce things about capture_application and image_save_by etc as interpretation
    and derivation rely on them
    """
    def enforce2005(typeInfo):
    
        """
        Acquisition Device (2006.04): mandatory for I:Import API and D:DICOM Gateway but 
        never C:Capture Workstation 
        """
        if "capture_application" not in typeInfo:
            if "acquisition_device" in typeInfo:
                raise Exception("Didn't expect acquisition device if no capture_application")
        else:
            totalCAID = sum(typeInfo["capture_application"]["byValueCount"][ca] for ca in typeInfo["capture_application"]["byValueCount"] if ca != "C:Capture Workstation")
            if totalCAID and ("acquisition_device" not in typeInfo or typeInfo["acquisition_device"]["count"] != totalCAID):
                raise Exception("Expected acquisition device if capture application is D:DICOM or I:Import")
                
        """
        Image Save By:
        - mandatory for I:Import API and C:Capture and even for DICOM Gateway
        if it leads to DICOM:TIU (unsure how that can happen!) ie/ not for DICOM:RADIOLOGY
          ... possible that DICOM:TIU is one user too??????
        - I:Import API leads to one and only one user across the system ie a default guy!
        """
        totalCAIC = sum(typeInfo["capture_application"]["byValueCount"][ca] for ca in typeInfo["capture_application"]["byValueCount"] if "capture_application" in typeInfo and ca != "D:DICOM Gateway")
        if ("image_save_by" in typeInfo and (typeInfo["image_save_by"]["count"] != totalCAIC)) or (totalCAIC and "image_save_by" not in typeInfo):
            raise Exception("Expected 'image_save_by' to match combo of capture I and C")
        totalCAI = sum(typeInfo["capture_application"]["byValueCount"][ca] for ca in typeInfo["capture_application"]["byValueCount"] if "capture_application" in typeInfo and ca == "I:Import API")
        # in == <=> as typeInfo is fixed to one capture_application
        if "capture_application" in typeInfo and "I:Import API" in typeInfo["capture_application"]["byValueCount"]:
            if "image_save_by" not in typeInfo:
                raise Exception("Import API but no Image Save User Set?")
            noI = typeInfo["capture_application"]["byValueCount"]["I:Import API"]
            possImportAPIUsers = set(userId for userId in typeInfo["image_save_by"]["byValueCount"] if typeInfo["image_save_by"]["byValueCount"][userId] == noI)
            if not len(possImportAPIUsers):
                raise Exception("Expect (at least) one user to a/c for Import API!")
    for subTypeData in subTypeDatas:
        enforce2005(subTypeData)
        
    # ####################### Make Report / Web Page #############################
            
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    if not os.path.isdir(userSiteDir):
        raise Exception("Expect User Site to already exist with its basic contents")

    title = "Imaging".format(stationNo)
    mu = TOP_MD_TEMPL.format("Imaging", title)
    mu += """VistA Imaging ...
    
> support(s) the goal making a patient’s complete medical record available online

"""
    
    # ################################ Format / Reference #################

    mu += webReportFormatReference(stationNo, allTypeData, subTypeDatas)
    
    # ################################ Others Plus ##################
    
    """
    The CAP and CAP-IMPORT actions in 2006_82 are already mined into an enhanced
    2005 to allow WS identification for CAPTURE and redundant definition for
    IMPORT API. Bringing this in again, allows more:
    - if only one user in byWS then can id the real user for IMPORT API as all seem 
    set to one
    - activity of READ-ONLY so can see number of workstations involved.
    
    _2006_82AllTypeInfo, _2006_82SubTypeInfos = splitTypeDatas(stationNo, "2006_82", reductionLabel="YR1", expectSubTypeProperty="workstation")
    mu += webReportImageAcquisition(stationNo, subTypeDatas, _2006_82SubTypeInfos)
    """
    # mu += webReportImageDocumentTypes(stationNo) 
    # mu += crudeTIULinkReport(stationNo)
            
    open(userSiteDir + "imaging.md", "w").write(mu)
        
# #################### Format/ Reference ###################

def webReportFormatReference(stationNo, allTypeData, subTypeDatas):

    """
    subtypes - splitting out (XRAY)_GROUP as not 'really' an image ie/ IMAGE GROUP
    - with fileref => individual images
    - without: expect object_group for children and grouper
    """
    def distinguishFileRefAndGroupSubTypes(subTypeDatas):
        filerefSubTypesByOT = defaultdict(list)
        groupSubTypes = []
        for i, subTypeInfo in enumerate(sorted(subTypeDatas, key=lambda x: singleValue(x, "object_type"), reverse=True), 1): 
            ot = singleValue(subTypeInfo, "object_type").split(" [")[0]
            if ot == "XRAY GROUP":
                if "object_group" not in subTypeInfo:
                    raise Exception("Expected ALL groupers to have children")
                groupSubTypes.append(subTypeInfo)
                continue
            if "object_group" in subTypeInfo:
                raise Exception("Expected NO Individual Images to have children")
            filerefSubTypesByOT[ot].append(subTypeInfo)
        return filerefSubTypesByOT, groupSubTypes 
    filerefSubTypesByOT, groupSubTypes = distinguishFileRefAndGroupSubTypes(subTypeDatas)

    mu = ""
        
    """
    Individual Images: all have fileref 
    
    Missing: [TODO]
    - patient as didn't capture byValueCount for 2 in reduction. Must redo OR redo
    uniques iff do subtyping just by type and not type_pdf
    
    Note: keeping 'capture' for now - will expand Acquisition below to report on formats
    and capture mode and take out of here later. TODO
    """
    tbl = MarkdownTable(["Type", "Count", "Form", "Capture", "Direct Referenced", "Group Referenced", "Orphan"])
    imageTotal = 0
    userCntByTypeSubType = defaultdict(lambda: defaultdict(dict))
    allTotalLessDICOM = 0
    allTotalOrphansLessDICOM = 0 
    pdfLabelsSeen = set()  
    importAPIUser = "" 
    
    """
    TO AUDIT: iffy logic - assuming that individual images get link as well as
    parent if parent has link. There is NO separate check that only a parent
    link. Doesn't seem to matter but??
    """
    # Global one to isolate out just by PDFLabel irrespective of image type (ot)
    # ... will see only TIU (and a few NOSET) apply for import api
    byCAByPDFLabel = defaultdict(lambda: defaultdict(int))
    # type ie/ DICOM IMAGE etc
    summs = []
    summPies = []
    for typeId in sorted(filerefSubTypesByOT, key=lambda x: sum(y["_total"] for y in filerefSubTypesByOT[x]), reverse=True):
        
        subTypeInfos = filerefSubTypesByOT[typeId]
        
        typeTotal = sum(subTypeInfo["_total"] for subTypeInfo in subTypeInfos)
        imageTotal += typeTotal
        if typeId != "DICOM IMAGE":
            allTotalLessDICOM += typeTotal
        
        suffixesCount = defaultdict(int)
        caCount = defaultdict(int)
        oiCount = defaultdict(int)

        linksDirectByPDF = defaultdict(int)
        linksFromParentByPDF = {}
        orphanNo = 0
            
        for subTypeInfo in subTypeInfos:
                                
            # typeLabel = subTypeValue.split("/")[0]
            typeLabel = singleValue(subTypeInfo, "object_type").split(" [")[0]
            pdfLabel = singleValue(subTypeInfo, "pdf", "NOSET")
            pdfLabelsSeen.add(pdfLabel)
                            
            for suffix in subTypeInfo["fileref_suffix"]["byValueCount"]:
                suffixesCount[suffix] += subTypeInfo["fileref_suffix"]["byValueCount"][suffix]
            for ca in subTypeInfo["capture_application"]["byValueCount"]:
                caCount[ca] += subTypeInfo["capture_application"]["byValueCount"][ca]
                byCAByPDFLabel[ca][pdfLabel] += subTypeInfo["capture_application"]["byValueCount"][ca]
                
            # User - for CA == capture_workstation only - come back to him later
            # ... note: some Capture Workstation missing em!
            if "image_save_by" in subTypeInfo:
                for userId in subTypeInfo["image_save_by"]["byValueCount"]:
                    userCntByTypeSubType[typeId][pdfLabel][userId] = subTypeInfo["image_save_by"]["byValueCount"][userId]
            if "origin_index" in subTypeInfo:
                for oi in subTypeInfo["origin_index"]["byValueCount"]:
                    oiCount[oi] += subTypeInfo["origin_index"]["byValueCount"][oi]
                            
            """
            The following leverages:
            - one NOSET vs others
            - others "parent_data_file" < "_total" => parent is responsible!
            """
            if pdfLabel != "NOSET":
                if "parent_data_file" in subTypeInfo:
                    linksDirectByPDF[pdfLabel] += subTypeInfo["parent_data_file"]["count"]
                if "group_parent" in subTypeInfo:
                    rangeCount = subTypeInfo["group_parent"]["rangeCount"] if "rangeCount" in subTypeInfo["group_parent"] else len(subTypeInfo["group_parent"]["byValueCount"])
                    # rem: B3 sub typing so must be incremental
                    if pdfLabel not in linksFromParentByPDF:
                        linksFromParentByPDF[pdfLabel] = [subTypeInfo["group_parent"]["count"], rangeCount]
                    else: 
                        linksFromParentByPDF[pdfLabel][0] += subTypeInfo["group_parent"]["count"]
                        linksFromParentByPDF[pdfLabel][1] += rangeCount
                continue
                
            # From NOSET (must exist as here!) ... can be C or I
            orphanNo += subTypeInfo["_total"]    
            if typeId != "DICOM IMAGE":
                allTotalOrphansLessDICOM += subTypeInfo["_total"]  
            
        summ = {"name": re.sub(r'\_', ' ', typeId)}
        summPie = {"Type": re.sub(r'\_', ' ', typeId)}
            
        # Note: argument to take parent and not direct DICOM which would then show orphans
        # ... seems like RAD goes to GROUP and not individual and may be missing.             
        totalLinked = sum(linksFromParentByPDF[x][0] for x in linksFromParentByPDF if typeId != "DICOM_IMAGE") + sum(linksDirectByPDF[x] for x in linksDirectByPDF)
 
        typeTotalMU = "{:,}".format(typeTotal)
        
        summPie["Count"] = typeTotal
 
        if len(suffixesCount) == 1:
            suffixesMU = list(suffixesCount)[0]
        else:
            suffixesMU = "<br><br>".join(["{} ({:,})".format(suffix, suffixesCount[suffix]) for suffix in sorted(suffixesCount, key=lambda x: suffixesCount[x], reverse=True)])

        if len(caCount) == 1:
            captureMU = list(caCount)[0].split(":")[1]
        else:
            captureMU = "<br><br>".join(["{} ({:,})".format(vc.split(":")[1], caCount[vc]) for vc in sorted(caCount, key=lambda x: caCount[x], reverse=True)])

        if len(oiCount) == 1:
            originMU = list(oiCount)[0].split(":")[1]
        else:
            originMU = "<br><br>".join(["{} ({:,})".format(vc.split(":")[1], oiCount[vc]) for vc in sorted(oiCount, key=lambda x: oiCount[x], reverse=True)])  

        """
        Direct Links
        """
        directLinkMU = "<br><br>".join(["{} ({:,})".format(re.sub(r'_', ' ', pdf), linksDirectByPDF[pdf]) for pdf in linksDirectByPDF])
        
        summ["directReferenced"] = sum(linksDirectByPDF[pdf] for pdf in linksDirectByPDF)        

        """
        Parent/Group
        """
        parentLinkMU = "<br><br>".join(["{} ({:,}/{:,})".format(re.sub(r'_', ' ', gpdf), linksFromParentByPDF[gpdf][0], linksFromParentByPDF[gpdf][1]) for gpdf in linksFromParentByPDF]) 
        
        summ["groupReferenced"] = sum(linksFromParentByPDF[gpdf][0] for gpdf in linksFromParentByPDF) if typeId != "DICOM_IMAGE" else 0 # as redundant
        
        orphansMU = "" if orphanNo == 0 else "{:,}".format(orphanNo)
        
        summ["orphan"] = orphanNo

        # removed 'originMU' as better looked at below. Seems not to be accurate.        
        tbl.addRow([
            "__{}__".format(re.sub(r'\_', ' ', typeId)), 
            typeTotalMU, 
            suffixesMU, 
            captureMU, 
            directLinkMU,
            parentLinkMU, 
            orphansMU
        ])
    
        # Don't include DICOM in summary    
        if not re.match(r'DICOM', typeId):
            summs.append(summ)
        summPies.append(summPie)
                
    objectTypesInfo, sts = splitTypeDatas(stationNo, "2005_02", expectSubTypeProperty="")        
    
    totalXRG = sum(x["_total"] for x in groupSubTypes)
    
    overallFirstCreateDate = allTypeData["_firstCreateDate"].split("T")[0] 
    overallLastCreateDate = allTypeData["_lastCreateDate"].split("T")[0]
    
    mu += """<span class='yellowIt'>{imageTotal:,}</span> individual images were entered into this VistA from {overallFirstCreateDate} through {overallLastCreateDate}, the last full year for which data is available. <span class='yellowIt'>{filerefSubTypesByOTCount:,}</span> formats of image were entered from the <span class='yellowIt'>{objectTypesInfoTotal:,}</span> supported by the _VistA Imaging_ Subsystem. These images are for <span class='yellowIt'>{allTypeDataPatientRangeCount:,}</span> distinct patients.

<span class='yellowIt'>{totalXRG:,}</span> “XRAY” GROUP “Images” were also entered during this period. These group individual images and, despite their name, don’t just group XRAYs or even DICOM Images - they can group PDFs, TIFs and other Image formats too. Grouping allows individual TIU Notes (TIU) and Radiology Notes (RADIOLOGY) reference a group of Images.
    
An image can be entered in one of three ways - _Capture Workstation_ for manually entering images and _DICOM Gateway_ and _Import API_, both automated entry mechanisms.

""".format(
        imageTotal=imageTotal, 
        overallFirstCreateDate=overallFirstCreateDate, 
        overallLastCreateDate=overallLastCreateDate, 
        filerefSubTypesByOTCount=len(filerefSubTypesByOT), 
        objectTypesInfoTotal=objectTypesInfo["_total"], 
        allTypeDataPatientRangeCount=allTypeData["patient"]["rangeCount"],
        totalXRG=totalXRG
    )
    
    # #################### Formats and References ###################
    """
    Two things - by format, ac dev AND reference pattern. Probably too much
    as both dimensions can be looked at separately.
    
    TO CHANGE:
    ie/ BREAK THIS PROPERLY AFTER DOING AC DEV. Ex/ of what's lost.
    ie/ the dimension of format and ac and ref both there ... two different
    items ie/ format:ref and format:ac
    
    Cheyenne:
    - 67 :C for DICOM ... sub refs to that is TIU (30), TMP (37) both from non main
    institution ie/ kind of shows no gateway there to take in DICOMS so doing in CAPTURE
    (should see those WS's as being from those places!)
    
    Note: devices too - references. Question of whether ac dev and references
    should be in same subsection. Doing AC DEV below and if appropriate then will keep
    """
    
    mu += "## Image Formats and References\n\n"
    
    mu += "The following table describes these images: [1] their types and formats, [2] their quantities, [3] whether and how they are referenced from structured data such as TIU or Radiology notes, both directly and through groups, and [4] whether they go unreferenced (\"Orphan\") ...\n\n"
    
    mu += tbl.md() + "\n\n"
        
    mu += "<strong>IMAGE \"Images by Format and References\" - sb_imagesByFormatAndReferences - put in Office Excel and 2D Bar (Stacked) Chart ...\n\n"
    mu += "__VALUES__: {}\n\n".format(json.dumps(summs))
    mu += "![](/imgs/sb_imagesByFormatAndReferences.png)\n\n"
        
    """
    Orphans
    """
        
    mu += "Setting aside DICOM (.DCM), there are <span class='yellowIt'>{:,}</span> images, <span class='yellowIt'>{}</span> of which are _Orphans_.\n\n".format(allTotalLessDICOM, reportAbsAndPercent(allTotalOrphansLessDICOM, allTotalLessDICOM))
            
    mu += "Most _Orphans_ are accounted for by a property of most images called type index. In general, this property is ambiguous with most images ending up in catch-all categories such as _Medical Record_. However, many of its less used values do account for most of the Orphans.\n\n"

    # Reframe PDF under TI. Want to see TI that are all or mainly NOSET PDF.
    def groupTypeIndexes(subTypeInfos):
        tiUnsetGroupingByOT = defaultdict(lambda: defaultdict(int))
        tiGroupingByPDF = defaultdict(lambda: defaultdict(int))
        for subTypeInfo in subTypeInfos:
            if "type_index" not in subTypeInfo:
                continue
            otLabel = singleValue(subTypeInfo, "object_type").split(" [")[0]
            pdfLabel = singleValue(subTypeInfo, "pdf", "NOSET")
            for ti in subTypeInfo["type_index"]["byValueCount"]:
                tiGroupingByPDF[ti][pdfLabel] += subTypeInfo["type_index"]["byValueCount"][ti]
                if pdfLabel == "NOSET":
                    tiUnsetGroupingByOT[ti][otLabel] += subTypeInfo["type_index"]["byValueCount"][ti]
        return tiGroupingByPDF, tiUnsetGroupingByOT
    subTypeInfos = [subTypeInfo for ot in filerefSubTypesByOT for subTypeInfo in filerefSubTypesByOT[ot]] # if ot == "ADOBE"
    tiGroupingByPDF, tiUnsetGroupingByOT = groupTypeIndexes(subTypeInfos)
    majNoSetTIs = set()
    otherNoSetTIs = set()
    majNoSetOnlysTotal = 0
    otherNoSetOnlysTotals = 0
    for ti in tiGroupingByPDF:
        if "NOSET" not in tiGroupingByPDF[ti]:
            continue
        totalTI = sum(tiGroupingByPDF[ti][pdf] for pdf in tiGroupingByPDF[ti])
        noSetPercent = (float(tiGroupingByPDF[ti]["NOSET"])/float(totalTI)) * 100
        if noSetPercent >= 50.0: # > 50 percent then!
            majNoSetTIs.add(ti)
            majNoSetOnlysTotal += tiGroupingByPDF[ti]["NOSET"] # REM: don't want to cnt if any links
        else:
            otherNoSetTIs.add(ti)
            otherNoSetOnlysTotals += tiGroupingByPDF[ti]["NOSET"]
                
    mu += "Of <span class='yellowIt'>{:,}</span> active _type index_ values, <span class='yellowIt'>{:,}</span> account for <span class='yellowIt'>{:,}</span> Orphans ...\n\n".format(len(tiGroupingByPDF), len(majNoSetTIs), majNoSetOnlysTotal)
    
    tbl = MarkdownTable(["Type Index", "All/Majority Orphans", "Minority Referenced", "Orphan Type(s)"])
    for ti in sorted(list(majNoSetTIs), key=lambda x: tiGroupingByPDF[x]["NOSET"], reverse=True):
    
        setPDFMU = ", ".join(["{} ({})".format(pdfLabel, tiGroupingByPDF[ti][pdfLabel]) for pdfLabel in tiGroupingByPDF[ti] if pdfLabel != "NOSET"])
        otUSMU = ", ".join(["{} ({})".format(re.sub(r'\_', ' ', ot), tiUnsetGroupingByOT[ti][ot]) for ot in sorted(tiUnsetGroupingByOT[ti], key=lambda x: tiUnsetGroupingByOT[ti][x], reverse=True)]) if len(tiUnsetGroupingByOT[ti]) > 1 else list(tiUnsetGroupingByOT[ti])[0]
        
        tbl.addRow([
            "__{}__".format(ti.split(" [")[0]), 
            tiGroupingByPDF[ti]["NOSET"], 
            setPDFMU, 
            otUSMU
        ])
        
    mu += tbl.md() + "\n\n"
    
    mu += "The balance of unreferenced Images, <span class='yellowIt'>{:,}</span>, belong to <span class='yellowIt'>{:,}</span> types that usually have references. For example, Progress Notes and Images are nearly always referenced. These Orphans are either mischaracterized or mistakenly left unreferenced.\n\n".format(otherNoSetOnlysTotals, len(otherNoSetTIs))
    
    tbl = MarkdownTable(["Type Index", "Minority Orphans", "Majority Referenced", "Orphan Type(s)"])
    for ti in sorted(list(otherNoSetTIs), key=lambda x: tiGroupingByPDF[x]["NOSET"], reverse=True):
    
        setPDFMU = ", ".join(["{} ({})".format(pdfLabel, tiGroupingByPDF[ti][pdfLabel]) for pdfLabel in tiGroupingByPDF[ti] if pdfLabel != "NOSET"])
        otUSMU = ", ".join(["{} ({})".format(re.sub(r'\_', ' ', ot), tiUnsetGroupingByOT[ti][ot]) for ot in sorted(tiUnsetGroupingByOT[ti], key=lambda x: tiUnsetGroupingByOT[ti][x], reverse=True)]) if len(tiUnsetGroupingByOT[ti]) > 1 else list(tiUnsetGroupingByOT[ti])[0]
        cntAllOfTI = sum(tiGroupingByPDF[ti][pdfLabel] for pdfLabel in tiGroupingByPDF[ti])
        
        tbl.addRow([
            "__{}__".format(ti.split(" [")[0]), 
            reportAbsAndPercent(tiGroupingByPDF[ti]["NOSET"], cntAllOfTI),
            setPDFMU, 
            otUSMU
        ])
        
    mu += tbl.md() + "\n\n"
    
    """
    All possible referencing types 
    """ 
           
    tbl = MarkdownTable(["Id", "(Parent) Reference File", "Reference Subfile", "Abbrev", "Pkg", "Class"])
    noInThisSystemImages = 0
    resourceIter = filteredResultIterator(stationNo, "2005_03")
    for i, resource in enumerate(resourceIter, 1):
        # Chey 442 has corruption in its file ... 640 doesn't
        parentFileMU = "{} ({})".format(resource["file_pointer"]["label"], resource["file_pointer"]["id"].split("-")[1]) if resource["file_pointer"]["id"] != "1--1" else ""
        subFileMU = "{} ({})".format(resource["label"], resource["_id"].split("-")[1]) if resource["_id"].split("-")[1] != resource["file_pointer"]["id"].split("-")[1] else ""
        package_indexMU = "" if "package_index" not in resource else resource["package_index"].split(":")[1]
        class_indexMU = "" if "class_index" not in resource else resource["class_index"]["label"] # 2005_82
        root = resource["global_root_type"].split(":")[1]
        
        # Ignoring Root = [1] simple global (ex/ ^SRO), [2] global with fileid (ex/ ^XMB(3.9,) or [3] LAB with its multiples ie/ only ROOT 3 of interes
        # TODO: consider spec_subspec_index and proc_event_index (ie/ only other fields)
        
        inThisSystemsImages = resource["file_subfile_name"] in pdfLabelsSeen
        name = "__{}__".format(resource["file_subfile_name"]) if inThisSystemsImages else resource["file_subfile_name"]
        if inThisSystemsImages:
            noInThisSystemImages += 1
        
        tbl.addRow([
            name, 
            parentFileMU, 
            subFileMU, 
            resource["abbreviation"], 
            package_indexMU, 
            class_indexMU
        ])
                    
    mu += "VistA Imaging supports image references from <span class='yellowIt'>{:,}</span> types of record (\"parent data files\"). Many of these types - for example, Cardiac Catherization (691.1) - have been deprecated since VistA Imaging was launched and only a minority reference images today. This system employs only <span class='yellowIt'>{:,}</span> ...\n\n".format(i, noInThisSystemImages)
    
    mu += tbl.md() + "\n\n"
    
    return mu
    
"""
DICOM Image Report

FIRST OFF:
- redo last third for PUGET as must allow NONE for SOP too
- references: showing total indiv referenced vs unique TIU etc referencing ... gotta get at that (how?)
  - tie in types too
- nice if know roles involved + image first or doc first (preps for in general work)
- overlap cohorts
- ac devices
- location fixed or not

----- clean what's below here ----

Goal: ALL mand and key props exposed in a detailed dive
... REM: if fixed for some (RAD?) then want to SPLIT 2005 into logical sub types for DICOM/RAD vs others. ie/ what props relevant or not for different types of image work (TIU centric vs radiology note centric) ex/ pacs_procedure ONLY for rad_nuc ... (want to go to dataRF with 2005_X, 2005_Y)

Note: typer rerun 668 - added force on 74/radiology_report refs + group_parent refs + added status as prop <------- if works, must change args in base config + redo 663 too
... if same results => ie/ never see cross subTypeInfo linkage then go back to narrow
way (shouldn't see as 
NOTE: doing custom ... 8925 may be wrong as redoing within a date range but will be roughly right

TODO:
- 74's ... RangeCount + Real Count combo won't work (why group # != 74#?)
  <---- change code below to exception is not byValueCount for all!
- Group Parents as explicit too => see if really necessary AS should be unique for a set of images ie/ for spec_subspec_index 
  <------------ use explicit refs to a/c for why different? Do RAD NOTEs keep object ids?
<---------- ie want to know if 74 <----> Group is 1-1 and if not, why?
<---------- if you see the GROUP + ... CT Image ... seems like NOT to do with range combos (well if assume group and members share same SOP)
- see acquisition_site -- all ONE for biggies ie/ for RAD
- for RAD/NUC, is type_index always IMAGE?
- status for non RAD/NUC varies -- a/cs for TMP use of refs?
- note that patient # for DICOM is half overall patient # ie/ many have docs and no rad work?
- distinguish CLIN, DIAG and for Diag, Cardio, ECG etc. -----> comes from procedure?
- mand/opt props: MAND COUNT RN, NRN (see doing utils)
- XRAY GROUP other way for QA ie/ reference down. Should be broken by XRAY GROUP + sop class needed. See that the down reference works.
- DICOM GMRC TEMP LIST (http://localhost:9100/rambler#1-2006.5839) pathway ie/ independent
- ac device (ie/ round before going on to all the other images
- doc type (as do custom version typer) for the referenced dicoms!

TODO Utils:
- mand/opt props
- combine using subset of subtype props => if no byValueCount and > one use then exclude prop + combo those byValueCount + ie/ recombine properly
  <----- will greatly simplify code from broken down type
  
    TODO: going to own

https://wiki.cerner.com/display/VHAMigrationRequirements/Image+Migration+Details+-+Data+Volumes

FROM WIKI etc.            
    ... in the wiki, missing counts except for DICOM Studies
    ... have 34,820,989
    - got to break out cardiology as well as radiology
      - I think TIU DICOM?
    - they want to associate notes with images and images with notes so can relink after transfer (ADD BLURB to Image report on this)
    - images without TIU => will use patient ids and optionally encounter if available ... um!
    - REF: TIFF going to PDF ie/ TODO a format to linkage report
    - ECG is pending and not lumped with Radiology and Doc (but in Diag otherwise)
    - OR is cardiology rad reports and "Millenium will link to procedure/study"
      ... very focused on Rad Cardio Procedure/Study matching and criteria for it ... could do one ie/ do up front in pipeline
    - Use Case:
      Diagnostic Imaging
      - Radiology
      - Cardiovascular - Vascular, Echo, Cath Lab
      - Cardiology ECG
    ... TODO: see if images have any prop indicating Cardio/Rad?
      Clinical Imaging: no doc link, doc link
      Document Imaging
      (didn't capture non clinical images with no link!)
      <------ see if VA doc types differentiate at all?
      ... work to sprinkle in wiki
      
      Imaging Cohort is unclear (last three years seen or?)
"""
def webReportYR3DICOM(stationNo):

    print("FIRST CHECK: overlap bold alg wrong - had to manually fix in PDF spaces and things run in as does TITLE[sop class oid]")
    print(x)

    allThere, details = checkDataPresent(stationNo, [
    
        {"fileType": "2005", "check": "YR3"}, 
        {"fileType": "2006_532", "check": "ALL"} # SOP ids

    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    allTypeData, subTypeDatas = splitTypeDatas(stationNo, "2005", reductionLabel="YR3", expectSubTypeProperty="object_type-capture_application-dicom_sop_class-spec_subspec_index-status")
    
    overallFirstCreateDate = allTypeData["_firstCreateDate"].split("T")[0] 
    overallLastCreateDate = allTypeData["_lastCreateDate"].split("T")[0]
    
    dicomSOPClassNameByUID = dict((resource["sop_class_uid"], resource["sop_class_name"]) for resource in filteredResultIterator(stationNo, "2006_532"))
    
    subTypeInfosByOT = defaultdict(list)
    for subTypeInfo in subTypeDatas:
        ot = singleValue(subTypeInfo, "object_type").split(" [")[0]
        subTypeInfosByOT[ot].append(subTypeInfo)
        
    totalDICOM = 0
    sopClassCategoryCount = Counter()
    allSOPClassed = True
    patients = set()
        
    totalDICOMRN = 0 
    countBySpecIndexBySOPClassRN = defaultdict(lambda: Counter())
    patientRN = set()
    propCountsRN = Counter()
    radRepRefsBySOPClass = defaultdict(lambda: set())
    countGroupRefsBySOPClassRN = Counter() 
    countByPacsProcBySOPClass = defaultdict(lambda: Counter()) # only RAD/NUC

    totalDICOMNRN = 0 
    patientNRN = set()
    propCountsNRN = Counter()
    countBySpecIndexBySOPClassNRN = defaultdict(lambda: Counter())
    countGroupRefsBySOPClassNRN = Counter()
    countByPDFBySOPClassNRN = defaultdict(lambda: Counter()) # only non RAD/NUC as ambig

    # All 1.2.840.10008.5.1.4.1.1.77.1.4 ie/ non RAD/NUC, not DICOM Gateway but Capture Workstation)
    totalDICOMNRNCA = 0   
    patientNRNCA = set() 
    propCountsNRNCA = Counter()
    countBySpecIndexBySOPClassNRNCA = defaultdict(lambda: Counter())
    countGroupRefsBySOPClassNRNCA = Counter()
    countByPDFBySOPClassNRNCA = defaultdict(lambda: Counter())
    countByStatusBySOPClassNRNCA = defaultdict(lambda: Counter())
    
    for subTypeInfo in subTypeInfosByOT["DICOM IMAGE"]:

        # REM: split by it so all and 1!
        if "dicom_sop_class" in subTypeInfo:
            sopClassRef = list(subTypeInfo["dicom_sop_class"]["byValueCount"])[0] # only one
            sopClassUID = sopClassRef.split(" [")[0]
        else:
            sopClassUID = "NOTSET"
            allSOPClassed = False

        if "spec_subspec_index" not in subTypeInfo:
            specSubSpecIndexLabel = "NOTSET"
        else:
            if subTypeInfo["spec_subspec_index"]["count"] != subTypeInfo["_total"]:
                raise Exception("If spec_subspec_index for SOP then except for all of SOP")
            specSubSpecIndexLabel = list(subTypeInfo["spec_subspec_index"]["byValueCount"])[0].split(" [")[0]
                            
        """
        RADIOLOGY and NUCLEAR MEDICINE 
          * always and only ones ref'ed by radiology_report
          * has pacs_procedure (and others?) too?
          * status is ALWAYs Viewable
        
        Enforce:
            > if spec_subspec_index is RADIOLOGY or NUCLEAR MEDICINE then expect radiology_report for all (see range), parent_data_file of RADIOLOGY [2005_03...] ( radiology_report should equal 74 + parent_global_root_0) AND capture_application is always DICOM_Gateway and there is a pacs_procedure
        
        Note: may have > #  of group_parent's (2005's) than radiology_reports => > 1
        group possible. But should never have more groups than radiology reports 
        """
        if specSubSpecIndexLabel in ["RADIOLOGY", "NUCLEAR MEDICINE"]:
        
            if not (
            
                "parent_data_file" in subTypeInfo and
                subTypeInfo["parent_data_file"]["count"] == subTypeInfo["_total"] and
                len(subTypeInfo["parent_data_file"]["byValueCount"]) == 1 and
                re.match(r'RADIOLOGY', list(subTypeInfo["parent_data_file"]["byValueCount"])[0]) and
                
                "radiology_report" in subTypeInfo and
                subTypeInfo["radiology_report"]["count"] == subTypeInfo["_total"] and
                
                "capture_application" in subTypeInfo and             
                len(subTypeInfo["capture_application"]["byValueCount"]) == 1 and 
                list(subTypeInfo["capture_application"]["byValueCount"])[0] == "D:DICOM Gateway" and
                
                "pacs_procedure" in subTypeInfo and
                subTypeInfo["pacs_procedure"]["count"] == subTypeInfo["_total"] and
                
                "group_parent" in subTypeInfo and
                subTypeInfo["group_parent"]["count"] == subTypeInfo["_total"] and
                
                "status" in subTypeInfo and
                set(subTypeInfo["status"]["byValueCount"]) == set(["1:Viewable"])
                
                # for RAD/NUC, is type_index always IMAGE?
                # is class_index always CLIN?
                
                # Agreement of D0 spread (if there) and group_parent and radiology_report ie/ #'s if byValueCounted should agree
                
            ):
                raise Exception("If spec_subspec_index is RADIOLOGY or NUCLEAR MEDICINE then expect a radiology_report for all members, status Viewable (as DICOM Gateway), pacs procedure and other things")
                
            sopClassCategoryCount[sopClassUID] += 1 # for overlaps
                
            for prop in subTypeInfo:
                if re.match(r'_', prop):
                    continue
                propCountsRN[prop] += subTypeInfo[prop]["count"]
            
            # total DICOM Rad Nuc (vs others)
            totalDICOMRN += subTypeInfo["_total"]
            totalDICOM += subTypeInfo["_total"]
            
            for patientRef in subTypeInfo["patient"]["byValueCount"]:
                patientRN.add(patientRef)
                patients.add(patientRef)
            
            countBySpecIndexBySOPClassRN[sopClassUID][specSubSpecIndexLabel] += subTypeInfo["_total"]
                        
            radRepRefsBySOPClass[sopClassUID] |= set(subTypeInfo["radiology_report"]["byValueCount"])
            
            bvc = subTypeInfo["pacs_procedure"]["byValueCount"]
            for pacsProc in bvc:
                countByPacsProcBySOPClass[sopClassUID][pacsProc.split(" [")[0]] += bvc[pacsProc]
                
            # Note: TODO - change to being set like rad refs as MUST be explicit
            countGroupRefsBySOPClassRN[sopClassUID] += subTypeInfo["group_parent"]["rangeCount"] if "rangeCount" in subTypeInfo["group_parent"] else len(subTypeInfo["group_parent"]["byValueCount"])
                           
        else:
        
            # All not RAD/NUC: no rad rep or pacs
            if (
                "radiology_report" in subTypeInfo or
                "pacs_procedure" in subTypeInfo
            ):
                raise Exception("Don't expect a radiology_report reference or pacs_procedure for any images not in RADIOLOGY/NUCLEAR MEDICINE spec_subspec_index")  
        
            """
            Second: not RAD/NUC but from DICOM Gateway
            """
            if re.search(r'DICOM_Gateway', subTypeInfo["_subTypeId"]): # NRN (all G/W) 
            
                if not (
                    "status" in subTypeInfo and
                    set(subTypeInfo["status"]["byValueCount"]) == set(["1:Viewable"])
                ):
                    raise Exception("Expected 2: non RAD/NUC but DICOM Gateway to always have status Viewable ie G/W import is fixed to Viewable")
            
                sopClassCategoryCount[sopClassUID] += 1 # for overlaps
                
                for prop in subTypeInfo:
                    if re.match(r'_', prop):
                        continue
                    propCountsNRN[prop] += subTypeInfo[prop]["count"]
                
                totalDICOMNRN += subTypeInfo["_total"]
                totalDICOM += subTypeInfo["_total"]
            
                for patientRef in subTypeInfo["patient"]["byValueCount"]:
                    patientNRN.add(patientRef)
                    patients.add(patientRef)
            
                countBySpecIndexBySOPClassNRN[sopClassUID][specSubSpecIndexLabel] += subTypeInfo["_total"]

                # Note: assuming separate groups if separate SPEC INDEX 
                countGroupRefsBySOPClassNRN[sopClassUID] += subTypeInfo["group_parent"]["rangeCount"] if "rangeCount" in subTypeInfo["group_parent"] else len(subTypeInfo["group_parent"]["byValueCount"])
            
                if "parent_data_file" in subTypeInfo:
                    bvc = subTypeInfo["parent_data_file"]["byValueCount"]
                    for pdf in bvc:
                        countByPDFBySOPClassNRN[sopClassUID][pdf.split(" [")[0]] += bvc[pdf]
                else:
                    countByPDFBySOPClassNRN[sopClassUID]["NOTSET"] += subTypeInfo["_total"]
                
            # Third: not RAD/NUC and (NOT from DICOM Gateway) Capture Application
            # - Mix of status: Viewable but others too
            # - Only SOP UID (which is set) fits here
            #      VL Photographic Image Storage [1.2.840.10008.5.1.4.1.1.77.1.4]
            else: # NRNCA
            
                if not (
                    sopClassUID in ["1.2.840.10008.5.1.4.1.1.77.1.4", "NOTSET"] and
                    
                    singleValue(subTypeInfo, "capture_application", "NOTSET") == "C:Capture Workstation"
                ):
                    raise Exception("Expect all NRNCA to be UID 1.2.840.10008.5.1.4.1.1.77.1.4 or NONE and as not DICOM Gateway to be CAPTURE APPLICATION")
            
                sopClassCategoryCount[sopClassUID] += 1 # for overlaps
                
                for prop in subTypeInfo:
                    if re.match(r'_', prop):
                        continue
                    propCountsNRNCA[prop] += subTypeInfo[prop]["count"]
                
                totalDICOMNRNCA += subTypeInfo["_total"]
                totalDICOM += subTypeInfo["_total"]
                
                for patientRef in subTypeInfo["patient"]["byValueCount"]:
                    patientNRNCA.add(patientRef)
                    patients.add(patientRef)
            
                countBySpecIndexBySOPClassNRNCA[sopClassUID][specSubSpecIndexLabel] += subTypeInfo["_total"]

                # Note: assuming separate groups if separate SPEC INDEX 
                # Saw missing in PUG - seemed to be a test image(s) 
                if "group_parent" in subTypeInfo: 
                    countGroupRefsBySOPClassNRNCA[sopClassUID] += subTypeInfo["group_parent"]["rangeCount"] if "rangeCount" in subTypeInfo["group_parent"] else len(subTypeInfo["group_parent"]["byValueCount"])
            
                if "parent_data_file" in subTypeInfo:
                    bvc = subTypeInfo["parent_data_file"]["byValueCount"]
                    for pdf in bvc:
                        countByPDFBySOPClassNRNCA[sopClassUID][pdf.split(" [")[0]] += bvc[pdf]
                else:
                    countByPDFBySOPClassNRNCA[sopClassUID]["NOTSET"] += subTypeInfo["_total"]
                    
                status = singleValue(subTypeInfo, "status", "NOTSET")
                countByStatusBySOPClassNRNCA[sopClassUID][status] += subTypeInfo["status"]["byValueCount"][status]
                
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    if not os.path.isdir(userSiteDir):
        raise Exception("Expect User Site to already exist with its basic contents")
        
    title = "Imaging [DICOM]".format(stationNo)
    mu = TOP_MD_TEMPL.format(title, "DICOM Images")
                                    
    sopClassCoverageQualifier = ""
    if not allSOPClassed:
        sopClassCoverageQualifier = " nearly "    
    mu += """Of the <span class='yellowIt'>{:,}</span> images added to this VistA between _{}_ and _{}_, a three year span, the <span class='yellowIt'>{}</span> DICOM Images represent the vast majority. They are for <span class='yellowIt'>{:,}</span> patients and {}all are tagged with a \"SOP Class\". Three categories of DICOM image are detailed below and note that should a SOP Class belong to more than one category, its name is rendered in bold. 
 
""".format(
        allTypeData["_total"],
        overallFirstCreateDate,
        overallLastCreateDate,
        reportAbsAndPercent(totalDICOM, allTypeData["_total"]),
        len(patients),
        sopClassCoverageQualifier
    )
    
    # Bolds if class appears in more than one of the three categories
    def muSOPClass(sopClassUID):
        if sopClassUID != "NOTSET":
            labelMU = "__{}__".format(dicomSOPClassNameByUID[sopClassUID]) if sopClassCategoryCount[sopClassUID] > 1 else dicomSOPClassNameByUID[sopClassUID]
            labelMU = "{} [{}]".format(labelMU, sopClassUID)
        else:
            labelMU = "NOTSET"
        return labelMU
        
    def muCounter(counter):
        if len(counter) > 1:
            cmu = ", ".join(["{} [{:,}]".format(k.split(":")[1] if re.search(r':', k) else k, counter[k]) for k in sorted(counter, key=lambda x: counter[x], reverse=True)])
        else:
            k = list(counter)[0]
            cmu = k if not re.search(r':', k) else k.split(":")[1]      
        return cmu
        
    """
    First: RAD/NUC (and DICOM Gateway)
    """
    mu += """The majority of DICOM Images, <span class='yellowIt'>{}</span>, are classed as _RADIOLOGY_ or _NUCLEAR MEDICINE_ and cover <span class='yellowIt'>{}</span> patients. All are referenced from Radiology Reports and imported using _DICOM Gateway_. A \"pacs procedure\" is specified for all these images. Note that apart from references from Radiology Reports, the System maintains these images in groups (\"XRAY GROUP\") ..."
    
""".format(
        reportAbsAndPercent(totalDICOMRN, totalDICOM),
        reportAbsAndPercent(len(patientRN), len(patients))
    )
    tbl = MarkdownTable(["SOP Class", "Count", "Class(es)", "Radiology Report Referrers", "Groups", "PACS Procedure Types"])
    for sopClassUID in sorted(countBySpecIndexBySOPClassRN, key=lambda x: sum(countBySpecIndexBySOPClassRN[x][y] for y in countBySpecIndexBySOPClassRN[x]), reverse=True):
        thisTotal = sum(countBySpecIndexBySOPClassRN[sopClassUID][x] for x in countBySpecIndexBySOPClassRN[sopClassUID])
        tbl.addRow([
            muSOPClass(sopClassUID),
            reportAbsAndPercent(thisTotal, totalDICOMRN),
            muCounter(countBySpecIndexBySOPClassRN[sopClassUID]),
            len(radRepRefsBySOPClass[sopClassUID]),
            countGroupRefsBySOPClassRN[sopClassUID],
            len(countByPacsProcBySOPClass[sopClassUID])
        ])
    mu += tbl.md() + "\n\n"
    
    """
    Second: not RAD/NUC but from DICOM Gateway
    """
    mu += """Most other DICOM Images, <span class='yellowIt'>{}</span>, are also entered through the DICOM Gateway and cover <span class='yellowIt'>{}</span> patients. They either go unreferenced, are referenced by a temporary holding file (\"DICOM GMRC TEMP LIST\") or from TIU Notes. They cover Ophthalmology, Dentistry and Vascular measurement. Some of these SOP Classes (in bold) are also used for the Radiology images detailed above ...
    
""".format(
        reportAbsAndPercent(totalDICOMNRN, totalDICOM),
        reportAbsAndPercent(len(patientNRN), len(patients))
    )
    tbl = MarkdownTable(["SOP Class", "Count", "Class(es)", "Referrers", "Groups"])
    for sopClassUID in sorted(countBySpecIndexBySOPClassNRN, key=lambda x: sum(countBySpecIndexBySOPClassNRN[x][y] for y in countBySpecIndexBySOPClassNRN[x]), reverse=True):
    
        thisTotal = sum(countBySpecIndexBySOPClassNRN[sopClassUID][x] for x in countBySpecIndexBySOPClassNRN[sopClassUID])
                
        tbl.addRow([
            muSOPClass(sopClassUID),
            reportAbsAndPercent(thisTotal, totalDICOMNRN),
            muCounter(countBySpecIndexBySOPClassNRN[sopClassUID]),
            muCounter(countByPDFBySOPClassNRN[sopClassUID]),
            countGroupRefsBySOPClassNRN[sopClassUID]
        ])
    mu += tbl.md() + "\n\n"
    
    """
    Third: Not RAD/NUC and not from DICOM Gateway
    
    Either SOP 1.2.840.10008.5.1.4.1.1.77.1.4 or NO SOP 
    """
    if set(countBySpecIndexBySOPClassNRNCA) == set(["1.2.840.10008.5.1.4.1.1.77.1.4"]):
        sopClassMsg = "They all share the same SOP Class, _VL Photographic Image Storage [1.2.840.10008.5.1.4.1.1.77.1.4]_"
    else:
        sopClassMsg = "Where SOP Class is set, it is always, _VL Photographic Image Storage [1.2.840.10008.5.1.4.1.1.77.1.4]_"
    mu += """The remaining DICOM Images, <span class='yellowIt'>{}</span>, are imported using \"Capture Application\" and cover <span class='yellowIt'>{}</span> patients. {}. References are like those of their non RADIOLOGY peers but these images have a tracked status value too. That status captures whether they are viewable of not ..."
    
""".format(
        reportAbsAndPercent(totalDICOMNRNCA, totalDICOM),
        reportAbsAndPercent(len(patientNRNCA), len(patients)),
        sopClassMsg
    )
    
    tbl = MarkdownTable(["SOP Class", "Count", "Class(es)", "Referrers", "Groups", "Status"], includeNo=False)
    for sopClassUID in sorted(countBySpecIndexBySOPClassNRNCA, key=lambda x: sum(countBySpecIndexBySOPClassNRNCA[x][y] for y in countBySpecIndexBySOPClassNRNCA[x]), reverse=True):
    
        thisTotal = sum(countBySpecIndexBySOPClassNRNCA[sopClassUID][x] for x in countBySpecIndexBySOPClassNRNCA[sopClassUID])
                
        tbl.addRow([
            muSOPClass(sopClassUID),
            reportAbsAndPercent(thisTotal, totalDICOMNRNCA),
            muCounter(countBySpecIndexBySOPClassNRNCA[sopClassUID]),
            muCounter(countByPDFBySOPClassNRNCA[sopClassUID]),
            countGroupRefsBySOPClassNRNCA[sopClassUID],
            muCounter(countByStatusBySOPClassNRNCA[sopClassUID])
        ])
    mu += tbl.md() + "\n\n"
    
    """
    TODO: overlap section - give overlap with other known systems but qualify when those were cut. Give exclusive to this and its overlaps and total overall.
    """
    
    """
    TODO: AC DEV's 
    
    and note dominantly [3] is Dermatology ...
    
    VL Photographic Image Storage [1.2.840.10008.5.1.4.1.1.77.1.4]
    """
    
    """
    TODO: acquisition_site
    """
     
    # Output   
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "imagingDICOM.md", "w").write(mu)
    
"""
Beyond DICOM
"""
def webReportYR3Other(stationNo): 
    allTypeData, subTypeDatas = splitTypeDatas(stationNo, "2005", reductionLabel="YR3", expectSubTypeProperty="object_type-capture_application-dicom_sop_class-spec_subspec_index")
    
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

    webReportImaging(stationNo)
                 
if __name__ == "__main__":
    main()
