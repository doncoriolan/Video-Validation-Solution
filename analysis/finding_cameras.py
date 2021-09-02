#!/usr/bin/python3

import subprocess
import os
import sys
import re
import datetime
import os.path
from os import listdir
import multiprocessing
from multiprocessing import Process
import timeit
import pandas as pd
from file_management import locations
import url_strings
import network_checks
import argparse
current_time = datetime.datetime.now()

#start = timeit.default_timer()

NMAPLOCATION = '/usr/bin/nmap'
ffprobe_location = '/usr/bin/ffprobe'
ffmpeg_location = '/usr/bin/ffmpeg'

def camera_loop(manufacturer, ips, username, password):
    actual_cams = {}
    if username and password:
        urls = url_strings.urls_auth[manufacturer]
    else:
        urls = url_strings.urls[manufacturer]
    for ip in ips:
        print(ips)
        print(ip)
        ffprobe_log = (f"{locations['persistent_location']}/camerafinder/logs/" + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = (f"{locations['persistent_location']}/camerafinder/logs/" + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            if username and password:
                url = url.format(ip=ip, usr=username, pwd=password)
            else:
                url = url.format(ip=ip)
            #print(url)
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            #print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                print(waiting)
                time.sleep(0.5)
            rc = videoprocess.returncode
            #print(rc)
            if rc == 0:
                # assuming that once a working URL was found, we know it's a camera and don't need to know more
                #XXX: let me know if the above shouldn't be the case, can easily be changed back
                actual_cams[ip] = url
                break
            #else:
            #    print("Not a camera")
        if ip not in actual_cams:
            actual_cams[ip] = None
    return actual_cams


#print(actual_cams)


#stop = timeit.default_timer()
#execution_time = stop - start

#print("Program Executed in "+str(execution_time)) # It returns time in seconds

def main():
    parser = argparse.ArgumentParser(description="Find cameras based on subnet and optionally supplied username/password.")
    parser.add_argument('manufacturer', type=str, help=f"The manufacturer of the camera, out of the following list: {list(url_strings.urls.keys())}")
    parser.add_argument('subnet', type=str, help="A subnet in CIDR notation e.g. 127.0.0.1/8")
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)

    args = parser.parse_args()
    #print(args)

    # RUN NMAP to find IPs that are online
    subnetRegex = re.compile(r'^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))$')
    if not re.search(subnetRegex, args.subnet):
        raise Exception("Incorrect subnet")
    reachable, unreachable = network_checks.nmap_ping_scan(args.subnet)
    print(reachable)
    print(unreachable)

    # Camera URL REGEX
    #urlRegex = re.compile((r'(\D{1,5}://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\S*)'))

    actual_cams = camera_loop(args.manufacturer, reachable, args.username, args.password)

    df = pd.DataFrame.from_dict(actual_cams, orient="index", columns=['result'])
    df.to_excel(f'{locations["persistent_location"]}/search.xlsx', index=True, index_label="address")
    print(f"df: {df}")

if __name__ == "__main__":
    main()
