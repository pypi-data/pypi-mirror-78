# -*- encoding:utf-8 -*-
"""
    各种交易对类
"""

class Symbol(object):
    """交易对"""
    def __init__(self,symbol):
        self.symbol_str = symbol
        self.exchange = ""
        self.basesymbol = ""
        self.assetsymbol = ""
        self.source = None
        self.symbol = symbol
        self.is_spot = False
        symbol_array = symbol.split(".")
        
        if len(symbol_array) == 1:  # 外汇交易对: BTC/USDT
            self.basesymbol = symbol_array[0].split('/')[0]
            self.assetsymbol = symbol_array[0].split('/')[1]
        elif len(symbol_array) == 2:    # 现货交易对: BTC/USDT.BN
            self.exchange = symbol_array[1]
            self.basesymbol = symbol_array[0].split('/')[0]
            self.assetsymbol = symbol_array[0].split('/')[1]
            self.is_spot = True
        elif len(symbol_array) == 3:    # 期货交易对： BTC/USDT.BN.Q
            self.exchange = symbol_array[1]
            self.basesymbol = symbol_array[0].split('/')[0]
            self.assetsymbol = symbol_array[0].split('/')[1]
            self.future_type = symbol_array[2]
            self.is_spot = False

class SymbolModel(object):
    '''
        现货交易对
    '''
    def __init__(self, symbol, baseasset, quoteasset, symboltype,subsymboltype, status, \
        displaysymbol, tradesymbol, exchange, listedtime, delistedtime):
        self.symbol = symbol
        self.baseasset = baseasset
        self.quoteasset = quoteasset
        self.type = SymbolTypeModel(symboltype, subsymboltype)
        self.status = status
        self.tradesymbol = tradesymbol
        self.exchange = exchange
        self.listedtime = listedtime
        self.delistedtime = delistedtime

class FutureModel(object):
    '''
        期货交易对
    '''
    def __init__(self, symbol, baseasset, quoteasset, contractmultiple, contractmonth, \
        listedtime, deliverydate, deliverymonth, deliveryprice, minprice, symboltype,subsymboltype, \
            status, displaysymbol, tradesymbol, exchange,latestcontract):
        self.symbol = symbol
        self.baseasset = baseasset
        self.quoteasset = quoteasset
        self.contractmultiple = contractmultiple
        self.contractmonth = contractmonth
        self.delistedtime = listedtime
        self.deliverydate = deliverydate
        self.deliverymonth = deliverymonth
        self.deliveryprice = deliveryprice
        self.minprice = minprice
        self.type = SymbolTypeModel(symboltype, subsymboltype)
        self.status = status
        self.tradesymbol = tradesymbol
        self.exchange = exchange
        self.listedtime = listedtime
        self.latestcontract = latestcontract    

class IndexModel(object):
    '''
        指数交易对
    '''
    def __init__(self, symbol, baseasset, quoteasset, symboltype, subsymboltype, status, displaysymbol, \
        tradesymbol, exchange, listedtime, delistedtime):
        self.symbol = symbol
        self.baseasset = baseasset
        self.quoteasset = quoteasset
        self.type = SymbolTypeModel(symboltype, subsymboltype)
        self.status = status
        self.displaysymbol = displaysymbol
        self.tradesymbol = tradesymbol
        self.exchange = exchange
        self.listedtime = listedtime
        self.delistedtime = delistedtime

class SymbolTypeModel(object):
    '''
        交易对类型
    '''
    def __init__(self,symboltype, subsymboltype):
        self.symboltype = symboltype
        self.subsymboltype = subsymboltype