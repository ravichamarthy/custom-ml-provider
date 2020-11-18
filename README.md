## IBM Watson OpenScale Custom ML Provider - Reference Implementation

With IBM Watson OpenScale you can monitor a machine learning model that is deployed in various serv engines like, Watson Machine Learning, Azure, AWS, SPSS. And if your machine learning models are not deployed in these serv engines, say it is hosted as a docker endpoint in your in-house environment or it is hosted in Google Cloud ML, BigML or Domino, or Arimo engines, and you want to monitor the models for their fairness in predictions, drift or monitor the quality and be able to explain the transactions, then the option is to expose the model scoring endpoints as a custom ML provider and subscribe these endpoints with OpenScale for model monitoring. To simply put - wrap the model scoring as a REST endpoint and subscribe this REST endpoint with OpenScale for model monitoring.

So, in this repo what is included are two notebooks for creating two models a) Credit Risk prediction and b) Product Line prediction and deploy them to IBM Watson Machine Learning. (Notebooks included).

And then create a Python Flask App in cloud.ibm.com by creating a python starter pack from https://cloud.ibm.com/developer/appservice/create-app?starterKit=db553c13-0d86-3291-b523-bbcc7e610a52&defaultLanguage=undefined

Then change the index.py file from this app, in such a way that this application will now act as a scoring gateway to the two models that we have deployed in WML. (Source code for index.py included)

Subscribe this end point with OpenScale as Subscription 1 and Subscription 2 (one for each model deployment) and thereby configure the OpenScale monitors. (Included the sample data as well).

Files included in this repo:

* Credit Risk with Spark.ipynb - Notebook to create and deploy the credit risk prediction model in WML
* Product Line with Spark.ipynb - Notebook to create and deploy the product line prediction model model in WML

* index.py - The code that can be exposed as a custom ML provider wrapping any number of deployments. Pretty generic code.

* call_custom_ml_product_line.py - Python code to call the product line custom ml provider end point and store the payload logging records to OpenScale data mart.
* ProductLine.csv - Sample data, that would be used to score the model and payload log to OpenScale

* call_custom_ml_credit_risk.py - Python code to call the credit risk custom ml provider end point and store the payload logging records to OpenScale data mart.
* german_credit_data_biased_test.csv - Sample data, that would be used to score the model and payload log to OpenScale
