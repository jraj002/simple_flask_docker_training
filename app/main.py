from flask import Flask
from flask import json
from flask import request
from flask import jsonify
import traceback
import pandas as pd
from sklearn.externals import joblib

clf = joblib.load('test.pkl')
features = ["Sex","Pclass","SibSp","Age"]

app = Flask(__name__)

@app.route("/")
def hello():
    return "Home Page For Titanic Survival Prediction"

@app.route('/echo', methods=['POST'])
def echo():
    if request.method == 'POST':
        return "Echo: POST"

@app.route('/predict', methods=['POST'])
def predict():
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    else:
        return request.headers['Content-Type']

@app.route('/predicttest', methods=['POST'])
def predicttest():
    try:
        json_request = request.get_json(silent=True)
        print(json_request)
        print(type(json_request))
        req_df = pd.DataFrame([json_request])
        print(req_df)

        #prediction = list(clf.predict(X = req_df[features]))
        #return jsonify({'prediction': prediction})

        prediction = clf.predict(X = req_df[features])
        return jsonify(id=1,result=prediction.tolist()[0])

        #prediction = clf.predict(X = req_df[features])
        #print(type(prediction))
        #lst = [{'id':'id', 'prediction': prediction[0]}]
        #print(prediction[0])
        #return jsonify(results=lst)

    except Exception:
        return jsonify({'error': 'exception', 'trace': traceback.format_exc()})

@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
