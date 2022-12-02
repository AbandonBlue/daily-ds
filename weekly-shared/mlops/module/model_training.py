"""
    模型訓練模組，將訓練程式放置於此即可。
"""
from sklearn.ensemble import RandomForestClassifier

def retrain(X_train, y_train):
    """
        
    """
    if not X_train:
        # 快速先串
        return None
    rf_hyper = {
        'n_estimators': 100,
        'max_depth': None,
        'random_state': 222
    }

    rf = RandomForestClassifier(**rf_hyper)
    rf.fit(X_train, y_train)

    return rf


    
    
    
