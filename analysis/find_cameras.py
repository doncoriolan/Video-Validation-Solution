#!/usr/bin/python3

import argparse
import re
from network_checks import nmap_port_scan, extended_ports, camera_check
from file_management import locations
import pandas as pd

import logging
logging.basicConfig(filename=f"{locations['persistent_location']}/finder.log", level=logging.DEBUG)
logger = logging.getLogger('finder.log')

# check the logs for live cameras
def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('subnet', type=str)
    args = vars(parser.parse_args())
    
    #FIXME: subnet is probably not the only way this should be passed
    #FIXME: add try/except for the subnet
    ip_regex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})')
    subnet_validated = ip_regex.findall(args['subnet'])

    results = nmap_port_scan(subnet_validated.pop(), extended_ports)
    logger.info(results)
    camera_finder_results = {}
    for ip in results.keys():
        camera_finder_results[ip] = camera_check(ip)

    parsed_data = pd.DataFrame.from_dict(camera_finder_results, orient='index')
    logger.info(parsed_data)
    parsed_data.to_excel(locations['explorer_output_file'], index=False)


if __name__ == "__main__":
    main()
