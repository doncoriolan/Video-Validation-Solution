import subprocess
import os
import sys
import re
import datetime

current_time = datetime.datetime.now()

NMAPLOCATION = '/usr/bin/nmap'
ffprobe_location = '/usr/bin/ffprobe'
ffmpeg_location = '/usr/bin/ffmpeg'
NMAPLOG = '/home/camerafinder/nmaplog'

# Username and Password. We may have to pass this option is the UI. 
usr = 'myuser'
pwd = 'mypassword'

# This is where the client enters a subnet
print('Enter a Subnet. Example 172.28.12.0/24')
IPADDR = input()

# Run NMAP and send output to variable
process = subprocess.run([NMAPLOCATION, '-sn', IPADDR], check=True, stdout=subprocess.PIPE, universal_newlines=True)
output = process.stdout

# IP REGEX. Grabs the IPs from the output
IPRegex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
ips = IPRegex.findall(output)
print(ips)

# Assigns each IP and password then assigns it to the URL. Then Runs FFMPEG against the URLS.
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
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffprobe_output.write(videoprocess.communicate()[1])
