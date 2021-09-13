from flask import Flask
from flask_restful import Api, Resource
import pandas
import os
import os.path
import json
import time

app = Flask(__name__)
api = Api(app)

# Put the whole code in a while true so we can loop back to the top
while True:
    try:
        # read excel to pandas dataframe
        excel_data_fragment = pandas.read_excel('/opt/vvs/diamond_sheet.xlsx', index_col=False)
        # Dataframe to Json and put in the correct format using orient
        vvs_output_json = excel_data_fragment.to_json(orient="records")
        # Pretty print the JSON
        parsed = json.loads(vvs_output_json)
        # Class for the API to return the JSON
        class VvsResults(Resource):
            def get(self):
                return parsed
        # set the URL of the API
        api.add_resource(VvsResults, "/vvsapi")
        # run the code 
        if __name__ == "__main__":
            app.run(debug=True, host='0.0.0.0')
    # Accept the error if the excel sheet isnt ready yet
    except ValueError as err:
        time.sleep(60)
        continue
