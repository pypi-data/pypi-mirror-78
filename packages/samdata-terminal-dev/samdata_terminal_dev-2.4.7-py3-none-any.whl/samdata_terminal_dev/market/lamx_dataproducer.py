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

class LamxDataApi(threading.Thread):
    """ 实时获取"""
    symbols = []    #  格式化后的交易对列表
    symbol_dit = {}    #  交易对与连接websocket的订阅交易对信息的映射

    reconnect_count = 0
    is_reconnect = True

    def __init__(self, t_name, e, on_data):
        """
        初始化
        :params t_name: 线程名
        :params e: 策略引擎
        :params on_data:回调函数
        """
        threading.Thread.__init__(self, name=t_name)
        self.symbols = e.symbol_list
        self.data_type = e.data_type   # 数据类型
        self.time_type = e.time_type   # 时间精度
        self.on_data = on_data
        self.e = e
        self._stop_event = threading.Event()

        self.last_kline_data = None   # 上一条k线数据
        self.bar_data = None    # 当前bar的第一条数据
        self.count = 0

        self.ws_address = "ws://" + context.websocketserver.server_url + ": " + context.websocketserver.port

    def on_message(self, message):
        try:
            data, is_send = self.convert_to_data(json.loads(message))

            if is_send:
                msg = "weboscket send: " + str(data[self.e.symbol_list[0]][0].get())
                LogHelper.info(msg)
                self.on_data(data, self.e)
        except Exception as ex:
            LogHelper.error(ex)
            traceback.print_exc()

    def on_error(self, error):
        LogHelper.error(error)
        if type(error) == ConnectionRefusedError or type(error) == websocket._exceptions.WebSocketConnectionClosedException:
            LogHelper.warn("正在尝试第%d次重连websocket" % self.reconnect_count)
            self.reconnect_count += 1

            while self.is_reconnect:
                time.sleep(0.05)
                self.run()
        else:
            LogHelper.error("其他error!")
            LogHelper.error(error)

    def on_close(self):
        LogHelper.info("### websocket close ###")

    def on_open(self):
        def run():
            params = []
            if (self.data_type == "kline"):
                for symbol in self.symbols:
                    param = symbol + "@kline_" + self.time_type
                    params.append(param)
            elif (self.data_type == "tick"):
                for symbol in self.symbols:
                    param = symbol + "@ticker"
                    params.append(param)
            message = {"Method": "subscribe", "Params": params}
            self.ws.send(json.dumps(message))
            LogHelper.info("向websocket发送订阅: %s" % (str(message)))
        thread.start_new_thread(run, ())

    def run(self):
        """
        从lamx中获取实时数据
        """
        try:
            LogHelper.info("开始连接websocket")
            self.ws = websocket.WebSocketApp(self.ws_address,
                                             on_open=self.on_open,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close)
            self.ws.run_forever()
        except Exception as ex:
            LogHelper.error("连接Lamx Api出错")
            traceback.print_exc()

    def stop(self):
        self.is_reconnect = False
        self.ws.close()
        self._stop_event.set()

    def convert_to_data(self, message):
        """
        将返回的实时数据转换成对应的k线、tick数据类型
        :params message: 从IB中获取的实时数据字符串
        :return result: 转换后的数据，返回实时获取数据的
        """
        result = {}
        is_send = True
        data_type = message["Type"]

        if (data_type == "kline"):
            symbol = message["Symbol"]
            bar_time = convert_from_timeStamp(message["Time"])  # 将13位时间戳转换成时间 
            kline_data = KlineData(symbol, bar_time, message["Open"], message["High"], message["Low"], message["Close"])
            kline_data = self.send_last_data(kline_data)

            if kline_data is None:
                is_send = False
            else:
                result ={symbol: [kline_data]}
        elif (data_type == "ticker"):
            symbol = message["Symbol"]
            result = {symbol: [
                TickData(symbol = symbol, bar_time=convert_from_timeStamp(message["Time"]),  bid_size=message["BidSize"], ask_size=message["AskSize"],
                          bid_price=message["BidPrice"], ask_price=message["AskPrice"])]}
        else:
            pass
        return result, is_send

    def send_last_data(self, data):
        send_data = self.last_kline_data

        if send_data:
            if data.bar_time != send_data.bar_time:
                send_data.is_last = True
            else:
                send_data.is_last = False
        self.last_kline_data = data

        return  send_data
