import requests
import json

__author__ = "Hany Elgaml, Jayaram Kancherla"
__copyright__ = "mit"
__license__ = "mit"

class S3HDF5File():
    """
    S3HDF5 uses an API endpoint (`url`) that makes S3-Select calls 
    to a resource stored on S3.
    """
    def __init__(self, url, file):

        self.url = url
        self.file = file
        
        self.headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }

    def getMatrix(self, row_indices, column_indices):

        params = {
            "s3_url" : self.file,
            "query" : f"['samp_data']['data'][{row_indices},{column_indices}]",
            "format":"json"
        }

        payload = json.dumps(params)

        try:
            r = requests.request("POST", self.url, headers=self.headers, data=payload)
        except Exception as e:
            raise Exception(f"Request failed, {e}")

        if r.status_code != 200:
            raise Exception(f"API Error")
            
        return r.json()
