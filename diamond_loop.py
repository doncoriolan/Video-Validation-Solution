import csv
import subprocess
import datetime
import os
import os.path
from os import listdir, getenv
import pandas as pd

persistent_location = getenv('vvs_persistent_data')
input_file = getenv('vvs_input_csv')
#FIXME:utilise this for output
output_file = getenv('vvs_output_sheet')

# only one directory currently planned to be persistent
csv_location        = f"{persistent_location}/{input_file}"
ffmpeglogs          = f"{persistent_location}/ffmpeglog/"
black_results       = f"{persistent_location}/stream_results/result.txt"
videofiles          = f"{persistent_location}/videofiles/"
blacklog            = f"{persistent_location}/blacklog/"
rtsp_err_txt        = f"{persistent_location}/stream_results/rtsp_error.txt"
videofiles          = f"{persistent_location}/videofiles/"
staticlog           = f"{persistent_location}/staticlogs/"
static_result       = f"{persistent_location}/stream_results/static_results.txt"
frozenlog           = f"{persistent_location}/frozenlog/"
frozen_results      = f"{persistent_location}/stream_results/frozen.txt"
csv_files           = f"{persistent_location}/stream_results/"

# external binaries
convert_location    = f"/usr/bin/convert"
ffmpeg_location     = f"/usr/bin/ffmpeg"

#FIXME: make this configurable
static_check        = f"/static_check.sh"


# Open the streams list csv file
with open(csv_location) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)  # skip the headers
    for row in csv_reader:
        ffmpeg_log = (ffmpeglogs + row[0]) # set the ffmpeg log to be named the stream name
        # Open log file for writing
        with open(ffmpeg_log, 'wb') as ffmpeg_output: 
            # Iterate through streams list
            #for row in csv_reader:
            print(row)
            stream_output = (videofiles + row[0] + ".mpeg") # stream output variable
            # Subprocess record 1 stream at a time & send the output t0 stdout & stdeer
            ffmpeg_instance = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', row[1], stream_output], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # sent output to ffmpeg log
            ffmpeg_output.write(ffmpeg_instance.communicate()[1])

# grab the rtsp errors from the log files we made above
with open(rtsp_err_txt, "w") as f:
    f.write("Name," + "RTSP_ERROR" + '\n')
    for filename in listdir(ffmpeglogs):
        with open(ffmpeglogs + filename) as currentFile:
            text = currentFile.read()
            if ('401 Un' in text):
                f.write( filename + ',401' + '\n')
            if ('404 No' in text):
                f.write( filename + ',404' + '\n')
            else:
                f.write( filename + ',Good Stream' + '\n')


# for the files recorded above check if the video is black
for files in os.listdir(videofiles):
    black_log = (blacklog + files)
    with open(black_log, 'wb') as ffmpegblack_output:
        ffmpeg_blackdetect = subprocess.Popen([ffmpeg_location, '-i', videofiles+files, '-vf', 'blackdetect=d=2:pix_th=0.00', '-an', '-f', 'null', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ffmpegblack_output.write(ffmpeg_blackdetect.communicate()[1])

# looks at the log output from the blackdetect and generates a csv to tell you if its dark or not
with open(black_results, "w") as f:
    f.write("Name," + "IsBlack" + '\n')
    for filename in listdir(blacklog):
        with open(blacklog + filename) as currentFile:
            text = currentFile.read()
            if ('blackdetect' in text):
                f.write( filename + ',Yes' + '\n')
            else:
                f.write( filename + ',No' + '\n')


# for the files recorded check if the video is pure static using a bash scripts and generate log file for every video
subprocess.call(f"bash {static_check}", shell=True)


# check if log files in the static log directory and read each file and generates a txt file to tell you if its static or not
with open(static_result, "w") as s:
    s.write("Name," + "Is_Static" + '\n')
    for filename in listdir(staticlog):
        with open(staticlog + filename) as currentFile:
            text = currentFile.read()
            if ('sat=0' in text):
                s.write( filename + ',Yes' + '\n')
            else:
                s.write( filename + ',No' + '\n')

# check if files recorded were frozen and put the output in a log file
for files in os.listdir(videofiles):
    frozen_log = (frozenlog + files)
    with open(frozen_log, 'wb') as ffmpegfreeze_output:
        ffmpeg_freezedetect = subprocess.Popen([ffmpeg_location, '-i', videofiles+files, '-vf', 'freezedetect=d=7', '-f', 'null', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ffmpegfreeze_output.write(ffmpeg_freezedetect.communicate()[1])

# checks log file generated above for freezedetect in the log file. and creates a txt file with the results. 
with open(frozen_results, "w") as f:
    f.write("Name," + "IsFrozen" + '\n')
    for filename in listdir(frozenlog):
        with open(frozenlog + filename) as currentFile:
            text = currentFile.read()
            if ('freezedetect' in text):
                f.write( filename + ',Yes' + '\n')
            else:
                f.write( filename + ',No' + '\n')

writer = pd.ExcelWriter('diamond_sheet.xlsx')
for csvs in os.listdir(csv_files):
    df = pd.read_csv(csv_files+csvs)
    df.to_excel(writer, sheet_name=csvs)
writer.save()
