#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter

"""           
Station Numbers

- 3 digits (say 5+ too but why?)
- appended with a suffix such as 'A' or '9' (9 is a special case, representing a nursing home subdivision).
- 200-series station numbers, which are only allocated to Austin Information Technology
Center (AITC) systems
(from vistalink manual: https://www.va.gov/vdl/documents/Infrastructure/VistALink/vistalink_1_6_dg.pdf)
"""
SSNO_DEFINITIONS = { # see p81 for main SSNs ... list all and role
    "101": "Central Office, Washington, DC",
    "104": "AAC, Finance Center",
    "200": "AAC",
    
    # Go with 100 for CAPRI ie/ pairing - logon first with 100 and then back?
    "318": "Regional Office - Winston-Salem, NC", # see p82 for regional offices and their 3**
    "377": "Regional Office - San Diego, CA",
    
    "436": "FORT HARRISON MT",
    "442": "CHEYENNE", # given as "regional office and medical center"
    "459": "VA Pacific Islands Health Care System", # Tripler (and used for JLV testing)
    "463": "ANCHORAGE AK", # given as Domiciliary - REGION 2
    "506": "ANN ARBOR", # given as medical center
    "523": "BOSTON", # given as "medical center"
    "528": "BUFFALO", # given as "medical center"
    "531": "BOISE ID", # REGION 2
    "554": "DENVER", # given as "medical center"
    "570": "FRESNO", # given as medical center
    "573": "GAINESVILLE", # given as "medical center"
    "580": "HOUSTON", # given as "medical center"
    "583": "INDIANAPOLIS", # given as medical center
    "589": "KANSAS CITY",
    "600": "LONG BEACH",
    "612": "MARTINEZ (NORTHERN CA)", # https://www.northerncalifornia.va.gov/locations/Martinez_OPC.asp - given as Medical Center
    "636": "OMAHA", # given as "medical center"
    "640": "PALO ALTO", # given as "medical center"
    "644": "PHOENIX", # VAMC
    "648": "PORTLAND OR", # given as "medical center" - REGION 2
    "653": "ROSEBURG OR", # REGION 2
    "660": "SALT LAKE CITY", # given as "medical center"
    "662": "SAN FRANCISCO",
    "663": "PUGET SOUND", # America Lake + Seattle Division - given as "medical center" Seattle - REGION 2 
    "664": "SAN DIEGO",
    "668": "SPOKANE", # Mann-Grandstaf - https://www.spokane.va.gov/ - given as "medical center" - REGION 2
    "671": "SAN ANTONIO", # given as medical center
    "678": "SOUTHERN ARIZONA",
    "687": "WALLA WALLA", # given as "medical center" - REGION 2
    "691": "WEST LA",
    "692": "WHITE CITY OR", # REGION 2
    
    "740": "VA Texas Valley Coastal Bend Health Care System", # VISN 17 - part of lift and
}

SUBSSNS = {
    "663": "Seattle",
    "663A4": "America Lake (Tacoma)", # given as DOMICILIARIES, REHABILITATION TREATMENT PROGRAM
    "663GA": "Richland", 
    "663GB": "Bremerton",
    "663GC": "Longview",
    "663GD": "Chehalis",
    
    "442": "Cheyenne",
    "442GC": "Fort Collins",
    
    "200": "VA AAC", # see more 200's in PDF p68 ie/ Austin Automation Center
    "200AA": "VA Records Center and Vault",
    "200BR": "Blind Rehabilitation System"
}

REMOTE_CHECK = ["442", "640"]
INTERESTING_CHECK = ["442", "523", "531", "640", "648", "653", "663", "668", "687", "692"]

"""
CRUDE 640 - IP VPR

	Counter({u'10.206.18.34': 4243, u'10.206.18.33': 4183, u'10.206.18.32': 4123, u'10.206.18.35': 4066, u'10.206.18.17': 3703, u'10.206.18.16': 3671, u'10.206.18.19': 3641, u'10.206.18.18': 3593, u'10.206.18.20': 3340, u'10.227.224.40': 1662, u'10.227.224.37': 1564, u'10.227.224.35': 1556, u'10.227.224.36': 1496, u'10.227.224.126': 1140, u'10.227.224.85': 1128, u'10.227.224.108': 1101, u'10.227.224.106': 1018, u'10.227.224.138': 945, u'10.206.18.70': 509, u'10.206.18.63': 492, u'10.206.18.64': 485, u'10.206.18.66': 460, u'10.206.18.69': 460, u'10.206.18.71': 438, u'10.206.18.65': 427, u'10.206.18.68': 427, u'10.206.18.90': 426, u'10.206.18.67': 425, u'10.206.18.89': 393, u'10.224.18.18': 247, u'10.224.18.17': 240, u'10.224.18.30': 236, u'10.224.18.19': 236, u'10.224.18.20': 216, u'10.224.18.31': 211, u'10.224.18.33': 207, u'10.224.18.16': 200, u'10.224.18.32': 199, u'10.206.184.44': 128, u'10.206.184.46': 126, u'10.206.184.38': 117, u'10.206.184.45': 114, u'10.206.184.67': 53, u'10.206.184.69': 48, u'10.206.184.21': 43, u'10.206.184.83': 36, u'10.227.224.167': 34, u'10.206.184.70': 33, u'10.227.224.171': 25, u'10.227.224.175': 21})
"""

# JLV_PRODUCTION_VDS_IP_ADDRESSES 
JLV_INVA_IPS = [
    '10.224.18.16',
    '10.224.18.17',
    '10.224.18.18',
    '10.224.18.19',
    '10.224.18.20',
    '10.224.18.30',
    '10.224.18.31',
    '10.224.18.32',
    '10.224.18.33',
    '10.224.18.65',
    '10.224.18.66',
    '10.224.18.67',
    '10.224.18.68',
    '10.224.18.69',
    '10.224.18.70',
    '10.224.18.71',
    '10.224.18.72',
    '10.224.18.73',
    '10.224.18.74',
    '10.224.18.75',
    '10.224.18.137',
    '10.224.18.138',
    '10.224.18.139',
    '10.224.18.140',
    '10.224.18.141',
    
    '10.206.18.16',
    '10.206.18.17',
    '10.206.18.18',
    '10.206.18.19',
    '10.206.18.20',
    '10.206.18.32',
    '10.206.18.33',
    '10.206.18.34',
    '10.206.18.35',
    '10.206.18.63',
    '10.206.18.64',
    '10.206.18.65',
    '10.206.18.66',
    '10.206.18.67',
    '10.206.18.68',
    '10.206.18.69',
    '10.206.18.70',
    '10.206.18.71',
    '10.206.18.72',
    '10.206.18.73'
]
    
JLV_CV_IPS = [    # Community Viewer - does this make sense?
    '10.227.224.167',
    '10.227.224.171',
    '10.227.224.173',
    '10.227.224.174',
    '10.227.224.175',
]

# EXTRA IPs - have 10WS too and right SMOs (with VPR) in user
JLV_INVA_EXTRA_IPS = [

	'10.206.18.89', # extra two - or fill in 72-88 too?
	'10.206.18.90',
	
	'10.206.184.21', # extra 206 for JLV?
	'10.206.184.38',
	'10.206.184.44',
	'10.206.184.45',
	'10.206.184.46',
	'10.206.184.67',
	'10.206.184.69',
	'10.206.184.70',
	'10.206.184.83',
	
	'10.227.224.35', # PERHAPS more COMMUNITY? and see above, have VPR!
	'10.227.224.36',
	'10.227.224.37',
	'10.227.224.40',
	'10.227.224.85',
    '10.227.224.106',
	'10.227.224.108',
	'10.227.224.126',
	'10.227.224.138'
	
]

JLV_ALL_IPS = list(set(JLV_INVA_IPS).union(set(JLV_INVA_EXTRA_IPS)).union(set(JLV_CV_IPS)))

# 10.184.[36|38|165].

VISTAWEBPROD_IP = '10.224.74.88'

# Question here of whether see a XWB{ old style sign on and then the real BSE one?
IMAGING_IP_BY_STATION = {
    '442': '10.152.80.125',
    '640': '10.168.30.145',
    '740': '10.141.141.40' 
}


# User identifying information from 3.081 reduction by user (vs JLV IPs)
# ... note: app is 'VISTA IMAGING VIX' and MHV probably == MyHealtheVet
# ... no special IPs as use local IPs
CVIX_MHVUSER_SSNIEN = "200:412864" # expect 2001 too and 2006_95's >> sign ons
CVIX_USER_SSNIEN = "200:217122" # expect 2001 too; 2006_95 << sign ons 

## MM == million man
MM_BOSTON_APP_SSNIEN = "523:14358"
MM_BOSTON_APP_IPS = ["10.225.31.135", "10.224.31.182"]
MM_ANN_ARBOR_APP_SSNIEN = "506:10000029117"
MM_ANN_ARBOR_APP_IPS = ["10.224.80.121", "10.225.81.65"] # first IP used in other users too

CONNECTOR_PROXIES = [

    {
        "name": "VISTALINK",
        "description": "The VistALink 1.5 resource adapter is a transport layer that provides communication between HealtheVet-VistA Java applications and VistA/M servers ... Supports VistA modules requiring this communication capability, including Patient Advocate Tracking System (PATS), Veterans Personal Finance System (VPFS) and Blind Rehabilitation",
        "notes": [
            "Kernel XUMGR key is required to create the connector proxy user account",
            "To allow VistALink access from a specific J2EE system (app server), you need an M Kernel 'connector proxy user' account. Each connector deployed on the app server uses this account to establish initial authentication and a trusted connection",
            "Hines EMC data center. These servers host the HealtheVet-VistA Blind Rehabilitation 5.0 application and require the Connector Proxy User account to execute RPC’s on your VistA/M system [ie/ this service is Hines and it gets one a/c?] ... The Blind Rehabilitation (BR) V5.0 application provides enhanced tracking, and reporting, of the blind rehabilitation services provided to veterans"
        ],
        "inMonograph": True,
        "connectionProxyNamePattern": "VISTALINK,EMC *",
        "connectionProxyExamples": "VISTALINK,EMC SSPFW SPOKANE / VISTALINK,EMC HINES",
        "rpcOptions": [
            "XOBV VISTALINK TESTER",
            "XUPS VISTALINK"
        ],
        "rpcOptionQuestions": [
            "AMOJ VISTALINK EQP INV",
            "PSN VISTALINK CONTEXT",
            "VBECS VISTALINK CONTEXT"
        ]
    },

    {
        "name": "Emergency Department Integration Software (EDIS)",
        "description": "incorporates several Web-based views that extend the current Computerized Patient Record System (CPRS) to help healthcare professionals track and manage the flow of patient care in the emergency department setting. ... EDIS runs in Adobe Flash Player",
        "notes": [
            "You must assign to users and clinical application coordinators (CACs) at least one of the following secondary menu options",
            "Site IRM will need to take note of the ACCESS and VERIFY codes and keep these codes in a place that can be later retrieved since these codes will need to be provided to the VPS point of contact in  order to configure the VETLINK VPS Kiosk",
            "Once the CONNECT,VPS user has been defined, the XMUSER menu will need to added as the PRIMARY MENU option AND add the VPS KIOSK INTERFACE broker menu as a Secondary Menu option"
        ],
        "inMonograph": True,
        "connectionProxyName": "CONNECTOR,EDIS",
        "TODO": "fill out all EDPF options",
        "rpcOptions": [
            "EDPF TRACKING MENU ALL",
            "EDPF TRACKING MENU CLINICAN"
        ]
    },

    {
        "name": "VETLINK VA Point of Service (VPS)",
        "description": "VHA has recently identified interactive kiosks as an innovation that will enable VA Medical Centers (VAMCs) to enhance services to veterans and improve the efficiency of operations. ... The VETLINK VPS Kiosk Application Server uses the RPC BROKER to make calls to the Remote Procedures (RPCs) residing on the VistA host.",
        "questions": [
            "Most GET RPCs but can write questionaires and vitals (what files?)",
            "RPC 'VPS WRITE KIOSK PARAMETERS' - what file is this?"
        ],
        "seeAlso": ["https://github.com/OSEHRA/VistA/blob/master/Packages/VA Point of Service/Patches/VPS_1.0_1/VPS-1_SEQ-1_PAT-1.TXT"],
        "inMonograph": True,
        "connectionProxyName": "CONNECT,VPS",
        "rpcOptions": ["VPS KIOSK INTERFACE"]
    },
    
    {
        "name": "DATABRIDGE,PHILIPS",
        "?": "DSS Clinical Information System (CIS)-DataBridge is a software interface solution that filters patient data information from Veterans Health Information Systems and Technology Architecture (VistA) and Clinical Patient Record System (CPRS) to a commercial Intensive Care Unit (ICU)/Anesthesia record keeping (ARK) system."
    }
    
]
