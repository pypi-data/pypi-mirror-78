# -*- encoding:utf-8 -*-
"""
    策略引擎模块：策略回测入口
"""

import random
import string
import datetime
from datetime import datetime
import json
import threading
from queue import Queue
import traceback

from . import env
from .consumer import DataConsumer, LogConsummer,OrderConsummer
from .producer import LogProduce, OrderProduce
from .env import EDataSourceType, EMarketType, EModeType
from ..market.dataproducer import DataProducer
from .storage import context
from .utils import complete_datetime
from ..model.order import Order
from ..helper.loghelper import LogHelper
from ..helper.mysqlhelper import MySqLHelper
from ..trade.manager import tradeengine
from ..trade.ibmanager import ibtradeengine
from ..market.datagetting_sdk import get_download_path
from .producer import order_queue, log_queue
from ..market.live_dataproducer import IBDataApi
from ..market.lamx_dataproducer import LamxDataApi
from ..dbconn.db_config import config

# IB策略引擎
class SAMTraderEngine(object):
    def __init__(self,userid,strategyid,symbol_list,time_type,cash,
                fill_bar_type,running_type,account_type, data_type, data_source_type, mode, get_data_way = "", \
                    starttime = "",endtime = "",api_key = '', api_secret = '', open_percent = 1, leverage_multiple = 1, \
                    paper_id = "", mysql_conn = None, pg_conn = None, websocket_conn = None, order_conn = None, is_reverse_operate = False):
        """
        策略引擎创建
        :params userid: 用户id，str
        :params strategyid: 策略id， str
        :params symbol_list: 交易对列表（每个交易对用“，”拼接）， str
        :params time_type: 时间精度, str，其值可为"1m", "5m","30m","1h"...
        :params cash: 初始资金, float
        :params starttime: 回测开始时间, str
        :params endtime：回测结束时间, str
        :params fill_bar_type: 订单成交方式（1：当前bar价格成交，2：下一bar的价格成交）, int
        :params running_type: 执行模式（0：手动模式，返回数据库地址；1：自动模式，自动拉取行情数据）, int
        :params account_type: 账户类型（USD：美元,CNY:人民币）, int
        :params data_type: 数据类型(kline(k线)、depth(盘口)、tick(tick)), str
        :params data_source_type: 市场类型（Forex（外汇）、DigitalCurrency（数字货币））,str
        :params get_data_way: 获取数据方式（1（本地csv）、2（api）、3（同步数据库））, 4(自定义数据源), str
        :params api_key: api_key, str, 默认为空
        :params api_secret：api_secret, str ,默认为空
        :params open_percent:开仓比率,即用于开仓的资金占用本金的比率，float,默认为1，即全部本金进行开仓
        :params leverage_multiple:杠杆倍数, float， 默认为1，使用1杯杠杆
        :params mode: 策略加载模式, int, backtest(MODE_BACKTEST，回测模式)、live(MODE_LIVE，实时模式)
        :params mysql_conn: 终端数据库信息,dict，其中包含url(数据库ip)、port（数据库端口号）、username（用户名）、pwd（密码）
        :params pg_conn: 同步数据库信息,dict，其中包含url(数据库ip)、port（数据库端口号）、username（用户名）、pwd（密码）
        :params websocket_conn: IB实时数据连接信息,dict，其中包含url(websoocket的ip)、port（数据库端口号）
        :params paper_id: 仿真交易id,str
        :params order_conn: 仿真交易ID, dict
        :params lamx_websocket_conn: Lamx平台的实时数据连接信息,dict，其中包含url(websoocket的ip)、port（数据库端口号）
        :params is_reverse_operate: 平仓时是否支持反向开仓， bool, True:平仓时没有足够的仓位，则反向开仓, False：不支持反向开仓 
        :return:
        """
        self.userid = userid
        self.strategyid = strategyid 
        self.symbol_list = symbol_list.split(',')    # 每个交易对数据 BTC/USDT.OK
        self.time_type = time_type 
        self.cash = cash
        self.fill_bar_type = fill_bar_type 
        self.running_type = running_type 
        self.account_type = account_type
        self.data_type = data_type
        self.data_source_type = data_source_type
        self.get_data_way = get_data_way
        self.api_key = api_key
        self.api_secret = api_secret
        self.open_percent = open_percent
        self.leverage_multiple = leverage_multiple
        self.mode = EModeType(mode)
        self.mysql_conn = mysql_conn
        self.pg_conn = pg_conn
        self.websocket_conn = websocket_conn
        self.order_conn = order_conn
        env.get_mode = EModeType(mode)
        context.data_source_type = data_source_type
        context.is_reverse_operate = is_reverse_operate
        self.context = self.initial(context, mysql_conn, pg_conn, websocket_conn, order_conn, data_source_type)

        if (self.mode == EModeType.BACKTEST):
            self.starttime = complete_datetime(starttime)
            self.endtime = complete_datetime(endtime)
        else:
            self.starttime = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            self.endtime = None
            context.paperid = paper_id


    def initial(self, context, mysql_conn, pg_conn, websocket_conn, order_conn, data_source_type):
        """
        引擎初始化
        :params context: 全局上下文实例，Context对象
        :return context: 全局上下文实例 
        """
        context.cash = self.cash            # 初始资金
        context.total_cash = self.cash   # 总资产
        context.capital = self.cash   # 本金
        context.strategyid = self.strategyid    # 策略id
        context.open_percent = self.open_percent    #  开仓比率
        context.leverage_multiple = self.leverage_multiple    #  杠杆倍数
        context.period = self.time_type
        context.da = data_source_type
        context.mysql_conn = mysql_conn
        context.pg_conn = pg_conn
        context.websocket_conn = websocket_conn
        context.order_conn = order_conn
        context.set_conn()
        config.set_sql_conn()

        if (self.mode == EModeType.BACKTEST):
            env.get_public_data_source = EDataSourceType(int(self.get_data_way))
            env.get_market_type = EMarketType(self.data_source_type)
        else:
            ibtradeengine.set_order_conn()

        return context
    
    def run(self):
        if env.get_mode == EModeType.BACKTEST:
            self.__create_back_test()
        else:
            self.__create_paper_trade()

    def place_order(self,  symbol, direction, order_time, quantity, open_or_close, order_type, fillprice=0, limit_price=0, order_id= None):
        """
        下单。当策略模式为实时模式时，则在IB中进行仿真交易；策略模式为回测模式时，则仍使用自定义的交易系统进行交易
        :params symbol: 品种名, str
        :params direction: 方向("Buy":多，"Sell":空), str
        :params order_time: 下单时间, str
        :params quantity: 数量, int
        :params open_or_close：开仓("Open")/平仓("Close"), str
        :params order_type: 订单类型、0:市价单，1：限价单， int
        :params fillprice: 成交价, float
        :params limitprice: 限价，float
        :return 
        """
        status = ""
        result = None
        order = Order(symbol, direction, order_time, quantity, open_or_close, order_type, fillprice, limit_price)
        order.order_id = order_id

        if self.mode == EModeType.LIVE:
            iborderid = ""
            try:
                status, result, iborderid = ibtradeengine.fit_order(order)
            except Exception as ex:
                print("创建订单时，出错")
                print(ex)
                traceback.print_exc()
            return status, result, iborderid
        else:
            tradeengine.fit_order(order)
        return status, result
    
    def place_order_percent_capital(self,  symbol, direction, order_time, open_or_close, order_type, fillprice, limit_price=0):
        """
        根据本金指定比例决定开仓量
        :params symbol: 品种名, str
        :params direction: 方向("Buy":多，"Sell":空), str
        :params order_time: 下单时间, str
        :params quantity: 数量, int
        :params open_or_close：开仓("Open")/平仓("Close"), str
        :params fillprice: 成交价, float
        :params limitprice: 限价，float
        :params quantity: 数量，float
        :return 
        """
        order = Order(symbol, direction, order_time, 0, open_or_close, order_type, fillprice, limit_price)
        tradeengine.fit_order_by_leverage(order, self.time_type, context.open_percent, context.leverage_multiple, True)  

    def place_order_percent_cash(self,  symbol, direction, order_time, open_or_close, order_type, fillprice,limit_price=0):
        """
        根据可用资金指定比例决定开仓量
        :params symbol: 品种名, str
        :params direction: 方向("Buy":多，"Sell":空), str
        :params order_time: 下单时间, str
        :params quantity: 数量, int
        :params open_or_close：开仓("Open")/平仓("Close"), str
        :params fillprice: 成交价, float
        :params limitprice: 限价，float
        :params quantity: 数量，float
        :return 
        """
        order = Order(symbol, direction, order_time, 0, open_or_close, order_type, fillprice, limit_price)
        tradeengine.fit_order_by_leverage(order, self.time_type, context.open_percent, context.leverage_multiple, False)

    def get_account(self,):
        """
        获取账户信息, 包含可用资金
        """
        return context.cash

    def get_holdings(self,):
        """
        获取持仓信息
        :return context.holdings: 返回持仓信息，ditc，其中key：品种名，value：仓位信息,dict(key：仓位方向:Buy/Sell,value: 仓位信息, Holding对象)
        """
        return context.holdings
    
    def get_orders(self,):
        """
        获取当前回测的所有订单
        :return result: 所有订单信息, list[StrategyOrder]
        """
        if env.get_mode == EModeType.BACKTEST:
            sql = "select * from strategyorder where JobId = " + context.backtestid
            result = MySqLHelper().selectall(sql)
            return result
        else:
            sql = "select * from paperorder where JobId = " + context.backtestid
            result = MySqLHelper().selectall(sql)
            return result

    def get_order_status(self,order_id):
        if self.mode == EModeType.LIVE:
            result = ibtradeengine.get_order_status(order_id)
        else:
            sql = "select * from strategyorder where OrderId = " + order_id
            result = MySqLHelper().selectone(sql)

        return result

    def get_local_csvpath(self,):
        """
        获取数据文件路径
        :return data_path: 本地csv存放路径, str
        """
        data_path = get_download_path()
        return data_path

    def client_close(self,):
        """
        结束回测
        """
        LogHelper.info("##### client_close ####")
        try:
            if env.get_mode == EModeType.LIVE:
                sql = "update papertrade set UpdatedAt = \'{0}\' ,status = \'{1}\', EndTime = \'{2}\' where Id = \'{3}\'".format(datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S"), "end", datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S"),  context.paperid)
                MySqLHelper().update(sql)
            else:
                sql = "update backtest set UpdatedAt = \'{0}\' ,status = \'{1}\' where Id = \'{2}\'".format(datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S"), "end", context.backtestid)
                MySqLHelper().update(sql)

            LogHelper.info("finish!!!")
            p1 = threading.Thread(target=LogProduce,  name="结束日志线程", args=('finish',))
            p1.start()
            p2 = threading.Thread(target=OrderProduce,  name="结束订单线程", args=('finish',))
            p2.start()
        except Exception as ex:
            LogHelper.error("client_close出现异常: " + str(ex))
            traceback.print_exc()
    
    def __create_back_test(self):
        """
        创建回测
        """
        try:
            LogHelper.info("#### 更新回测交易信息 ####")
            back_test_id = self.__get_backtest_id()
            context.backtestid = back_test_id
            now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

            sql = "insert into backtest(`Id`, `StrategyId`, `CreatedAt`, `UpdatedAt`,`BacktestTime`, `StartTime`, `EndTime`, `Amount`, `Status`, `CumPnlRatio`, `MaxDrawdown`, `SharpRatio`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            value = (back_test_id, self.strategyid, now_time, now_time, now_time, self.starttime, self.endtime,
                     self.cash, "start", 0, 0.0, 0.0)
            MySqLHelper().insertone(sql, value)

            # 更新回测次数
            sql = "update strategy set BacktestNum = BacktestNum + 1 , UpdatedAt = \'{0}\' where UserId = \'{1}\' and Id = \'{2}\'".format(
                datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f"), self.userid, self.strategyid)
            MySqLHelper().update(sql)

            # 添加回测参数信息
            params = {"symbol": self.symbol_list, "time_type": self.time_type, "data_type": self.data_type,
                      "get_data_way": self.get_data_way, "starttime": self.starttime,
                      "endtime": self.endtime, "account_type": self.account_type, "execution": self.fill_bar_type,
                      "running_type": self.running_type, "data_source_type": self.data_source_type,
                      "open_percent": self.open_percent, "leverage_multiple": self.leverage_multiple,
                      "mode": self.mode.value}
            data = json.dumps(params)

            now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            sql = "insert into backtestinfo(`BacktestId`, `BacktestParam`,`CreatedAt`, `UpdatedAt`) values (%s, %s, %s, %s)"
            value = (back_test_id, data, now_time, now_time)
            MySqLHelper().insertone(sql, value)

            msg = 'start backtest, backtestid为: ' + back_test_id
            LogHelper.info(msg)
        except Exception as ex:
            LogHelper.error("创建回测失败: " + ex)
            traceback.print_exc()

    def __create_paper_trade(self):
        """
        创建仿真交易
        """
        try:
            LogHelper.info("#### 更新仿真交易信息 ####")
            now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

            # 更新仿真交易信息
            """
            sql = "update papertrade set TradeTime = \'{0}\' ,StartTime = \'{1}\', Amount = \'{2}\', Status = \'{3}\', CumPnlRatio = \'{4}\', MaxDrawdown =\'{5}\', SharpRatio = \'{6}\', UpdatedAt = \'{7}\' where Id = \'{8}\'".format(
                now_time, self.starttime, self.cash, "start", 0,0,0, now_time, context.paperid)
            """
            sql = "update papertrade set StartTime = \'{0}\', Amount = {1},Status = \'{2}\', CumPnlRatio = {3}, MaxDrawdown ={4}, SharpRatio = {5},UpdatedAt = \'{6}\'  where Id = \'{7}\'".format(self.starttime, self.cash,"start", 0,0,0,now_time, context.paperid)
            MySqLHelper().update(sql)

            # 添加仿真交易参数信息
            params = {"symbol": self.symbol_list, "time_type": self.time_type, "data_type": self.data_type,
                      "get_data_way": self.get_data_way, "starttime": self.starttime,
                      "endtime": self.endtime, "account_type": self.account_type,
                      "execution": self.fill_bar_type,
                      "running_type": self.running_type, "data_source_type": self.data_source_type,
                      "open_percent": self.open_percent, "leverage_multiple": self.leverage_multiple,
                      "mode": self.mode.value}
            data = json.dumps(params)

            now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            sql = "insert into paperinfo(`PaperId`, `PaperParam`,`CreatedAt`, `UpdatedAt`) values (%s, %s, %s, %s)"
            value = (context.paperid, data, now_time, now_time)
            MySqLHelper().insertone(sql, value)

            msg = 'start paper trade, paperid为: ' + context.paperid
            LogHelper.info(msg)
        except Exception as ex:
            LogHelper.error("创建仿真交易失败: " + str(ex))
            traceback.print_exc()
    
    def __get_backtest_id(self):
        """
        生成唯一的回测id
        :return value:回测id
        """
        value = "BT" + datetime.strftime(datetime.utcnow(), "%Y%m%d") + ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return value

    def __get_paper_id(self):
        """
        生成唯一的仿真交易id
        :return value:仿真交易id
        """
        value = "PT" + datetime.strftime(datetime.utcnow(), "%Y%m%d") + ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return value

class SAMTrader(object):
    """
        入口函数
    """
    __instance = None

    def __init__(self, initial, on_data):
        """
        初始化
        :params initial: 初始化策略引擎, func
        :param on_data：推数据，实现策略逻辑, func
        :return 
        """
        self.initial = initial
        self.on_data = on_data
        self.e = self.initial()
        self.livedataapi = None

        if self.e.mode == EModeType.BACKTEST:
            self.data_queue = Queue()
            self.data_producer = DataProducer("数据生产者", self.e.symbol_list[0], self.e.time_type, self.e.starttime, self.e.endtime,
                                            self.e.data_type, self.data_queue)
            self.data_consumer = DataConsumer("数据消费者", self.data_queue, self.e, self.on_data)
        else:
            if EDataSourceType(int(self.e.get_data_way)) == EDataSourceType.E_DATA_SOURCE_LIVE_IB:
                self.livedataapi = IBDataApi("数据生产者", self.e, on_data)
            elif EDataSourceType(int(self.e.get_data_way)) == EDataSourceType.E_DATA_SOURCE_LIVE_LAMX:
                self.livedataapi = LamxDataApi("数据生产者", self.e, on_data)

        self.order_consumer = OrderConsummer("订单消费者", order_queue)
        self.log_consumer = LogConsummer("日志消费者", log_queue)
        context.trader = self.__instance

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance
   
    def start(self):
        """
        开始进行回测
        """
        try:
            if self.e.running_type == 1:
                if self.e.mode  == EModeType.BACKTEST:
                    self.e.run()
                    self.data_producer.start()
                    self.data_consumer.start()
                    self.order_consumer.start()
                    self.log_consumer.start()

                    self.data_producer.join()
                    self.data_consumer.join()
                else:
                    self.order_consumer.start()
                    self.log_consumer.start()
                    self.e.run()
                    self.livedataapi.start()
                    self.livedataapi.join()
            elif self.e.running_type == 0:
                return self.e.get_local_csvpath()
        except BaseException as ex:
            print(ex)
            traceback.print_exc()
        finally:
            if (self.e.mode == EModeType.LIVE):
                self.livedataapi.stop()   # 取消实时数据订阅
            self.stop()

    def stop(self):
        """
        回测结束
        """
        if self.e.mode == EModeType.BACKTEST:
            if self.data_consumer.is_alive():
                self.data_consumer.stop()
            if self.data_producer.is_alive():
                self.data_producer.stop()
        else:
            if self.livedataapi.is_alive():
                self.livedataapi.stop()

            # 查看未在数据库中保存的订单状态是否有变化，如果有，则相应的往数据库中
            if len(ibtradeengine.order_id_dict.keys()) != 0:
                for item in ibtradeengine.order_id_dict.keys():
                    order = ibtradeengine.get_order_status(item)
                    ibtradeengine.create_order(order)

        self.e.client_close()