# -*- encoding:utf-8 -*-
# """
#     实时数据源模块
# """

import json
import websocket
import _thread as thread
import threading
import traceback
import time

from ..model.data_model import KlineData, TickData, DepthData
from ..helper.loghelper import LogHelper
from ..core.utils import  convert_from_timeStamp, bar_to_second
from ..core.storage import context

class IBDataApi(threading.Thread):
    """ 实时获取"""
    symbols = []    #  格式化后的交易对列表
    symbol_dit = {}    #  交易对与连接websocket的订阅交易对信息的映射
    depth_datas = {}
    kline_datas = {}
    
    high = None    # 当前BAR的最高价
    low = None    #  当前bar的最低价
    close = None  # 当前bar的收盘价
    open = None   # 当前bar的开盘价

    fist_time = None    # 第一个k线数据的时间戳
    first_bar_time = None   # 标识当前数据对应的k线数据的bar时间

    reconnect_count = 0
    is_reconnect = True

    def __init__(self, t_name, e, on_data):
        """
        初始化
        :params symbols: 交易对列表, 格式如下： 基础币种/计价币种.交易所简称
        :params market_type: 市场类型
        :params data_type: 数据类型: kline/depth/tick
        """
        threading.Thread.__init__(self, name=t_name)
        self.symbols = self.convert_symbol(e.symbol_list, e.data_source_type, e.data_type, e.time_type)
        self.data_type = e.data_type
        self.on_data = on_data
        self.e = e
        self._stop_event = threading.Event()

        self.last_kline_data = None   # 上一条k线数据
        self.bar_data = None    # 当前bar的第一条数据
        self.count = 0

        self.ws_address = "ws://" + context.websocketserver.server_url + ":" + context.websocketserver.port

    def on_message(self, message):
        try:
            data, is_ondata = self.convert_to_data(json.loads(message))

            if is_ondata:
                symbol = self.symbols[0].split('@')[0].split(":")[1]
                msg = "weboscket send: " + str(data[symbol][0].get())
                LogHelper.info(msg)
                self.on_data(data, self.e)
        except Exception as ex:
            LogHelper.error(ex)
            traceback.print_exc()

    def on_error(self, error):
        LogHelper.error("on_error: 【" + str(type(error)) + "】 " + str(error))
        if type(error) == ConnectionRefusedError or type(error) == websocket._exceptions.WebSocketConnectionClosedException:
            LogHelper.warn("正在尝试第%d次重连websocket" % self.reconnect_count)
            self.reconnect_count += 1

            while self.is_reconnect:
                time.sleep(0.05)
                self.run()
        else:
            LogHelper.error("websocket出现其他error!")
            traceback.print_exc()

    def on_close(self):
        LogHelper.info("### websocket close ###")

    def on_open(self):
        def run():
            LogHelper.info("###### websocket connect ####")
            if (self.data_type == "depth"):
                for symbol in self.symbols:
                    depth_symbol = symbol.split("@")[0].split(":")[1]
                    self.depth_datas[depth_symbol] = DepthData(depth_symbol, "")
            message = {"Method": "subscribe", "Params": self.symbols}
            self.ws.send(json.dumps(message))
            LogHelper.info("向websocket发送订阅: %s" % (str(message)))
        try:
            thread.start_new_thread(run, ())
        except Exception as ex:
            LogHelper.error("one_open: " + str(ex))
            traceback.print_exc()

    def run(self):
        """
        从IB中获取实时数据
        """
        try:
            LogHelper.info("开始连接websocket")
            LogHelper.info("连接的websocek: " + str(self.ws_address))
            self.ws = websocket.WebSocketApp(self.ws_address,
                                             on_open=self.on_open,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close)
            self.ws.run_forever()
        except Exception as e:
            LogHelper.error("连接IB Api出错")
            traceback.print_exc()

    def stop(self):
        """
        停止从IB中获取实时数据
        """
        LogHelper.info("关闭连接ib的websocket")
        self.is_reconnect = False
        self.ws.close()
        self._stop_event.set()

    def convert_symbol(self, symbols, market_type, data_type, time_type):
        """
        将交易对字符串标准化成如下格式：市场类型:基础币种/计价币种.交易所@数据类型
        :params symbols: 交易对列表,每个交易对格式如下: 基础币种/计价币种.交易所
        :params market_type: 市场类型
        :params data_type: 数据类型,如kline、tick、depth
        :params time_type: 时间精度: 如1m、5m、15m、30m
        :returns result: 返回向ib发送的订阅字符串格式列表，转换后的数据格式如下：市场类型:基础币种/计价币种.交易所@数据类型, 如"Forex:USD/JPY.IDEALPRO@kline_1m", "Forex:USD/JPY.IDEALPRO@ticker", "Forex:USD/JPY.IDEALPRO@depth"
        """
        result = []

        for symbol in symbols:
            arg = market_type + ":" + symbol

            if data_type == "kline":
                arg = arg + "@kline_" + time_type
            elif data_type == "tick":
                arg = arg + "@ticker"
            elif data_type == "depth":
                arg = arg + "@depth"
            result.append(arg)
            self.symbol_dit[arg] = symbol

        return result

    def convert_to_data(self, message):
        """
        将返回的实时数据转换成对应的k线、盘口、tick数据类型
        :params message: 从IB中获取的实时数据字符串
        :return result: 转换后的数据，返回实时获取数据的
        :return is_ondata: 是否将该数据传给on_data，执行回测逻辑
        """
        result = {}
        is_ondata = True

        if (self.data_type == "kline"):
            symbol = message["Symbol"].split(":")[1]
            bar_time = convert_from_timeStamp(message["Time"])  # 将13位时间戳转换成时间 
            kline_data = KlineData(symbol, bar_time, message["Open"], message["High"], message["Low"], message["Close"])
            kline_data = self.send_last_data(kline_data)

            if kline_data is None:
                is_ondata = False
            else:
                result ={symbol: [kline_data]}
        elif (self.data_type == "tick"):
            symbol = message["Symbol"].split(":")[1]
            result = {symbol: [
                TickData(symbol = symbol, bar_time=convert_from_timeStamp(message["Time"]),  bid_size=message["BidSize"], ask_size=message["AskSize"],
                          bid_price=message["BidPrice"], ask_price=message["AskPrice"])]}
        elif (self.data_type == "depth"):
            operation = message["Operation"]
            symbol = message["Symbol"].split(":")[1]
            position = message["Position"]
            size = message["Size"]
            price = message["Price"]

            if message["Side"] == 0:
                if operation == 0:
                    self.depth_datas[symbol].asks_price_list.append(price)
                    self.depth_datas[symbol].asks_quantity_list.append(size)
                    is_ondata = False
                elif operation == 1:
                    self.depth_datas[symbol].asks_price_list[position] = price
                    self.depth_datas[symbol].asks_quantity_list[position] = size
                else:
                    self.depth_datas[symbol].asks_price_list[position] = 0
                    self.depth_datas[symbol].asks_quantity_list[position] = 0
            else:
                if operation == 0:
                    self.depth_datas[symbol].bids_price_list.append(price)
                    self.depth_datas[symbol].bids_quantity_list.append(size)
                    is_ondata = False
                elif operation == 1:
                    self.depth_datas[symbol].bids_price_list[position] = price
                    self.depth_datas[symbol].bids_quantity_list[position] = size
                else:
                    self.depth_datas[symbol].bids_price_list[position] = 0
                    self.depth_datas[symbol].bids_quantity_list[position] = 0

            self.depth_datas[symbol].bar_time = convert_from_timeStamp(message["Time"])

            if is_ondata:
                result = {symbol: [self.depth_datas[symbol]]}

        return result, is_ondata

    def send_last_data(self, data):
        send_data = self.last_kline_data

        if send_data:
            if data.bar_time != send_data.bar_time:
                send_data.is_last = True
            else:
                send_data.is_last = False
        self.last_kline_data = data

        return  send_data
    