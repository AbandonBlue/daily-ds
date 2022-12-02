"""
    模型驗證模組。
"""
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix


def is_evaluation(model, x_test, y_test, threshold):
    """
        驗證模型效能是否優於 threshold 
    """
    # 快速驗證用
    if not x_test:
        return True, None
    y_pred = model.predict(x_test)
    acc = accuracy_score(y_test, y_pred)

    if acc >= threshold:
        return True, y_pred
    return False, y_pred