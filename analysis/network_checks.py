import subprocess
import re
import logging
import nmap
from urllib.parse import urlparse
import requests

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

    scanner = nmap.PortScanner()
    results = {}
    output = scanner.scan(subnet, ports)

    for address in output['scan']:
        results[address] = []
        for port in output['scan'][address]['tcp'].keys():
            if output['scan'][address]['tcp'][int(port)]['state'] == 'open':
                results[address].append(port)

    return results

def camera_check(address, port):
    #will need https checks as well
    try:
        r = requests.get(f"http://{address}:{port}")
        keywords = ["camera", "video", "user interface"]

        for keyword in keywords:
            if keyword in r.text:
                return True
        return False
    except:
        return False
