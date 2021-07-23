import subprocess
import os
import os.path
from os import listdir, getenv, remove, stat
from sys import stderr

videos = '/home/test/video_files/'
bin_location    = f"/usr/bin"
ffmpeg_location     = f"{bin_location}/ffmpeg"
laglist = {}
laglist2 = {}
laglist3 = {}

for video in listdir(videos):
    ffmpeg_lagdetect = subprocess.Popen([ffmpeg_location, '-filter:v', 'idet', '-frames:v', '360', '-an', '-f', 'rawvideo', '-y', 'null', '-i', videos+video, '-hide_banner'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    laglist["%s" %video] = str(ffmpeg_lagdetect.communicate()).split('\\n')[-2].split(' ') # send the output to a dictionary name to the key and output to value pairs

# Remove extra spaces 
for x in laglist.values():
    while '' in x:x.remove('')
    x[-1] = int(x[-1]) # set last value to a integer
    x[-3] = int(x[-3]) # set third to last value to a integer

print(laglist)


# add divide the numbers and send it to a dictionary 
for key, value in laglist.items():
    if value[-3] != 0:
        laglist2["%s" %key] = value[-1] / value[-3]
    else:
        laglist2["%s" %key] = 0

print(laglist2)

# If the number is greater than 8% the video is showing

for key, value in laglist2.items():
    if value >= .08:
        laglist3["%s" %key] = "Distorted"
    else:
        laglist3["%s" %key] = "Not Distorted"

print(laglist3)
