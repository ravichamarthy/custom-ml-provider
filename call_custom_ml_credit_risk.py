import pandas as pd
import random, requests, datetime, json
from ibm_ai_openscale import APIClient
from ibm_ai_openscale.supporting_classes import PayloadRecord
import requests
from datetime import datetime, timedelta

file_name = '/Users/ravi/Downloads/AISphere/Notebooks/german_credit_data_biased_test.csv'
delimiter = ','
scoring_url = "http://custom-ml-providers-01.us-south.cf.appdomain.cloud/deployments/3462b215-21f3-4d82-8a66-b1ffd93c9f95?version=2020-10-25"
aios_credentials = {"apikey": "R4ZmoGqWaQyxy5370P_eEP7N4iWZpUJWpfbPzQ6IAGG0", "url": "https://api.aiopenscale.cloud.ibm.com", "instance_guid": "819899f3-86be-406a-8a23-bf0a0131df7b"}
allowed_status = [200,201,202]

def main():
    data = pd.read_csv(file_name, delimiter=delimiter, na_filter = False)
    del data['Risk']
    features = data.columns.tolist()

    print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
    print('features:')
    print(features)
    print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
    
    rows = data[features].values.tolist()
    request_data = {"fields": features, "values": rows}
    
    print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
    print('request_data:')
    print(request_data)
    print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
    
    start_time = datetime.now()
    post_resp = requests.post(scoring_url, json=request_data, auth=('admin', 'password'))
    end_time = datetime.now()
    response_time = (end_time - start_time).total_seconds()

    print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
    print('response_time:')
    print(response_time)
    print(str(int(response_time)))
    print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')

    status_code = int(post_resp.status_code)
    print("SCORE RESPONSE STATUS CODE: " + str(status_code))
    if status_code not in allowed_status:
        print("SCORING FAILED WITH ERROR: " + str(post_resp.text)) 
    else:
        response_data = json.loads(post_resp.text)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
        print('response_data:')
        print(response_data)
        print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')

        client = APIClient(aios_credentials)
        subscription = client.data_mart.subscriptions.get(subscription_uid="721893c9-4df6-48c3-809e-53314acbdfc3")
        records = [PayloadRecord(request=request_data, response=response_data, response_time=int(response_time))]
        subscription.payload_logging.store(records=records)

main()