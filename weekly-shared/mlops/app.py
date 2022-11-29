import numpy as np
from joblib import load, dump
from flask import Flask, request, jsonify


app = Flask(__name__)

# 需要用 config
model_name = './models/2022-11-29-11_29_08_483980rf.joblib'
model = load(model_name)


@app.route('/predict/cancer/', methods=['POST'])
def predict_cancer():
    global model
    labels = {}
    data = request.get_json()  # {'data1': [features]}
    print(data)

    y_pred = model.predict(list(data.values()))

    for key, label in zip(data, y_pred):
        labels[key] = int(label) # pervent TypeError: Object of type int32 is not JSON serializable
    print(labels)
    return jsonify(labels)


if __name__ == '__main__':
    app.run(debug=True)