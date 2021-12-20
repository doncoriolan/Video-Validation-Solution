#!/usr/bin/python3

import pandas
import os
import signal
import os.path
import json
import time
import subprocess
import logging 

def process():
    # Ask user for the name of process
    name = "vvs_api"
    # iterating through each instance of the process
    for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
        fields = line.split()     
        # extracting Process ID from the output
        pid = fields[0]
        logger.info(f"killing {pid}")
        os.kill(int(pid), signal.SIGKILL)

def start_api():
    api_process = subprocess.call(['/analysis/vvs_api.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    api_output = str(api_process.communicate()[1])
    logger.debug(api_output)


if __name__ == "__main__":
    logging.basicConfig(filename="/opt/vvs/kill_and_restart.log", level=logging.DEBUG)
    logger = logging.getLogger('kill_and_restart.log')
    process()
    logger.info('running VVS API')
    start_api()
