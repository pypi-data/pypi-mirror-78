#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os

from fmqlutils.cacher.cacherUtils import flip

"""
Peer of flip44
"""
def flipAppointments(stationNo):
    from fmqlutils.cacher.cacherUtils import flip
    flip(stationNo, "2", "appointment", "2_98", "PATIENT APPOINTMENT")

# ################################# DRIVER #######################

def main():

    assert(sys.version_info >= (2,7))

    if len(sys.argv) < 2:
        print("need to specify station # ex/ 442 - exiting")
        return

    stationNo = sys.argv[1]

    flipAppointments(stationNo)

if __name__ == "__main__":
    main()
