#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
import statistics

from fmqlutils import VISTA_DATA_BASE_DIR
from fmqlutils.cacher.cacherUtils import FMQLReplyStore, FilteredResultIterator, SCHEMA_LOCN_TEMPL, DATA_LOCN_TEMPL, DATARF_LOCN_TEMPL, TMPWORKING_LOCN_TEMPL
from fmqlutils.typer.reduceTypeUtils import checkDataPresent
from fmqlutils.typer.reduceReportType import TYPER_REDUCTIONS_LOCN_TEMPL
from fmqlutils.reporter.reportUtils import MarkdownTable

"""
Site
"""
SITE_DIR_TEMPL = VISTA_DATA_BASE_DIR + "{}/ReportSite/" 

TOP_MD_TEMPL = """---
layout: default
title: {}
---

"""

def ensureWebReportLocations(stationNo):
    reportSiteLocation = SITE_DIR_TEMPL.format(stationNo)
    if not os.path.isdir(reportSiteLocation):
        os.mkdir(reportSiteLocation)

def dtdd(dt, dd):
    return "{}\n:    {}\n\n".format(dt, dd)
    
"""
Hide need to include DATA_LOCN_TEMPL and SCHEMA
"""
def filteredResultIterator(stationNo, flTyp, useRF=False, startAtReply=""):
    locn = DATARF_LOCN_TEMPL.format(stationNo) if useRF else DATA_LOCN_TEMPL.format(stationNo)
    return FilteredResultIterator(locn, flTyp, startAtReply=startAtReply)
    
def loadSelectTypes(stationNo):
    return  json.load(open(SCHEMA_LOCN_TEMPL.format(stationNo) + "SELECT_TYPES.json"))

# ############################### Stat Utils #########################

"""
Shows off key stats with a little (obvious) stats observations

https://docs.scipy.org/doc/numpy/user/

TODO: more on statistics (and numpy?) ... median_low etc for rounded
"""
def reportKeyStats(kstats):
    print("Count Values: {}".format(kstats["count"]))
    mn = kstats["mean"]
    print("Mean: {}".format(mn))
    M = kstats["median"]
    print("Median (M): {}".format(M))
    if M > mn:
        print("\t... M bigger than Mean so data skews left")
    elif M < mn:
        print("\t... M smaller than Mean so data skews right")
    print("Standard Deviation (s): {}".format(kstats["std"]))
    print("\treflect skew of min {} and max {}".format(kstats["min"], kstats["max"]))
    print("IQR: {}".format(kstats["iqr"]))                                                   
    print("\tbetween 1st ({}) and 3rd ({}) quartiles".format(kstats["quartileOne"], kstats["quartileThree"]))
    if "olt" in kstats:
        print("Outliers below", kstats["olt"])
    print("Outliers above\n", kstats["oht"])
    
"""
Key stats for distribution of values

TODO: fully expand on statistics (median_low etc) and not just numpy repeat
(method= ...)

min, max
Quartile: 1, 2 (Median), 3 for data-spread
... "five-number summary" ideal for data w/ outliers and a 'box-and-whisker' plot 
... Quartiles divide a rank-ordered data set into four equal parts at 25, 50, 75
percentiles
IQR
... "midspread" - best at spread if outliers
olt < (Q1-1.5*IQR)
oht > Q3+1.5*IQR
... for key outliers: < are lows, > are highs. Only present if > max, < min
mean
std
... for symm distributions with no outliers where five numbers don't kick in

TODO: consider <span class='yellowIt'>{:.2f}%</span> and numpy.around or
roundFloat (see below)

oht: 1.5 == "inner fences"
major outliers: Q3 + 3*IQR == "outer fences" ... need name for this.

Note: this is 'Univariate method' (See: https://www.kdnuggets.com/2017/01/3-methods-deal-outliers.html / 'Minkowski error' etc)

https://en.wikipedia.org/wiki/Outlier (Tukey's fences)
- above: Q3 + K(Q3-Q1) where K is 1.5 and K = 3 is "far out"
- below: Q1 - K(Q1-Q3)
ie/ K times Quartile. Fences for box plots.
"""    
def keyStats(values):
    try: # tmp allow for < 3.8
        quartiles = statistics.quantiles(values, method="inclusive") # inc matched numpy
    except:
        import numpy
        quartiles = [numpy.percentile(values, 25), numpy.percentile(values, 50), numpy.percentile(values, 75)]
    quartileOne = quartiles[0] # numpy.percentile(values, 25)
    median = quartiles[1] # numpy.percentile(values, 50)
    quartileThree = quartiles[2] # numpy.percentile(values, 75)
    # get variance in middle 50% of data
    # numpy.subtract(*numpy.percentile(values, [75, 25]))
    iqr = quartileThree - quartileOne # interquartile range    
    oht = quartileThree + (1.5 * iqr) # Outlier High above this
    cntValsGTOHT = sum(1 for val in values if val > oht) 
    ohto = quartileThree + (3 * iqr) # idea of "outer fence": TODO: get name
    cntValsGTOHTO = sum(1 for val in values if val > ohto) 
    mx = sorted(values)[-1] # numpy.max(values)
    mn = sorted(values)[0] # numpy.min(values)
    stats = {"total": sum(val for val in values), "count": len(values), "min": mn, "quartileOne": quartileOne, "median": median, "quartileThree": quartileThree, "max": mx, "iqr": iqr, "oht": oht, "ohto": ohto, "mean": statistics.mean(values), "std": statistics.stdev(values)}
    olt = quartileOne - (1.5 * iqr) # Outlier Low below this
    if int(olt) > 0: # only olt if > 0 ie/ negative ie/ all acceptable
        stats["olt"] = olt
    """
    Own: should show outliers? only go into outliers if big ie/ if pretty smooth 
    """
    stats["hasOutliers"] = True if stats["max"] - stats["oht"] > stats["median"] else False
    if cntValsGTOHT:
        stats["gtoht"] = cntValsGTOHT
    if cntValsGTOHTO:
        stats["gtohto"] = cntValsGTOHTO
    return stats
    
"""
Use typically for byValueCount off typer or a Counter

    "a": 1
    "b": 2
    "c": 1
    
-----> [a, b, b, c]

and can pass into kstats if forceInt

Note: forceInt is for the measured values which may be integers but
are in string form.
"""
def flattenFrequencyDistribution(freqDistrib, forceInt=True):
    freqDistribFlat = []
    for entry in freqDistrib:
        f = [int(entry) if forceInt else entry for i in range(int(freqDistrib[entry]))]
        freqDistribFlat.extend(f)
    return freqDistribFlat
    
"""
New Stats to expand:

- (basic) and relative (percent/ration) frequency distribution ie/ cnt occurrences
        from collections import Counter
        Counter([...]) ... 
  ... put relatives into a stacked bar chart
  ... conditional => a number of freq distribs, one each per condition (ex/ for PDFs, WSs)
- bar (or a pie) to histogram: when # of distict values too big then go to histogram
- null hypothesis/expected frequencies: variables unrelated (type of image and WS?)
  - https://www.spss-tutorials.com/chi-square-independence-test/
"""

"""
- cumulative frequencies add as go (https://www.spss-tutorials.com/frequency-distribution-what-is-it/) ... no good for nominals ("French" or "PDF") but for good/better/best ...
  ie age of patients  ... https://www.wyzant.com/resources/lessons/math/statistics_and_probability/averages/cumulative_frequency_percentiles_and_quartiles
  ... A cumulative frequency graph, also known as an Ogive
  ... good site for stuff.
  ... cumulative freq can be used to gen quartiles
"""        

"""
Clustering, numpy has it (ntlk uses it - but mainly see intelligent web book)
... k ... and clumping 'users' or ... based on similarity/distance.
"""

"""
after excel, try matplotlib, networkx 
"""
    
# ############################ Simple Report Utils #################

"""
If X.0 -> 0 otherwise to 2 pts (or whatever is passed in)
"""
def roundFloat(no, to=2):
    no = no.round(to)
    if no.is_integer():
        return int(no)
    return no
    
# ############################ Plot Utils ##########################

"""
Crude Example of Graph

import matplotlib.pyplot as plt

See: https://python-graph-gallery.com/120-line-chart-with-matplotlib/ and
https://matplotlib.org/gallery/index.html

    plot([2007, 2008, 2009, 2010], [1, 2, 3, 4])

"""
def plot(xs, ys):

    import matplotlib.pyplot as plt
    plt.plot(xs, ys, "ro")
    plt.xlabel("Time")
    plt.ylabel("Ibs")
    plt.show()
            
# ######################### Reduce Users ###########################

"""
Returns Users, Indexed 

Note: RF part ie/ 200 into DataRF will move out of here. Tmp index
maker for any type (including RF types) will become one simple utility.

TODO: go to lookup by IEN as simpler

Note: not dynamic if primary_menu_option or creator or title or # props >= 18 (or 16?)
"""
def reduce200(stationNo, onlyUsers=None, forceNew=False, coreOnly=False):

    jsnFl = TMPWORKING_LOCN_TEMPL.format(stationNo) + "userReduction{}.json".format("CORE" if coreOnly else "")
    
    if not forceNew:
        try:
            infosByRef = json.load(open(jsnFl))
        except:
            pass
        else:
            return infosByRef

    allThere, details = checkDataPresent(stationNo, [
        # Additional settings/properties:
        # - duration (in seconds)
        # - force count on
        #     ipv4_address, remote_station_id, remote_user_ien, duration
        {"fileType": "200", "check": "ALL"} # Index
    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    print("First time through, creating index by id for Users (200) for {}".format(stationNo))
    
    dataLocn = DATA_LOCN_TEMPL.format(stationNo)
    resourceIter = FilteredResultIterator(dataLocn, "200")
    infosByRef = {}
    cnt = 0
    for resource in resourceIter:
        cnt += 1
                
        if cnt % 1000 == 0:
            print("Processed another 1000 users - now at {:,}".format(len(infosByRef)))
        
        if onlyUsers and resource["_id"] not in onlyUsers:
            continue
        
        userId = "{} [{}]".format(resource["label"], resource["_id"])
                
        info = {"hasProps": sorted([key for key in resource if key not in set(["_id", "label", "type"])])}
        
        if "initial" in resource: # ex/ SMITH, JOE M --> JMS etc
            info["initial"] = resource["initial"]
        
        if "creator" in resource:
            # Only v1.1 will even have this ie/ not V10 on
            if resource["creator"]["id"] != "200-0":
                creatorRef = "{} [{}]".format(resource["creator"]["label"], resource["creator"]["id"])
                info["creator"] = creatorRef
        
        if "date_entered" in resource:
            info["date_entered"] = resource["date_entered"]["value"]
            
        if "title" in resource:
            info["title"] = resource["title"]["label"] # it's a pointer
            
        if "sex" in resource:
            info["sex"] = resource["sex"] # old fashioned gender
            
        if "ssn" in resource:
            info["ssn"] = resource["ssn"]
            
        # used for lookup BEFORE SSN in setup. goes with subject_organizations etc
        # ... comment says within VA, VA SSOi, secid is the unique field
        if "secid" in resource:
            info["secid"] = resource["secid"]
            # MOST are Dept of Vet Affairs - some VHA
            if "subject_organization" in resource:
                if resource["subject_organization"] not in ["Department Of Veterans Affairs", "Veterans Health Administration"]:
                    print("** WARNING: Expected Subject Org for sec id to always be VA! but {}".format(resource["subject_organization"]))
                if resource["subject_organization"] == "Veterans Health Administration":
                    info["is_subject_organization_vha"] = True
            
        # leave termination_reason for props list (ie/ presence or not)
        if "termination_date" in resource:
            info["termination_date"] = resource["termination_date"]["value"]
            
        if "network_username" in resource:
            info["network_username"] = resource["network_username"]   
            
        # adupn == va.gov email ... just check for now
        if "adupn" in resource and not re.search(r'va.gov$', resource["adupn"]):
            print("** unexpected adupn - email - not va.gov: {}".format(resource["adupn"]))
            if "email_address" in resource and resource["email_address"] != resource["adupn"]:
                print("** unexpected adupn - doesn't match email_address property: {}".format(resource["adupn"], resource["email_address"]))            
            
        """
        Latest entries can have unique_user_id BUT mainly == secid or is email.
        
        Issue with not taking as is maybe that intention to use for lookup may
        be missed - no as obvious there as listed in has_props
        """
        if "unique_user_id" in resource and not re.sub(r' ', '', resource["unique_user_id"]) == "":
            if re.search(r'\@', resource["unique_user_id"]):
                if "email_address" in resource and resource["unique_user_id"] != resource["email_address"]:
                    info["distinct_unique_user_id"] = resource["unique_user_id"]
            elif ("secid" in info and resource["unique_user_id"] != info["secid"]) or "secid" not in info:
                info["__distinct_unique_user_id"] = resource["unique_user_id"]
                                            
        if "last_signon_date_time" in resource:
            info["last_signon_date_time"] = resource["last_signon_date_time"]["value"]
            
        infosByRef[userId] = info 
            
        if coreOnly:
            continue
                            
        if "user_class" in resource:
            if len(resource["user_class"]) > 1:
                raise Exception("Expected only one user class assertion - ie/ singleton multiple")
            info["user_class"] = [uci["user_class"]["label"] for uci in resource["user_class"]][0]
            
        if "file_manager_access_code" in resource and resource["file_manager_access_code"] == "@":
            info["has_fileman_programmer_access"] = True
                
        if "primary_menu_option" in resource:
            info["primary_menu_option"] = resource["primary_menu_option"]["label"]
                
        if "secondary_menu_options" in resource:
            smos = set() # allows for dups with crude SMO addition
            for smo in resource["secondary_menu_options"]:
                if "secondary_menu_options" not in smo:
                    continue
                if not re.match(r'\d+$', smo["secondary_menu_options"]["label"]):
                    smos.add(smo["secondary_menu_options"]["label"])
            if len(smos):
                info["secondary_menu_options"] = sorted(list(smos))
            
        if "delegated_options" in resource:
            dos = set()
            for delo in resource["delegated_options"]:
                if "delegated_options" not in delo:
                    continue # seen in 663
                if not re.match(r'\d+$', delo["delegated_options"]["label"]):
                    dos.add(delo["delegated_options"]["label"])
            if len(dos):                   
                info["delegated_options"] = sorted(list(dos))
            
        if "keys" in resource:
            keys = set() 
            for key in resource["keys"]:
                if "key" not in key:
                    continue
                if not re.match(r'\d+$', key["key"]["label"]):
                    keys.add(key["key"]["label"])
            if len(keys):
                info["keys"] = sorted(list(keys))   
                
        if "preferred_editor" in resource: # for REMOTE user checks
            info["preferred_editor"] = resource["preferred_editor"]["label"]
            
        if "terminal_type_last_used" in resource:
            info["terminal_type_last_used"] = resource["terminal_type_last_used"]["label"] 
            
        # Consider "first sign on"
        if "visited_from" in resource:
            finalVisitedTime = None
            visitedFroms = {}
            for i, mresource in enumerate(resource["visited_from"]):
                if "visited_from" in mresource: 
                    visitedFrom = re.sub(r'[^\d]+', '', mresource["visited_from"])
                    duzAtHomeSite = mresource["duz_at_home_site"] if "duz_at_home_site" in mresource else ""
                    siteName = mresource["site_name"] if "site_name" in mresource else ""
                    siteId = ":".join([visitedFrom, duzAtHomeSite, siteName])
                    details = None
                    if "first_visit" in mresource or "last_visited" in mresource:
                        details = {}
                        if "first_visit" in mresource:
                            details["first"] = mresource["first_visit"]["value"]
                        if "last_visited" in mresource:
                            details["last"] = mresource["last_visited"]["value"]                            
                    visitedFroms[siteId] = details
            if len(visitedFroms):
                info["signed_on_froms"] = visitedFroms
            
    print("Serializing and Returning Index of {:,} Users (200)".format(cnt))
    if coreOnly:
        print("\t... core only")

    json.dump(infosByRef, open(jsnFl, "w"), indent=4)
    
    return infosByRef
    
# ############################ Reduce Patient ########################

"""
if "date_of_death" in info: # note: may or may not have date_entered_into_file too
    isDeceased
... 1/5 or more.
"""
def reduce2(stationNo, forceNew=False):

    jsnFl = TMPWORKING_LOCN_TEMPL.format(stationNo) + "patientReduction.json"
    
    if not forceNew:
        try:
            infosByIEN = json.load(open(jsnFl))
        except:
            pass
        else:
            return infosByIEN

    print("First time through, creating patient entered reduction for {}".format(stationNo))
    sys.stdout.flush()
    
    dataLocn = DATA_LOCN_TEMPL.format(stationNo)
    resourceIter = FilteredResultIterator(dataLocn, "2")
    infosByIEN = {}
    PROPS_TO_TAKE = set([
        "name", 
        "sex", 
        "date_of_birth", 
        "social_security_number", 
        
        "who_entered_patient", 
        "date_entered_into_file", 
        
        "city", 
        "state", 
        "zip_code", 
        
        "period_of_service", 
        
        "date_of_death", 
        "death_entered_by", 
        
        "primary_eligibility_code", 
        "combat_service_indicated", 
        
        "preferred_facility", 
        
        # TODO: expand these - ensure all id's used by VA/C are in here
        "integration_control_number", 
        "subscription_control_number", # 774 entries for CIRN (see if sync file
        "full_icn",
        "primary_long_id", # see queue on where differs from SSN
        "primary_short_id" # may be redundant but get to see   
    ])
    """
    What should be
    - short_id == end of long_id
    - long_id == - version of ssn ie/ 111-22-3333 vs 111223333
    - icn is first part of full_icn
    ... ie/ nixing redundancies
    """
    def cutIds(info):
        if "integration_control_number" in info:
            if "full_icn" in info and info["integration_control_number"] == info["full_icn"].split("V")[0]:
                del info["integration_control_number"]
        if "primary_short_id" in info:
            if "primary_long_id" in info and info["primary_short_id"] == info["primary_long_id"].split("-")[-1]:
                del info["primary_short_id"]
        # in WWW, only if bug
        if "social_security_number" in info and "primary_long_id" in info:
            if info["social_security_number"] == re.sub(r'\-', "", info["primary_long_id"]):
                del info["primary_long_id"]
    for resource in resourceIter:
        patientIEN = resource["_id"].split("-")[1]
        info = {"ien": patientIEN}
        for prop in PROPS_TO_TAKE:
            if prop in resource:
                if isinstance(resource[prop], list):
                    raise Exception("Not reducing multiples of 2")
                if isinstance(resource[prop], dict):
                    if "value" in resource[prop]:
                        info[prop] = resource[prop]["value"]
                    else:
                        info[prop] = resource[prop]["label"]
                else: 
                    info[prop] = resource[prop]
        cutIds(info)
        infosByIEN[patientIEN] = info
        if len(infosByIEN) % 1000 == 0:
            print("Processed another 1000 patients - now at {:,}".format(len(infosByIEN)))
            sys.stdout.flush()
    
    print("Serializing and Returning Index of {:,} Patients (2)".format(len(infosByIEN)))
    sys.stdout.flush()

    json.dump(infosByIEN, open(jsnFl, "w"), indent=4)
    
    return infosByIEN
    
# ################# Reduce Location (44) n Institution (4) ####################

"""
Like other "anchor file" reductions, preludes to more formal reframes (RF) that
split out different types of key data into distinct types AND establishes a
lookup 

<----- will see if AppointmentHospitalLocation can be a sub class or split out appt info

Note: allows RF take - right now that RF is just the result of extracting the
44.001 and other multiples.
"""
def reduce44(stationNo, useRF=True): # do from RF

    jsnFl = TMPWORKING_LOCN_TEMPL.format(stationNo) + "hlReduction.json"
    try:
        infosByIEN = json.load(open(jsnFl))
    except:
        pass
    else:
        return infosByIEN
    print("First time through, creating hospital location reduction for {}".format(stationNo))
    sys.stdout.flush()
    infosByIEN = {}
    countWProvider = 0
    countDefaultProviderNotInProvider = 0
    def copyMProp(resource, red, mprop):
        if mprop not in resource:
            return None
        red[mprop] = set()
        for mresource in resource[mprop]:
            pref = "{} [{}]".format(mresource[mprop]["label"], mresource[mprop]["id"].split("-")[1])
            red[mprop].add(pref)
        red[mprop] = list(red[mprop])
        return red
    institutionsByHPrefix = defaultdict(lambda: Counter()) # for mapping
    cnt = 0
    for resource in filteredResultIterator(stationNo, "44", useRF=useRF):
        ien = resource["_id"].split("-")[1]
        red = {"ien": ien, "label": resource["name"]}
        infosByIEN[ien] = red
        cnt += 1
        if (cnt % 200) == 0:
            print("processed another 200 to {:,}".format(cnt))
            sys.stdout.flush()
        for litProp in ["abbreviation", "patient_friendly_name", "physical_location", "length_of_appointment", "default_appointment_type", "noncount_clinic_y_or_n", "clinic_meets_at_this_facility"]: # includes enum
            if litProp not in resource:
                continue
            red[litProp] = resource[litProp]
        for dtProp in ["inactivate_date", "reactivate_date", "availability_flag"]:
            if dtProp not in resource:
                continue
            red[dtProp] = resource[dtProp]["value"]
        for refProp in ["stop_code_number", "credit_stop_code", "institution", "division", "type_extension", "default_provider"]:
            if refProp not in resource:
                continue
            refv = resource[refProp]
            ref = "{} [{}]".format(refv["label"], refv["id"].split("-")[1])
            red[refProp] = ref
            if refProp == "institution":
                hprefix = re.sub(r'^ZZ', '', re.split(r'[ \-\/]', resource["name"])[0])
                if len(hprefix):
                    institutionsByHPrefix[hprefix][ref] += 1
        # Mult Availability - note many exs where no appts
        if "availability" in resource: # want to see if always there if appointments too
            red["has_availability"] = True
        if copyMProp(resource, red, "provider"):
            if "default_provider" in red and red["default_provider"] not in red["provider"]:
                countDefaultProviderNotInProvider += 1
            countWProvider += 1
        copyMProp(resource, red, "privileged_user") # the clerks etc
        # Note: appointment FLIPPED/REDUCED so won't know that?
    
    """    
    Fill in missing instit links based on prefix mappings from those with an instit
    
    Note that based on error'ed assignment of prefixes, > 1 institution my be assigned
    a prefix. We will take majority rule so it there is > one then 
    """
    ninstitutionsByHPrefix = {}
    for hprefix in institutionsByHPrefix:
        if len(list(institutionsByHPrefix)) == 1:
            ninstitutionsByHPrefix[hprefix] = list(institutionsByHPrefix)[0]
            continue
        useTotal = sum(institutionsByHPrefix[hprefix][instit] for instit in institutionsByHPrefix[hprefix])
        for instit in institutionsByHPrefix[hprefix]:
            if float(institutionsByHPrefix[hprefix][instit])/useTotal >= 0.75:
                ninstitutionsByHPrefix[hprefix] = instit
                break
    noMissing = 0
    noFilled = 0
    for ien in infosByIEN:
        info = infosByIEN[ien]
        if "institution" in info:
            continue
        noMissing += 1
        hprefix = re.split(r'[ \-\/]', info["label"])[0]
        if hprefix in ninstitutionsByHPrefix:
            info["institution"] = ninstitutionsByHPrefix[hprefix]
            noFilled += 1
    print("Of {:,} locations missing an institution link, {:,} were filled by heuristic".format(noMissing, noFilled))
        
    print("Dumping {:,} locations, {:,} have providers with {:,} having default provider not in provider list".format(len(infosByIEN), countWProvider, countDefaultProviderNotInProvider))
    json.dump(infosByIEN, open(jsnFl, "w"), indent=4)
    return infosByIEN

"""
name, short_name | names
status, inactive_facility_flag | National or Local and if active. Nationals are maintained by MFS and should have a station number (expect Nationals same across VistAs)
station_number, official_va_name | Nationals should have these and they should not be changed by a site (expect same cross VistAs)
facility_type | facility_type (pter to meta file) replaces va_type_code
reporting_station | "pointer back to the Institution file that indicates the site that does the reporting to VACO." TODO: if SPOK for clinics etc
location_timezone | time zone of location
multi-division facility | TODO: see if useful

For now ignoring, address, agency_code etc

TODO: push into reduction useful for nationals -- use association
"""
def reduce4(stationNo):
    jsnFl = TMPWORKING_LOCN_TEMPL.format(stationNo) + "4Reduction.json"
    try:
        infosByIEN = json.load(open(jsnFl))
    except:
        pass
    else:
        return infosByIEN
    print("First time through, creating institution reduction for {}".format(stationNo))
    infosByIEN = {}
    for resource in filteredResultIterator(stationNo, "4"):
        ien = resource["_id"].split("-")[1]
        red = {"ien": ien, "label": resource["name"]}
        infosByIEN[ien] = red
        # OPEN QUESTION: any useful or now used for national ... see
        for refProp in ["reporting_station", "facility_type", "location_timezone"]:
            if refProp not in resource:
                continue
            red[refProp] = "{} [{}]".format(resource[refProp]["label"], resource[refProp]["id"].split("-")[1])
        if "inactive_facility_flag" in resource:
            red["isInactive"] = True
        if "status" in resource:
            if resource["status"] == "N:National":
                red["isNational"] = True
        for prop in ["short_name", "multi_division_facility", "npi", "official_va_name", "station_number"]:
            if prop not in resource:
                continue
            red[prop] = resource[prop]
        # VISN, Parent Facility etc
        if "associations" in resource:
            for association in resource["associations"]:
                if "parent_of_association" not in association:
                    continue
                atyp = association["associations"]
                apred = re.sub(r' ', '_', atyp["label"].lower())
                ref = association["parent_of_association"]
                if ref["id"] == resource["_id"]:
                    continue # avoid self reference in Puget being parent of Puget
                red[apred] = ref
        # EX/ VISTANUM == stationNumber but npi too (also explicit?)
        # ... has status and effective_date_time too
        # ... https://npiregistry.cms.hhs.gov/registry/provider-view/1477502946 ... 
        # America Lake
        if "identifier" in resource:
            for identifier in resource["identifier"]:
                ityp = identifier["coding_system"]
                ipred = re.sub(r' ', '_', ityp.lower()) + "_id"
                id02 = identifier["id__02"]
                red[ipred] = id02
        # taxonomy_code - reduce to list
    json.dump(infosByIEN, open(jsnFl, "w"), indent=4)
    return infosByIEN

"""
Utility for making tmp's - flatten out dates, pters etc

TODO: add to reduction utilities.
"""
def flattenPropValues(resource, nixTypeLabel=True): # not recursive
    if nixTypeLabel:
        for prop in ["type", "label"]:
            if prop in resource:
                del resource[prop]
    for prop in resource.keys():
        if isinstance(resource[prop], list):
            for mresource in resource[prop]:
                flattenPropValues(mresource, False)
            continue
        if not isinstance(resource[prop], dict):
            continue
        if "value" in resource[prop]:
            resource[prop] = resource[prop]["value"]
            continue
        if "id" in resource[prop]:
            resource[prop] = "{} [{}]".format(resource[prop]["label"], resource[prop]["id"])
    
# ############################ Simple Reusable MD Makers ###############################

def mdFilesOfDomain(stationNo, domainName, bottomFileNo, beyondFileNo, usedFiles):

    selectTypes = loadSelectTypes(stationNo)

    fileTypeInfos = [typeInfo for typeInfo in selectTypes["results"] if "number" in typeInfo and float(typeInfo["number"]) >= bottomFileNo and float(typeInfo["number"]) < beyondFileNo and "count" in typeInfo]
     
    mu = """There are <span class="yellowIt">{:,}</span> files in the system dedicated to the _{}_ ...
    
""".format(len(fileTypeInfos), domainName)
    
    tbl = MarkdownTable(["Name", "\#", "Count"])
    for typeInfo in fileTypeInfos:
        tbl.addRow([
                "__{}__".format(typeInfo["name"]) if typeInfo["name"] in usedFiles else typeInfo["name"], 
            typeInfo["number"], 
            typeInfo["count"]
    ])
    mu += tbl.md() + "\n\n"
        
    return mu
    
# ##################### Plot Creation #########################
        
"""
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
    imageDir = f'{VISTA_DATA_BASE_DIR}{stationNo}/ReportSite/Images
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
    
# ######################### Simple Type Utils ########################

class PropertyCounter:
    
    def __init__(self):
        self.__counts = Counter()
        self.__countResources = 0
            
    def resourceProperties(self, props):
        for prop in props:
            self.__counts[prop] += 1
        self.__countResources += 1
            
    def mandatories(self):
        return sorted([prop for prop in self.__counts if self.__counts[prop] == self.__countResources]) 
            
    def optionalCounts(self):
        return dict((prop, self.__counts[prop]) for prop in self.__counts if self.__counts[prop] < self.__countResources) 
