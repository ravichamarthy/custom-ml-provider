from server import app
from flask import jsonify, render_template, request
import requests

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

@app.route("/deployments/<deployment_id>", methods=["POST"])
def score(deployment_id):
    print("Request recieved!")
    print("Request object: {}".format(request))
    print("Request arguments: {}".format(dict(request.args)))
    print("Request headers: {}".format(request.headers))
    print("Request URL: {}".format(request.url))
    print("Request auth: {}".format(request.authorization))
    print("Request payload: {}".format(request.json))
    print("Calling WML deployment!")
    #Your user API KEY
    API_KEY = "R4ZmoGqWaQyxy5370P_xxxxx"
    token_response = requests.post("https://iam.ng.bluemix.net/identity/token", data={"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"})
    mltoken = token_response.json()["access_token"]
    
    print("IAM token for calling the WML Python Function Deployment generated!")
    header = {"Content-Type": "application/json", "Authorization": "Bearer " + mltoken}
    payload_data = {
        "input_data": [
            request.json
        ]
    }
    version = request.args.get("version")
    response_scoring = requests.post("https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{}/predictions?version={}".format(deployment_id, version), json=payload_data, headers=header)
    output = response_scoring.json()
    print("Scoring response from WML recieved!")
    print("Response rows length: {}".format(len(output["predictions"][0]["values"])))

    return jsonify(output["predictions"][0])

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return app.send_static_file('500.html')
