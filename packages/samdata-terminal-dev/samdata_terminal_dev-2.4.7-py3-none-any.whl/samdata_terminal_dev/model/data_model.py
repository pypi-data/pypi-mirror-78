# -*- encoding:utf-8 -*-
"""
    各种数据类
"""

class KlineData(object):
    """
        k线数据
    """
    def __init__(self, symbol, bar_time, open, high, low, close, quote_volume=0, quoteasset_volume=0,trade_num='0', is_last = True):
        """
        初始化
        :params symbol: 交易对, str
        :params bar_time: 时间, str
        :params open: 开盘价, float
        :params high: 最高价, float
        :params low: 最低价, float
        :params close: 收盘价, float
        :params quote_volume: 
        :params quoteasset_volume:
        :params trade_num: 交易笔数
        :params is_last: 是否为当前bar的最后一条数据
        """
        self.symbol = symbol
        self.bar_time = bar_time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.quote_volume = quote_volume
        self.quoteasset_volume  = quoteasset_volume
        self.trade_num = trade_num
        self.is_last = is_last    # 标记该类型数据是否为当前bar的最后一条数据
    
    def __eq__(self,other):
        return self.__dict__ == other.__dict__

    def get(self):
        data = {}
        data["symbol"] = self.symbol
        data["bar_time"]= self.bar_time
        data["open"] = self.open
        data["high"] = self.high
        data["low"] = self.low
        data["close"] = self.close
        data["is_last"] = self.is_last
        return data

class DepthData(object):
    """
        盘口数据
    """
    def __init__(self, symbol, bar_time):
        """
        初始化
        :params symbol: 交易对, str
        :params bar_time: 时间, str
        """
        self.symbol = symbol
        self.bar_time = bar_time
        self.bids_price_list = []
        self.bids_quantity_list = []
        self.asks_price_list = []
        self.asks_quantity_list = []
    
    def __eq__(self,other):
        return self.__dict__ == other.__dict__

    def get(self):
        data = {}
        data["symbol"] = self.symbol
        data["bar_time"]= self.bar_time
        data["bids_price_list"] = self.bids_price_list
        data["bids_quantity_list"] = self.bids_quantity_list
        data["asks_price_list"] = self.asks_price_list
        data["asks_quantity_list"] = self.asks_quantity_list
        return data

class TickData(object):
    """
        tick 数据
    """
    def __init__(self, symbol, bar_time, bid_price, ask_price, bid_size = 0, ask_size = 0):
        """
        初始化
        :params symbol: 交易对, str
        :params bar_time: 时间, str
        :params bid_price: 买价, float
        :params ask_price: 卖价, float
        :params bid_size: 买量, float
        :params ask_size: 卖量, float
        """
        self.symbol = symbol
        self.bar_time = bar_time
        self.bid_price = bid_price
        self.ask_price = ask_price
        self.bid_size = bid_size
        self.ask_size = ask_size

    def __eq__(self,other):
        return self.__dict__ == other.__dict__

    def get(self):
        data = {}
        data["symbol"] = self.symbol
        data["bar_time"] = self.bar_time
        data["bid_price"] = self.bid_price
        data["ask_price"] = self.ask_price
        data["bid_size"] = self.bid_size
        data["ask_size"] = self.ask_size
        return data        