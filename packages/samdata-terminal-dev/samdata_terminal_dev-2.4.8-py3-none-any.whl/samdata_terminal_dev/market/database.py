# -*- encoding:utf-8 -*-
"""
    数据源基础模块
"""

from abc import abstractmethod

class BaseMarket(object):
    """ 数据源基础市场类 """
    def __init__(self,symbol): 
        """
        初始化
        :params symbol: Symbol对象
        """
        pass 
    
    @abstractmethod
    def get_data(self, start = None, end = None, count = 5000):
        pass