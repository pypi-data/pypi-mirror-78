#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime
import platform
import statistics

from fmqlutils import VISTA_DATA_BASE_DIR
from fmqlutils.cacher.cacherUtils import SCHEMA_LOCN_TEMPL 
from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

"""
# TODO: move fmqr/directory

TODO WORK OFF/IMPROVE CACHER:
- create date:
  - make sure create date seen (map out # with a create date ie/ adding in fmqlreports meta) to make it clear
  - not updated since ie/ last X entries 
- fmql data qa ie/ to tighten that by exposing it here

TODO WORK (and delete) Archive:
- https://github.com/caregraf/cgArchive/blob/master/Voldermort/schemaRankReporter.py ... schema rank, word soup etc
- Voldermort/vistaAnalytics.py ... and buildInfos
"""

class CommonFileDirectory(): 

    ENTRY_IDX_SNO = 0

    # SELECT TYPES
    ENTRY_IDX_ID = 1
    ENTRY_IDX_NAME = 2
    ENTRY_IDX_PARENTID = 3
    ENTRY_IDX_COUNT = 4
    
    # DESCRIBE TYPE
    # TODO: expand with 
    # - count pointers, literals etc
    # - boolean on pointers to PATIENT etc
    ENTRY_IDX_FIELDCOUNT = 5
    
    # BUILD/INSTALL
    ENTRY_IDX_BUILD_FIRST_DT = 6
    ENTRY_IDX_BUILD_LAST_DT = 7
    ENTRY_IDX_BUILD_COUNT = 8
    ENTRY_IDX_INSTALL_FIRST_DT = 9
    ENTRY_IDX_INSTALL_LAST_DT = 10
    ENTRY_IDX_INSTALL_COUNT = 11

    def __init__(self, vistaSNOs):
        self.__vistaSNOs = vistaSNOs
        self.__fdirFile = f'{VISTA_DATA_BASE_DIR}Common/Directory/FDIR.json'
        try:
            print("Attempting to load preexisting file Directory")
            self.__fdirInfo = json.load(open(self.__fdirFile))
        except:
            print("Starting Directory from Scratch")
            self.__fdirInfo = {"vistas": [], "entries": {}, "files": [], "sentries": {}, "sfiles": []}
        else:
            print(f'Loaded preexisting directory with {len(self.__fdirInfo["files"]):,} files')
        self.__changeUpdate()
        
    def vistas(self):
        return self.__fdirInfo["vistas"]
                
    # Fan out the file - good for reports
    def lookupFileEntriesByGIEN(self, gien):
        gienFile = None
        for file in self.__fdirInfo["files"]:
            if gien in file:
                gienFile = file
                break
        if not gienFile:
            return None
        entries = []
        for giene in gienFile:
            entry = self.__fdirInfo["entries"][giene]
            entries.append(entry)
        return {"gien": gien, "entries": entries}
                
    def lookupEntryByGIEN(self, gien):
        return self.__fdirInfo["entries"].get(gien, None)
        
    """
    Report on contents
    ... basis for .md's and graphics both PER SYSTEM and CROSS
    
    Issue of >0, -1 (UNTRACKED), ...
    
    Do 
        “{var1} {var2}”.format(var1=value1, var2=value2) ie/ easier read
        
    TODO ADDITIONS:
    - DSS and other vendors break out and not just exclusive files and per station files
    - excluding the empties post the first pass as deprecated
    """
    def report(self):        
        
        mu = "# File Directory Synopsis\n\n"
        mu += f'VistAs: {len(self.__fdirInfo["vistas"]):,}' + "\n"
        
        # Graphics - top: topTotal - isHasBH
        fls = self.fileIds()
        mu += f'Files: {len(fls):,}' + "\n"
        cores = set(self.commonFiles())
        mu += "Core (in all): {}\n".format(
            reportAbsAndPercent(len(cores), len(fls))
        )
        commonCount = self.commonCounts()
        mu += f'Common Files: {"/".join([reportAbsAndPercent(commonCount[cnt], len(fls)) for cnt in sorted(commonCount) if cnt > 1])}' + "\n"
        emptiesInAll = set(self.filesOfCount(count=0))
        flsNotEmptyInAll = set(fls) - emptiesInAll
        commonCountNoEmpties = self.commonCounts(excludeFLs=emptiesInAll)
        mu += f'Common Files (w/o empties in all): {"/".join([reportAbsAndPercent(commonCountNoEmpties[cnt], len(flsNotEmptyInAll)) for cnt in sorted(commonCountNoEmpties)])}' + "\n"
        exclFiles = self.commonFiles(count=1) # if they appear, are one
        mu += "Exclusive (in 1): {}\n".format(
            reportAbsAndPercent(len(exclFiles), len(fls)),
        )
        mu += "Exclusive files - own station more: {}\n".format(
            reportAbsAndPercent(len(self.stationSpecificFiles()), len(exclFiles))
        )
        mu += "Files with > 1 name: {}\n".format(
            reportAbsAndPercent(len(self.filesWithManyNames()), len(fls))
        )

        totalRecords = self.totalRecords()
        mu += f'Records: {totalRecords:,}' + "\n"         
        allFlsByGroup = {}
        for fl in exclFiles:
            allFlsByGroup[fl] = "EXCLUSIVE"
        for fl in cores:
            allFlsByGroup[fl] = "ALL"
        for fl in fls:
            if fl in allFlsByGroup or fl in emptiesInAll:
                continue
            allFlsByGroup[fl] = "SOME"
        totalsByGroup = self.totalRecords(groupOfFile=allFlsByGroup)
        mu += f'Records (by group): {"/".join([reportAbsAndPercent(totalsByGroup[grp], totalRecords) for grp in sorted(totalsByGroup, key=lambda x: totalsByGroup[x], reverse=True)])}' + "\n"
        singletons = set(self.filesOfCount(count=1))
        mu += "Singletons: {}\n".format(
            reportAbsAndPercent(len(singletons), len(fls))
        )
        mu += "Singleton Cores: {}\n".format(
            reportAbsAndPercent(len(singletons.intersection(cores)), len(singletons))
        )
        # May later (add note to see - empty in any?)
        mu += "Empties: {}\n".format(
            reportAbsAndPercent(len(emptiesInAll), len(fls))
        )
        # May change focus to "populated" cores (or will triple with > 1 populated)
        mu += "Empty Cores: {}\n".format(
            reportAbsAndPercent(len(emptiesInAll.intersection(cores)), len(emptiesInAll))
        )
        mu += "Empty Exclusives: {}\n".format( # rem: cores same for all!
            reportAbsAndPercent(len(emptiesInAll.intersection(exclFiles)), len(emptiesInAll))
        )
        mu += "Untracked: {}\n".format(
            reportAbsAndPercent(len(self.untrackedFiles()), len(fls))
        )       
        mu += f'Definitions across VistAs: {len(self.__fdirInfo["entries"]):,}' + "\n"
        mu += "\n"
        for vistaInfo in self.__fdirInfo["vistas"]:
        
            stationNo = vistaInfo["stationNumber"]
            mu += f'## VistA {stationNo}\n' + "\n"
            
            fls = self.fileIds(stationNo)
            mu += f'Files: {len(fls):,}' + "\n"
            commonCount = self.commonCounts(stationNo)
            mu += f'Common Files: {"/".join([reportAbsAndPercent(commonCount[cnt], len(fls)) for cnt in sorted(commonCount) if cnt > 1])}' + "\n"
            commonCountNoEmpties = self.commonCounts(stationNo, emptiesInAll)
            mu += f'Common Files (w/o empties in all): {"/".join([reportAbsAndPercent(commonCountNoEmpties[cnt], len(flsNotEmptyInAll)) for cnt in sorted(commonCountNoEmpties)])}' + "\n"
            exclFiles = set(self.commonFiles(stationNo, count=1))
            mu += "Exclusive (in 1): {}\n".format(
                reportAbsAndPercent(len(exclFiles), len(fls)),
            )
            vistaSpecificFiles = self.stationSpecificFiles(stationNo, [stationNo])
            mu += "Exclusive files - own station more: {}\n".format(
                reportAbsAndPercent(
                    len(vistaSpecificFiles),
                    len(exclFiles)
                )
            )
            mu += f'Records: {self.totalRecords(stationNo):,}' + "\n"
            totalsByGroup = self.totalRecords(stationNo, groupOfFile=allFlsByGroup)
            mu += f'Records (by group): {"/".join([reportAbsAndPercent(totalsByGroup[grp], totalRecords) for grp in sorted(totalsByGroup, key=lambda x: totalsByGroup[x], reverse=True)])}' + "\n"
            mu += f'Median Record per file (inc empties): {self.medianRecords(stationNo, True):,}' + "\n"
            mu += f'Median Record per file (excl empties): {self.medianRecords(stationNo, False):,}' + "\n"
            singletons = set(self.filesOfCount(stationNo, count=1))
            mu += "Singletons: {}\n".format(
                reportAbsAndPercent(
                    len(singletons),
                    len(fls)
                )
            )
            mu += "Singleton Cores: {}\n".format( # rem: cores same for all!
                reportAbsAndPercent(len(singletons.intersection(cores)), len(singletons))
            )
            empties = set(self.filesOfCount(stationNo, count=0))
            mu += "Empties: {}\n".format(
                reportAbsAndPercent(
                    len(empties),
                    len(fls)
                )
            )
            mu += "Empty Cores: {}\n".format( # rem: cores same for all!
                reportAbsAndPercent(len(empties.intersection(cores)), len(empties))
            )
            mu += "Empty Exclusives: {}\n".format( # rem: cores same for all!
                reportAbsAndPercent(len(empties.intersection(exclFiles)), len(empties))
            )
            mu += "Untracked: {}\n".format(
                reportAbsAndPercent(
                    len(self.untrackedFiles(stationNo)),
                    len(fls)
                )
            )
            mu += "\n" 
                
        return mu
        
    # ----------------- File Ids and Presence across VistAs -------------------
            
    def fileIds(self, stationNo=""):
        """
        All files known or just per VistA
        
        For Plot: enables a isHasBH - total files and then can give % with different 
        attributes using other methods below (emptyFileIds)
        """
        fids = [fl[0].split(":")[1] for fl in self.__fdirInfo["files"]] if stationNo == "" else [entry[CommonFileDirectory.ENTRY_IDX_ID] for entry in self.__entriesByVistA(stationNo)]
        return sorted(fids, key=lambda x: float(x))
        
    def commonFiles(self, stationNo="", count=0): 
        """
        # 0 == ALL
            ie/ commonFiles(stationNo) <=> allFiles([stationNo])
        # 1 == Exclusive (ie/ not common at all)
            ie/ commonFiles(stationNo, 1) <=> exclusiveFiles([stationNo])
        where stationNo being set limits the list to files in a particular vista
        
        # > 1 BUT < len(vistas) => mix ie/ not exclusive and not all
        """
        inCount = []
        count = count or len(self.__fdirInfo["vistas"])
        for fl in self.__fdirInfo["files"]:
            if len(fl) != count:
                continue
            if stationNo and sum(1 for f in fl if f.split(":")[0] != stationNo):
                continue
            inCount.append(fl[0].split(":")[1])
        return inCount
        
    def filesWithManyNames(self):
        manyNamedFls = []
        for fl in self.__fdirInfo["files"]:
            nms = set(self.__fdirInfo["entries"][f][CommonFileDirectory.ENTRY_IDX_NAME] for f in fl)
            if len(nms) > 1:
                manyNamedFls.append(fl[0].split(":")[1])
        return manyNamedFls
        
    def stationSpecificFiles(self, stationNo="", stationsToMatch=None):
        """
        - stationsToMatch: if None => vistas know in directory
        
        Picks out files with ids in the station space ie/ if 668 is station
        then file id starts with 668
        
        ex 687000, 6870500 ... 663 goes further 6631965
        """
        inSpecifics = []
        if stationsToMatch == None:
            stationsToMatch = [vi["stationNumber"] for vi in self.__fdirInfo["vistas"]]
        stationsToMatchRE = "({})".format("|".join(stationsToMatch))
        for fl in self.__fdirInfo["files"]:        
            if stationNo and sum(1 for f in fl if f.split(":")[0] != stationNo):
                continue
            if not re.match(stationsToMatchRE, fl[0].split(":")[1]):
                continue
            fid = fl[0].split(":")[1]
            if len(fid) < 6:
                continue # 668000 on
            inSpecifics.append(fid)
        return inSpecifics
                
    def commonCounts(self, stationNo="", excludeFLs=set()):
        """
        By count of vista's types are in, count types ex/
            4: 500 <---- in 4 VistAs
            3: 400 <---- in 3 VistAs
            ...
        
        Arguments:
        - stationNo: only do for files of one VistA
        - excludeFLs: can exclude files (ex/ empty files or ...) so 
        count files of different sorts

        For Plot: the SchemaCommon/plotCategoryBSV Plot and Explanation
        """
        crossVistATypesPresenceCount = Counter()
        for fl in self.__fdirInfo["files"]:
            crossVistATypesPresenceCount[fl[0].split(":")[1]] = len(fl)
        fls = self.fileIds(stationNo) # all if stationNo == ""
        commonCount = Counter()
        for flId in fls:
            if flId in excludeFLs:
                continue
            commonCount[crossVistATypesPresenceCount[flId]] += 1                    
        return commonCount
        
    # ----------------- Record Count and Categorize by Record Count -------------------
           
    def totalRecords(self, stationNo="", groupOfFile=None):
        """
        Support any grouping of files: fl: GRP ... ex/ Patient vs ...
        or Exclusive files vs ...
        
        For Plot: categoryBH (ala AllConsults top of IFC)
    
            One Bar broken down ...
    
            plotData["allRecords"] = {
                "title": "All Records",
                "plotName": "fileAllRecords",
                "plotMethod": "plotCategoryBH",
                "rows": ["records"],
                "columns": [],
                "data": []
            }
            dataOne = []
            for vistaInfo in self.__fdirInfo["vistas"]:
                stationNo = vistaInfo["stationNumber"]
                plotData["columns"].append(stationNo)
                dataOne.append(self.totalRecords(stationNo))
            plotData["data"].append(dataOne)
        """
        ttl = 0
        ttlByGRP = Counter()
        for gid in self.__fdirInfo["entries"]:
            if stationNo and not re.match(stationNo, gid):
                continue
            cnt = self.__fdirInfo["entries"][gid][CommonFileDirectory.ENTRY_IDX_COUNT]
            if cnt in [0, -1]:
                continue  
            if groupOfFile:
                flId = gid.split(":")[1]
                if flId not in groupOfFile:
                    raise Exception(f"Expect all files to be id'ed in groupOfFile: {flId}")
                grp = groupOfFile[flId]
                ttlByGRP[grp] += cnt                 
                continue 
            ttl += cnt
        return ttl or ttlByGRP

    def filesOfCount(self, stationNo="", count=-1):
        """
        - Empty files: count = 0
        - Singleton files: count = 1
        
        TODO: consider bucketing ie/ count=>bounds ie/ > 10 etc
        """
        flCounts = defaultdict(list)
        for entry in self.__fdirInfo["entries"].values():
            if stationNo and entry[CommonFileDirectory.ENTRY_IDX_SNO] != stationNo:
                continue
            fl = entry[CommonFileDirectory.ENTRY_IDX_ID]
            cnt = entry[CommonFileDirectory.ENTRY_IDX_COUNT]
            flCounts[fl].append(cnt)
        fls = []
        for fl in flCounts:
            if len(set(flCounts[fl])) > 1 or flCounts[fl][0] != count:
                continue   
            fls.append(fl) 
        if "996.2" in fls:
            print(flCounts["996.2"])
        return fls
        
    def untrackedFiles(self, stationNo=""):
        """
        Untracked files
        """
        return self.filesOfCount(stationNo, count=-1)
        
    def medianRecords(self, stationNo="", includeEmpties=True):
        """
        Arguments:
        - StationNo: "" => all known systems ie/ if merged; else one VistA's files
        - includeEmpties: ignore empty files (or not)
        ... always excludes untracked files
        """
        entries = self.__fdirInfo["entries"].values() if stationNo == "" else self.__entriesByVistA(stationNo)        
        minToCount = 0 if includeEmpties else 1
        medianRecordsPerFile = statistics.median([
            entry[CommonFileDirectory.ENTRY_IDX_COUNT]
            for entry in entries if entry[CommonFileDirectory.ENTRY_IDX_COUNT] >= minToCount
        ]) # don't count the untracked
        return medianRecordsPerFile

    # -------------------------- Utilities etc --------------------------
        
    def __entriesByVistA(self, stationNo):
        return [self.__fdirInfo["entries"][gid] for gid in self.__fdirInfo["entries"] if re.match(stationNo, gid)]
        
    # TODO: timing stuff is ever get to 9_4, 9_6 - see old Archives
             
    # ########################## CHANGE / UPDATE ######################
                        
    def __changeUpdate(self):
        changed = self.__fillFromAvailable()
        if changed:
            print("Changed - so rebuilding files")
            self.__rebuildFiles()
            self.__flush()    
                             
    # Only Select Types for now - can expand later   
    def __fillFromAvailable(self):
    
        """
        string.isnumeric() Returns True if there are only numeric characters in the string. If not, returns False.
string.isalpha() Returns True if there are only alphabetic characters in the string. If not, returns False.
        """
        def processSelectTypesOfStation(stationNo):
            try:
                selectTypes = json.load(open(SCHEMA_LOCN_TEMPL.format(stationNo) + "SELECT_TYPES.json"))
            except:
                raise Exception("Can't load SELECT_TYPE.json from {}".format(SCHEMA_LOCN_TEMPL.format(stationNo)))
            if selectTypes["siteId"] != stationNo:
                raise Exception(f'Didn\'t get SELECT TYPES expected for {stationNo}')
            print(f'Extracting entries from SELECTTYPES of {selectTypes["siteLabel"]}') 
            entries = []
            sentries = []
            for result in selectTypes["results"]:
                entry = [
                    stationNo, # STATION NO
                    result["number"], # ID
                    result["name"], # NAME
                ]
                if "parent" in result:
                    entry.extend([result["parent"], -1])
                    sentries.append(entry)
                    continue
                if "count" not in result:
                    cnt = 0
                elif re.search(r'\-', result["count"]):
                    cnt = -1
                else:
                    cnt = int(result["count"]) 
                entry.extend(["", cnt])  
                entries.append(entry)
            print(f'\tbuilt {len(entries):,} entries')
            return entries, sentries     
            
        changed = False
        for stationNo in self.__vistaSNOs:
            if sum(1 for vistaInfo in self.__fdirInfo["vistas"] if vistaInfo["stationNumber"] == stationNo):
                print("\t{} already in Directory - skipping".format(stationNo))
                continue
            try:
                stationEntries, stationSEntries = processSelectTypesOfStation(stationNo)
            except:
                print(f'Can\'t load SelectTypes for {stationNo} as not available/creatable here')
                raise
            changed = True
            for stationEntry in stationEntries:
                self.__fdirInfo["entries"][
                f'{stationNo}:{stationEntry[CommonFileDirectory.ENTRY_IDX_ID]}'] = stationEntry
            for stationSEntry in stationSEntries:
                self.__fdirInfo["sentries"][
                f'{stationNo}:{stationSEntry[CommonFileDirectory.ENTRY_IDX_ID]}'] = stationSEntry
            self.__fdirInfo["vistas"].append({"stationNumber": stationNo, "dateAdded": str(datetime.now()).split(" ")[0]})
        return changed
                
    def __rebuildFiles(self): # Just doing top files for now
        del self.__fdirInfo["files"]
        fileEntryGIDsById = defaultdict(list)
        for gid in self.__fdirInfo["entries"]:
            entry = self.__fdirInfo["entries"][gid]
            fileEntryGIDsById[entry[CommonFileDirectory.ENTRY_IDX_ID]].append(
                f'{entry[CommonFileDirectory.ENTRY_IDX_SNO]}:{entry[CommonFileDirectory.ENTRY_IDX_ID]}'
            )
        self.__fdirInfo["files"] = [fileEntryGIDsById[fid] for fid in sorted(fileEntryGIDsById, key=lambda x: float(x))]
        print(f'From {len(self.__fdirInfo["entries"]):,}, isolated {len(self.__fdirInfo["files"]):,} distinct files')

    def __flush(self):
        print("Files {:,}, Entries {:,} flushed".format(len(self.__fdirInfo["files"]), len(self.__fdirInfo["entries"])))
        json.dump(
            self.__fdirInfo, 
            open(self.__fdirFile, "w"), 
            indent=4
        )
        
# ############################## DRIVER ##########################
        
VISN20_VISTAS = {"668": "SPO", "663": "PUG", "648": "POR", "687": "WWW", "531": "BOI", "692": "WCO", "653": "ROS"}
        
def main():

    assert sys.version_info >= (3, 6)
    
    cfd = CommonFileDirectory(VISN20_VISTAS)
    print(cfd.report())
            
if __name__ == "__main__":
    main() 