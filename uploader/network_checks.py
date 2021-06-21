import subprocess
import re
import logging
from urllib.parse import urlparse

logger = logging.getLogger('stderr')

def ping(address):
    netloc = urlparse(address).netloc
    ping_process = subprocess.Popen(['/usr/bin/ping', '-c10', '-i0.2', '-W1', netloc], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ping_process.communicate()

def ping_readout(output):
    complete_failure = ("unreachable", "unreachable")
    if output[1]:
        logger.error("unknown error during ping")
        logger.info(output)
        return complete_failure
    output_lines = output[0].decode('utf-8').split('\n')

    counts = output_lines[-3]
    loss = float(re.sub('\D', '', counts.split(',')[2]))
    loss_verb = ""

    if loss > 99.0:
        return complete_failure
    elif loss >= 10.0:
        loss_verb = "lossy"
    elif loss < 10.0:
        loss_verb = "good"

    statistics = output_lines[-2]
    average = float(statistics.split(' ')[3].split('/')[1])
    standard_deviation = float(statistics.split(' ')[3].split('/')[3])
    ratio = standard_deviation/average
    stability_verb = ""

    if ratio >0.8:
        stability_verb = "very jittery"
    elif ratio >=0.2:
        stability_verb = "jittery"
    elif ratio <0.2:
        stability_verb = "stable"

    return (loss_verb, stability_verb)
