import logging
from os import getenv

persistent_location = getenv('vvs_persistent_data')

locations = {
    "persistent_location" : persistent_location,

    "analyzer_input_file" : f"{persistent_location}/{getenv('vvs_analyzer_input')}",
    "analyzer_output_file": f"{persistent_location}/{getenv('vvs_analyzer_output')}",

    "explorer_output_file": f"{persistent_location}/{getenv('vvs_explorer_output')}",

    "csv_files"           : f"{persistent_location}/stream_results/",
    "videofiles"          : f"{persistent_location}/videofiles/",
    "imagefiles"          : f"{persistent_location}/imagefiles/",
    "ffmpeglogs"          : f"{persistent_location}/ffmpeglog/",
    "blacklog"            : f"{persistent_location}/blacklog/",
    "staticlogs"          : f"{persistent_location}/staticlogs/",
    "frozenlog"           : f"{persistent_location}/frozenlog/",
    "rtsp_results"        : f"{persistent_location}/stream_results/rtsp_results",
    "black_results"       : f"{persistent_location}/stream_results/no_output_result",
    "frozen_results"      : f"{persistent_location}/stream_results/frozen_results",
    "static_results"      : f"{persistent_location}/stream_results/static_results",
    "ping_results"        : f"{persistent_location}/stream_results/ping_results",
}

def strip_extension(filename):
    if "." in filename:
        return ".".join(filename.split('.')[0:-1])
    else:
        return filename

def remove_leading_lines(filename, number):
    stripped = None
    with open(filename, "r") as f:
        stripped = f.read().split('\n')[number:]
    with open(filename, "w") as f:
        f.write("\n".join(stripped))

def remove_empty_lines(filename):
    stripped = []
    with open(filename, "r") as f:
        for line in f.read().split('\n'):
            if line != "": stripped.append(line)
    with open(filename, "w") as f:
        f.write("\n".join(stripped))
