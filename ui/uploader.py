#!/usr/bin/env python3

from flask import Flask, render_template, request, Markup
from werkzeug.utils import secure_filename
from os import stat, getenv
from sys import stderr
from datetime import datetime
from file_management import locations
import logging
import subprocess
import pandas
from diamond_loop import critical_checks, non_critical_checks

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('gunicorn.error')

vvs_instance = None
explorer_instance = None

landing_page = 'upload.html'

status = {
    "green": 'background-color: LightGreen',
    "yellow": 'background-color: LightGoldenrodYellow',
    "red": 'background-color: Salmon',
}

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/')
def upload():
    """Root route

    Code here is responsible for generating timestamps on data if it exists
    """

    try: 
        timestamp = stat(locations["analyzer_output_file"]).st_mtime
        date = str(datetime.fromtimestamp(timestamp)).split('.')[0]
        return render_template(landing_page, result_message=f"Last processed: {date}")
    except FileNotFoundError:
        return render_template(landing_page, result_message=f"No spreadsheet found")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")

#FIXME: rename to analyser and explorer (for new function)
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    """Function (and route) responsible for uploading lists of cameras to scan

    Validation is handled on both the frontend and backend,
    based on the number of columns in the incoming CSV.
    Separator used is ','

    Simple POST request can easily be used from eg. curl to automate.

    The function also assigns a global instance of the VVS analyser,
    used for keeping track of ongoing processing and its results.
    """

    try:
        if request.method == 'POST':
            if vvs_check()['state'] == "running":
                return render_template('error.html', title="Scheduling Error", message="Analysis already running")
            f = request.files['analyzer_input']
            if f.filename == "":  return render_template('error.html', title="Upload Error", message="No file attached")
            logger.info('check')
            try:
                f.save(locations["analyzer_input_file"])
            except Exception as e:
                logger.error(e)
                return render_template('error.html', title="Save Error", message="File could not be saved")

            # file is a stream, so have to save to read more than once
            with open(locations["analyzer_input_file"]) as f:
                for line in f:
                    if len(line.split(',')) != 2:
                        return render_template('error.html', title="Validation Error", message="File is malformed")

            global vvs_instance
            vvs_instance = subprocess.Popen(['/analysis/diamond_loop.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            return render_template('success.html')
    except Exception as e:
        logger.error(e)

@app.route('/explorer', methods = ['POST'])
def initiate_search():
    """Route for starting a camera search, given a subnet as input.

    Just like the analyzer route, a global search instance is used to
    keep track of the state and results of a search. Since this is
    another POST request, curl can also be used to initiate.
    """

    if request.method == 'POST':
        logger.debug('initiating search')
        #FIXME: subnet form validation
        if explorer_check()['state'] == "running":
            return render_template('error.html', title="Scheduling Error", message="Search already running")

        logger.debug(request.form['explorer_input'])
        #return render_template('error.html', title="Stop", message="exited")
        global explorer_instance
        explorer_instance = subprocess.Popen(['/analysis/find_cameras.py', request.form['explorer_input']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return render_template('success.html')

def analysis_results_colorcoding(row):
    if row['rtsp_error'] == "No":
        return [status['green']]*2 #*row_width just displaying name & rtsp error
    else:
        return [status['red']]*2

@app.route('/analysis_results', methods = ['GET'])
def show_analysis_results():
    """Web UI for seeing a preview of the downloadable results

    Using pandas for easy parsing of Excel sheets and a colorcoding
    function to distinguish between results.
    """
    try:
        excel_file = pandas.read_excel(locations['analyzer_output_file'])[['name','rtsp_error']]
        logger.info('file opened')
        styled_table = excel_file.style.apply(analysis_results_colorcoding, axis=1)
        return render_template('results.html', table=Markup(styled_table.render()))
    except Exception as e:
        logger.exception("Failed to serve analysis results")

def search_results_colorcoding(row):
    if row['open ports'] == 'None':
        return ['background-color: Salmon;']*3
    elif row['likely camera']:
        return ['background-color: LightGreen;']*3
    else:
        return ['background-color: LightGoldenrodYellow;']*3

@app.route('/search_results', methods = ['GET'])
def show_search_results():
    try:
        excel_file = pandas.read_excel(locations['explorer_output_file'])
        logger.info('file opened')
        logger.info(f"excel_file: {excel_file}")
        styled_table = excel_file.style.apply(search_results_colorcoding, axis=1)
        return render_template('results.html', table=Markup(styled_table.render()))
    except Exception as e:
        logger.exception("Failed to serve search results")

@app.route('/check_analyzer', methods = ['GET'])
def vvs_check():
    global vvs_instance
    return subprocess_state(vvs_instance)

@app.route('/check_explorer', methods = ['GET'])
def explorer_check():
    global explorer_instance
    return subprocess_state(explorer_instance)

def subprocess_state(instance):
    """Used for normalising output of the check_* functions

    Currently, only distinguishes between failed/successful runs and
    no results present.
    """
    logger.info(instance)
    if instance == None:
        return {"state": "stopped"}
    elif instance.poll() == None:
        return {"state": "running"}
    elif instance.poll() != None:
        logger.info(f"diamond_loop output: {instance.communicate()}")
        return {"state": "stopped", "result": instance.poll()}

if __name__ == '__main__':
    app.run(debug = True)
