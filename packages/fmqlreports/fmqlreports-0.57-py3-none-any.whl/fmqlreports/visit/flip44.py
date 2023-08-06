#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os

from fmqlutils.cacher.cacherUtils import flip

# flip(stationNo, "2", "appointment", "2_98", "PATIENT APPOINTMENT")

"""
A "multiple flipper" - RF of multiples ie/ simplest RF

Covers:
- 44_00[13] for Legacy Appointments out of 44
"""
def flipAppointments(stationNo):
    flip(stationNo, "44", "appointment", "44_001", "APPOINTMENT")
    # Note: leaving container prop == hospital location as is so pulled
    # in explicitly. 
    flip(stationNo, "44_001", "patient", "44_003", "PATIENT APPOINTMENT", explicitInheritProps=["appointment_date_time"], useRF=True)

# ################################# DRIVER #######################

def main():

    assert sys.version_info >= (3, 4)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO")

    flipAppointments(stationNo)

if __name__ == "__main__":
    main()
