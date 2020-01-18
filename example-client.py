#!/usr/local/bin/python3

import os
import sys
import pprint
import logging
import json

from pybluebolt import PyBlueBOLT

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main():
    user = os.getenv('BLUEBOLT_USER', None)
    password = os.getenv('BLUEBOLT_PASSWORD', None)

    if (user == None) or (password == None):
        print("ERROR! Must define env variables BLUEBOLT_USER and BLUEBOLT_PASSWORD")
        raise SystemExit

    #setup_logger()
    pp = pprint.PrettyPrinter(indent = 2)
 
    bluebolt = PyBlueBOLT(user, password)

    print(f"Connected? {bluebolt.is_connected}")

    print("\n--Locations--")
    locations = bluebolt.locations()
    pp.pprint( locations )

    print("\n--Single Location--")
    records = locations['records']
    location_info = records[0]
    if location_info:
        site_id = location_info.get('siteId')
        print(f"Site id: {site_id}")
        pp.pprint( bluebolt.location_details(site_id) )
    
    for location in locations['records']:
        site_id = location_info['siteId']
        print(f"\n--Devices in Location {site_id}--")
        pp.pprint( bluebolt.devices(site_id) )
    
if __name__ == "__main__":
    main()
