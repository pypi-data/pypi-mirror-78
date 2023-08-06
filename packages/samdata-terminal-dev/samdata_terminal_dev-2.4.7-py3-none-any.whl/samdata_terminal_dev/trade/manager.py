# coding=utf-8
"""
    交易订单模块
"""

import random
import string
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

from ..core.storage import context
from ..core.utils import str2datetime, bar_to_second
from ..helper.loghelper import LogHelper
from ..model.order import Order
from ..core.storage import Holding
from ..core.producer import OrderProduce

fill_time_cache = []
diverse_dict = {"Buy":"Sell", "Sell":"Buy"}

fee_ratio = 0.004   #  手续费率

# create_order_time = 0

class TradeEngine(object):
    """下单引擎类"""
    def __init__(self):
        # self.threadPool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="下单_")
        pass
    
    def __get_order_id(self):
        """
        生成唯一的下单id
        """
        value = "SO" + datetime.strftime(datetime.utcnow(), "%Y%m%d") + ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return value   

    def __create_order(self,order):
        """
        创建订单
        :params order: 订单, Order对象
        """
        start_time = time.time()
        orderid = self.__get_order_id()
        data = (context.strategyid, order.symbol, order.order_type, order.order_time, order.fill_time, datetime.now(), round(order.quantity, 4), order.open_or_close, orderid, order.fillprice, order.direction, context.backtestid, "fill", round(context.total_cash, 4),
                   round(context.cash, 4), order.close_profit, order.close_profit_ratio, order.fee, datetime.now(), datetime.now(), order.positionid, order.order_result, order.limit_price)

        # self.threadPool.submit(OrderProduce, data)
        OrderProduce(data)
        log = 'orderid : ' + orderid + ', 下单成功'
        LogHelper.info(log)
        # end_time = time.time()
        # global create_order_time
        # create_order_time = create_order_time + (end_time - start_time)

    def _get_fill_time(self, order_time, period):
        """
        根据下单时间计算订单完成时间
        :params order_time:str
        :params period: 时间精度， str
        """
        real_order_time = str2datetime(order_time) + relativedelta(seconds=bar_to_second(period))  # 实际下单是为下一个bar时间
        real_order_time_str = datetime.strftime(real_order_time, "%Y-%m-%d %H:%M:%S")
        fill_time = real_order_time + relativedelta(seconds=1)  # 成交时间=下一个bar_time + 1秒
        real_fill_time = datetime.strftime(fill_time, "%Y-%m-%d %H:%M:%S")

        global fill_time_cache
        if len(fill_time_cache) == 0:
            fill_time_cache.append(real_fill_time)
        else:
            while 1:  # 查看成交时间是否已经存在了，如果有，则加一秒
                if real_fill_time in fill_time_cache:
                    fill_time = fill_time + relativedelta(seconds=1)  # 成交时间=成交时间 + 1秒
                else:
                    if len(fill_time_cache) == 10:
                        fill_time_cache = []
                    fill_time_cache.append(real_fill_time)
                    break
                real_fill_time = datetime.strftime(fill_time, "%Y-%m-%d %H:%M:%S")
        return real_order_time_str, real_fill_time

    def fit_order(self, order):
        """
        成交订单
        :params order: 订单, Order对象
        :params period: 时间精度, str
        :return 
        """
        if context.period == "":
            period = "1m"
        else:
            period = context.period

        if isinstance(order, Order):
            order_time, fill_time = self._get_fill_time(order.order_time, period)

            if order.open_or_close == "Open":   # 开仓
                holds = context.holdings.get(order.symbol)
                if holds:    # 是否持有相同方向的仓库, 有则加仓， 否则建仓
                    same_hold = holds.get(order.direction)

                    if same_hold:
                        sum_price = same_hold.quantity * same_hold.averageprice
                        same_hold.quantity = same_hold.quantity + order.quantity
                        same_hold.averageprice = (sum_price + order.quantity * order.fillprice) / same_hold.quantity
                    else:
                        hold = Holding(order.symbol, order.direction, order.quantity, order.fillprice, fill_time)
                        holds[order.direction] = hold           
                else:
                    hold = Holding(order.symbol, order.direction, order.quantity, order.fillprice, fill_time)
                    holds = {}
                    holds[order.direction] = hold
                
                context.holdings[order.symbol] = holds
                fee = order.quantity * order.fillprice * fee_ratio
                context.cash = context.cash - order.quantity * order.fillprice - fee
                hold_cash = 0
                for item in holds:
                    hold_cash = hold_cash + holds[item].quantity * holds[item].averageprice
                context.total_cash = context.cash + hold_cash
                
                if order.direction == "Buy":
                    msg = "开仓成功, 开仓价: " + str(order.fillprice) + ', 开仓量: ' + str(order.quantity) + ', 开仓方向: 多, 手续费: ' + str(fee) + ',成交时间: ' + fill_time
                elif order.direction == "Sell":
                    msg = "开仓成功, 开仓价: " + str(order.fillprice) + ', 开仓量: ' + str(order.quantity) + ', 开仓方向: 空, 手续费: ' + str(fee) + '成交时间: ' + fill_time

                LogHelper.fatal(msg)
                        
                order.close_profit = None
                order.close_profit_ratio = None
                order.fill_time = fill_time
                order.positionid = holds[order.direction].positionid
                order.order_time = order_time
                order.fee = round(fee, 4)

                self.__create_order(order)
            else:           # 平仓
                holds = context.holdings.get(order.symbol)
                diverse_direction = diverse_dict[order.direction]

                if holds:   # 有持仓
                    diverse_hold = holds.get(diverse_direction)

                    if diverse_hold:  # 持有相同方向的仓库
                        if order.quantity <= diverse_hold.quantity:
                            diverse_hold.quantity = diverse_hold.quantity - order.quantity
                            open_price = diverse_hold.averageprice
                            order.positionid = holds[diverse_direction].positionid

                            if diverse_hold.quantity == 0:
                                holds.pop(diverse_direction)
                                context.holdings[order.symbol] = holds

                            # 资金计算
                            close_profit_ratio = ((order.fillprice - open_price) * (1 if diverse_direction == "Buy" else -1)) / open_price
                            close_profit = close_profit_ratio * open_price * order.quantity
                            fee = order.fillprice * order.quantity * fee_ratio
                            context.cash = context.cash + order.quantity * open_price + (order.fillprice - open_price) * (1 if diverse_direction == "Buy" else -1) * order.quantity - fee
                            hold_cash = 0
                            for item in holds:
                                hold_cash = hold_cash + holds[item].quantity * holds[item].averageprice

                            context.total_cash = context.cash + hold_cash
                            
                            msg = ""
                            if diverse_direction == "Sell":
                                msg = "平仓成功, 平仓价: " + str(order.fillprice) + ', 平仓量: ' + str(order.quantity) + ', 平仓方向: 空, 开仓价： ' + str(open_price) + ', 手续费: ' + str(fee) + ', 时间: ' + fill_time
                            elif diverse_direction == "Buy":
                                msg = "平仓成功, 平仓价: " + str(order.fillprice) + ', 平仓量: ' + str(order.quantity) + ', 平仓方向: 多, 开仓价： ' + str(open_price) + ', 手续费: ' + str(fee) + ', 时间: ' + fill_time
                            LogHelper.debug(msg)
                            
                            order.order_time = order_time
                            order.fill_time = fill_time
                            order.close_profit = round(close_profit, 4)
                            order.close_profit_ratio = round(close_profit_ratio, 4)
                            order.fee = round(fee, 4)
                            order.status = "fill"
                            self.__create_order(order)
                            
                        else:
                            msg =  diverse_direction + "方向仓位不够，无法进行平仓"
                            LogHelper.error(msg)
                            return                        
                    else:
                        msg = "没有" + diverse_direction + "方向持仓，无法进行平仓"
                        LogHelper.error(msg)
                        return
                else:
                    msg = "没有" + diverse_direction + "方向持仓，无法进行平仓"
                    LogHelper.error(msg)
                    return 

            msg = '总资产为' + str(context.total_cash)
            LogHelper.warn(msg)
            msg = '可用资金为' + str(context.cash)
            if context.cash < 0 :
                LogHelper.warn(msg)

            holds = context.holdings
            if len(holds.keys()) != 0:
                for symbol in holds:
                    LogHelper.warn("当前持仓情况: " + symbol)
                    for d in holds[symbol]:
                        msg = holds[symbol][d].direction + ", quantity= " + str(holds[symbol][d].quantity) + ", price=" + str(holds[symbol][d].averageprice)
                        LogHelper.warn(msg)

    def fit_order_by_leverage(self, order, period, open_ratio, leverage_multiple,is_capital = True):
        """
        根据杠杆倍数、开仓比率进行计算，其中开仓资金由is_capital、open_ratio决定
        :params order: 订单, Order对象
        :params period: 时间精度, str
        :params open_ratio: 开仓比率, float
        :params leverage_multiple: 杠杆倍数, int
        :return 
        """
        if period == "":
            period = "1m"

        if isinstance(order, Order):
            real_order_time = str2datetime(order.order_time) + relativedelta(seconds=bar_to_second(period))   # 实际下单是为下一个bar时间
            real_order_time_str = datetime.strftime(real_order_time, "%Y-%m-%d %H:%M:%S")
            fill_time= real_order_time + relativedelta(seconds=1)    # 成交时间=下一个bar_time + 1秒
            real_fill_time = datetime.strftime(fill_time, "%Y-%m-%d %H:%M:%S")

            global fill_time_cache
            if len(fill_time_cache) == 0:
                fill_time_cache.append(real_fill_time)
            else:
                while True:    # 查看成交时间是否已经存在了，如果有，则加一秒
                    if real_fill_time in fill_time_cache:
                        fill_time= fill_time + relativedelta(seconds=1)    # 成交时间=成交时间 + 1秒
                    else:
                        if len(fill_time_cache) == 10:
                            fill_time_cache = []
                        fill_time_cache.append(real_fill_time)
                        break
                    real_fill_time = datetime.strftime(fill_time, "%Y-%m-%d %H:%M:%S")
                
            if order.open_or_close == "Open":   # 开仓

                # 下单数计算
                if is_capital:
                    # 开仓可用资金 = 本金 * 开仓比率 * 杠杆倍数
                    open_cash = context.capital * open_ratio * leverage_multiple
                else:
                    # 开仓可用资金 = 可用资金 * 开仓比率 * 杠杆倍数
                    open_cash = context.cash * open_ratio * leverage_multiple

                #  开仓数量 = 开仓可用资金/ 价格
                order.quantity = open_cash / order.fillprice

                # 仓位操作
                holds = context.holdings.get(order.symbol)
                if holds:    # 是否持有相同方向的仓库, 有则加仓， 否则建仓
                    same_hold = holds.get(order.direction)

                    if same_hold:
                        sum_price = same_hold.quantity * same_hold.averageprice
                        same_hold.quantity = same_hold.quantity + order.quantity
                        same_hold.averageprice = (sum_price + order.quantity * order.fillprice) / same_hold.quantity
                    else:
                        hold = Holding(order.symbol, order.direction, order.quantity, order.fillprice, real_fill_time)
                        holds[order.direction] = hold           
                else:
                    hold = Holding(order.symbol, order.direction, order.quantity, order.fillprice, real_fill_time)
                    holds = {}
                    holds[order.direction] = hold
                
                context.holdings[order.symbol] = holds

                # 名义价值
                hold_cash = 0
                for item in holds:
                    hold_cash = hold_cash + holds[item].quantity * holds[item].averageprice
                
                # 资金计算
                # 本次开仓名义价值
                open_value = order.quantity * order.fillprice
                # 交易所需保证金 = 开仓总价值 /杠杆倍数
                margin_cash = open_value / leverage_multiple
                # 手续费 = 开仓总价值 * 手续费
                fee = open_value * fee_ratio
                # 可用资金 = 可用资金 - 保证金 - 手续费
                context.cash = context.cash - margin_cash- fee
                # 总资产 = 可用资金 + (持仓总价值（名义价值） /杠杆倍数)
                context.total_cash = context.cash + (hold_cash / leverage_multiple)
                
                if order.direction == "Buy":
                    msg = "开仓成功, 开仓价: " + str(order.fillprice) + ', 开仓量: ' + str(order.quantity) + ', 开仓方向: 多, 手续费: ' + str(fee) + '成交时间: ' + real_fill_time
                elif order.direction == "Sell":
                    msg = "开仓成功, 开仓价: " + str(order.fillprice) + ', 开仓量: ' + str(order.quantity) + ', 开仓方向: 空, 手续费: ' + str(fee) + '成交时间: ' + real_fill_time
                # log_into_mysql(msg, "fatal")
                LogHelper.fatal(msg)

                context.cumfee = context.cumfee + fee    
                order.close_profit = None
                order.close_profit_ratio = None
                order.fill_time = real_fill_time
                order.positionid = holds[order.direction].positionid
                order.fee = round(fee, 4)
                order.order_time = real_order_time_str 
                self.__create_order(order)
            else:           # 平仓
                # 仓位操作
                holds = context.holdings.get(order.symbol)
                diverse_direction = diverse_dict[order.direction]

                if holds:   # 有持仓
                    diverse_hold = holds.get(diverse_direction)

                    if diverse_hold:  # 持有相同方向的仓库
                        if order.quantity <= diverse_hold.quantity:
                            # 仓位数 = 仓位数-平仓数
                            diverse_hold.quantity = diverse_hold.quantity - order.quantity
                            # 开仓价 = 成本价
                            open_price = diverse_hold.averageprice
                            order.positionid = holds[diverse_direction].positionid

                            #  持仓变化
                            if diverse_hold.quantity == 0:
                                holds.pop(diverse_direction)
                                context.holdings[order.symbol] = holds

                            # 资金计算
                            # 平仓返回的保证金 = （平仓量 * 开仓价）/ 杠杆倍数
                            margin_cash = (order.quantity * open_price)/leverage_multiple
                            # 手续费 = 平仓量 * 平仓价 * 手续费率
                            fee = order.quantity * order.fillprice * fee_ratio

                            # 平仓收益率 = （平仓价-开仓价）*（方向系数）/ 开仓价
                            close_profit_ratio = (order.fillprice - open_price) * (1 if diverse_direction == "Buy" else -1)/ open_price
                            #  平仓收益 = 平仓收益率 * 保证金 * 杠杆倍数 (使用杠杆后的平仓收益被放大)
                            close_profit = close_profit_ratio * margin_cash * leverage_multiple 
                    
                            # 可用资金 = 可用资金+ 保证金  + 平仓收益 - 手续费
                            context.cash = context.cash + margin_cash + close_profit - fee
                            # 持仓名义价值 
                            hold_cash = 0
                            for item in holds:
                                hold_cash = hold_cash + holds[item].quantity * holds[item].averageprice

                            # 总资产 = 可用资金 + （持仓总价值/杠杆倍数)
                            context.total_cash = context.cash + hold_cash/leverage_multiple
                            
                            if diverse_direction == "Sell":
                                msg = "平仓成功, 平仓价: " + str(order.fillprice) + ', 平仓量: ' + str(order.quantity) + ', 平仓方向: 空, 开仓价： ' + str(open_price) + ', 手续费: ' + str(fee) + ',时间: ' + fill_time
                            elif diverse_direction == "Buy":
                                msg = "平仓成功, 平仓价: " + str(order.fillprice) + ', 平仓量: ' + str(order.quantity) + ', 平仓方向: 多, 开仓价： ' + str(open_price) + ', 手续费: ' + str(fee) + ', 时间: ' + fill_time
                            LogHelper.debug(msg)
                            
                            context.cumfee = context.cumfee + fee  
                            order.order_time = real_order_time_str
                            order.fill_time = real_fill_time
                            order.close_profit = round(close_profit,4)
                            order.close_profit_ratio = round(close_profit_ratio,4)
                            order.fee = round(fee,4)
                            order.status = "fill"
                            self.__create_order(order)
                            
                        else:
                            msg =  diverse_direction + "方向仓位不够，无法进行平仓"
                            LogHelper.error(msg)
                            return                        
                    else:
                        msg = "没有" + diverse_direction + "方向持仓，无法进行平仓"
                        LogHelper.error(msg)
                        return
                else:
                    msg = "没有" + diverse_direction + "方向持仓，无法进行平仓"
                    LogHelper.error(msg)
                    return 

            msg = '总资产为' + str(context.total_cash)
            LogHelper.warn(msg)
            msg = '可用资金为' + str(context.cash)

            if context.cash < 0 :
                LogHelper.warn(msg)

            holds = context.holdings
            if len(holds.keys()) != 0:
                for symbol in holds:
                    LogHelper.warn("当前持仓情况: " + symbol)
                    for d in holds[symbol]:
                        msg = holds[symbol][d].direction + ", quantity= " + str(holds[symbol][d].quantity) + ", price=" + str(holds[symbol][d].averageprice)
                        LogHelper.warn(msg)

# 下单引擎实例
tradeengine = TradeEngine()

