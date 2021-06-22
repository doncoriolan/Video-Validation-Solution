#!/usr/bin/env python3

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from os import stat, getenv
from sys import stderr
from datetime import datetime
import logging
import subprocess
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('gunicorn.error')
vvs_instance = None

#TODO: make this use an environment variable
sheet_dir=getenv("vvs_persistent_data")
input_csv=getenv("vvs_input_csv")
output_sheet=getenv("vvs_output_sheet")

landing_page = 'upload.html'

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/')
def upload():
    try: 
        timestamp = stat(sheet_dir + "/" + output_sheet).st_mtime
        date = str(datetime.fromtimestamp(timestamp)).split('.')[0]
        return render_template(landing_page, result_message=f"Last processed: {date}")
    except FileNotFoundError:
        return render_template(landing_page, result_message=f"No spreadsheet found")


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        global vvs_instance
        if vvs_result()['state'] == "running":
            return render_template('error.html', title="Scheduling Error", message="Analysis already running")
        f = request.files['file']
        if f.filename == "":  return render_template('error.html', title="Upload Error", message="No file attached")
        try:
            f.save(sheet_dir + "/" + input_csv)
        except:
            return render_template('error.html', title="Save Error", message="File could not be saved")

        # file is a stream, so have to save to read more than once
        with open(sheet_dir + "/" + input_csv) as f:
            for line in f:
                if len(line.split(',')) != 2:
                    return render_template('error.html', title="Validation Error", message="File is malformed")

        vvs_instance = subprocess.Popen(['/uploader/diamond_loop.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return render_template('success.html')

@app.route('/check_status', methods = ['GET'])
def vvs_check():
    return vvs_result()

def vvs_result():
    global vvs_instance
    logger.info(vvs_instance)
    if vvs_instance == None:
        return {"state": "stopped"}
    elif vvs_instance.poll() == None:
        return {"state": "running"}
    elif vvs_instance.poll() != None:
        logger.info(f"diamond_loop output: {vvs_instance.communicate()}")
        return {"state": "stopped", "result": vvs_instance.poll()}

if __name__ == '__main__':
    app.run(debug = True)
