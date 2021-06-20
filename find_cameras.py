import subprocess
import os
import sys
import re
import datetime
import os.path
from os import listdir
import multiprocessing
import timeit
current_time = datetime.datetime.now()


start = timeit.default_timer()

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
def rtspurlLoop():
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
        f'rtsp://{usr}:{pwd}@{ip}:554/Streaming/Channels/1',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.log')
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
        with open(ffprobe_log, 'wb') as ffprobe_output:
            for url in urls:
                # ffmpeg process 
                videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ffprobe_output.write(videoprocess.communicate()[1])

def rtspurlLoop2():
    for ip in ips:
        urls = [f'rtsp://{ip}:554/live0.264',
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
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '2_.log')
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '2_.mp4')
        with open(ffprobe_log, 'wb') as ffprobe_output:
            for url in urls:
                # ffmpeg process 
                videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ffprobe_output.write(videoprocess.communicate()[1])

def rtspurlLoop3():
    for ip in ips:
        urls = [f'rtsp://{ip}:554/cam1/mpeg4?user={usr}&pwd={pwd}',
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
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '3_.log')
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '3_.mp4')
        with open(ffprobe_log, 'wb') as ffprobe_output:
            for url in urls:
                # ffmpeg process 
                videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ffprobe_output.write(videoprocess.communicate()[1])

def rtspurlLoop4():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}:554/12',
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
        f'rtsp://{ip}/mpeg4/media.amp',
        f'rtsp://{ip}/axis-media/media.amp',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '4_.log')
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '4_.mp4')
        with open(ffprobe_log, 'wb') as ffprobe_output:
            for url in urls:
                # ffmpeg process 
                videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ffprobe_output.write(videoprocess.communicate()[1])

def rtspurlLoop5():
    for ip in ips:
        urls =  [f'rtsp://{ip}/stream1',
        f'http://{ip}/streams/view/0',
        f'http://{ip}:cameraPort/cgi-bin/faststream.jpg?stream=full&fps=1.0',
        f'rtsp://{ip}/h264',
        f'rtsp://{ip}/swVideo',
        f'rtsp://{ip}/MediaInput/h264',
        f'rtsp://{ip}:554/Streaming/Channels/1',
        f'rtsp://{ip}/stream2',
        f'rtsp://{ip}media/video2',
        f'rtsp://{ip}/cam/realmonitor?channel=1&subtype=1',
        f'rtsp://{ip}:554/usecondstream',
        f'rtsp://{ip}:554/ch0',
        f'rtsp://{ip}:554/cam/realmonitor?channel=1&subtype=1',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '5_.log')
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '5_.mp4')
        with open(ffprobe_log, 'wb') as ffprobe_output:
            for url in urls:
                # ffmpeg process 
                videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ffprobe_output.write(videoprocess.communicate()[1])

def rtspurlLoop6():
    for ip in ips:
        urls = [f'rtsp://{ip}/media',
        f'rtsp://{ip}/video1',
        f'rtsp://{ip}/media/video1',
        f'rtsp://{ip}:554/stream2',
        f'rtsp://{ip}:554/h26x=4&inst=2',
        f'rtsp://{ip}/h264.sdp1?res=half&ssn=101&doublescan=0&fps=0',
        f'rtsp://{ip}h264.sdp2?res=half&ssn=102&doublescan=0&fps=0',
        f'rtsp://{ip}:554/CH001.sdp',
        f'rtsp://{ip}:554/encoder2',
        f'rtsp://{ip}:554/defaultPrimary0?streamtype=u',
        f'http://{ip}:80/mjpg/video.mjpg',
        f'http://{ip}:80/snap.jpg?JpegSize=M&JpegCam=1',
        f'http://{ip}:80/oneshotimage1',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '_6.log')
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '_6.mp4')
        with open(ffprobe_log, 'wb') as ffprobe_output:
            for url in urls:
                # ffmpeg process
                videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ffprobe_output.write(videoprocess.communicate()[1])

def rtspurlLoop7():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}:554/11',
        f'http://{ip}:80/img/video.mjpeg',
        f'http://{ip}:80/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER',
        f'http://{ip}:80/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity',
        f'http://{ip}:80/cgi-bin/camera?resolution=640&amp;quality=1',
        f'http://{ip}:80/jpg/image.jpg',
        f'rtsp://{usr}:{pwd}@{ip}/mpeg4/media.amp',
        f'rtsp://{usr}:{pwd}@{ip}/axis-media/media.amp',
        f'rtsp://{usr}:{pwd}@{ip}/stream1',
        f'http://{usr}:{pwd}@{ip}/streams/view/0',
        f'http://{usr}:{pwd}@{ip}:cameraPort/cgi-bin/faststream.jpg?stream=full&fps=1.0',
        f'rtsp://{usr}:{pwd}@{ip}/h264',
        f'rtsp://{usr}:{pwd}@{ip}/swVideo',
        f'rtsp://{usr}:{pwd}@{ip}/MediaInput/h264',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '_7.log')
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '_7.mp4')
        with open(ffprobe_log, 'wb') as ffprobe_output:
            for url in urls:
                # ffmpeg process
                videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ffprobe_output.write(videoprocess.communicate()[1])

def rtspurlLoop8():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}/stream2',
        f'rtsp://{usr}:{pwd}@{ip}media/video2',
        f'rtsp://{usr}:{pwd}@{ip}/cam/realmonitor?channel=1&subtype=1',
        f'rtsp://{usr}:{pwd}@{ip}:554/usecondstream',
        f'rtsp://{usr}:{pwd}@{ip}:554/ch0',
        f'rtsp://{usr}:{pwd}@{ip}:554/cam/realmonitor?channel=1&subtype=1',
        f'rtsp://{usr}:{pwd}@{ip}/media',
        f'rtsp://{usr}:{pwd}@{ip}/video1',
        f'rtsp://{usr}:{pwd}@{ip}/media/video1',
        f'rtsp://{usr}:{pwd}@{ip}:554/stream2',
        f'rtsp://{usr}:{pwd}@{ip}:554/h26x=4&inst=2',
        f'rtsp://{usr}:{pwd}@{ip}/h264.sdp1?res=half&ssn=101&doublescan=0&fps=0',
        f'rtsp://{usr}:{pwd}@{ip}h264.sdp2?res=half&ssn=102&doublescan=0&fps=0',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '8_.log')
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '8_.mp4')
        with open(ffprobe_log, 'wb') as ffprobe_output:
            for url in urls:
                # ffmpeg process 
                videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ffprobe_output.write(videoprocess.communicate()[1])

def rtspurlLoop9():
    for ip in ips:
        urls = [f'rtsp://{usr}:{pwd}@{ip}:554/CH001.sdp',
        f'rtsp://{usr}:{pwd}@{ip}:554/encoder2',
        f'rtsp://{usr}:{pwd}@{ip}:554/defaultPrimary0?streamtype=u',
        f'http://{usr}:{pwd}@{ip}:80/mjpg/video.mjpg',
        f'http://{usr}:{pwd}@{ip}:80/snap.jpg?JpegSize=M&JpegCam=1',
        f'http://{usr}:{pwd}@{ip}:80/oneshotimage1',
        f'http://{usr}:{pwd}@{ip}:80/img/video.mjpeg',
        f'http://{usr}:{pwd}@{ip}:80/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER',
        f'http://{usr}:{pwd}@{ip}:80/SnapshotJPEG?Resolution=640x480&amp;Quality=Clarity',
        f'http://{usr}:{pwd}@{ip}:80/cgi-bin/camera?resolution=640&amp;quality=1',
        f'http://{usr}:{pwd}@{ip}:80/jpg/image.jpg',
        ]
        print(urls)
        ffprobe_log = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '9_.log')
        videoname = ('/home/camerafinder/logs/' + ip + current_time.strftime("%Y%m%d_%H%M%S") + '9_.mp4')
        with open(ffprobe_log, 'wb') as ffprobe_output:
            for url in urls:
                # ffmpeg process 
                videoprocess = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ffprobe_output.write(videoprocess.communicate()[1])

# Run each function together to speed up the script
if __name__ == "__main__":

    p1 = multiprocessing.Process(target=rtspurlLoop)
    p2 = multiprocessing.Process(target=rtspurlLoop2)
    p3 = multiprocessing.Process(target=rtspurlLoop3)
    p4 = multiprocessing.Process(target=rtspurlLoop4)
    p5 = multiprocessing.Process(target=rtspurlLoop5)
    p6 = multiprocessing.Process(target=rtspurlLoop6)
    p7 = multiprocessing.Process(target=rtspurlLoop7)
    p8 = multiprocessing.Process(target=rtspurlLoop8)
    p9 = multiprocessing.Process(target=rtspurlLoop9)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p9.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    p9.join()

# check the logs for live cameras
def find_live_cams():
    with open(foundcams, "w") as s:
        for filename in listdir(camfindlogs):
            with open(camfindlogs + filename, 'r', encoding='latin1') as f:
                for line in f.readlines():
                    if 'Input #0' in line:
                        #s.write(line + '\n')
                        print(line)
                        results = urlRegex.findall(line)
                        print(results)
                    else:
                        continue
find_live_cams()

stop = timeit.default_timer()
execution_time = stop - start

print("Program Executed in "+str(execution_time)) # It returns time in seconds
