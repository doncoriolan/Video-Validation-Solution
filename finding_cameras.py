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
current_time = datetime.datetime.now()


start = timeit.default_timer()

NMAPLOCATION = '/usr/bin/nmap'
ffprobe_location = '/usr/bin/ffprobe'
ffmpeg_location = '/usr/bin/ffmpeg'
NMAPLOG = '/home/camerafinder/nmaplog'
camfindlogs = '/home/camerafinder/logs/'
foundcams = '/home/camerafinder/results.txt'
actual_cams = []

#Ask user for the type of camera
while True:
    print('Please select the type of camera. Please enter the number assigned to the camera')
    print('1.Axis, 2.Sony 3.Bosch 4.Hikvision 5.Avigilon 6.Panasonic 7.Mobotix 8.Cohu 9.WTI 10.IQEYE 11.Pelco 12.Flir 13.Univision 14.Vicon 15.Geovision')
    CAMSELECT = input()
    try:
        CAMSELECT = int(CAMSELECT)
    except:
        print('Please Only select numbers 1-15')
        continue
    if CAMSELECT < 1:
        print('Please enter a positive number')
        print('1.Axis, 2.Sony 3.Bosch 4.Hikvision 5.Avigilon 6.Panasonic 7.Mobotix 8.Cohu 9.WTI 10.IQEYE 11.Pelco 12.Flir 13.Univision 14.Vicon 15.Geovision')
    if CAMSELECT > 15:
        print('Please enter a number from 1-15')
        print('1.Axis, 2.Sony 3.Bosch 4.Hikvision 5.Avigilon 6.Panasonic 7.Mobotix 8.Cohu 9.WTI 10.IQEYE 11.Pelco 12.Flir 13.Univision 14.Vicon 15.Geovision')
        continue
    break

while True:
    print('Does the camera have creds. Please select 1 or 2')
    print('1. Camera has no Creds')
    print('2. Camera has Creds')
    YESORNO = input()
    try:
        YESORNO = int(YESORNO)
    except:
        print('Please only enter the number 1 or 2')
        continue
    if YESORNO < 1:
        print('Please enter a positive number')
    if YESORNO > 2:
        print('Please enter 1 or 2')
        continue
    break
        
if YESORNO == 2:
    print('What is the username')
    usr = input()
    print('What is the password')
    pwd = input()
    


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
def axisLoop():
    for ip in ips:
        urls = [f'http://{ip}/mjpg/video.mjpg',
        f'rtsp://{ip}/mpeg4/media.amp ',
        f'rtsp://{ip}/axis-media/media.amp?',
        f'rtsp://{ip}/onvif-media/media.amp',
        f'http://{ip}/axis-cgi/mjpg/video.cgi',
        f'rtsp://{ip}/ucast/12',
        f'http://{ip}/mjpg/1/video.mjpg?Axis-Orig-Sw=true',
        f'http://{ip}/stream.asf',
        f'http://{ip}/mjpg/1/video.mjpg',
        f'rtsp://{ip}/mpeg4',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def sonyLoop():
    for ip in ips:
        urls = [f'rtsp://{ip}/media/video1',
        f'http://{ip}/h264',
        f'rtsp://{ip}/av0_0',
        f'rtsp://{ip}/live1.264',
        f'rtsp://{ip}/mjpeg',
        f'rtsp://{ip}/video1',
        f'rtsp://{ip}/11',
        f'rtsp://{ip}/videoinput_1:0/h264_1/onvif.stm',
        f'http://{ip}/oneshotimage1?COUNTER',
        f'rtsp://{ip}/profile',
        f'rtsp://{ip}/stream.asf',
        f'rtsp://{ip}/live/mpeg4',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def boschLoop():
    for ip in ips:
        urls = [f'rtsp://{ip}/h26x=4&inst=2',
        f'rtsp://{ip}/h26x=4&inst=1',
        f'rtsp://{ip}/rtsp_tunnel',
        f'rtsp://{ip}/video.h264',
        f'rtsp://{ip}/11',
        f'rtsp://{ip}/h264',
        f'rtsp://{ip}/1/stream1/Profile1',
        f'rtsp://{ip}/ch1-s1',
        f'rtsp://{ip}/line=2',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def hikvisionLoop():
    for ip in ips:
        urls = [f'rtsp://{ip}/MediaInput/h264',
        f'rtsp://{ip}/Streaming/Channels/1',
        f'rtsp://{ip}/Streaming/Channels/101',
        f'rtsp://{ip}/video.h264',
        f'rtsp://{ip}/HighResolutionVideo',
        f'rtsp://{ip}/mpeg4',
        f'rtsp://{ip}/H264',
        f'rtsp://{ip}/Streaming/Channels/102',
        f'rtsp://{ip}/Streaming/Channels/201',
        f'rtsp://{ip}/Streaming/Channels/301',
        f'rtsp://{ip}/Streaming/Channels/401',
        f'rtsp://{ip}/Streaming/Channels/501',
        f'rtsp://{ip}/h264/ch01/main/av_stream',
        f'rtsp://{ip}/cam1/mpeg4',
        f'rtsp://{ip}/mpeg4/media.amp?',
        f'rtsp://{ip}/ch0_0.h264',
        f'rtsp://{ip}/cam1/onvif-h264',
        f'rtsp://{ip}/11',
        f'rtsp://{ip}/live',
        f'rtsp://{ip}//Streaming/Channels/2',
        f'rtsp://{ip}/h264',
        f'rtsp://{ip}/rtsph2641080p',
        f'rtsp://{ip}/live.sdp',
        f'rtsp://{ip}/videoMain',
        f'rtsp://{ip}/Streaming/Channels/103',
        f'rtsp://{ip}/PSIA/Streaming/channels/0',
        f'rtsp://{ip}/LowResolutionVideo',
        f'rtsp://{ip}/cam1/onvif-h264-1',
        f'rtsp://{ip}/ch0_0.h264',
        f'rtsp://{ip}/1',
        f'rtsp://{ip}/image.mpg',
        f'rtsp://{ip}/live.sdp',
        f'rtsp://{ip}/h264_stream',
        f'rtsp://{ip}/live/ch0',
        f'rtsp://{ip}/live/ch00_0',
        f'rtsp://{ip}/cam0/h264',
        f'rtsp://{ip}/live/h264',
        f'rtsp://{ip}/live/av0',
        f'rtsp://{ip}/',
        f'rtsp://{ip}/av0_1',
        f'rtsp://{ip}/Video',
        f'rtsp://{ip}/mpeg4',
        f'rtsp://{ip}/onvif/live/2',
        f'rtsp://{ip}/cam/realmonitor',
        f'rtsp://{ip}/ucast/11',
        f'rtsp://{ip}/main',
        f'rtsp://{ip}/0',
        f'rtsp://{ip}/Streaming/Unicast/channels/101',
        f'rtsp://{ip}/ISAPI/streaming/channels/102',
        f'rtsp://{ip}/ISAPI/streaming/channels/101',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def avigilonLoop():
    for ip in ips:
        urls =  [f'rtsp://{ip}/deaultPrimary0streamtype=u',
        f'http://{ip}/media/still.jpg',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def panasonicLoop():
    for ip in ips:
        urls = [f'http://{ip}/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity',
        f'rtsp://{ip}/ONVIF/MediaInput',
        f'http://{ip}/videostream.asf?user={usr}&pwd={pwd}',
        f'rtsp://{ip}/cam/realmonitor',
        f'rtsp://{ip}/live.sdp',
        f'http://{ip}/videostream.asf',
        f'rtsp://{ip}/MediaInput/h264',
        f'rtsp://{ip}/MediaInput/mpeg4',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def mobotixLoop():
    for ip in ips:
        urls = [f'http://{ip}/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER',
        f'rtsp://{ip}/control/faststream.jpg?stream=MxPEG&needlength&fps=6',
        f'rtsp://{ip}/control/faststream.jpg?stream=full',
        f'rtsp://{ip}/onvif/stream3/mobotix.mjpeg',
        f'rtsp://{ip}/onvif/mobotix.h264',
        f'rtsp://{ip}/streams/view/0',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def cohuLoop():
    for ip in ips:
        urls = [f'rtsp://{ip}/ucast/11',
        f'rtsp://{ip}/11',
        f'rtsp://{ip}/stream1',
        f'rtsp://{ip}/1',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def wtiLooop():
    for ip in ips:
        urls = [f'rtsp://{ip}/swVideo',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def iqeyeLoop():
    for ip in ips:
        urls = [f'rtsp://{ip}/rtsp/onvif',
        f'rtsp://{ip}/rtsp/stream1',
        f'rtsp://{ip}/stream1',
        f'rtsp://{ip}/rtsp/now.mp4',
        f'rtsp://{ip}/rtsp/now.jpg',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def pelcoLoop():
    for ip in ips:
        urls = [f'rtsp://{ip}/stream1',
        f'rtsp://{ip}/1/stream1',
        f'http://{ip}/jpeg',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def flirLoop():
    for ip in ips:
        urls = [f'rtsp://{ip}/axis-cgi/mjpg/video.cgi',
        f'rtsp://{ip}/cam/realmonitor',
        f'rtsp://{ip}/ch0',
        f'rtsp://{ip}/vis',
        f'rtsp://{ip}/wfov',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def univisionLoop():
    for ip in ips:
        urls = [f'rtsp://{ip}/media/video1',
        f'rtsp://{ip}/live3.sdp',
        f'rtsp://{ip}/Streaming/Channels/1',
        f'rtsp://{ip}/Streaming/Channels/2',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def viconLoop():
    for ip in ips:
        urls = [f'rtsp://{ip}/h264',
        ]
        print(urls)
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def geovisionLoop():
    for ip in ips:
        urls = [f'rtsp://{ip}/CH001.sdp',
        f'rtsp://{ip}/CH002.sdp',
        f'rtsp://{ip}/Streaming/Channels/1',
        f'rtsp://{ip}/media/video1',
        f'rtsp://{ip}/0/{usr}:{pwd}/main',
        f'rtsp://{ip}/h264_stream',
        f'rtsp://{ip}/videostream.asf?',
        f'http://{ip}/cgi-bin/jpg/image.cgi',
        f'http://{ip}/img/snapshot.cgi?size=2',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")



def axispassLoop():
    for ip in ips:
        urls = [f'http://{usr}:{pwd}@{ip}/mjpg/video.mjpg',
        f'rtsp://{usr}:{pwd}@{ip}/mpeg4/media.amp',
        f'rtsp://{usr}:{pwd}@{ip}/axis-media/media.amp?',
        f'rtsp://{usr}:{pwd}@{ip}/onvif-media/media.amp',
        f'http://{usr}:{pwd}@{ip}/axis-cgi/mjpg/video.cgi',
        f'rtsp://{usr}:{pwd}@{ip}/ucast/12',
        f'http://{ip}/videostream.asf?user={usr}&pwd={pwd}&resolution=64&rate=0',
        f'http://{ip}/videostream.asf?user={usr}&pwd={pwd}',
        f'http://{ip}/videostream.asf?usr={usr}&pwd={pwd}',
        f'http://{usr}:{pwd}@{ip}/mjpg/1/video.mjpg?Axis-Orig-Sw=true',
        f'http://{usr}:{pwd}@{ip}/stream.asf',
        f'http://{usr}:{pwd}@{ip}/mjpg/1/video.mjpg',
        f'rtsp://{usr}:{pwd}@{ip}/mpeg4',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def sonypassLoop():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}/media/video1',
        f'http://{usr}:{pwd}@{ip}/h264',
        f'rtsp://{usr}:{pwd}@{ip}/av0_0',
        f'rtsp://{usr}:{pwd}@{ip}/live1.264',
        f'rtsp://{usr}:{pwd}@{ip}/mjpeg',
        f'rtsp://{usr}:{pwd}@{ip}/video1',
        f'rtsp://{usr}:{pwd}@{ip}/11',
        f'rtsp://{ip}/user={usr}_password={pwd}_channel=1_stream=0.sdp',
        f'http://{ip}/videostream.asf?usr={usr}&pwd={pwd}',
        f'rtsp://{usr}:{pwd}@{ip}/videoinput_1:0/h264_1/onvif.stm',
        f'http://{usr}:{pwd}@{ip}/oneshotimage1?COUNTER',
        f'rtsp://{usr}:{pwd}@{ip}/profile',
        f'rtsp://{usr}:{pwd}@{ip}/stream.asf',
        f'rtsp://{usr}:{pwd}@{ip}/live/mpeg4',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def boschpassLoop():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}/h26x=4&inst=2',
        f'rtsp://{usr}:{pwd}@{ip}/h26x=4&inst=1',
        f'rtsp://{usr}:{pwd}@{ip}/rtsp_tunnel',
        f'rtsp://{usr}:{pwd}@{ip}/video.h264',
        f'rtsp://{usr}:{pwd}@{ip}/11',
        f'rtsp://{usr}:{pwd}@{ip}/h264',
        f'rtsp://{usr}:{pwd}@{ip}/1/stream1/Profile1',
        f'rtsp://{usr}:{pwd}@{ip}/ch1-s1',
        f'rtsp://{usr}:{pwd}@{ip}/line=2',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def hikvisionpassLoop():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}/MediaInput/h264',
        f'rtsp://{usr}:{pwd}@{ip}/Streaming/Channels/1',
        f'rtsp://{usr}:{pwd}@{ip}/Streaming/Channels/101',
        f'rtsp://{usr}:{pwd}@{ip}/video.h264',
        f'rtsp://{usr}:{pwd}@{ip}/HighResolutionVideo',
        f'rtsp://{usr}:{pwd}@{ip}/mpeg4',
        f'rtsp://{usr}:{pwd}@{ip}/H264',
        f'rtsp://{usr}:{pwd}@{ip}/Streaming/Channels/102',
        f'rtsp://{usr}:{pwd}@{ip}/Streaming/Channels/201',
        f'rtsp://{usr}:{pwd}@{ip}/Streaming/Channels/301',
        f'rtsp://{usr}:{pwd}@{ip}/Streaming/Channels/401',
        f'rtsp://{usr}:{pwd}@{ip}/Streaming/Channels/501',
        f'rtsp://{usr}:{pwd}@{ip}/h264/ch01/main/av_stream',
        f'rtsp://{usr}:{pwd}@{ip}/cam1/mpeg4',
        f'rtsp://{usr}:{pwd}@{ip}/mpeg4/media.amp?',
        f'rtsp://{usr}:{pwd}@{ip}/ch0_0.h264',
        f'rtsp://{usr}:{pwd}@{ip}/cam1/onvif-h264',
        f'rtsp://{usr}:{pwd}@{ip}/11',
        f'rtsp://{usr}:{pwd}@{ip}/live',
        f'rtsp://{usr}:{pwd}@{ip}//Streaming/Channels/2',
        f'rtsp://{usr}:{pwd}@{ip}/h264',
        f'rtsp://{usr}:{pwd}@{ip}/rtsph2641080p',
        f'rtsp://{usr}:{pwd}@{ip}/live.sdp',
        f'rtsp://{usr}:{pwd}@{ip}/videoMain',
        f'rtsp://{usr}:{pwd}@{ip}/Streaming/Channels/103',
        f'rtsp://{usr}:{pwd}@{ip}/PSIA/Streaming/channels/0',
        f'rtsp://{usr}:{pwd}@{ip}/LowResolutionVideo',
        f'rtsp://{usr}:{pwd}@{ip}/cam1/onvif-h264-1',
        f'rtsp://{usr}:{pwd}@{ip}/ch0_0.h264',
        f'rtsp://{usr}:{pwd}@{ip}/1',
        f'rtsp://{usr}:{pwd}@{ip}/image.mpg',
        f'rtsp://{usr}:{pwd}@{ip}/live.sdp',
        f'rtsp://{usr}:{pwd}@{ip}/h264_stream',
        f'rtsp://{usr}:{pwd}@{ip}/live/ch0',
        f'rtsp://{usr}:{pwd}@{ip}/live/ch00_0',
        f'rtsp://{usr}:{pwd}@{ip}/cam0/h264',
        f'rtsp://{usr}:{pwd}@{ip}/live/h264',
        f'rtsp://{usr}:{pwd}@{ip}/live/av0',
        f'rtsp://{ip}/user={usr}_password={pwd}_channel=1_stream=1.sdp',
        f'rtsp://{usr}:{pwd}@{ip}/',
        f'rtsp://{ip}/videostream.asf?user={usr}&pwd={pwd}&resolution=64&rate=0',
        f'rtsp://{usr}:{pwd}@{ip}/av0_1',
        f'rtsp://{usr}:{pwd}@{ip}/Video',
        f'rtsp://{usr}:{pwd}@{ip}/mpeg4',
        f'rtsp://{usr}:{pwd}@{ip}/onvif/live/2',
        f'rtsp://{usr}:{pwd}@{ip}/cam/realmonitor',
        f'rtsp://{usr}:{pwd}@{ip}/ucast/11',
        f'rtsp://{usr}:{pwd}@{ip}/main',
        f'rtsp://{usr}:{pwd}@{ip}/0',
        f'rtsp://{ip}/user={usr}_password={pwd}_channel=1_stream=0.sdp',
        f'rtsp://{ip}/user={usr}&password={pwd}&channel=1&stream=0.sdp',
        f'rtsp://{usr}:{pwd}@{ip}/Streaming/Unicast/channels/101',
        f'rtsp://{usr}:{pwd}@{ip}/ISAPI/streaming/channels/102',
        f'rtsp://{usr}:{pwd}@{ip}/ISAPI/streaming/channels/101',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def avigilonpassLoop():
    for ip in ips:
        urls =  [f'rtsp://{usr}:{pwd}@{ip}/deaultPrimary0streamtype=u',
        f'http://{usr}:{pwd}@{ip}/media/still.jpg',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def panasonicpassLoop():
    for ip in ips:
        urls = [f'http://{usr}:{pwd}@{ip}/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity',
        f'rtsp://{usr}:{pwd}@{ip}/ONVIF/MediaInput',
        f'http://{ip}/videostream.asf?user={usr}&pwd={pwd}',
        f'rtsp://{usr}:{pwd}@{ip}/cam/realmonitor',
        f'rtsp://{usr}:{pwd}@{ip}/live.sdp',
        f'http://{ip}/videostream.asf',
        f'rtsp://{usr}:{pwd}@{ip}/MediaInput/h264',
        f'rtsp://{usr}:{pwd}@{ip}/MediaInput/mpeg4',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def mobotixpassLoop():
    for ip in ips:
        urls = [f'http://{usr}:{pwd}@{ip}/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER',
        f'rtsp://{usr}:{pwd}@{ip}/control/faststream.jpg?stream=MxPEG&needlength&fps=6',
        f'rtsp://{usr}:{pwd}@{ip}/control/faststream.jpg?stream=full',
        f'rtsp://{usr}:{pwd}@{ip}/onvif/stream3/mobotix.mjpeg',
        f'rtsp://{usr}:{pwd}@{ip}/onvif/mobotix.h264',
        f'rtsp://{usr}:{pwd}@{ip}/streams/view/0',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")

def cohupassLoop():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}/ucast/11',
        f'rtsp://{usr}:{pwd}@{ip}/11',
        f'rtsp://{usr}:{pwd}@{ip}/stream1',
        f'rtsp://{usr}:{pwd}@{ip}/1',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def wtipassLooop():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}/swVideo',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def iqeyepassLoop():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}/rtsp/onvif',
        f'rtsp://{usr}:{pwd}@{ip}/rtsp/stream1',
        f'rtsp://{usr}:{pwd}@{ip}/stream1',
        f'rtsp://{usr}:{pwd}@{ip}/rtsp/now.mp4',
        f'rtsp://{usr}:{pwd}@{ip}/rtsp/now.jpg',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def pelcopassLoop():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}/stream1',
        f'rtsp://{usr}:{pwd}@{ip}/1/stream1',
        f'http://{usr}:{pwd}@{ip}/jpeg',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def flirpassLoop():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}/axis-cgi/mjpg/video.cgi',
        f'rtsp://{usr}:{pwd}@{ip}/cam/realmonitor',
        f'rtsp://{usr}:{pwd}@{ip}/ch0',
        f'rtsp://{usr}:{pwd}@{ip}/vis',
        f'rtsp://{usr}:{pwd}@{ip}/wfov',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def univisionpassLoop():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}/media/video1',
        f'rtsp://{usr}:{pwd}@{ip}/live3.sdp',
        f'rtsp://{usr}:{pwd}@{ip}/Streaming/Channels/1',
        f'rtsp://{usr}:{pwd}@{ip}/Streaming/Channels/2',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def viconpassLoop():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}/h264',
        ]
        print(urls)
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


def geovisionpassLoop():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}/CH001.sdp',
        f'rtsp://{usr}:{pwd}@{ip}/CH002.sdp',
        f'rtsp://{usr}:{pwd}@{ip}/Streaming/Channels/1',
        f'rtsp://{usr}:{pwd}@{ip}/media/video1',
        f'rtsp://{ip}/0/{usr}:{pwd}/main',
        f'rtsp://{usr}:{pwd}@{ip}/h264_stream',
        f'rtsp://{usr}:{pwd}@{ip}/videostream.asf?',
        f'htpp://{usr}:{pwd}@{ip}/cgi-bin/jpg/image.cgi',
        f'http://{usr}:{pwd}@{ip}/img/snapshot.cgi?size=2',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S"))
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        for url in urls:
            # ffmpeg process 
            videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_output = videoprocess.communicate()
            print("the commandline is {}".format(videoprocess.args))
            while videoprocess.poll() is None:
                time.sleep(0.5)
            rc = videoprocess.returncode
            print(rc)
            if rc == 0:
                actual_cams.append({'Working URLS': url})
            else:
                print("Not a camera")


if CAMSELECT == 1 and YESORNO == 1:
    axisLoop()
if CAMSELECT == 2 and YESORNO == 1:
    sonyLoop()
if CAMSELECT == 3 and YESORNO == 1:
    boschLoop()
if CAMSELECT == 4 and YESORNO == 1:
    hikvisionLoop()
if CAMSELECT == 5 and YESORNO == 1:
    avigilonLoop()
if CAMSELECT == 6 and YESORNO == 1:
    panasonicLoop()
if CAMSELECT == 7 and YESORNO == 1:
    mobotixLoop()
if CAMSELECT == 8 and YESORNO == 1:
    cohuLoop()
if CAMSELECT == 9 and YESORNO == 1:
    wtiLooop()
if CAMSELECT == 10 and YESORNO == 1:
    iqeyeLoop()
if CAMSELECT == 11 and YESORNO == 1:
    pelcoLoop()
if CAMSELECT == 12 and YESORNO == 1:
    flirLoop()
if CAMSELECT == 13 and YESORNO == 1:
    univisionLoop()
if CAMSELECT == 14 and YESORNO == 1:
    viconLoop()
if CAMSELECT == 15 and YESORNO == 1:
    geovisionLoop()

if CAMSELECT == 1 and YESORNO == 2:
    axispassLoop()
if CAMSELECT == 2 and YESORNO == 2:
    sonypassLoop()
if CAMSELECT == 3 and YESORNO == 2:
    boschpassLoop()
if CAMSELECT == 4 and YESORNO == 2:
    hikvisionpassLoop()
if CAMSELECT == 5 and YESORNO == 2:
    avigilonpassLoop()
if CAMSELECT == 6 and YESORNO == 2:
    panasonicpassLoop()
if CAMSELECT == 7 and YESORNO == 2:
    mobotixpassLoop()
if CAMSELECT == 8 and YESORNO == 2:
    cohupassLoop()
if CAMSELECT == 9 and YESORNO == 2:
    wtipassLooop()
if CAMSELECT == 10 and YESORNO == 2:
    iqeyepassLoop()
if CAMSELECT == 11 and YESORNO == 2:
    pelcopassLoop()
if CAMSELECT == 12 and YESORNO == 2:
    flirpassLoop()
if CAMSELECT == 13 and YESORNO == 2:
    univisionpassLoop()
if CAMSELECT == 14 and YESORNO == 2:
    viconpassLoop()
if CAMSELECT == 15 and YESORNO == 2:
    geovisionpassLoop()


print(actual_cams)


stop = timeit.default_timer()
execution_time = stop - start

print("Program Executed in "+str(execution_time)) # It returns time in seconds

df = pd.DataFrame(actual_cams)
df.to_excel('finalcams.xlsx', index=False)
print(df)
