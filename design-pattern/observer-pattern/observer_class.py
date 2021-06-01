"""
    Observer design patter.
    在物件間定義一種一對多的依賴關係，當這個物件狀態發生改變時，所有依賴物件都會被通知並自動更新。
    常用於: 訊息推送。
"""

from abc import ABCMeta, abstractmethod
# ABCMeta: 用以定義抽象類別, abstractmethod: 用以定義抽象方法

class Observer(metaclass=ABCMeta):
    """ 
        定義:
            觀察者 的 base class，為一個抽象類別。
            至少需要override update 方法，也就是通知、更新的具體實作。
    """
    @abstractmethod
    def update(self, observable, object):
        pass


class Observable:
    """
        定義:
            被觀察者的 base class，為一個類別。
            基礎地定義需要有加入觀察者、去除觀察者、通知觀察者
    """
    def __init__(self):
        self._observers = []
    
    def addObserver(self, observer):
        self._observers.append(observer)
    
    def removeObserver(self, observer):
        self._observers.remove(observer)
    
    def notifyObserver(self, object=0):
        for o in self._observers:
            o.update(self, object)
        