#!/usr/bin/python3
# Main Script for the Video Validation Solution. The purpose of this script is to record video and run specific checks on the video.
# Copyright of Mike Coriolan.

import csv
import subprocess
import datetime
import os
import os.path
from os import listdir, remove, stat
from time import sleep
from sys import stderr, exit
import pandas as pd
import concurrent.futures
import logging
import signal
import time
from file_management import strip_extension, remove_leading_lines, remove_empty_lines, locations
from network_checks import ping, ping_readout


dirs_to_clean = [
    locations["csv_files"],
    locations["videofiles"],
    locations["ffmpeglogs"],
    locations["blacklog"],
    locations["staticlogs"],
    locations["frozenlog"],
    locations["imagefiles"]
]

bin_location        = f"/usr/bin"
convert_location    = f"{bin_location}/convert"
ffmpeg_location     = f"{bin_location}/ffmpeg"
sed_location        = f"{bin_location}/sed"
find_location       = f"{bin_location}/find"
grep_location       = f"{bin_location}/grep"

def cleanup(directories):
    for directory in directories:
        for found_file in listdir(directory):
            try:
                remove(directory + found_file)
            except FileNotFoundError as e:
                logger.exception(f"Couldn't delete file {directory}{found_file} due to below exception:")
                logger.exception(e)


df = pd.read_csv(locations["analyzer_input_file"], index_col=False)
name = df['name'].tolist()
urls = df['url'].tolist()


stream_output = (locations["videofiles"])

cameras = []
def ffmpeg_function(urls, name):
    ffmpeg_instance = subprocess.Popen([ffmpeg_location, '-y', '-t', '10', '-i', urls, stream_output + name + ".mp4"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # sent output to ffmpeg log
    output, error = ffmpeg_instance.communicate()
    logger.debug(output)
    error = str(error)
    cameras.append({'name': name, 'url': urls, 'checks': [], 'ffmpeg_output': error})

    return cameras

def check_streams():
    with concurrent.futures.ThreadPoolExecutor() as executor:
       multiple_p = executor.map(ffmpeg_function, urls,name)
       return cameras


def check_ping(cameras, check_name):
    for camera in cameras:
        try:
            result = ping_readout(ping(camera['url']))

            camera['checks'].append((check_name, f"{result[0]} and {result[1]}"))
        except:
            logger.exception('Ping failed')
            camera['checks'].append((check_name, "check failed"))


rtsp_error_list = [
    ('400 Ba', '400'),
    ('401 Un', '401'),
    ('402 Pa', '402'),
    ('403 Fo', '403'),
    ('404 No', '404'),
    ('405 Me', '405'),
    ('406 No', '406'),
    ('407 Pr', '407'),
    ('408 Re', '408'),
    ('410 Go', '410'),
    ('411 Le', '411'),
    ('412 Pr', '412'),
    ('413 Re', '413'),
    ('414 Re', '414'),
    ('415 Un', '415'),
    ('451 Pa', '451'),
    ('452 Co', '452'),
    ('453 No', '453'),
    ('454 Se', '454'),
    ('455 Me', '455'),
    ('456 He', '456'),
    ('457 In', '457'),
    ('458 Pa', '458'),
    ('459 Ag', '459'),
    ('460 On', '460'),
    ('461 Un', '461'),
    ('462 De', '462'),
    ('463 Ke', '463'),
    ('500 In', '500'),
    ('501 No', '501'),
    ('502 Ba', '502'),
    ('503 Se', '503'),
    ('504 Ga', '504'),
    ('505 RT', '505'),
    ('551 Op', '551'),
    ('failed:', 'Failed to download stream'),
    ('Connection refused', 'Connection refused'),
    ('Protocol not found', 'Invalid protocol'),
    ('does not contain any stream', 'No stream'),
    ('Invalid data found when processing input', 'Invalid data'),
    ('Cannot read RTMP handshake response', 'RTMP handshake failed'),
]


# grab the rtsp errors from the log files we made above
# TODO: implement this in a cleaner fashion, using a dict w/ inputs and responses
def get_rtsp_errors(cameras, check_name):
    for camera in cameras:
        try:
            failed = False
            for error in rtsp_error_list:
                if error[0] in camera['ffmpeg_output']:
                    failed = True
                    logger.info('rtsp_check failed successfully')
                    camera['checks'].append(('rtsp_error', error[1]))
                    break
            if not failed: camera['checks'].append((check_name, 'No'))
        except:
            logger.exception('rtsp check failed')
            camera['checks'].append((check_name, 'check failed'))


# for the files recorded above check if the video is black
def check_no_output(cameras, check_name):
    for camera in cameras:
        try:
            # Black detect d set the durations we want to find and pix_th sets the level of black. 0 is pure black and 1 a little black
            ffmpeg_blackdetect = subprocess.Popen([ffmpeg_location, '-i', locations["videofiles"]+camera['name']+'.mp4', '-vf', 'blackdetect=d=2:pix_th=.15', '-an', '-f', 'null', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            black_check_output = str(ffmpeg_blackdetect.communicate()[1])

            if 'blackdetect' in black_check_output:
                camera['checks'].append((check_name, 'Yes'))
            else:
                camera['checks'].append((check_name, 'No'))
        except:
            camera['checks'].append((check_name, 'check failed'))


# for the files recorded check if the video is pure static using a bash scripts and generate log file for every video
# static refers to noise>signal
def check_static_output(cameras, check_name):
    for camera in cameras:
        try:
            # done as a PNG to prevent further lossiness making an image that's too close to static noise for ImageMagick
            imagename = camera['name'] + '.png'
            #FIXME: generate image to check 
            process = subprocess.Popen([ffmpeg_location, "-ss", "5", "-i", f"{locations['videofiles']}/{camera['name']}.mp4", "-frames:v", "1", f"{locations['imagefiles']}/{imagename}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = str(process.communicate())
            logger.debug(f"stdout: {output}")


            process = subprocess.Popen([
                convert_location,
                f"{locations['imagefiles']}{imagename}",
                '-colorspace', 'HSL',
                '-channel', 'S',
                '-separate',
                '-format', '%M avg sat=%[fx:int(mean*100)]',
                "info:"
            ], stdout=subprocess.PIPE)
            # wait until Popen call finished
            output = str(process.communicate()[0])
            logger.debug(f"stdout: {output}")

            #output = list(filter(lambda x: x != '', output.split('\n')))
            #output = '\n'.join(output[200:])

            if ('sat=0' in output):
                camera['checks'].append((check_name, 'Yes'))
            else:
                camera['checks'].append((check_name, 'No'))
        except:
            camera['checks'].append((check_name, 'check failed'))


def check_frozen_output(cameras, check_name):
    # check if files recorded were frozen and put the output in a log file
    for camera in cameras:
        try:
            ffmpeg_freezedetect = subprocess.Popen([ffmpeg_location, '-i', locations["videofiles"]+camera['name']+'.mp4', '-vf', 'freezedetect=d=7', '-f', 'null', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            frozen_output = str(ffmpeg_freezedetect.communicate()[1])

            if 'freezedetect' in frozen_output:
                camera['checks'].append((check_name, 'Yes'))
            else:
                camera['checks'].append((check_name, 'No'))
        except:
            camera['checks'].append((check_name, 'check failed'))

def restart_api():
    subprocess.Popen(['python3', '/analysis/kill_and_restart_api.py'], shell=False)

def main():
    # clean up so that things don't stack
    logger.info('beginning cleanup')
    cleanup(dirs_to_clean)
    cameras = []

    logger.info('checking streams')
    try:
        cameras = check_streams()
    except Exception as e:
        logger.exception(e)
        exit(1)

    stream_checks = {}
    for check in critical_checks:
        stream_checks[check] = critical_checks[check]
    for check in non_critical_checks:
        stream_checks[check] = non_critical_checks[check]

    for check in stream_checks:
        logger.info(f"trying {check}")
        try:
            stream_checks[check](cameras, check)
        except:
            logger.exception(f"Unable to perform {check}")
    
    #logger.info(cameras)
    exportable_data = []
    for camera in cameras:
        exportable_data.append(
            [camera['name']] + [check[1] for check in camera['checks']]
        )
    for camera in cameras:
        logger.info(f"{camera['name']}: {camera['checks']}")
    exportable_data = pd.DataFrame(
        columns = ["name"] + list(stream_checks.keys()),
        data = exportable_data
    )
    logger.info(exportable_data)

    restart_api()

    exportable_data.to_excel(locations['analyzer_output_file'], index=False)

# putting the checks here allows them to be exportable through modules and hooked up to relevant functions
critical_checks = {
    "rtsp_error": get_rtsp_errors,
    "no_output_check": check_no_output,
    "static_output_check": check_static_output,
    "frozen_output_check": check_frozen_output,
}

non_critical_checks = {
    "ping_check": check_ping,
}


if __name__ == "__main__":
    logging.basicConfig(filename=f"{locations['persistent_location']}/diamond.log", level=logging.DEBUG)
    logger = logging.getLogger('diamond.log')
    main()
