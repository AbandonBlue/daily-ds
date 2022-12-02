"""
    監控效能使用的模組。
"""
import requests
import time


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
    

if __name__ == '__main__':
    # LINE Notify 權杖
    token = ''
    # 要發送的訊息
    message = '您的模型好囉!'
    notify(message, token)
    pass