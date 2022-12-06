"""
    監控效能使用的模組。
"""
import requests
import time
from sklearn.metrics import accuracy_score, confusion_matrix
from .db import query_db, get_column_name_from_sqlite, transform_db_query_to_df


def function_spent_time(func):
    def wrap(*args, **kwargs):
        t = time.time()
        result = func(*args, **kwargs)
        print(f'花費時間: {round(time.time()-t, 3)} 秒')
        return result
    return wrap


def notify(notify_method, token, message):
    if notify_method == 'line-notify':
        # HTTP 標頭參數與資料
        headers = {"Authorization": "Bearer " + token}
        data = {'message': message }

        # 以 requests 發送 POST 請求
        requests.post(
            "https://notify-api.line.me/api/notify",
            headers=headers,
            data=data
        )
    else:
        # 可以自己擴展
        pass


def get_monotoring_data(db_name, db_query, table_name):
    """
        取得監控判斷資料。
    """
    df = transform_db_query_to_df(db_name, db_query)
    column_names = get_column_name_from_sqlite(db_name, table_name)
    df.columns = column_names
    y = df['label']
    x = df.drop(columns=['id', 'label', 'prob'])
    return x, y


def get_model_performance(model, x, y):
    """
        計算模型效能在特定資料集上，
        現在簡化表示，所以將x, y直接傳入，真實應用可以直接在BQ上。
    """
    y_pred = model.predict(x)
    print(y_pred)
    acc = accuracy_score(y, y_pred)
    return acc


def check_model_performance(acc, threshold):
    if acc > threshold:
        return False
    return True



if __name__ == '__main__':
    # LINE Notify 權杖
    token = ''
    # 要發送的訊息
    message = '您的模型好囉!'
    notify(message, token)
    pass