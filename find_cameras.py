import subprocess
import os
import sys
import re
import datetime
import os.path
from os import listdir

current_time = datetime.datetime.now()

NMAPLOCATION = '/usr/bin/nmap'
ffprobe_location = '/usr/bin/ffprobe'
ffmpeg_location = '/usr/bin/ffmpeg'
NMAPLOG = '/home/camerafinder/nmaplog'
usr = 'myuser'
pwd = 'mypassword'
camfindlogs = '/home/camerafinder/logs/'
foundcams = '/home/camerafinder/results.txt'

# ASK user to enter IP address
print('Enter a Subnet. Example 172.28.12.0/24')
IPADDR = input()

# RUN NMAP to find IPs that are online
process = subprocess.run([NMAPLOCATION, '-sn', IPADDR], check=True, stdout=subprocess.PIPE, universal_newlines=True)
output = process.stdout

# IP Address regex
IPRegex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
ips = IPRegex.findall(output)
print(ips)

# Camera URL REGEX
urlRegex = re.compile((r'(\D{1,5}://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\S*)'))

# For loop to put the IPs, username and password in the list
for ip in ips:
    urls = [f'rtsp://{usr}:{pwd}@{ip}:554/cam/realmonitor?channel=1&subtype=0',
        f'rtsp://{ip}:554/live=2.2&username={usr}&password={pwd}',
        f'rtsp://{usr}:{pwd}@{ip}:554/1',
        f'rtsp://{usr}:{pwd}@{ip}:554/stream1',
        f'rtsp://{usr}:{pwd}@{ip}:554/Stream1',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=1&stream=0.sdp?',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=1&stream=0.sdp',
        f'rtsp://{ip}:554/videostream.asf?user={usr}&pwd={pwd}',
        f'rtsp://{ip}:554/ucast/11',
        f'rtsp://{ip}:554/11',
        f'rtsp://{ip}:554/12',
        f'rtsp://{ip}:554/live0.264',
        f'rtsp://{ip}:554/mpeg4cif',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=1&stream=0.sdp?',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=1&stream=0.sdp',
        f'rtsp://{ip}:554/live1.264',
        f'rtsp://{ip}:554/cam1/h264',
        f'rtsp://{ip}:554/mpeg4cif',
        f'rtsp://{ip}:554/ucast/11',
        f'rtsp://{ip}:554/ROH/channel/11',
        f'rtsp://{ip}:554/user={usr}_password={pwd}_channel=1_stream=0.sdp',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=1&stream=0.sdp?',
        f'rtsp://{ip}:554/user={usr}_password={pwd}_channel=1_stream=0.sdp',
        f'rtsp://{ip}:554/user={usr}_password={pwd}_channel=1_stream=0.sdp?',
        f'rtsp://{ip}:554/cam1/mpeg4?user={usr}&pwd={pwd}',
        f'rtsp://{ip}:554/h264_stream',
        f'rtsp://{ip}:554/live/ch0',
        f'rtsp://{ip}:554/live/ch1',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=1&stream=0.sdp?',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=1&stream=1.sdp?',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=0&stream=1.sdp?',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=0&stream=0.sdp?',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=1&stream=0.sdp',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=1&stream=1.sdp',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=0&stream=1.sdp',
        f'rtsp://{ip}:554/user={usr}&password={pwd}&channel=0&stream=0.sdp',
        f'rtsp://{usr}:{pwd}@{ip}:554/ucast/11',
        f'rtsp://{usr}:{pwd}@{ip}:554/11',
        f'rtsp://{usr}:{pwd}@{ip}:554/12',
        f'rtsp://{usr}:{pwd}@{ip}:554/live0.264',
        f'rtsp://{usr}:{pwd}@{ip}:554/mpeg4cif',
        f'rtsp://{usr}:{pwd}@{ip}:554/live1.264',
        f'rtsp://{usr}:{pwd}@{ip}:554/cam1/h264',
        f'rtsp://{usr}:{pwd}@{ip}:554/mpeg4cif',
        f'rtsp://{usr}:{pwd}@{ip}:554/ucast/11',
        f'rtsp://{usr}:{pwd}@{ip}:554/ROH/channel/11',
        f'rtsp://{usr}:{pwd}@{ip}:554/h264_stream',
        f'rtsp://{usr}:{pwd}@{ip}:554/live/ch0',
        f'rtsp://{usr}:{pwd}@{ip}:554/live/ch1',
        ]
    print(urls)
    ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.log')
    videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
    with open(ffprobe_log, 'wb') as ffprobe_output:
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffprobe_output.write(videoprocess.communicate()[1])

# Function to read output from above and print the working camera URL.
def find_live_cams():
    with open(foundcams, "w") as s:
        for filename in listdir(camfindlogs):
            with open(camfindlogs + filename, 'r', encoding='latin1') as f:
                for line in f.readlines():
                    if 'Input #0' in line:
                        print(line)
                        results = urlRegex.findall(line)
                        print(results)
                    else:
                        continue
find_live_cams()
