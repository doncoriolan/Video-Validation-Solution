#!/usr/bin/python3

import pandas
import os
import signal
import os.path
import json
import time
import subprocess

def process():
     
    # Ask user for the name of process
    name = "vvs_api"
    try:
         
        # iterating through each instance of the process
        for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
            fields = line.split()
             
            # extracting Process ID from the output
            pid = fields[0]
             
            # terminating process
            os.kill(int(pid), signal.SIGKILL)
    except:
        print('unable to kill process')



process()


subprocess.call(['/analysis/vvs_api.py'])
