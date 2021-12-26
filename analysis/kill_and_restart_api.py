#!/usr/bin/python3

import pandas
import os
import signal
import os.path
import json
import time
import subprocess
import logging 
import re

def process():
    # subprocess to find PIDs for the API
    api_ps = subprocess.Popen(['pgrep', '-lf', 'vvs_api'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = str(api_ps.communicate()[0])
    # Regex to get the PID
    process_regex = re.compile(r'(\d\d)')
    # send numbers found from Regex to Variable
    pids = process_regex.findall(output)
    for pid in pids:
        # subprocess to kill the PIDs
        subprocess.run(['/usr/bin/sudo', 'kill', '-9', pid])
        logger.info(f"Killing Process {pid}")

# Function to start the API
def start_api():
    subprocess.call(['/analysis/vvs_api.py'])


logging.basicConfig(filename="/opt/vvs/kill_and_restart.log", level=logging.DEBUG)
logger = logging.getLogger('kill_and_restart.log')
process()
logger.info('running VVS API')
start_api()
