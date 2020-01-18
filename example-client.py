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

    print("\n--Location Info--")
    records = locations['records']
    location_info = records[0]
    if location_info:
        site_id = location_info.get('siteId')
        print(f"Site id: {site_id}")
        pp.pprint( bluebolt.location_details(site_id) )
    
    for location in locations['records']:
        site_id = location['siteId']
        print(f"\n--Devices in Location {site_id}--")
        devices = bluebolt.devices(site_id)
        pp.pprint( devices )

        for device in devices['devList']:
            device_class = device['devClass']
            device_id = device['devId']
            
            print(f"\nOutlet status for device {device_class} / {device_id}")
            pp.pprint( bluebolt.device(site_id, device_class, device_id) )
            pp.pprint( bluebolt.outlets(site_id, device_class, device_id) )
    
if __name__ == "__main__":
    main()
