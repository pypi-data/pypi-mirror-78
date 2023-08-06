#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime
import platform

from fmqlutils import VISTA_DATA_BASE_DIR
from fmqlutils.reporter.reportUtils import MarkdownTable, reportAbsAndPercent, muBVC
from fmqlreports.webReportUtils import reduce2

from fileDirectory import VISN20_VISTAS # TMP - move to webReportUtils
from userDirectory import CommonUserDirectory

"""
TODO:
- more on dumpIdIssues to tighten matches
- feed into matrix (by date) of yearly activity in key areas => current or not
  ... see: https://towardsdatascience.com/3-python-visualization-libraries-you-must-know-as-a-data-scientist-8d0cd25e1c73 at end on missingno and it showing nulls ... 
- feed back the UserDirectory -- may do common base class.
"""

class CommonPatientDirectory():

    ENTRY_FICN_IDX = 6
    ENTRY_ICN_IDX = 7
    ENTRY_SSN_IDX = 8
    ENTRY_PLID_IDX = 9
    ENTRY_SCN_IDX = 10
    
    IDINFOs = [
        (ENTRY_FICN_IDX, "FICN"),
        (ENTRY_ICN_IDX, "ICN"),
        (ENTRY_SSN_IDX, "SSN"),
        (ENTRY_PLID_IDX, "PLID"),
        (ENTRY_SCN_IDX, "SCN"),
    ]

    def __init__(self, vistaSNOs, userDirectory=None):
        self.__vistaSNOs = vistaSNOs
        self.__dirFile = f'{VISTA_DATA_BASE_DIR}Common/Directory/PDIR.json'
        try:
            print("Attempting to load preexisting Patient Directory")
            self.__pdirInfo = json.load(open(self.__dirFile))
        except:
            print("Starting Directory from Scratch")
            self.__pdirInfo = {"vistas": [], "entries": {}, "patients": []}
        else:
            print("Loaded preexisting directory with {:,} patients".format(len(self.__pdirInfo["patients"])))
        self.__changeUpdate(userDirectory)
        
    def report(self):
        mu = self.__report()
        return(mu)
        
    # ################## All Directory Accessors ######################
    # ... same as UserDirectory -- belongs in common base
        
    def vistas(self):
        return self.__pdirInfo["vistas"]
        
    # To see, per station, add stationNo
    def total(self, stationNo=""):
        if stationNo == "":
            return len(self.__pdirInfo["patients"])
        return sum(1 for patient in self.__pdirInfo["patients"] if sum(1 for gien in patient if gien.split(":")[0] == stationNo))
        
    def entryTotal(self, stationNo=""):
        if stationNo == "":
            return len(self.__pdirInfo["entries"])
        return sum(1 for gien in self.__pdirInfo["entries"] if gien.split(":")[0] == stationNo)
                    
    """
    Presence of SSN etc in one or more entries of patients
    
    To see SSN
        noW, noWGT1 = .idPresence(CommonUserDirectory.ENTRY_SSN_IDX)
    same for ENTRY_SECID_IDX, ENTRY_NWNM_IDX, ENTRY_DUID_IDX
    """
    def idPresence(self, entryIdx, gt1=False):
        noW = 0
        noWGT1 = 0
        for i, patient in enumerate(self.__pdirInfo["patients"], 1):
            vals = set(self.__pdirInfo["entries"][gien][entryIdx] for gien in patient if self.__pdirInfo["entries"][gien][entryIdx])
            if len(vals):
                noW += 1
                if len(vals) > 1:
                    noWGT1 += 1
        return noWGT1 if gt1 else noW
        
    """
    Number w/o any ID
    """
    def noIds(self):
        cnt = 0
        for i, patient in enumerate(self.__pdirInfo["patients"], 1):
            has = False
            for gien in patient:
                if sum(1 for idx in [
                    CommonPatientDirectory.ENTRY_FICN_IDX,
                    CommonPatientDirectory.ENTRY_ICN_IDX,
                    CommonPatientDirectory.ENTRY_SSN_IDX,
                    CommonPatientDirectory.ENTRY_PLID_IDX,
                    CommonPatientDirectory.ENTRY_SCN_IDX
                ] if self.__pdirInfo["entries"][gien][idx]):
                    has = True
                    break
            if has == False:
                cnt += 1
        return cnt
        
    def gt1VistACount(self):
        cnt = 0
        for i, patient in enumerate(self.__pdirInfo["patients"], 1):
            snos = set(gien.split(":")[0] for gien in patient)         
            if len(snos) > 1:
                cnt += 1
        return cnt  
        
    def commonCounts(self, stationNo=""):
        """
        By count of vista's patients are in, count types ex/
            4: 500 <---- in 4 VistAs
            3: 400 <---- in 3 VistAs
            ...
        
        Arguments:
        - stationNo: only do for files of one VistA

        For Plot: the common/plotCategoryBSV Plot and Explanation
        """
        commonCount = Counter()
        for patient in self.__pdirInfo["patients"]:
            stationNos = set(gien.split(":")[0] for gien in patient)
            if stationNo and stationNo not in stationNos:
                continue
            commonCount[len(stationNos)] += 1
        return commonCount # may not be in order ie/ 3, 1, 4, 2, ...
        
    """
    For a given id - ex SSN - return all values.

    Use: entryIDX = CommonPatientDirectory.ENTRY_FICN_IDX ... ENTRY_ICN_IDX, 
    ENTRY_SSN_IDX, ENTRY_PLID_IDX, ENTRY_SCN_IDX
    """
    def idValues(self, entryIdx):
        allVals = set()
        for i, patient in enumerate(self.__pdirInfo["patients"], 1):
            vals = set(entries[gien][entryIdx] for gien in patient if self.__pdirInfo["entries"][gien][entryIdx])
            allVals |= vals
        return allVals
        
    # ###################### Specifics #################
                        
    def deceased(self): # if any record marks individual as deceased then true
        cnt = 0
        for i, patient in enumerate(self.__pdirInfo["patients"], 1):
            has = False
            for gien in patient:
                if self.__pdirInfo["entries"][gien][5] == "Y":
                    has = True
                    break
            if has:
                cnt += 1
        return cnt
        
    def usersToo(self):
        if "sameAsUserBySSN" not in self.__pdirInfo:
            raise Exception("no sameUser calc for pdir so can't do Users Too")
        return len(self.__pdirInfo["sameAsUserBySSN"])
        
    def males(self): # all must be male
        cnt = 0
        for i, patient in enumerate(self.__pdirInfo["patients"], 1):
            sexes = set([self.__pdirInfo["entries"][gien][2] for gien in patient if self.__pdirInfo["entries"][gien][2]])
            if len(sexes) != 1:
                continue
            if list(sexes)[0] == "M":
                cnt += 1
        return cnt
        
    # ###################### Others (clean up) ####################
        
    """
    For time graphing
    
    TODO: may pad and guess for no dates that == between next ahead and last behind
    
    Big "NO DATE" problem ... 
    - 159K out of 960K Patients
    - 100K of 515K entries in PUG etc
    """
    def entryDatesBySNO(self):
        dtBySNO = defaultdict(list)
        entries = self.__pdirInfo["entries"]
        entryWODateBySNO = Counter()
        for gien in entries:
            entry = entries[gien]
            sno = gien.split(":")[0]
            if entry[3] == "": 
                entryWODateBySNO[sno] += 1
                continue
            dtBySNO[sno].append(entry[3])
        # Crude - ignoring order of orders - just resorting
        for sno in dtBySNO:
            dtBySNO[sno] = sorted(dtBySNO[sno])
        dtPatients = []
        for patient in self.__pdirInfo["patients"]:
            entriesSDT = sorted([self.__pdirInfo["entries"][gien][3] for gien in patient if self.__pdirInfo["entries"][gien][3]])
            if len(entriesSDT) == 0:
                entryWODateBySNO["PATIENT"] += 1
                continue
            dtPatients.append(entriesSDT[0]) # take first date of the patient
        dtBySNO["PATIENT"] = dtPatients # overall uniques
        print("Serializing dates by station + PATIENT overall:")
        for snop in dtBySNO:
            print("\t{}: {:,} - no date {:,}".format(snop, len(dtBySNO[snop]), entryWODateBySNO[snop]))
        return dtBySNO
        
    """
    Simple lookup by GIEN
    """
    def lookupEntryByGIEN(self, gien):
        self.__pdirInfo["entries"].get(gien, None)
        
    """
    Full (flat) lookup by GIEN
    """
    def lookupFPatientByGIEN(self, gien):
        try:
            self.__byGIEN
        except:
            patientsFlat = self.__flattenPatients()
            self.__byGIEN = {}
            for i, pf in enumerate(patientsFlat):
                for gien in pf[0]:
                    self.__byGIEN[gien] = (i, pf)
        if gien in self.__byGIEN:
            idx, pf = self.__byGIEN[gien]
            sameAsIDX = True if idx in self.__pdirInfo["sameAsUserBySSN"] else False
            pf.append(sameAsIDX)
            return pf
        return None
        
    """
    QA Dump: ID issues
    
    Total: 574
    W One Name ...: 280
    W Many Sexes ...: 85 <---- should break and ignore SSN match? TODO
    
    TODO:
    - more on multi SSNs
    - tie into deceased
    """
    def dumpIdIssues(self):
        mu = "## ID Issues - > 1 GICN\n"
        cntMFICNs = 0
        cntSameName = 0
        cntMultiSexes = 0
        patientsFlat = self.__flattenPatients()
        for pf in patientsFlat:
            if pf[CommonPatientDirectory.ENTRY_FICN_IDX] and len(pf[CommonPatientDirectory.ENTRY_FICN_IDX]) > 1:
                cntMFICNs += 1
                if len(pf[1]) == 1 or len(set(name.split(",")[0] for name in pf[1])) == 1:
                    cntSameName += 1
                if len(pf[2]) == 2:
                    cntMultiSexes += 1
        mu += "Total: {:,}\n".format(cntMFICNs)
        mu += "W One Name or Same Last Name (good indication that right): {:,}\n".format(cntSameName)
        mu += "W Many Sexes (strong mismatch?): {:,}\n".format(cntMultiSexes)
        print(mu)
        
    """
    Subset - used by TeleReader to produce sub directory (which it de-identifies)
    
        from deid import IDMaker, NameMaker
        sdeid = cpd.subsetNDEID(allGIENs, IDMaker(), NameMaker())
        
    Bonus: keeps ZZ if in original name AND leaves machine names (XX,PATIENT...) as is
    
    Handles (as here or DEID does)
    - middle initial or full middle name or no middle at all 
    - gender appropriate first and middle names
    - suffix (JR, II) of 2 part or three part names
    
    Doesn't handle (DEID doesn't or this doesn't)
    - > 3 elements (other than JR, SR, I, II ...)
    
    Roughly same as User Equivalent.
    
    TODO: could move to simpler, get name form from firstEntry as ALL ENTRIES seem
    to have same name (unlike User). Must re-inforce in Patient Report First.
    """
    def subsetNDEID(self, patientGIENs, idMaker, nameMaker):
        npatients = []
        nentries = {}
        snos = set()
        for i, patient in enumerate(self.__pdirInfo["patients"]):
            if len(patientGIENs) and sum(1 for gien in patient if gien in patientGIENs) == 0:
                continue
            # TODO: add to nameMaker to reuse names already given to same patient
            if i in self.__pdirInfo["sameAsUserBySSN"]:
                raise Exception("Haven't a/ced for Patient same as User in DEID name yet")
            npatients.append(patient)
            fentry = self.__pdirInfo["entries"][patient[0]]
            sexes = set([self.__pdirInfo["entries"][gien][2] for gien in patient if self.__pdirInfo["entries"][gien][2]])
            if len(sexes) > 1:
                raise Exception("Can't de id with SEX as > 1 Sex for a patient")
            if len(sexes) == 0:
                sex = "female" if randint(1, 5) == 1 else "male" # 20% female
                print("** sexless patient: {} - picking {} (Female 20%)".format(self.__pdirInfo["entries"][patient[0]][1], sex))
            else:
                sex = "male" if list(sexes)[0] == "M" else "female"
            keepOrigName = True if re.search(r'(PATIENT|TEST|\,VET)', fentry[1]) else False
            if not keepOrigName:    
                sname, iname, fname = nameMaker.getPatientNames(gender=sex, originalName=fentry[1]) 
                namesUsed = set() # see if Patient, like User varies - doesn't seem to
            else:
                print("** Keeping Original Patient Name {}".format(fentry[1]))
            warned = False
            for gien in patient:
                snos.add(gien.split(":")[0])
                entry = self.__pdirInfo["entries"][gien]
                nentries[gien] = entry
                for idxd in CommonPatientDirectory.IDINFOs:
                    if entry[idxd[0]] == "":
                        continue
                    if idxd[1] in ["SSN", "FICN", "ICN"]:
                        entry[idxd[0]] = idMaker.nextID(idxd[1], entry[idxd[0]])
                        continue
                    # PLID, SCN as ignoring for now
                    entry[idxd[0]] = "Y" # TODO
                if keepOrigName:
                    continue
                origName = entry[1]
                namesUsed.add(origName)
                pieces = re.split(r',| ', origName)
                suffix = ""
                if pieces[-1] in ["SR", "JR", "I", "II", "III", "IV", "V"]:
                    suffix = pieces.pop()
                # May be crude but nixing last bit of "SMITH JAMES L K" etc.
                if len(pieces) > 3:
                    if not warned:
                        print("** Warning - DEID Patient Name {} doesn't account for its length - taking it as a three long name".format(origName))
                        warned = True # only warn once
                    while len(pieces) > 3:
                        pieces.pop()
                if len(pieces) == 3:
                    entry[1] = iname if len(pieces[2]) == 1 else fname
                else:
                    entry[1] = sname
                if suffix:
                    entry[1] = "{} {}".format(entry[1], suffix) 
                if re.match(r'ZZ', origName):
                    entry[1] = "ZZ{}".format(entry[1])
                    print("** Putting back ZZ on patient name: {} - {}".format(origName, entry[1]))
            # MAY USE THIS TO SIMPLIFY THE ABOVE ie/ firstEntry good enough for name calc
            if len(namesUsed) > 1:
                raise Exception("Enforcing - though not relying on - that Patient has same name across entries")
        print("Returning {:,} entries and {:,} patients from Patient Directory{}".format(len(nentries), len(npatients), " [DEIDENTIFIED]" if nameMaker else ""))
        nvistas = [vinfo for vinfo in self.__pdirInfo["vistas"] if vinfo["stationNumber"] in snos]
        return {"vistas": nvistas, "entries": nentries, "patients": npatients}
        
    # REM: gien is a patient gien
    def sameAsUser(self, gien):
        patientsFlat = self.__flattenPatients()
        for idx in self.__pdirInfo["sameAsUserBySSN"]:
            pf = patientsFlat[int(idx)]
            if gien in pf[0]:
                return idx
        return ""
        
    # ########################## Report #####################
    
    """
    TODO: 
    - re-inforce in all entries for Patient have same name ie/ entry[1] the same.
    Seems to be true in deid above but see if generally so and if not, count the 
    exceptions (different from variation counter for users! ie/ much more Patient
    grooming/management)
    - isolate the synth and machine patients (ZZTEST ...?)
    """
    def __report(self, userGIENs=None):

        patientsFlat = self.__flattenPatients()
        entries = self.__pdirInfo["entries"].values()
                
        mu = ""
        mu += "# Cross-VistA Patient Directory\n\n"
        mu += "The following reports on a __Cross-VistA Patient Directory__ built from the Patient file (2) of <span class='yellowIt'>{:,}</span> VistAs, {}. Together they hold <span class='yellowIt'>{:,}</span> distinct patients.\n\n".format(
            len(self.__vistaSNOs), 
            ", ".join(["{} [{}]".format(self.__vistaSNOs[sno], sno) for sno in sorted(self.__vistaSNOs, key=lambda x: int(x))]),
            len(patientsFlat)
        )
        
        tbl = MarkdownTable([":Property", "Value"], includeNo=False)

        tbl.addRow(["Records", "{:,}".format(len(entries))])
        # Focus back on source records (may go in a final report)
        cntRecordBySNO = Counter()
        cntDTOutOfOrderBySNO = Counter()
        ienAndDTBySNO = defaultdict(list)  
        woDateBySNO = Counter() 
        wDeceasedBySNO = Counter()    
        for entry in entries:
            sno = entry[0].split(":")[0]
            cntRecordBySNO[sno] += 1
            if entry[5] == "Y":
                wDeceasedBySNO[sno] += 1
            if entry[3]:
                if len(ienAndDTBySNO[sno]) and entry[3] < ienAndDTBySNO[sno][-1]: 
                    cntDTOutOfOrderBySNO[sno] += 1
                ienAndDTBySNO[sno].append(entry[3])
            else:
                woDateBySNO[sno] += 1
        tbl.addRow([
            "Record per VistA", 
            muBVC(cntRecordBySNO)
        ])
        tbl.addRow([
            "Record with deceased indicated", 
            muBVC(wDeceasedBySNO)
        ])
        tbl.addRow([
            "Record w/o Date", 
            muBVC(woDateBySNO)
        ])
        tbl.addRow([
            "Record date out of order", 
            muBVC(cntDTOutOfOrderBySNO)
        ])
        tbl.addRow([
            "Record w/ names begin with ZZ (Deleted?)", 
            reportAbsAndPercent(
                sum(1 for entry in entries if re.match(r'ZZ', entry[1])),
                len(entries)
            )
        ])
         
        tbl.addRow(["Patients", "{:,}".format(len(patientsFlat))])
        tbl.addRow([
            "In more than VistA", 
            reportAbsAndPercent(
                sum(1 for pf in patientsFlat if len(set(e.split(":")[0] for e in pf[0])) > 1),
                len(patientsFlat)
            )
        ])
        tbl.addRow([
            "> 1 Record in an individual VistA", 
            reportAbsAndPercent(
                sum(1 for pf in patientsFlat if len(set(e.split(":")[0] for e in pf[0])) < len(pf[0])),
                len(patientsFlat)
            )
        ])
        tbl.addRow([
            "W/ Pseudo SSN", 
            reportAbsAndPercent(
                sum(1 for pf in patientsFlat if pf[CommonPatientDirectory.ENTRY_SSN_IDX] and sum(1 for e in pf[CommonPatientDirectory.ENTRY_SSN_IDX] if re.search(r'P$', e))),
                len(patientsFlat)
            ) 
        ])
        tbl.addRow([
            "Male", 
            reportAbsAndPercent( # not QA'ing > 1 val but should?
                sum(1 for pf in patientsFlat if pf[2] and pf[2][0] == "M"),
                len(patientsFlat)
            ) 
        ])
        tbl.addRow([
            "W/ deceased indicated somewhere", 
            reportAbsAndPercent(
                sum(1 for pf in patientsFlat if pf[5]),
                len(patientsFlat)
            ) 
        ])
        for idInfo in CommonPatientDirectory.IDINFOs:
            tbl.addRow([
                "Has {}".format(idInfo[1]),
                "{} [> 1 {:,}]".format(
                    reportAbsAndPercent(
                        sum(1 for pf in patientsFlat if pf[idInfo[0]]),
                        len(patientsFlat)
                    ),
                    sum(1 for pf in patientsFlat if pf[idInfo[0]] and len(pf[idInfo[0]]) > 1))
            ])
        tbl.addRow([
            "No ID", 
            reportAbsAndPercent(
                sum(1 for pf in patientsFlat if sum(1 for i in range(CommonPatientDirectory.ENTRY_FICN_IDX, len(pf)) if pf[i]) == 0),
                len(patientsFlat)
            )
        ])
        if "sameAsUserBySSN" in self.__pdirInfo:
            tbl.addRow(["Patients that are users ('sameAs')", reportAbsAndPercent(len(self.__pdirInfo["sameAsUserBySSN"]), len(patientsFlat))])
        mu += tbl.md() + "\n\n"
        
        patientCountPerVistA = Counter()
        recordCountPerVistA = Counter()
        recordCountPerPatientCount = Counter()
        perSNOHowMany = defaultdict(Counter)
        for pf in patientsFlat:
            recordCountPerPatientCount[len(pf[0])] += 1
            snos = set(gien.split(":")[0] for gien in pf[0])
            for sno in snos:
                patientCountPerVistA[sno] += 1
                recordCountPerVistA[sno] += len([gien for gien in pf[0] if re.match(sno, gien)])     
                perSNOHowMany[sno][len(snos)] += 1
        mu += "Per VistA ...\n\n"
        tbl = MarkdownTable([":VistA", "Patients", "Records"], includeNo=False)
        for sno in sorted(patientCountPerVistA, key=lambda x: patientCountPerVistA[x], reverse=True):
            tbl.addRow([
                "__{} [{}]__".format(self.__vistaSNOs[sno], sno),
                reportAbsAndPercent(patientCountPerVistA[sno], len(patientsFlat)),
                reportAbsAndPercent(recordCountPerVistA[sno], len(entries))
            ])  
        mu += tbl.md() + "\n\n"
        
        mu += "Across the {:,} VistAs, individual patients have the following number of records. For example, a count for 3 records indicates how many patients have 3 records ...\n\n".format(len(self.__pdirInfo["vistas"]))
        tbl = MarkdownTable([":Records", "Patient"], includeNo=False)
        for cnt in sorted(recordCountPerPatientCount, key=lambda x: recordCountPerPatientCount[x], reverse=True):
            tbl.addRow([
                "__{}__".format(cnt), 
                reportAbsAndPercent(recordCountPerPatientCount[cnt], len(patientsFlat))
            ])
        mu += tbl.md() + "\n\n"
        
        mu += "The following shows how many other VistAs also hold a patient of a VistA. Note that dominant VistAs have proportionately higher single VistA counts - they alone hold certain patients. Smaller VistAs contain patients that also in other VistAs - they are less likely to be the only VistA with a patient.\n\n"
        cols = [":VistA"]
        for i in range(1, len(patientCountPerVistA) + 1):
            cols.append(str(i))
        tbl = MarkdownTable(cols, includeNo=False)
        for sno in sorted(perSNOHowMany, key=lambda x: sum(cnt for cnt in perSNOHowMany[x].values()), reverse=True):
            row = ["__{} [{}]__".format(self.__vistaSNOs[sno], sno)]
            for i in range(1, len(patientCountPerVistA) + 1):
                if i not in perSNOHowMany[sno]:
                    row.append("")
                    continue
                row.append(reportAbsAndPercent(perSNOHowMany[sno][i], patientCountPerVistA[sno]))
            tbl.addRow(row)
        mu += tbl.md() + "\n\n"
        
        open("patientDirectoryReportN.md", "w").write(mu)
        
        return mu
        
    # ########################## Flatten Records ######################
    
    """
    Merges entries - replaces gien at start with plain sno
    """
    def __flattenPatients(self):
        if "patientsFlat" in self.__pdirInfo:
            return self.__pdirInfo["patientsFlat"]
        print("Flattening patients ...")
        self.__pdirInfo["patientsFlat"] = []            
        for patient in self.__pdirInfo["patients"]:
            for i, gien in enumerate(patient):
                entry = self.__pdirInfo["entries"][gien]
                if i == 0:
                    patientFlat = [[e] if e != "" else None for e in entry]
                    continue
                for j in range(0, len(patientFlat)):
                    if entry[j] == "":
                        continue
                    if patientFlat[j] == None:
                        patientFlat[j] = [entry[j]]
                        continue
                    if entry[j] in patientFlat[j]:
                        continue
                    patientFlat[j].append(entry[j])
                    patientFlat[j] = sorted(patientFlat[j])
            self.__pdirInfo["patientsFlat"].append(patientFlat)
        print("... finished")
        return self.__pdirInfo["patientsFlat"]
            
    # ########################## CHANGE / UPDATE ######################
            
    def __changeUpdate(self, userDirectory=None):
        changed = self.__fillFromAvailable()
        if changed:
            print("Changed - so rebuilding patients")
            self.__rebuildPatients()
            if "sameAsUserBySSN" in self.__pdirInfo: # set for update
                del self.__pdirInfo["sameAsUserBySSN"]    
        if userDirectory and "sameAsUserBySSN" not in self.__pdirInfo:
            self.__sameAsToUserDirectory(userDirectory)
            changed = True
        if changed:
            self.__flush()    
            self.dumpIdIssues()
                                
    def __fillFromAvailable(self):
        def reduceRed2Further(stationNo, red2):
            entry = []
            props = [
                ["gien", "{}:{}".format(stationNo, red2["ien"])], 
                "name", 
                ["sex", red2["sex"].split(":")[0] if "sex" in red2 else ""],
                "date_entered_into_file", 
                "preferred_facility", 
                ["dead", "Y" if ("date_of_death" in red2 or "death_entered_by" in red2) else ""], 
                "full_icn", 
                "integration_control_number", 
                "social_security_number", 
                "primary_long_id", 
                "subscription_control_number"
            ]
            for prop in props:
                if isinstance(prop, list):
                    entry.append(prop[1])
                    continue
                entry.append(red2.get(prop, ""))
            return entry
            
        changed = False
        for stationNo in self.__vistaSNOs:
            if sum(1 for vistaInfo in self.__pdirInfo["vistas"] if vistaInfo["stationNumber"] == stationNo):
                print("\t{} already in Directory - skipping".format(stationNo))
                continue
            try:
                patientInfoByIEN = reduce2(stationNo)    
            except:
                print("Can't load Patient Reduction for {} as not available/creatable here".format(stationNo))
                raise
            changed = True
            print("Loaded Patients for {}: {:,}".format(stationNo, len(patientInfoByIEN)))
            print("Adding {} to directory".format(stationNo))
            for ien in patientInfoByIEN:
                red2 = patientInfoByIEN[ien]
                entry = reduceRed2Further(stationNo, red2)
                self.__pdirInfo["entries"][entry[0]] = entry
            self.__pdirInfo["vistas"].append({"stationNumber": stationNo, "dateAdded": str(datetime.now()).split(" ")[0]})
        return changed
        
    """
    Any entries that share the same FICN, ICN (FICN missing) or SSN (non P)
    - for now, not using primary_long_id (only left if different from social with -'s)
    - primary_short_id == last 4 of social, again only for ref.
    
    Alg: establish patients based on all ids of each entry, consistently
    - if id already allocated to use (by previous entry) then reuse that Patient (WARN as unusual for Patient)
    - need two passes as if entry has > 1 id, different ones may have been
    allocated to separate users by previous entries that didn't share the same
        id combo (entry with only SSN, then one with only ICN, then one with both)
    - second pass must see indexes that need to be combined

    Note: allows for many entries for a single Patient in a VistA (based on two
    key ids - FICN, ICN (small part - few), SSN (non P)
    """
    def __rebuildPatients(self):
        del self.__pdirInfo["patients"]
        
        patientIndexesByGID = defaultdict(set)
        patients = [] # no fixed entries unlike user
        for gien in self.__pdirInfo["entries"]:
        
            entry = self.__pdirInfo["entries"][gien]

            # may have > 1 idx as diff ids may appear w/o each other in earlier entries
            patientIndexes = set() 
            gids = set()
            # No PLID or SCN for now
            for idxd in [(CommonPatientDirectory.ENTRY_FICN_IDX, "FICN"), (CommonPatientDirectory.ENTRY_ICN_IDX, "ICN"), (CommonPatientDirectory.ENTRY_SSN_IDX, "SSN")]:  
                if entry[idxd[0]] == "":
                    continue
                if idxd[1] == "SSN" and not re.match(r'\d{9}$', entry[idxd[0]]):
                    continue # P SSN or other invalid
                gid = "{}:{}".format(idxd[1], entry[idxd[0]])
                gids.add(gid)
                if gid in patientIndexesByGID:
                    patientIndexes.add(patientIndexesByGID[gid][0])                   
            if len(patientIndexes) == 0:
                patientIndexes = set([len(patients)])
                patients.append([])
            patientIndex = sorted(list(patientIndexes))[0] # pick first
            patients[patientIndex].append(gien)
            for gid in gids: 
                if gid not in patientIndexesByGID:
                    patientIndexesByGID[gid] = [patientIndex] 
                    continue
                if patientIndex not in patientIndexesByGID[gid]:
                    patientIndexesByGID[gid].append(patientIndex)
        print("First Pass Patients: {:,} patients, {:,} gids and {:,} of the gids are in > 1 patient".format(
            len(patients),
            len(patientIndexesByGID),
            sum(1 for gid in patientIndexesByGID if len(patientIndexesByGID[gid]) > 1)
        ))
        indexesToNix = set()
        cpatients = []
        for gid in patientIndexesByGID:
            if len(patientIndexesByGID[gid]) == 1:
                continue
            cpatient = set()
            for patientIndex in patientIndexesByGID[gid]:
                indexesToNix.add(patientIndex)
                for gien in patients[patientIndex]:
                    cpatient.add(gien)
            cpatient = sorted(list(cpatient))
            cpatients.append(cpatient)
        npatients = []
        for i, patient in enumerate(patients):
            if i in indexesToNix:
                continue
            npatients.append(patient)
        npatients.extend(cpatients)
        self.__pdirInfo["patients"] = npatients
        print("Second Pass Patients: {:,} patients".format(
            len(npatients)
        ))
        
    """
    UserDirectory has SSNs for many users. How many Patient entries are also users
    somewhere
    """
    def __sameAsToUserDirectory(self, userDirectory):
        def patientSSNs(patient):
            ssns = set()
            for gien in patient:
                entry = self.__pdirInfo["entries"][gien]
                if entry[CommonPatientDirectory.ENTRY_SSN_IDX]:
                    ssns.add(entry[CommonPatientDirectory.ENTRY_SSN_IDX])
            return ssns        
        self.__pdirInfo["sameAsUserBySSN"] = {} # reset
        for i, patient in enumerate(self.__pdirInfo["patients"]):
            ssns = patientSSNs(patient)
            for ssn in ssns:
                userIndex, userNames = userDirectory.lookupUserBySSN(ssn)
                if userIndex != -1:
                    self.__pdirInfo["sameAsUserBySSN"][i] = userIndex
        return self.__pdirInfo["sameAsUserBySSN"]

    def __flush(self):
        print("Patients {:,}, Entries {:,}, SameAs User {:,} flushed".format(len(self.__pdirInfo["patients"]), len(self.__pdirInfo["entries"]), len(self.__pdirInfo["sameAsUserBySSN"]) if "sameAsUserBySSN" in self.__pdirInfo else 0))
        json.dump(
            self.__pdirInfo, 
            open(self.__dirFile, "w"), 
            indent=4
        )
        
# ######################## Driver ###################
        
def main():

    assert sys.version_info >= (3, 6)
    
    cud = CommonUserDirectory(VISN20_VISTAS)    
    cpd = CommonPatientDirectory(VISN20_VISTAS, cud)
    print(cpd.report())
    json.dump(cpd.entryDatesBySNO(), open("Meta/Common/patientDatesBySNO.json", "w"), indent=4)
    # cpd.dumpSameAsUser()
            
if __name__ == "__main__":
    main()  
    