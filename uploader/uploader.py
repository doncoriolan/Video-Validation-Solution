#!/usr/bin/env python3

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from os import stat, getenv
from sys import stderr
from datetime import datetime
app = Flask(__name__)

#TODO: make this use an environment variable
sheet_dir=getenv("vvs_persistent_data")
input_csv=getenv("vvs_input_csv")
output_sheet=getenv("vvs_output_sheet")

landing_page = 'upload.html'

@app.route('/')
def upload():
    try: 
        timestamp = stat(sheet_dir + "/" + output_sheet).st_mtime
        date = str(datetime.fromtimestamp(timestamp)).split('.')[0]
        return render_template(landing_page, output_message=f"Last processed: {date}")
    except FileNotFoundError:
        return render_template(landing_page, output_message=f"No spreadsheet found")


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
        return render_template('success.html')

if __name__ == '__main__':
    app.run(debug = True)
