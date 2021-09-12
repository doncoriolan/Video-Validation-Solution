from flask import Flask
from flask_restful import Api, Resource
import pandas
import os
import os.path
import json

app = Flask(__name__)
api = Api(app)

# Turn excel sheet to pandas data fram
excel_data_fragment = pandas.read_excel('/opt/vvs/diamond_sheet.xlsx', index_col=False)
# turn data frame into excel 
vvs_output_json = excel_data_fragment.to_json(orient="records")
# Pretty print the json
parsed = json.loads(vvs_output_json)


# Class for API and return the pretty print API above
class VvsResults(Resource):
    def get(self):
        return parsed

# define API URL
api.add_resource(VvsResults, "/vvsapi")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
