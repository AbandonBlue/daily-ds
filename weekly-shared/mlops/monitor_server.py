"""
    監控模型、資料的程式，通常是排程執行，或者資料流入執行。
    雲端服務常見 composer, cloud function 觸發.py檔案執行。
    以此次範例來說，可以用 serving server 去紀錄資料筆數，
    當累積達一定再呼叫此 server 之API來計算。
    
    --- 
    
    以公司來說，可能是呼叫 BQ API 來做運算。

    以雲端服務來說，是 cloud function / Google App Engine / Composer 的替代。
"""
import numpy as np
import requests
from joblib import load, dump
from flask import Flask, request, jsonify
from module.db import get_json
from module.monitoring import notify, get_model_performance, get_monotoring_data
from module.monitoring import check_model_performance
from module.model_training import retrain
from module.model_evaluation import is_evaluation

# app
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False     # 解決json中文問題

# config
config = get_json('./data/config.json')
model_name = './models/2022-11-29-11_29_08_483980rf.joblib'
model = load(model_name)


@app.route('/monitoring/cancer/', methods=['GET'])
def monitoring_cancer():
    """
        提供一個 monitoring 的 API，serving server 會呼叫此API，進行效能、資料監控。
        
        1. serving server 呼叫此 API，
        2. 此 server 計算目前模型的效能，
        3. 若異常呼叫retraining，若正常則不做事情。
    """
    global model
    x, y = get_monotoring_data(config['db_name_monitoring'], config['db_query_monitoring'], config['table_name_monitoring'])
    print(x.shape, y.shape)
    acc = get_model_performance(model, x, y)
    is_monitor = check_model_performance(acc, config['monitoring_threshold'])
    
    if is_monitor:
        message = '\n模型效能不佳，呼叫重新訓練 API'
        notify('line-notify', config['line-notify'], message)
        url = config['retraining_url']
        resp = requests.get(url)
        return jsonify({'state': f'模型效能異常: {acc}，以觸發重新訓練。'})
    else:
        message = '\n'
        notify('line-notify', config['line-notify'], message)
        return jsonify({'state': f'模型效能正常: {acc}，不須處理。'})


if __name__ == '__main__':
    app.run(debug=False, port=8002)



