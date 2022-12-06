"""
    Model API，主要用來預測的 server code.

    ---

    以雲端服務來說，是 cloud function / Google App Engine 的替代。
"""
import numpy as np
import os
import sqlite3
from joblib import load, dump
from flask import Flask, request, jsonify

# module
from module.db import save_prediction_data, query_db


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False     # 解決json中文問題


# 需要用 config
model_name = './models/2022-11-29-11_29_08_483980rf.joblib'
model = load(model_name)
base_dir = os.path.dirname(os.path.abspath(__file__))

@app.route('/predict/cancer/', methods=['POST'])
def predict_cancer():
    """
        Serving API，模型與外界的管道，如果要更好地完善，
        可以搭配 Dcard 用的方式，用一些 middleware 去減少惡意呼叫。
    """
    global model
    labels = {}
    data = request.get_json()  # {'data1': [features]}
    #print(data)

    y_pred = model.predict(list(data.values()))

    for key, label in zip(data, y_pred):
        labels[key] = int(label) # pervent TypeError: Object of type int32 is not JSON serializable
    #print(labels)


    ids = np.array([[i for i in range(len(data))]]).reshape(len(data), -1)
    fake_labels = np.array([[0]*len(data)]).reshape(len(data), -1)
    y_pred = np.array([y_pred]).reshape(len(data), -1)
    data = np.array(list(data.values()))

    print(ids.shape, fake_labels.shape, y_pred.shape, data.shape)

    data = np.concatenate([ids, data, fake_labels, y_pred], axis=1)
    
    save_prediction_data(data, 'mlops.db')
    return jsonify(labels)


if __name__ == '__main__':
    app.run(debug=False, port=8000)