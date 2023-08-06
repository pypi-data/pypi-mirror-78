# -*- encoding:utf-8 -*-
"""
    数据源实现模块
"""

from ..core import env
from ..core.env import EMarketType
from ..core.storage import context
from .database import BaseMarket
from .datagetting_sdk import get_spot_kline_data, get_future_kline_data, get_spot_depth_data, get_future_depth_data, get_history_kline_data_by_api, get_sync_spot_kline_data,get_sync_forex_kline_data, get_sync_forex_tick_data
from ..model.symbol import Symbol

class CsvKlineApi(BaseMarket):
    """ csv k线数据源，支持现货、期货"""

    def __init__(self, symbol, period):
        super(CsvKlineApi, self).__init__(symbol)
        self.symbol = Symbol(symbol)
        self.period = period

    def get_data(self, start=None, end=None, count = 10000):
        """获取k线数据方法 """
        if self.symbol.is_spot:
            kline_data = get_spot_kline_data(self.symbol.exchange, self.symbol.basesymbol , self.symbol.assetsymbol , self.period, start, end, count)
        else:
            kline_data = get_future_kline_data(self.symbol.exchange, self.symbol.basesymbol , self.symbol.assetsymbol, self.symbol.future_type, self.period, start, end,count)
        return kline_data

class ApiKlineApi(BaseMarket):
    """ Api k线数据源，支持现货"""

    def __init__(self, symbol, period):
        super(ApiKlineApi, self).__init__(symbol)
        self.symbol = Symbol(symbol)
        self.period = period 

    def get_data(self, start=None, end=None, count = 10000):
        """获取k线数据方法 """
        if self.symbol.is_spot:
            kline_data = get_history_kline_data_by_api(context.api_key, context.api_secret, self.symbol.symbol_str, self.period, start, end, count)
        return kline_data

class DbKlineApi(BaseMarket):
    """ 同步数据库 k线数据源，支持现货、期货、外汇"""
    def __init__(self, symbol, period):
        super(DbKlineApi, self).__init__(symbol)
        self.symbol = Symbol(symbol)
        self.period = period

    def get_data(self, start=None, end=None, count = 10000):
        """获取k线数据方法 """
        if env.get_market_type == EMarketType.E_MARKET_TYPE_DigitalCurrency:    
            if self.symbol.is_spot:
                kline_data = get_sync_spot_kline_data(self.symbol.exchange, self.symbol.basesymbol , self.symbol.assetsymbol , self.period, start, end,count)
        elif env.get_market_type == EMarketType.E_MARKET_TYPE_Forex:
            kline_data = get_sync_forex_kline_data(self.symbol.basesymbol , self.symbol.assetsymbol , self.period, start, end, count)
        return kline_data

class CsvDepthApi(BaseMarket):
    """ csv 盘口数据源，支持现货、期货"""

    def __init__(self, symbol):
        super(CsvDepthApi, self).__init__(symbol)
        self.symbol = Symbol(symbol)

    def get_data(self, start=None, end=None, count = 10000):
        """获取盘口数据方法 """
        if env.get_market_type == EMarketType.E_MARKET_TYPE_DigitalCurrency:    
            if self.symbol.is_spot:   # 现货盘口数据
                depth_data = get_spot_depth_data(self.symbol.exchange, self.symbol.basesymbol, self.symbol.assetsymbol, start, end, count )
            else:    # 期货盘口数据
                depth_data = get_future_depth_data(self.symbol.exchange, self.symbol.basesymbol, self.symbol.assetsymbol, self.symbol.future_type, start, end, count)
        return depth_data

class DbTickApi(BaseMarket):
    """ 同步数据库 Tick数据源, 支持外汇数据"""

    def __init__(self, symbol):
        super(DbTickApi, self).__init__(symbol)
        self.symbol = Symbol(symbol)

    def get_data(self, start=None, end=None, count = 10000):
        """获取tick数据方法 """
        tick_data = None
        if env.get_market_type == EMarketType.E_MARKET_TYPE_Forex:
            tick_data = get_sync_forex_tick_data(self.symbol.basesymbol, self.symbol.assetsymbol, start, end, count)
        return tick_data
