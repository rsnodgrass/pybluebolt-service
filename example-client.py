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

    print(f"User = #{bluebolt.user_id}")

    print("\n--Data--")
    pp.pprint( bluebolt.data() )

    print("\n--Locations--")
    locations = bluebolt.locations()
    pp.pprint( locations )

    print("\n--Single Location--")
    location_info = locations[0]
    location_id = location_info['id']    
    pp.pprint( bluebolt.location(location_id) )

    for location in locations:
        for device in location['devices']:
            id = device['id']
        
            print("\n--Device in Locations--")
            pp.pprint( device )
            
            print("\n--Consumption--")
            pp.pprint( bluebolt.consumption(id) )

            print("\n--Device Info--")
            pp.pprint( bluebolt.device(id) )

if __name__ == "__main__":
    main()
