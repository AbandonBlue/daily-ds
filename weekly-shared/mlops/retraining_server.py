"""
    模型重新訓練 API Server.
    正常透過排程呼叫。
"""

import numpy as np
from joblib import load, dump
from flask import Flask, request, jsonify
from module.db import get_json
from module.monitoring import notify
from module.model_training import retrain
from module.model_evaluation import is_evaluation

# app
app = Flask(__name__)

# config
config = get_json('./data/config.json')



@app.route('/retraining/cancer/', methods=['GET'])
def retraining_cancer():
    """
        提供一個 retraining 的 API，溝通 servre 去執行 retraining。
        
        1. 發送 request 至此，
        2. 觸發訓練程式、模組，
            2.1 比較是否更好
                if yes, 部屬
                else, notify...
        3. notify
    """
    try:
        # 直接執行，呼叫 訓練程式。用threading?然後好了可能用 line notify 提醒?(反正就是一個提醒)
        
        # 取得訓練資料, 從config
        x_train, y_train = None, None
        x_test, y_test = None, None
        
        # 2.觸發訓練程式、模組，
        notify('line-notify', config['line-notify'], '重新訓練模型，訓練完會通知您！')
        model = retrain(x_train, y_train)

        # 2.1 驗證是否比較好
        is_better, y_pred = is_evaluation(model, x_test, y_test, config['threshold'])
        
        # 3. notify
        if is_better:
            notify('line-notify', config['line-notify'], '模型訓練完成，表現較佳，可以部屬了！')
        else:
            notify('line-notify', config['line-notify'], '模型訓練完成，表現較差，需要被檢視！')

        return jsonify({'state': '成功執行'})
    except Exception as e:
        notify('line-notify', config['line-notify'], f'retraining server 發生問題，請聯繫開發人員！\n錯誤訊息：\n{e}')
        return jsonify({'state': '不可預期的錯誤'})


if __name__ == '__main__':
    app.run(debug=False, port=8001)