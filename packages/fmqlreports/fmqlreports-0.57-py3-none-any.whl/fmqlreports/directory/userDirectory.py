#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime
import platform
from random import randint

from fmqlutils import VISTA_DATA_BASE_DIR
from fmqlutils.reporter.reportUtils import MarkdownTable, reportAbsAndPercent
from fmqlreports.webReportUtils import reduce200

from fileDirectory import VISN20_VISTAS # TMP - move to webReportUtils

"""
TODO FOR PATIENT/USER RE-ALIGN + PLOT EASY -- make the directories align and
preferably delegate/specialize a basic directory class ... just do the user dir
first and then do that.

LONGER GOAL: base class with PatientDirectory and simplify this so that like
Patient Directory has "usersFlat" and direct from 200 reduction etc.

TODO:
- md report
- for teler users, custom report on their overlaps (ie/ put into directory)
--------
- key is PROP cnt creator (most > 25+)/no creator (most <15) ... see breakdown as load and work out exceptions ... ie/ REMOTE vs LOCAL marker and more (termination goes with no creator?)
- sex for deid + deid for subset only ... make list and label mand
- more on later JLV (secid only, its context) vs earlier ie/ JLV stages
- isolate the HL7 user creation (any sig?)
- see TERMINATION ie/ how to gather "last sign in info" too ... possible to "purge" but must be clear ... align last sign in ... again push max 200 offers
- record date of clone in the vistas list
--------
- to fm.. inside/merge classify (then rename as 'makeTeleReaderUserDirectory' - see one function below to use the generic dir)

Observation from userReport.txt (from complete UserDirectory regen)
- have dateEntered for nearly all
- 46K of 324K explicit setup in 668 but 96K of 551K ie/ higher prop explicit in bigger 663 (ie/ less proportional remote setup which is to be expected)
- less ssn, more secid in 663, but seems to track explicit ie/ remotes still seem to be mainly ssn.
- other ids less important later: (but marker of unusual user?)
  - "distinct_unique_user_id" => not same as email or secid. High earlier (ie/ field used) but not many later (42/1K in 668; 79/1K for 663)
  - email only unique in very few of later entries (35/1K, 32/1K) 
- 648 only one that did bulk terminates (mainly of remotes? or?) and effects prop #'s and term props scew it up
"""
    
class CommonUserDirectory():

    ENTRY_SSN_IDX = 8
    ENTRY_SECID_IDX = 9
    ENTRY_NWNM_IDX = 10
    ENTRY_DUID_IDX = 11

    def __init__(self, vistaSNOs):
        self.__vistaSNOs = vistaSNOs
        self.__udirFile = f'{VISTA_DATA_BASE_DIR}Common/Directory/UDIR.json'
        try:
            print("Attempting to load preexisting User Directory")
            self.__udirInfo = json.load(open(self.__udirFile))
        except:
            print("Starting Directory from Scratch")
            self.__udirInfo = {"vistas": [], "entries": {}, "users": []}
        else:
            print("Loaded preexisting directory with {:,} users".format(len(self.__udirInfo["users"])))
        self.__changeUpdate()
        
    # ################## All Directory Accessors ######################
        
    def vistas(self):
        return self.__udirInfo["vistas"]
        
    # To see, per station, add stationNo
    def total(self, stationNo=""):
        if stationNo == "":
            return len(self.__udirInfo["users"])
        return sum(1 for user in self.__udirInfo["users"] if sum(1 for gien in user if gien.split(":")[0] == stationNo))
        
    def entryTotal(self, stationNo=""):
        if stationNo == "":
            return len(self.__udirInfo["entries"])
        return sum(1 for gien in self.__udirInfo["entries"] if gien.split(":")[0] == stationNo)
                    
    """
    Presence of SSN etc in one or more entries of users
    
    To see SSN
        noW, noWGT1 = .idPresence(CommonUserDirectory.ENTRY_SSN_IDX)
    same for ENTRY_SECID_IDX, ENTRY_NWNM_IDX, ENTRY_DUID_IDX
    """
    def idPresence(self, entryIdx, gt1=False):
        noW = 0
        noWGT1 = 0
        for i, user in enumerate(self.__udirInfo["users"], 1):
            vals = set(self.__udirInfo["entries"][gien][entryIdx] for gien in user if self.__udirInfo["entries"][gien][entryIdx])
            if len(vals):
                noW += 1
                if len(vals) > 1:
                    noWGT1 += 1
        return noWGT1 if gt1 else noW
        
    def gt1VistACount(self):
        cnt = 0
        for i, user in enumerate(self.__udirInfo["users"], 1):
            snos = set(gien.split(":")[0] for gien in user)         
            if len(snos) > 1:
                cnt += 1
        return cnt  
        
    def commonCounts(self, stationNo=""):
        """
        By count of vista's users are in, count types ex/
            4: 500 <---- in 4 VistAs
            3: 400 <---- in 3 VistAs
            ...
        
        Arguments:
        - stationNo: only do for files of one VistA

        For Plot: the common/plotCategoryBSV Plot and Explanation
        """
        commonCount = Counter()
        for user in self.__udirInfo["users"]:
            stationNos = set(gien.split(":")[0] for gien in user)
            if stationNo and stationNo not in stationNos:
                continue
            commonCount[len(stationNos)] += 1
        return commonCount # may not be in order ie/ 3, 1, 4, 2, ...
        
    """
    For a given id - ex SSN - return all values.

    Use: entryIDX = CommonUserDirectory.ENTRY_SSN_IDX ... ENTRY_SECID_IDX, 
    ENTRY_NWNM_IDX, ENTRY_DUID_IDX
    """
    def idValues(self, entryIdx):
        allVals = set()
        for i, user in enumerate(self.__udirInfo["users"], 1):
            vals = set(entries[gien][entryIdx] for gien in user if self.__udirInfo["entries"][gien][entryIdx])
            allVals |= vals
        return allVals
        
    # ###################### User Specific Methods #########################
        
    """
    TODO: promote to "All Directory"
    
    For time graphing
    
    Note: "ALL" => first date for a user irrespective
    """
    def entryDatesBySNO(self):
        dtBySNO = defaultdict(list)
        entries = self.__udirInfo["entries"]
        entryWODateBySNO = Counter()
        for gien in entries: # all entries now
            entry = entries[gien]
            sno = gien.split(":")[0]
            if entry[3] == "":
                entryWODateBySNO[sno] += 1
                continue
            dtBySNO[sno].append(entry[3])
        # Crude - ignoring order of orders - just resorting
        for sno in dtBySNO:
            dtBySNO[sno] = sorted(dtBySNO[sno])
        dtUsers = []
        for user in self.__udirInfo["users"]:
            entriesSDT = sorted([self.__udirInfo["entries"][gien][3] for gien in user if self.__udirInfo["entries"][gien][3]])
            if len(entriesSDT) == 0:
                entryWODateBySNO["USER"] += 1
                continue
            dtUsers.append(entriesSDT[0]) # take first date of the user
        dtBySNO["USER"] = dtUsers # overall uniques
        print("Serializing dates by station + USER overall:")
        for snop in dtBySNO:
            print("\t{}: {:,} - no date {:,}".format(snop, len(dtBySNO[snop]), entryWODateBySNO[snop]))
        return dtBySNO

    def lookupUserBySSN(self, ssn):
        try:
            self.__userBySSN
        except:
            self.__flattenUserData()
        if ssn in self.__userBySSN:
            userIndex = self.__userBySSN[ssn]
            userNames = self.__userNames[userIndex]
            # userNames one or many
            return userIndex, userNames
        return -1, []
        
    """
    This will fan out to entries that don't even have the SSN (or
    could have another!) but are pulled in by matching
    """
    def lookupUserEntriesBySSN(self, ssn):
        entriesOfSSN = []
        for user in self.__udirInfo["users"]:
            entriesOfUser = []
            gotOne = False
            for gien in user:
                entry = self.__udirInfo["entries"][gien]
                entriesOfUser.append(entry)
                if entry[CommonUserDirectory.ENTRY_SSN_IDX] == "":
                    continue
                if entry[CommonUserDirectory.ENTRY_SSN_IDX] == ssn:
                    gotOne = True
            if gotOne:
                entriesOfSSN.extend(entriesOfUser)
        return entriesOfSSN if len(entriesOfSSN) else None
        
    def userSSNs(self):
        return set(self.__udirInfo["entries"][gien][CommonUserDirectory.ENTRY_SSN_IDX] for gien in self.__udirInfo["entries"] if self.__udirInfo["entries"][gien][CommonUserDirectory.ENTRY_SSN_IDX])
        
    # Fan out the user - good for reports
    def lookupUserEntriesByGIEN(self, gien):
        gienUser = None
        for user in self.__udirInfo["users"]:
            if gien in user:
                gienUser = user
                break
        if not gienUser:
            return None
        entries = []
        for giene in gienUser:
            entry = self.__udirInfo["entries"][giene]
            entries.append(entry)
        return {"gien": gien, "entries": entries}
        
    # Can be > 1 as systems can have > 1
    def lookupGIENSByStationAndName(self, stationNo, name):
        giens = []
        for gien in self.__udirInfo["entries"]:
            if not re.match(stationNo, gien):
                continue
            entry = self.__udirInfo["entries"][gien]
            if entry[1] == name:
                giens.append(gien)
        return giens
        
    def lookupEntryByGIEN(self, gien):
        return self.__udirInfo["entries"].get(gien, None)
        
    """
    userGIENs => will fan out and if a user has any then it is pulled in as 
    are its other GIENs.
    
    TODO: move to work off usersFlat 
    
    TO ADD:
    - more on details (sex, termination etc ie/ PORTLAND more)
    - JLV and secid move ... ie/ SSN over time
    - date of VistA from first (.5) record + LAST RECORD date (as need for currency of report)
    """
    def report(self, userGIENs=None):
        countPerVistA = Counter()
        rec200CntPerSNO = Counter() # > count per VistA as dup 200's for some users 
        userRecordCount = Counter()
        cntGT1VistA = 0
        noWSSN = 0
        noWSECID = 0
        noWNWNM = 0
        noWDUID = 0
        noGT1NWNM = 0
        noGT1SSN = 0
        noGT1SECID = 0
        noGT1DUID = 0
        noNoSSNPlusNoSECIDPlusNoDUID = 0
        secids = set()
        nwnms = set()
        ssns = set()
        duids = set()
        perSNOHowMany = defaultdict(Counter) # per SNO, how many in other SNOs (graph)
        userIdIssuesByUserIndex = {}
        userNameIssueByUserIndex = {}
        if userGIENs:
            users = [user for user in self.__udirInfo["users"] if sum(1 for gien in user if gien in userGIENs)]
            inScopeGIENs = set(gien for user in users for gien in user)
            entries = dict((gien, self.__udirInfo["entries"][gien]) for gien in self.__udirInfo["entries"] if gien in inScopeGIENs)
        else:
            users = self.__udirInfo["users"]
            entries = self.__udirInfo["entries"]
        for i, user in enumerate(users, 1):
            userRecordCount[len(user)] += 1
            for gien in user:
                rec200CntPerSNO[gien.split(":")[0]] += 1
            snos = set(gien.split(":")[0] for gien in user)            
            for sno in snos:
                countPerVistA[sno] += 1
                perSNOHowMany[sno][len(snos)] += 1
            if len(snos) > 1:
                cntGT1VistA += 1
            tssns = set(entries[gien][CommonUserDirectory.ENTRY_SSN_IDX] for gien in user if entries[gien][CommonUserDirectory.ENTRY_SSN_IDX])
            tsecids = set(entries[gien][CommonUserDirectory.ENTRY_SECID_IDX] for gien in user if entries[gien][CommonUserDirectory.ENTRY_SECID_IDX])
            tnwnms = set(entries[gien][CommonUserDirectory.ENTRY_NWNM_IDX] for gien in user if entries[gien][CommonUserDirectory.ENTRY_NWNM_IDX])
            tduids = set(entries[gien][CommonUserDirectory.ENTRY_DUID_IDX] for gien in user if entries[gien][CommonUserDirectory.ENTRY_DUID_IDX])
            if len(tnwnms):
                noWNWNM += 1
                if len(tnwnms) > 1:
                    noGT1NWNM += 1
            if len(tssns):
                noWSSN += 1
                if len(tssns) > 1:
                    noGT1SSN += 1
            if len(tsecids):
                noWSECID += 1
                if len(tsecids) > 1:
                    noGT1SECID += 1
            if len(tduids):
                noWDUID += 1
                if len(tduids) > 1:
                    noGT1DUID += 1
            nwnms.update(tnwnms)
            ssns.update(tssns)
            secids.update(tsecids)
            duids.update(tduids)
            uentries = [entries[gien] for gien in user]
            idissues = []
            for idxd in [(CommonUserDirectory.ENTRY_SSN_IDX, "SSN"), (CommonUserDirectory.ENTRY_SECID_IDX, "SECID"), (CommonUserDirectory.ENTRY_DUID_IDX, "DUID")]:
                ids = set(entry[idxd[0]] for entry in uentries if entry[idxd[0]])        
                if len(ids) > 1:
                    namesNInitials = list(set("{} [{}]".format(entry[1], entry[2]) if entry[2] else entry[1] for entry in uentries))
                    idissues.append([idxd[1], list(ids), namesNInitials])
            if len(idissues):
                userIdIssuesByUserIndex[i] = idissues
            names = list(set(entry[1] for entry in uentries))
            if len(names) > 1: # Mainly one letter out or an initial
                userNameIssueByUserIndex[i] = names
            if len(tsecids) == 0 and len(tssns) == 0 and len(tduids) == 0:
                noNoSSNPlusNoSECIDPlusNoDUID += 1    
                    
        mu = ""
        mu += "# Cross-VistA User Directory\n\n"
        mu += "The following reports on a __Cross-VistA User Directory__ built from the User file (200) of <span class='yellowIt'>{:,}</span> VistAs, {}. Together they hold <span class='yellowIt'>{:,}</span> distinct users.\n\n".format(
            len(self.__vistaSNOs), # TODO: move into "vistas" (with POSTMASTER USER TOO)
            ", ".join(["{} [{}]".format(self.__vistaSNOs[sno], sno) for sno in sorted(self.__vistaSNOs, key=lambda x: int(x))]),
            len(users)
        )
        
        mu += """__Note__: this is the first version of this report. The presence of user records in more than one VistA, the dynamic addition of records to allow remote login and interfacility consults and the new move away from using SSNs and towards using VA's proprietary SECID as a user identifier, all allow for redundancy and contradiction across the VistAs. These mismatches and partial copying will be analyzed further in subsequent versions of this report.

"""
        
        tbl = MarkdownTable([":Property", "Value"], includeNo=False)
        tbl.addRow(["Users", "{:,}".format(len(users))])
        tbl.addRow(["Records", "{:,}".format(len(entries))])
        tbl.addRow(["In more than VistA", reportAbsAndPercent(cntGT1VistA, len(users))])
        tbl.addRow(["> 1 Record in an individual VistA", sum(1 for user in users if len(set(gien.split(":")[0] for gien in user)) != len(user))])
        tbl.addRow(["Has SSN", "{} [> 1 {:,}]".format(reportAbsAndPercent(noWSSN, len(users)), noGT1SSN)])
        tbl.addRow(["Has SECID", "{} [> 1 {:,}]".format(reportAbsAndPercent(noWSECID, len(users)), noGT1SECID)])
        tbl.addRow(["Has VA Network Name", "{} [>1 {:,}]".format(reportAbsAndPercent(noWNWNM, len(users)), noGT1NWNM)])
        tbl.addRow(["Has DUID", "{} [> 1 {}]".format(reportAbsAndPercent(noWDUID, len(users)), noGT1DUID)])
        tbl.addRow(["No SSN or SECID or DUID", reportAbsAndPercent(noNoSSNPlusNoSECIDPlusNoDUID, len(users))])
        mu += tbl.md() + "\n\n"
                                
        mu += "Per VistA ...\n\n"
        tbl = MarkdownTable([":VistA", "Users", "Records"], includeNo=False)
        for sno in sorted(countPerVistA, key=lambda x: countPerVistA[x], reverse=True):
            tbl.addRow([
                "__{} [{}]__".format(self.__vistaSNOs[sno], sno),
                reportAbsAndPercent(countPerVistA[sno], len(users)),
                reportAbsAndPercent(rec200CntPerSNO[sno], len(entries))
            ])  
        mu += tbl.md() + "\n\n"
        
        mu += "Across the {:,} VistAs, individual users have the following number of records. For example, a count for 3 records indicates how many users have 3 records ...\n\n".format(len(countPerVistA))
        tbl = MarkdownTable([":Records", "Users"], includeNo=False)
        for cnt in sorted(userRecordCount, key=lambda x: userRecordCount[x], reverse=True):
            tbl.addRow([
                "__{}__".format(cnt), 
                reportAbsAndPercent(userRecordCount[cnt], len(users))
            ])
        mu += tbl.md() + "\n\n"
        
        mu += "The following shows how many other VistAs also hold a user of a VistA. Note that dominant VistAs have proportionately higher single VistA counts - they alone hold certain users. Smaller VistAs contain users that also in other VistAs - they are rarely the only VistA with a user.\n\n"
        cols = [":VistA"]
        for i in range(1, len(countPerVistA) + 1):
            cols.append(str(i))
        tbl = MarkdownTable(cols, includeNo=False)
        for sno in sorted(perSNOHowMany, key=lambda x: sum(cnt for cnt in perSNOHowMany[x].values()), reverse=True):
            row = ["__{} [{}]__".format(self.__vistaSNOs[sno], sno)]
            for i in range(1, len(countPerVistA) + 1):
                if i not in perSNOHowMany[sno]:
                    row.append("")
                    continue
                row.append(reportAbsAndPercent(perSNOHowMany[sno][i], countPerVistA[sno]))
            tbl.addRow(row)
        mu += tbl.md() + "\n\n"
                
        return mu
        
    """
    Subset - used by TeleReader to produce sub directory (which it de-identifies)
    
        from deid import IDMaker, NameMaker
        sdeid = cud.subsetNDEID(allGIENs, IDMaker(), NameMaker())
    
    To see: pass in nm.report()
    """
    def subsetNDEID(self, userGIENs, idMaker, nameMaker):
        nusers = []
        nentries = {}
        snos = set()
        for i, user in enumerate(self.__udirInfo["users"]):
            if len(userGIENs) and sum(1 for gien in user if gien in userGIENs) == 0:
                continue
            nusers.append(user)
            # Only a Home User would have Sex
            sexes = set([self.__udirInfo["entries"][gien][4] for gien in user if self.__udirInfo["entries"][gien][4]])
            if len(sexes) > 1:
                raise Exception("Can't de id with SEX as > 1 Sex for a user")
            if len(sexes) == 0:
                sex = "female" if randint(1, 2) == 1 else "male" # fifty fifty
                print("** sexless user: {} - picking  {} 50/50".format(self.__udirInfo["entries"][user[0]][1], sex))
            else:
                sex = "male" if list(sexes)[0] == "M" else "female"
            name, nameInitials, iname, inameInitials, nwnmEnd = nameMaker.getUserNames(gender=sex, originalName=self.__udirInfo["entries"][user[0]][1])
            origNWNM = ""
            for gien in user:
                snos.add(gien.split(":")[0])
                entry = self.__udirInfo["entries"][gien]
                nentries[gien] = entry
                nameToUse = iname if re.search(r' [A-Z]$', entry[1]) else name
                origName = entry[1]
                entry[1] = nameToUse
                if entry[2]:
                    entry[2] = inameInitials if nameToUse == iname else nameInitials
                for idxd in [(CommonUserDirectory.ENTRY_SSN_IDX, "SSN"), (CommonUserDirectory.ENTRY_SECID_IDX, "SECID"), (CommonUserDirectory.ENTRY_NWNM_IDX, "NWNM"), (CommonUserDirectory.ENTRY_DUID_IDX, "DUID")]:
                    if entry[idxd[0]] == "":
                        continue
                    if idxd[1] in ["SSN", "SECID"]:
                        entry[idxd[0]] = idMaker.nextID(idxd[1], entry[idxd[0]])
                        continue
                    if idxd[1] == "NWNM": 
                        # Part enforce, part repeat - saw same user with a BOI and 
                        # PUG VHA ID!
                        if origNWNM:
                            if entry[idxd[0]] != origNWNM:
                                print("** Warning > 1 NWNM - must be different starts: {} - {}".format(origNWNM, entry[idxd[0]]))
                            else:
                                origNWNM = entry[idxd[0]]
                        if re.match(r'VHA', entry[idxd[0]]): # allows for multi's in DEID too
                            nwnm = entry[idxd[0]][0:6] + nwnmEnd
                            entry[idxd[0]] = nwnm
                        else:
                            raise Exception("Only setup for VHA NW Names")     
                        continue
                    entry[idxd[0]] = "Y" # TODO
        print("Returning {:,} entries and {:,} users from User Directory{}".format(len(nentries), len(nusers), " [DEIDENTIFIED]" if nameMaker else ""))
        nvistas = [vinfo for vinfo in self.__udirInfo["vistas"] if vinfo["stationNumber"] in snos]
        return {"vistas": nvistas, "entries": nentries, "users": nusers}
        
    """
    QA Dump: nwnms
    
    TODO: more beyond VHA and get dups etc
    """
    def dumpNWNMs(self):
        
        vhaCounts = Counter()
        # '(VHA|VBA|VAF|VAHRC|VACO|VAH|VAMQA)' ... more than VHA and more than these too
        # ... but just do VHA for now
        # ... TODO: could [a] see NWNAME reuse which happens and [b] try tie to home sys
        for user in self.__udirInfo["users"]:
            nwnms = list(set(self.__udirInfo["entries"][gien][CommonUserDirectory.ENTRY_NWNM_IDX] for gien in user if self.__udirInfo["entries"][gien][CommonUserDirectory.ENTRY_NWNM_IDX]))
            vhaVistANWNames = set()
            for nwnm in nwnms:
                # nwname re.match('(VHA|VBA|VAF|VAHRC|VACO|VAH|VAMQA)', entry[idxd[0]]) <--- yep before do the events names
                nwnameMtch = re.match('VHA([A-Z]{3})', nwnm) 
                if nwnameMtch:
                    vhaVistANWNames.add(nwnameMtch.group(1))
            if len(vhaVistANWNames) == 1:
                vhaCounts[list(vhaVistANWNames)[0]] += 1
            elif len(vhaVistANWNames):
                vhaCounts["*VHAGT1*"] += 1
            elif len(nwnms):
                vhaCounts["*NON_VHAS_ONLY*"] += 1
            else:
                vhaCounts["*NONE*"] += 1
        print("NWNMs (VHA) [{:,}] - top 10:".format(len(vhaCounts)))
        for i, vha in enumerate(sorted(vhaCounts, key=lambda x: vhaCounts[x], reverse=True), 1):
            if i > 10:
                break
            print("\t{}: {:,}".format(vha, vhaCounts[vha]))
     
    """
    QA Dump: ID issues
    
    Overlaps, dups, inconsistencies across the Directory
    """
    def dumpIdIssues(self):
        userIdIssuesByUserIndex = {}
        userNameIssueByUserIndex = {}
        for i, user in enumerate(self.__udirInfo["users"], 1):
            entries = [self.__udirInfo["entries"][gien] for gien in user]
            idissues = []
            for idxd in [(CommonUserDirectory.ENTRY_SSN_IDX, "SSN"), (CommonUserDirectory.ENTRY_SECID_IDX, "SECID"), (CommonUserDirectory.ENTRY_DUID_IDX, "DUID")]:
                ids = set(entry[idxd[0]] for entry in entries if entry[idxd[0]])        
                if len(ids) > 1:
                    namesNInitials = list(set("{} [{}]".format(entry[1], entry[2]) if entry[2] else entry[1] for entry in entries))
                    idissues.append([idxd[1], list(ids), namesNInitials])
            if len(idissues):
                userIdIssuesByUserIndex[i] = idissues
            names = list(set(entry[1] for entry in entries))
            if len(names) > 1: # Mainly one letter out or an initial
                userNameIssueByUserIndex[i] = names
    
        print("Of {:,} users, {:,} have matching id issues (> 1 of same id), {:,} have matching name issues:".format(
            len(self.__udirInfo["users"]),
            len(userIdIssuesByUserIndex),
            len(userNameIssueByUserIndex)
        ))
        print("Id Issues:")
        for i in userIdIssuesByUserIndex:
            print("\t{}: {}".format(i, json.dumps(userIdIssuesByUserIndex[i])))
            
    """
    Index/flattening for lookups etc
    
    TODO: like patientDirectory - usersFlat
    """
    def __flattenUserData(self):
        self.__userBySSN = {}
        self.__userNames = []
        for i, user in enumerate(self.__udirInfo["users"]):
            tUserNames = set()
            for gien in user:
                entry = self.__udirInfo["entries"][gien]
                tUserNames.add(entry[1])
                if entry[CommonUserDirectory.ENTRY_SSN_IDX] == "":
                    continue
                essn = entry[CommonUserDirectory.ENTRY_SSN_IDX]
                self.__userBySSN[essn] = i      
            self.__userNames.append(sorted(list(tUserNames)))
            
    # ########################## CHANGE / UPDATE ######################
                        
    def __changeUpdate(self):
        changed = self.__fillFromAvailable()
        if changed:
            print("Changed - so rebuilding users")
            self.__rebuildUsers()
            self.__flattenUserData()
            self.__flush()    
                                
    def __fillFromAvailable(self):
        changed = False
        for stationNo in self.__vistaSNOs:
            if sum(1 for vistaInfo in self.__udirInfo["vistas"] if vistaInfo["stationNumber"] == stationNo):
                print("\t{} already in Directory - skipping".format(stationNo))
                continue
            try:
                usrs = reframeReportUsers(stationNo)
            except:
                print("Can't load User Reduction for {} as not available/creatable here".format(stationNo))
                raise
            changed = True
            print("Loaded USRs for {}: {:,}".format(stationNo, len(usrs)))
            print("Adding {} to directory".format(stationNo))
            # [gien, dateEntered, ssn, secid, distinctUniqueUserId] - in list, has index
            for info in usrs:
                entry = ["{}:{}".format(stationNo, info["ien"]), info.get("name", ""), info.get("initial", ""), info.get("dateEntered", ""), info["sex"].split(":")[0] if "sex" in info else "", "Y" if info.get("hasCreator") else "", "Y" if info.get("hasTerminationProp") else "", info.get("noProps"), info.get("ssn", ""), info.get("secid", ""), info.get("networkUserName", ""), info.get("distinctUniqueUserId", "")]
                self.__udirInfo["entries"][entry[0]] = entry
            self.__udirInfo["vistas"].append({"stationNumber": stationNo, "dateAdded": str(datetime.now()).split(" ")[0]})
        return changed
                
    """
    Any entries that share the same SSN or SECID (leaving DUID)

    TODO:
    - for deid, will replace actual ids with BOOLEAN of present or not in entries
    - add in true if CREATOR known
    - for n/w id, have an enum of type ie/ SPO, PUG etc. -- proxy for home
    - ... can save this as basis for report
    [NOTE: move to do DIRECTLY OFF USER RED and no intermediate]
    [DO FULL REPORT]
    [DO GRAPHIC ON IT]
    """
    def __rebuildUsers(self):
        del self.__udirInfo["users"]
        """
        Alg: establish users based on all ids of each entry, consistently
        - if id already allocated to use (by previous entry) then reuse that User
        - need two passes as if entry has > 1 id, different ones may have been
        allocated to separate users by previous entries that didn't share the same
        id combo (entry with only SSN, then one with only NWNM, then one with both)
        - second pass must see indexes that need to be combined

        Note: allows for many entries for a single user in a VistA (based on three
        key ids - SSN, SECID, NWNM).
                
        problem: SSN for User, then a SECID only user on own? and then both ...
        """
        userIndexesByGID = defaultdict(set)
        users = [[]] # only fixed entry for .5
        for gien in self.__udirInfo["entries"]:
            # Handle .5 manually
            if gien.split(":")[1] == ".5":
                users[0].append(gien)
                continue
            entry = self.__udirInfo["entries"][gien]
            # may have > 1 idx as diff ids may appear w/o each other in earlier entries
            userIndexes = set() 
            gids = set()
            
            # Can't enforce (5, "NWNM") as find duplicate use
            for idxd in [(CommonUserDirectory.ENTRY_SSN_IDX, "SSN"), (CommonUserDirectory.ENTRY_SECID_IDX, "SECID"), (CommonUserDirectory.ENTRY_DUID_IDX, "DUID")]:
                if entry[idxd[0]] == "":
                    continue
                gid = "{}:{}".format(idxd[1], entry[idxd[0]])
                gids.add(gid)
                if gid in userIndexesByGID:
                    userIndexes.add(userIndexesByGID[gid][0])                   
            if len(userIndexes) == 0:
                userIndexes = set([len(users)])
                users.append([])
            userIndex = sorted(list(userIndexes))[0] # pick first
            users[userIndex].append(gien)
            for gid in gids: 
                if gid not in userIndexesByGID:
                    userIndexesByGID[gid] = [userIndex] 
                    continue
                if userIndex not in userIndexesByGID[gid]:
                    userIndexesByGID[gid].append(userIndex)
        print("First Pass Users: {:,} users, {:,} gids and {:,} of the gids are in > 1 user".format(
            len(users),
            len(userIndexesByGID),
            sum(1 for gid in userIndexesByGID if len(userIndexesByGID[gid]) > 1)
        ))
        indexesToNix = set()
        cusers = []
        for gid in userIndexesByGID:
            if len(userIndexesByGID[gid]) == 1:
                continue
            cuser = set()
            for userIndex in userIndexesByGID[gid]:
                indexesToNix.add(userIndex)
                for gien in users[userIndex]:
                    cuser.add(gien)
            cuser = sorted(list(cuser))
            cusers.append(cuser)
        nusers = []
        for i, user in enumerate(users):
            if i in indexesToNix:
                continue
            nusers.append(user)
        nusers.extend(cusers)
        self.__udirInfo["users"] = nusers
        print("Second Pass Users: {:,} users".format(
            len(nusers)
        ))

    def __flush(self):
        print("Users {:,}, Entries {:,} flushed".format(len(self.__udirInfo["users"]), len(self.__udirInfo["entries"])))
        json.dump(
            self.__udirInfo, 
            open(self.__udirFile, "w"), 
            indent=4
        )
    
"""
TODO remove: Intermediate Form made to report/isolate better. Once know form
will nix this intermediate form.

ids: secid, ssn, [network_username] (tie to MUMPS/BSE - how created, how used)
"""
def reframeReportUsers(stationNo):

    userInfoByIEN = reduce200(stationNo)    
    
    print("Reframing/reporting user red {} - {:,}".format(stationNo, len(userInfoByIEN)))
    
    rinfos = []
    datesEntered = []
    noPropsHasCreator = Counter()
    noPropsNoCreator = Counter()
    for userRef in sorted(userInfoByIEN, key=lambda x: float(x.split("200-")[1].split("]")[0])):
        info = userInfoByIEN[userRef]
        ien = re.search(r'200\-([^\]]+)', userRef).group(1)
        # REM: reduce200 embeds name in id!
        rinfo = {"ien": ien, "name": userRef.split(" [")[0], "noProps": len(info["hasProps"])}
        if "initial" in info:
            rinfo["initial"] = info["initial"]
        if "date_entered" in info:
            rinfo["dateEntered"] = info["date_entered"]
            datesEntered.append(info["date_entered"])
        # Probably means "MACHINE" or "REMOTE"
        if "sex" in info:
            rinfo["sex"] = info["sex"]
        if "ssn" in info:
            rinfo["ssn"] = info["ssn"]
        if "secid" in info:
            rinfo["secid"] = info["secid"]
        if "network_username" in info:
            rinfo["networkUserName"] = info["network_username"]
        if "termination_date" in info["hasProps"] or "inactive_date" in info["hasProps"] or "termination_reason" in info["hasProps"]:
            rinfo["hasTerminationProp"] = True
        # if len(set(info["hasProps"]).intersection(set(["title", "creator", "primary_menu_option"]))) or len(info["hasProps"]) > 18: # may go 16 later
        #    rinfo["hasExplicitSetup"] = True
        if "creator" in info:
            rinfo["hasCreator"] = True
            noPropsToUse = "<25" if rinfo["noProps"] < 25 else "25+"
            noPropsHasCreator[noPropsToUse] += 1   
        else: # 20 for 648
            if "hasTerminationProp" not in rinfo:
                noPropsToUse = rinfo["noProps"] if rinfo["noProps"] < 15 else "15+"
            else:
                noPropsToUse = "HAS_TERMINATION_PROP"
            noPropsNoCreator[noPropsToUse] += 1                    
        if "__distinct_unique_user_id" in info:
            rinfo["distinctUniqueUserId"] = info["__distinct_unique_user_id"]
        if "is_subject_organization_vha" in info:
            rinfo["isSubjectOrganizationVHA"] = True
        rinfos.append(rinfo)
        
    print("__{}__: Returning {:,}; {} have date entered; {} have sex; {} has creator; {} has a \"termination property\"; {} have SSN ({:,} non 9 SSN, {:,} last 5000); {} network username ({}/last 5K); {} secid ({:,}/last 1K, {:,}/last 5K, {:,}/last 10K - org VHA {:,}); {} distinct unique user ids [special property normalized] ({:,} no secids, {:,}/last 1K, {:,}/last 5K)".format(
    
        stationNo,
        
        len(rinfos),
        reportAbsAndPercent(sum(1 for rinfo in rinfos if "dateEntered" in rinfo), len(rinfos)),
        reportAbsAndPercent(sum(1 for rinfo in rinfos if "sex" in rinfo), len(rinfos)),
        # Vast majority have 20+ props
        reportAbsAndPercent(sum(1 for rinfo in rinfos if "hasCreator" in rinfo), len(rinfos)),
        reportAbsAndPercent(sum(1 for rinfo in rinfos if "hasTerminationProp" in rinfo), len(rinfos)),
        
        reportAbsAndPercent(sum(1 for rinfo in rinfos if "ssn" in rinfo), len(rinfos)),
        sum(1 for rinfo in rinfos if "ssn" in rinfo and not re.match(r'\d{9}$', rinfo["ssn"])),
        sum(1 for rinfo in rinfos[-5000:] if "ssn" in rinfo),
        
        reportAbsAndPercent(sum(1 for rinfo in rinfos if "networkUserName" in rinfo), len(rinfos)),
        reportAbsAndPercent(sum(1 for rinfo in rinfos[-5000:] if "networkUserName" in rinfo), len(rinfos[-5000:])), 
        
        reportAbsAndPercent(sum(1 for rinfo in rinfos if "secid" in rinfo), len(rinfos)),
        sum(1 for rinfo in rinfos[-1000:] if "secid" in rinfo),
        sum(1 for rinfo in rinfos[-5000:] if "secid" in rinfo),
        sum(1 for rinfo in rinfos[-10000:] if "secid" in rinfo),
        sum(1 for rinfo in rinfos if "isSubjectOrganizationVHA" in rinfo),
        
        # DO MUMPS ISSUE
        reportAbsAndPercent(sum(1 for rinfo in rinfos if "distinctUniqueUserId" in rinfo), len(rinfos)),     
        sum(1 for rinfo in rinfos if "distinctUniqueUserId" in rinfo and "secid" not in rinfo),
        sum(1 for rinfo in rinfos[-1000:] if "distinctUniqueUserId" in rinfo and "secid" not in rinfo),
        sum(1 for rinfo in rinfos[-5000:] if "distinctUniqueUserId" in rinfo and "secid" not in rinfo)
    ))
    print("... Last date: {}".format(sorted(datesEntered)[-1]))
    print("... 5000 back has date {}".format(datesEntered[-5000]))
    print("# Props Has Creator:")
    for noProps in sorted(noPropsHasCreator, key=lambda x: noPropsHasCreator[x], reverse=True):
        print("\t{}: {}".format(noProps, noPropsHasCreator[noProps]))
    print("# Props No Creator:")
    for noProps in sorted(noPropsNoCreator, key=lambda x: noPropsNoCreator[x], reverse=True):
        print("\t{}: {}".format(noProps, noPropsNoCreator[noProps]))        
    return rinfos
    
# ############################## DRIVER ##########################
        
def main():

    assert sys.version_info >= (3, 6)
    
    cud = CommonUserDirectory(VISN20_VISTAS)
    print(cud.report())
    json.dump(cud.entryDatesBySNO(), open("Meta/Common/userDatesBySNO.json", "w"), indent=4)
            
if __name__ == "__main__":
    main()  
    