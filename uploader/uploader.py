#!/usr/bin/env python3

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from os import stat, getenv
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

        for line in f:
            if len(str(line).split(',')) != 2:
                del f
                return render_template('error.html')

        f.save(sheet_dir + "/" + secure_filename(input_csv))
        return render_template('success.html')

if __name__ == '__main__':
    app.run(debug = True)
