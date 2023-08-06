#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict
from datetime import datetime

from fmqlutils.cacher.cacherUtils import metaOfVistA
from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

from ..webReportUtils import SITE_DIR_TEMPL, TOP_MD_TEMPL, ensureWebReportLocations, reduce4

"""
Note on VistA use

>  ; After setup XOPT holds XUS props of kernel system parameters and DUZ^XUS1A
> ; uses that to pick out the default institution. It does not use SITE^VASITE
> ; which uses (time sensitive) 389.9 to find the system's facility
> ; Note that if a user's entry in 200 indicates multiple institutions, then
> ; normally a user is asked to choose (see: https://www.ihs.gov/RPMS/PackageDocs/XU/krn8_0sm.pdf)
> S DUZ(2)=$S($D(^XTV(8989.3,1,"XUS")):$P(^("XUS"),"^",17),1:"")

and mas pararameters (43) sets divisions ...
https://github.com/vistadataproject/VICSServer/blob/a1b6162148a0ce22c37cd0029c079f4a515309b2/dataAccess/mongoDB/schemas/MasParameters.json
"""

# ################################# DRIVER #######################

"""
Goal is an overall report on institutions highlighting
1. National No Parent (with # of subs)
2. Per National No Parent, subs
3. Locals
... count em and then one table with all including internal refs?

VISN -> VistA (main) Institution -> Child Institutions
Local?

Non VA -- any national?
Non National - what per station? ... move to local station?

state
city
zip
street addr 1
... do mailing too ie/ capture classic nationals and all others are aberations and enforce
National Expectations
"""
def reportInstitutions(stationNo):
    institInfosByIEN = reduce4(stationNo)
    print("Nationals: {}".format(sum(1 for info in institInfosByIEN.values() if "isNational" in info))) 

def main():

    assert sys.version_info >= (3, 4)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO")

    reportInstitutions(stationNo)

if __name__ == "__main__":
    main()
