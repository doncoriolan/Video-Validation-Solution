import subprocess
import re
import logging
import nmap
from urllib.parse import urlparse
import requests
import timeit
import datetime
current_time = datetime.datetime.now()

# list of most common ports we can use to check if the address is for a camera
extended_port_list=[
    "80",
    "81",
    "82",
    "83",
    "84",
    "85",
    "86",
    "87",
    "88",
    "89",
    "1080",
    "8080",
    "1081",
    "1082",
    "1083",
    "1084",
    "1085",
    "1086",
    "1087",
    "1088",
    "1089",
    "8081",
    "8082",
    "8083",
    "8084",
    "8085",
    "8086",
    "8087",
    "8088",
    "8089",
]
extended_ports = ",".join(extended_port_list)

logger = logging.getLogger('stderr')

def ping(address):
    netloc = urlparse(address).netloc
    port = urlparse(address).port
    if port:
        netloc = netloc.replace(f":{port}", "")
    if "@" in netloc:
        netloc = netloc.split('@')[-1]
    logger.info("address: " + netloc)
    ping_process = subprocess.Popen(['/usr/bin/ping', '-c10', '-i0.2', '-W1', netloc], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ping_process.communicate()

def ping_readout(output):
    """Utility function for qualifying the ping results.

    The two verbs output are to describe the packet loss (if) present
    and the deviation of return times. This is, however, inherently
    flawed since most network admins will either block ICMP outright or
    deprioritise pings to the point where they mostly indicate if the
    network is congested.
    """
    if output[1]:
        logger.error("unknown error during ping")
        logger.info(output)
        raise ConnectionError('No response to ICMP ping')
    output_lines = output[0].decode('utf-8').split('\n')

    counts = output_lines[-3]
    loss = float(re.sub('\D', '', counts.split(',')[2]))
    loss_description = ""

    if loss > 99.0:
        raise ConnectionError('Responses to ICMP ping below 1 per 100')
    elif loss >= 10.0:
        loss_description = "lossy"
    elif loss < 10.0:
        loss_description = "Lossless"

    statistics = output_lines[-2]
    average = float(statistics.split(' ')[3].split('/')[1])
    standard_deviation = float(statistics.split(' ')[3].split('/')[3])
    ratio = standard_deviation/average
    stability_description = ""

    if ratio >0.8:
        stability_description = "very jittery"
    elif ratio >=0.2:
        stability_description = "jittery"
    elif ratio <0.2:
        stability_description = "stable"

    return (loss_description, stability_description)


def nmap_port_scan(subnet, ports='554'):
    """Nmap wrapper to port-scan addresses.

    Uses a subnet and either single or a list of ports to scan for each
    address in the subnet. For now it is TCP only.
    """

    scanner = nmap.PortScanner()
    results = {}
    output = scanner.scan(subnet, ports)

    for address in output['scan']:
        results[address] = []
        for port in output['scan'][address]['tcp'].keys():
            if output['scan'][address]['tcp'][int(port)]['state'] == 'open':
                results[address].append(port)

    return results


def camera_check(address):
    actual_cams = []
    urls = [f'http://{address}/mjpg/video.mjpg',
        f'rtsp://{address}/mpeg4/media.amp',
        f'rtsp://{address}/axis-media/media.amp?',
        f'rtsp://{address}/onvif-media/media.amp',
        f'http://{address}/axis-cgi/mjpg/video.cgi',
        f'rtsp://{address}/ucast/12',
        f'http://{address}/mjpg/1/video.mjpg?Axis-Orig-Sw=true',
        f'http://{address}/stream.asf',
        f'http://{address}/mjpg/1/video.mjpg',
        f'rtsp://{address}/mpeg4',
        ]
    videoname = ('/opt/vvs/videofiles/' + address + current_time.strftime("%Y%m%d_%H%M%S") + '.mp4')
    for url in urls:
        # ffmpeg process 
        videoprocess = subprocess.Popen(['/usr/bin/ffmpeg', '-y', '-t', '1', '-i', url, videoname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ffmpeg_output = videoprocess.communicate()
        while videoprocess.poll() is None:
            time.sleep(0.5)
        rc = videoprocess.returncode
        if rc == 0:
            actual_cams.append({'Working URLS': url})

        return actual_cams
