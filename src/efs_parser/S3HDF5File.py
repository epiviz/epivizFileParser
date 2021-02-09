import requests
import json
class S3HDF5File():
    def __init__(self,url,s3_url):
        self.url = url
        self.s3_url=s3_url
        self.headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }

    def getMatrix(self,row_indices, column_indices):

        params = {
            "s3_url" : self.s3_url,
            "query" : f"['samp_data']['data'][{row_indices},{column_indices}]",
            "format":"json"
        }
        payload = json.dumps(params)

        #payload="{\"s3_url\":\"https://gred-cerberus-uat.s3.us-west-2.amazonaws.com/DS000000109/1/ASY000000100/RES000000465_1_MAE.hdf5\",\"query\":\"['samp_data']['data'][1:10,10]\",\"format\":\"json\"}"

        response = requests.request("POST", self.url, headers=self.headers, data=payload)

        if response.status_code == 200:
            eval_level1 = eval(response.content)
            result = eval(eval_level1)
        else:
            result = 'error'
        return result

