import csv
import subprocess
import datetime
import os
import os.path
from os import listdir, getenv, remove, stat
from time import sleep
from sys import stderr
import pandas as pd
import logging
from file_management import strip_extension, remove_leading_lines, remove_empty_lines

persistent_location = getenv('vvs_persistent_data')
input_file = getenv('vvs_input_csv')
#FIXME:utilise this for output
output_file = getenv('vvs_output_sheet')

# only one directory currently planned to be persistent
csv_location        = f"{persistent_location}/{input_file}"
csv_files           = f"{persistent_location}/stream_results/"
videofiles          = f"{persistent_location}/videofiles/"
ffmpeglogs          = f"{persistent_location}/ffmpeglog/"
blacklog            = f"{persistent_location}/blacklog/"
staticlogs          = f"{persistent_location}/staticlogs/"
frozenlog           = f"{persistent_location}/frozenlog/"
rtsp_results        = f"{persistent_location}/stream_results/rtsp_results"
black_results       = f"{persistent_location}/stream_results/no_output_result"
frozen_results      = f"{persistent_location}/stream_results/frozen_results"
static_results      = f"{persistent_location}/stream_results/static_results"

dirs_to_clean       = [csv_files, videofiles, ffmpeglogs, blacklog, staticlogs, frozenlog]

# external binaries
bin_location        = f"/usr/bin"
convert_location    = f"{bin_location}/convert"
ffmpeg_location     = f"{bin_location}/ffmpeg"
sed_location        = f"{bin_location}/sed"
find_location       = f"{bin_location}/find"
grep_location       = f"{bin_location}/grep"

#FIXME: make this configurable
static_check        = f"/static_check.sh"

def cleanup(directories):
    for directory in directories:
        for found_file in listdir(directory):
            try:
                remove(directory + found_file)
            except FileNotFoundError as e:
                logger.warning(f"Couldn't delete file {directory}{found_file} due to below exception:")
                logger.warning(e)


# Open the streams list csv file
def check_streams():
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
def get_rtsp_errors():
    with open(rtsp_results, "w") as f:
        f.write("Name," + "RTSP_ERROR" + '\n')
        for filename in listdir(ffmpeglogs):
            with open(ffmpeglogs + filename) as currentFile:
                text = currentFile.read()
                if ('401 Un' in text):
                    f.write( strip_extension(filename) + ',401' + '\n')
                elif ('404 No' in text):
                    f.write( strip_extension(filename) + ',404' + '\n')
                elif ('does not contain any stream' in text):
                    f.write( strip_extension(filename) + ',No stream' + '\n')
                else:
                    f.write( strip_extension(filename) + ',Good Stream' + '\n')


# for the files recorded above check if the video is black
def check_no_output():
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
                    f.write( strip_extension(filename) + ',Yes' + '\n')
                else:
                    f.write( strip_extension(filename) + ',No' + '\n')


# for the files recorded check if the video is pure static using a bash scripts and generate log file for every video
def check_static_output():
    #subprocess.call(f"bash {static_check}", shell=True)
    for video in listdir(videofiles):
        logname = strip_extension(video) + ".log"
        with open(staticlogs + logname, 'w') as logfile:
            process = subprocess.Popen([
                convert_location,
                f"{videofiles}/{video}",
                '-colorspace', 'HSL',
                '-channel', 'S',
                '-separate',
                '-format', '%M avg sat=%[fx:int(mean*100)]\n',
                "info:"
            ], stdout=logfile)
            # wait until Popen call finished
            process.communicate()

    for log in listdir(staticlogs):
        remove_empty_lines(staticlogs + log)
        remove_leading_lines(staticlogs + log, 200)


    # check if log files in the static log directory and read each file and generates a txt file to tell you if its static or not
    with open(static_results, "w") as f:
        f.write("Name," + "Is_Static" + '\n')
        for filename in listdir(staticlogs):
            with open(staticlogs + filename) as currentFile:
                text = currentFile.read()
                if ('sat=0' in text):
                    f.write( strip_extension(filename) + ',Yes' + '\n')
                else:
                    f.write( strip_extension(filename) + ',No' + '\n')


def check_frozen_output():
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
                    f.write( strip_extension(filename) + ',Yes' + '\n')
                else:
                    f.write( strip_extension(filename) + ',No' + '\n')


def main():
    writer = pd.ExcelWriter(f"{persistent_location}/{output_file}")
    old_date = None
    current_date = None

    while True:
        # clean up so that things don't stack
        cleanup(dirs_to_clean)

        # if the loop is skipped by exception, all following instructions (like sleep) would be skipped
        # if there's a repeating failure, don't run at full blast erroring out
        sleep(1)

        try:
            current_date = stat(csv_location).st_mtime
        except FileNotFoundError:
            logger.info(f"No {csv_location} found")
            continue

        if current_date == old_date:
            continue

        print('checking streams')
        try:
            check_streams()
        except Exception as e:
            logger.error(e)
            continue

        stream_checks = {
            "get_rtsp_errors": get_rtsp_errors,
            "check_no_output": check_no_output,
            "check_static_output": check_static_output,
            "check_frozen_output": check_frozen_output
        }

        for check in stream_checks:
            logger.info(f"trying {check}")
            try:
                stream_checks[check]()
            except Exception as e:
                logger.warning(f"Non-critical exception during {check}: {e}")

        # exceptions during sheet output are critical, to the point the program becomes pointless
        # forceful exit preferred
        for csvs in os.listdir(csv_files):
            df = pd.read_csv(csv_files+csvs)
            df.to_excel(writer, sheet_name=csvs)
        writer.save()

        old_date = current_date


if __name__ == "__main__":
    # so that it runs infinitely
    # TODO: differentiate between errors about input, working logs or output
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('stderr')
    main()
