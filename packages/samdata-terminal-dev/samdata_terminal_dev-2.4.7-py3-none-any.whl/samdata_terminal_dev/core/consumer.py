import threading
import time
from datetime import datetime
from dateutil.parser import parse as dateparser
from dateutil.relativedelta import relativedelta
import traceback

from .utils import bar_to_second
from .storage import context
from ..helper.mysqlhelper import MySqLHelper
from ..helper.loghelper import LogHelper
from .env import EModeType
from . import env

class LogConsummer(threading.Thread):
    """日志消费者"""
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        if env.get_mode == EModeType.LIVE:
            write_count = 1
        else:
            write_count = 5000

        try:
            is_end = False
            while not is_end:
                if not self.data.empty():
                    log_list = []
                    while len(log_list) < write_count:
                        d = self.data.get()
                        if d != "finish":
                            log_list.append(d)
                        else:
                            is_end = True
                            break

                    if env.get_mode == EModeType.BACKTEST:
                        sql = "insert into logs(`BacktestId`, `Log`, `Level`, `CreatedAt`, `UpdatedAt`) values (%s, %s, %s, %s, %s)"
                    else:
                        sql = "insert into paperlogs(`PaperId`, `Log`, `Level`, `CreatedAt`, `UpdatedAt`) values (%s, %s, %s, %s, %s)"
                    db = MySqLHelper()
                    print(sql)
                    print("往数据库中插入日志,数量: " + str(len(log_list)))
                    db.insertmany(sql, log_list)
                else:
                    time.sleep(0.02)
        except BaseException as e:
            print("日志，出错： ")
            print(e)
            traceback.print_exc()

class OrderConsummer(threading.Thread):
    """订单消费者"""
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        try:
            if env.get_mode == EModeType.LIVE:
                write_count = 1
            else:
                write_count = 200

            is_end = False
            global order_time

            while not is_end:
                if not self.data.empty():
                    data_list = []
                    while len(data_list) < write_count:
                        d = self.data.get()
                        if d != "finish":
                            data_list.append(d)
                        else:
                            is_end = True
                            break

                    if env.get_mode == EModeType.BACKTEST:
                        sql = "insert into strategyorder (`StrategyId`, `Symbol`, `OrderType`, `OrderTime`, `FillTime`, `OperateTime`, `Quantity`, `Offset`, `OrderId`, `FillPrice`, `Direction`, `JobId`, `Status`, `Nav`, `Cach` , `CloseProfit`, `CloseProfitRatio`," + \
                              "`OrderFee`, `CreatedAt`, `UpdatedAt`, `PositionId`, `OrderResult`,`LimitPrice`) values (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s)"
                    else:
                        sql = "insert into paperorder (`StrategyId`, `Symbol`, `OrderType`, `OrderTime`, `FillTime`, `OperateTime`, `Quantity`, `Offset`, `OrderId`, `FillPrice`, `Direction`, `PaperId`, `Status`, `Nav`, `Cach` , `CloseProfit`, `CloseProfitRatio`," + \
                              "`OrderFee`, `CreatedAt`, `UpdatedAt`, `PositionId`, `OrderResult`,`LimitPrice`) values (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s)"
                    db = MySqLHelper()
                    print(sql)
                    print("往数据库中插入订单数据,数量： " + str(len(data_list)))
                    db.insertmany(sql, data_list)
                else:
                    time.sleep(0.02)
        except BaseException as ex:
            print("订单消费者，出错： ")
            print(ex)
            traceback.print_exc()

class DataConsumer(threading.Thread):
    """数据消费者"""
    def __init__(self, t_name, queue, e, on_data):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue
        self.on_data = on_data
        self.e = e
        self.count = 0
        self.next_time = dateparser(e.starttime)
        self.temp_data = None
        self._stop_event = threading.Event()

    def run(self):
        try:
            if self.e.data_type == "kline":
                self.consume_kline_data()
            else:
                self.consume_other_data()
        except BaseException as e:
            print("数据消费者： 数据处理出错")
            print(e)
            traceback.print_exc()

    def stop(self):
        self._stop_event.set()

    def consume_kline_data(self):
        """消费k线数据"""
        current_time = dateparser(self.e.starttime)
        next_time = current_time + relativedelta(seconds = bar_to_second(context.period))
        temp_data = None    # 存放未遍历到的bar数据
        is_end = False
        is_get_data = True

        while not is_end and next_time <= dateparser(self.e.endtime) and not self._stop_event.is_set():
            if not self.data.empty():
                if is_get_data:
                    temp_data = self.data.get()

                if temp_data != "finish":
                    bar_time = temp_data[self.e.symbol_list[0]][0].bar_time
                    self.count = self.count + 1
                    if dateparser(bar_time) >= current_time and dateparser(bar_time) < next_time:
                        msg = '处理第' + str(self.count) + '根数据, 时间为 ' + temp_data[self.e.symbol_list[0]][0].bar_time
                        LogHelper.info(msg)
                        self.on_data(temp_data, self.e)
                        is_get_data = True
                    else:
                        msg = '处理第' + str(self.count) + '根数据, 时间为 ' + datetime.strftime(current_time,"%Y-%m-%d %H:%M:%S") + ",没有数据"
                        LogHelper.info(msg)

                        is_get_data = False
                else:
                    if next_time == dateparser(self.e.endtime):
                        is_end = True
                current_time = next_time
                next_time = current_time + relativedelta(seconds = bar_to_second(context.period))
            else:
                if temp_data !="finish":
                    time.sleep(0.002)
                else:
                    msg = '处理第' + str(self.count) + '根数据, 时间为 ' + datetime.strftime(current_time,"%Y-%m-%d %H:%M:%S") + ",没有数据"
                    LogHelper.info(msg)
                    current_time = next_time
                    next_time = current_time + relativedelta(seconds=bar_to_second(context.period))

    def consume_other_data(self):
        """消费其他类型数据"""
        while True and not self._stop_event.is_set():
            if not self.data.empty():
                self.temp_data = self.data.get()
                d = self.data.get()
                if d != "finish":
                    self.count = self.count + 1
                    msg = '处理第' + str(self.count) + '根数据, 时间为 ' + d[self.e.symbol_list[0]][0].bar_time
                    context._temporary_now = dateparser(d[self.e.symbol_list[0]][0].bar_time)
                    LogHelper.info(msg)
                    self.on_data(d, self.e)
                else:
                    break
            else:
                time.sleep(0.002)