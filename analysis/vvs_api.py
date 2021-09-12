from flask import Flask
from flask_restful import Api, Resource
import pandas
import os
import os.path
import json
import time

app = Flask(__name__)
api = Api(app)

while True:
    try:
        excel_data_fragment = pandas.read_excel('/opt/vvs/diamond_sheet.xlsx', index_col=False)
        vvs_output_json = excel_data_fragment.to_json(orient="records")
        parsed = json.loads(vvs_output_json)
        class VvsResults(Resource):
            def get(self):
                return parsed
        api.add_resource(VvsResults, "/vvsapi")
        if __name__ == "__main__":
            app.run(debug=True, host='0.0.0.0')
    except ValueError as err:
        time.sleep(60)
        continue
