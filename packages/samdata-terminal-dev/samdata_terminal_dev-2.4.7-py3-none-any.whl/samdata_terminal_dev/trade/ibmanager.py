# coding=utf-8
"""
    仿真交易订单模块
"""

from datetime import datetime
import requests
import json
import random
import string
import traceback

from ..core.storage import context, Holding
from ..helper.loghelper import LogHelper
from ..model.order import Order
from ..core.producer import OrderProduce

fill_time_cache = []
diverse_dict = {"Buy": "Sell", "Sell": "Buy"}
# type_dict = {"Forex": "CASH", "Commodity": "CMDTY", "Future":"FUT", "Index":"IND","Stock":"STK","FOption":"FOP","Combo":"BAG","Bond":"BOND","Warrant":"WAR","News":"NEWS", "Fund":"FUND"}

fee_ratio = 0  # 手续费率

class IBTradeEngine(object):
    """IB仿真交易引擎类"""

    def __init__(self):
        self.order_id_dict = {}    # 保存数据库的订单id与在IB创建的订单ID的映射
        self.client_id = None    #  标记连接IB的客户端Id，便于通过该值和IB订单Id,查询订单的状态
        self.order_dict = {}    #  保存没有完成的订单信息，便于查询该订单信息
        self.order_env = ""

    def set_order_conn(self):
        self.order_env = "http://" + context.orderserver.server_url + ":" + context.orderserver.port

    def __get_order_id(self):
        """
        生成唯一的下单id
        """
        value = "SO" + datetime.strftime(datetime.utcnow(), "%Y%m%d") + ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return value

    def create_order_into_mysql(self, order):
        """
        往数据库中插入订单数据
        :params order: 订单, Order对象
        """
        data = (context.strategyid, order.symbol, order.order_type, order.order_time, order.fill_time, datetime.now(),
                round(order.quantity, 4), order.open_or_close, order.order_id, order.fillprice, order.direction,
                context.paperid, order.status, round(context.total_cash, 4),
                round(context.cash, 4), order.close_profit, order.close_profit_ratio, order.fee, datetime.now(),
                datetime.now(), order.positionid, order.order_result, order.limit_price)
        print(data)
        OrderProduce(data)
        log = 'orderid : ' + str(order.order_id) + ', 状态： ' + order.status
        LogHelper.info(log)

    def create_order(self, order):
        self.create_order_into_mysql(order)

    def fit_order(self, order):
        """
        成交订单
        :params order: 订单, Order对象
        :return order: 订单
        :returns status: 成交状态
        """
        iborderid = ""
        if order.order_id is None:
            order.order_id = self.__get_order_id()

        print("************ orderid : " + order.order_id)

        if isinstance(order, Order):

            is_operate, order = self.check_order_operate(order)

            if is_operate:
                if order.order_type == 0:
                    status, order, iborderid = self.fit_market_order(order)
                else:
                    status, order = self.fit_limit_order(order)

                print("从IB返回的状态: "+ status)
                if status == "Filled":
                    self.handle_position(order)
                    self.create_order(order)
        return order.status, order, iborderid

    def fit_limit_order(self, order):
        """
        按限价成交订单
        :params order: 订单, Order对象
        :returns status: 订单状态,
        :returns order: 订单
        """
        status = ""
        side = order.direction.upper()

        # 如果为平仓操作，则反向操作仓位
        if order.direction == "Buy":
            side = "BUY"
        else:
            side = "SELL"

        url = self.order_env + "/api/Order/CreateLimitOrder"
        headers = {'Content-Type':'application/json'}

        try:
            order.symbol = context.data_source_type + ":" + order.symbol
        except Exception as str_ex:
            print("将品种名转换成指定格式时出错")
            print(str_ex)
            traceback.print_exc()

        data = {
            "contract": order.symbol,  # "CASH:USD-JPY-IDEALPRO"
            "side": side,
            "quantity": order.quantity,
            "limitprice":order.limit_price
        }

        LogHelper.info("向ib 发送订单数据: "+ data)

        if self.client_id != None:
            data['clientid'] = self.client_id

        req = requests.post(url= url, headers = headers, data = json.dumps(data), timeout=10)

        try:
            if req.status_code == 200:
                response_data = req.json()
                LogHelper.info("订单返回信息: "+ response_data)
                if "orderStatus" in response_data:
                    order.status = response_data["orderStatus"]

                    if order.status != "Fail":
                        order.fillprice = response_data["order"]["avgFillPrice"]
                        order.quantity = response_data["order"]["filled"]
                        order.fill_time = response_data["order"]["time"]
                        order.order_result = response_data["message"]
                        if order.fill_time == None:
                            order.fill_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")

                        self.client_id = response_data["order"]["clientId"]
                    else:
                        status = "fail"
                        order.fill_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
                        print("下单失败, code: " + str(req.status_code))
                    status = order.status
                else:
                    print("没有下单数据返回")
                    order.status = "fail"
                    order.fill_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
            else:
                status = "fail"
                print("下单失败, code: " + str(req.status_code))
                print(req.json())
        except Exception as ex:
            print("处理订单信息时出现异常！！！")
            print(ex)
            traceback.print_exc()
        return status, order

    def fit_market_order(self, order):
        """
        按市价成交订单
        :params order: 订单
        :returns result： 订单状态， 其值为相应的在IB的订单状态值
        :returns order: 订单
        """
        side = order.direction.upper()
        result = ""
        ib_orderid = ""
        status = ""

        if order.direction == "Buy":
            side = "BUY"
        elif order.direction == "Sell":
            side = "SELL"
        else:
            pass

        request_symbol = ""
        try:
            request_symbol = context.data_source_type + ":" + order.symbol
        except Exception as str_ex:
            print("将品种名转换成指定格式时出错")
            print(str_ex)
            traceback.print_exc()
        try:
            url = self.order_env + "/api/Order/CreateMarketOrder"
            headers = {'Content-Type':'application/json'}
            data = {
                "contract": request_symbol,
                "side": side,
                "quantity": order.quantity,
                "orderid":order.order_id
            }

            LogHelper.info("向ib 发送订单数据: "+ str(data))

            if self.client_id != None:
                data['clientid'] = self.client_id

            req = requests.post(url= url, headers = headers, data = json.dumps(data), timeout=10)

            if req.status_code == 200:
                response_data = req.json()["result"]
                LogHelper.info("订单返回信息: "+ str(response_data))

                order.status = response_data["orderStatus"]
                ib_orderid = response_data["ibOrderId"]

                if order.status == "Filled":
                    if  response_data["order"] is not None:
                        order.fillprice = response_data["order"]["avgFillPrice"]
                        order.quantity = response_data["order"]["filled"]
                        order.fill_time = response_data["order"]["time"]
                        if order.fill_time == None:
                            order.fill_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
                        else:
                            fill_time = order.fill_time.split(".")[0]
                            order.fill_time = datetime.strptime(fill_time, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

                        self.client_id = response_data["order"]["clientId"]
                elif order.status == "Fail":
                    print("没有下单数据返回")
                    order.fill_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
                    status = order.status
                else:
                    order.fill_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")

                status = order.status
                order.order_result = response_data["message"]
            else:
                status = "Fail"
                print("下单失败, code: " + str(req.status_code))
                print(req.json())
        except Exception as ex:
            print("处理订单信息时出现异常！！！")
            print(ex)
            traceback.print_exc()

        return status, order, ib_orderid

    def get_order_status(self, order_id):
        """
        查询订单成交状态
        :params order_id: 订单Id
        :returns order: 订单
        """
        url = self.order_env + "/api/Order/GetOrderInfo"
        data = {
            'orderId':self.order_id_dict[order_id],
            'clientId':self.client_id
        }
        req = requests.get(url, params=data)
        response = req.json()
        print("查询订单状态")
        print(response)
        status = response["status"]
        order = self.order_dict[order_id]

        if status != order.status:
            order.status = status
            order.quantity = response["filled"]
            order.fill_time = response["time"]

            if order.fill_time == None:
                order.fill_time = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")

            if order.status == "filled":
                self.handle_position(order)
            else:
                self.status = "invalid"
                self.order_result = response["message"]
            self.order_dict.pop(order_id, "")
            self.order_id_dict.pop(order_id, "")

        return order

    def check_order_operate(self,order):
        """
        判断该订单是否可以进行操作：
        """
        result = order
        is_operate = True
        if isinstance(result, Order):
            if result.open_or_close == "Close":  # 平仓
                holds = context.holdings.get(result.symbol)
                diverse_direction = diverse_dict[result.direction]

                if holds:  # 有持仓
                    diverse_hold = holds.get(diverse_direction)

                    if diverse_hold:
                        spread = diverse_hold.quantity - result.quantity

                        if spread < 0 :
                            # 是否可以进行反手开仓
                            if context.is_reverse_operate:
                                open_order = result
                                import math
                                open_order.quantity = math.fabs(spread)
                                open_order.open_or_close = "Open"
                                result.quantity = diverse_hold.quantity
                                self.fit_order(result)
                                msg = "没有" + diverse_direction + "方向持仓，无法进行平仓，但可以进行反手开仓！！！"
                                LogHelper.error(msg)
                            else:
                                msg = "没有足够" + diverse_direction + "方向持仓，无法进行平仓"
                                LogHelper.error(msg)
                                is_operate = False
                    else:
                        if context.is_reverse_operate:
                            open_order = result
                            open_order.open_or_close = "Open"
                            result.quantity = order.quantity
                            self.fit_order(result)
                            msg = "没有" + diverse_direction + "方向持仓，无法进行平仓，但可以进行反手开仓！！！"
                            LogHelper.error(msg)
                            is_operate = False
                        else:
                            msg = "没有足够" + diverse_direction + "方向持仓，无法进行平仓"
                            LogHelper.error(msg)
                            is_operate = False
                else:
                    if context.is_reverse_operate:
                        result.open_or_close = "Open"
                        msg = "没有" + diverse_direction + "方向持仓，无法进行平仓，但可以进行反手开仓！！！"
                        LogHelper.error(msg)
                    else:
                        msg = "没有" + diverse_direction + "方向持仓，无法进行平仓！！！"
                        LogHelper.error(msg)
                        is_operate = False

            return is_operate, result

    def handle_position(self, order):
        """
        仓位处理、资金计算
        :params order: 订单, Order对象
        :return
        """
        global  fee

        if isinstance(order, Order):
            if order.open_or_close == "Open":  # 开仓
                holds = context.holdings.get(order.symbol)

                if holds:  # 是否持有相同方向的仓库, 有则加仓， 否则建仓
                    msg = "有相同方向的仓位，直接进行加仓"
                    LogHelper.info(msg)
                    same_hold = holds.get(order.direction)

                    if same_hold:
                        sum_price = same_hold.quantity * same_hold.averageprice
                        same_hold.quantity = same_hold.quantity + order.quantity
                        same_hold.averageprice = (sum_price + order.quantity * order.fillprice) / same_hold.quantity
                    else:
                        hold = Holding(order.symbol, order.direction, order.quantity, order.fillprice, order.fill_time)
                        holds[order.direction] = hold
                else:
                    msg = "没有有相同方向的仓位，直接进行建仓"
                    LogHelper.info(msg)
                    hold = Holding(order.symbol, order.direction, order.quantity, order.fillprice, order.fill_time)
                    holds = {}
                    holds[order.direction] = hold

                context.holdings[order.symbol] = holds
                fee = order.quantity * order.fillprice * fee_ratio
                context.cash = context.cash - order.quantity * order.fillprice - fee
                hold_cash = 0
                for item in holds:
                    hold_cash = hold_cash + holds[item].quantity * holds[item].averageprice
                context.total_cash = context.cash + hold_cash
                order.positionid = holds[order.direction].positionid
                if order.direction == "Buy":
                    msg = "开仓成功, 开仓价: " + str(order.fillprice) + ', 开仓量: ' + str(
                        order.quantity) + ', 开仓方向: 多, 手续费: ' + str(fee) + ',成交时间: '+ order.fill_time
                elif order.direction == "Sell":
                    msg = "开仓成功, 开仓价: " + str(order.fillprice) + ', 开仓量: ' + str(
                        order.quantity) + ', 开仓方向: 空, 手续费: ' + str(fee) + '成交时间: ' + order.fill_time

                LogHelper.fatal(msg)
            else:  # 平仓
                holds = context.holdings.get(order.symbol)
                diverse_direction = diverse_dict[order.direction]

                if holds:  # 有持仓
                    diverse_hold = holds.get(diverse_direction)
                    diverse_hold.quantity = diverse_hold.quantity - order.quantity
                    open_price = diverse_hold.averageprice
                    order.positionid = holds[diverse_direction].positionid

                    if diverse_hold.quantity == 0:
                        holds.pop(diverse_direction)
                        context.holdings[order.symbol] = holds

                    # 资金计算
                    close_profit_ratio = ((order.fillprice - open_price) * (
                        1 if diverse_direction == "Buy" else -1)) / open_price
                    close_profit = close_profit_ratio * open_price * order.quantity
                    fee = order.fillprice * order.quantity * fee_ratio
                    context.cash = context.cash + order.quantity * open_price + (
                                order.fillprice - open_price) * (
                                       1 if diverse_direction == "Buy" else -1) * order.quantity - fee
                    hold_cash = 0
                    for item in holds:
                        hold_cash = hold_cash + holds[item].quantity * holds[item].averageprice

                    context.total_cash = context.cash + hold_cash

                    if diverse_direction == "Sell":
                        msg = "平仓成功, 平仓价: " + str(order.fillprice) + ', 平仓量: ' + str(
                            order.quantity) + ', 平仓方向: 空, 开仓价： ' + str(open_price) + ', 手续费: ' + str(
                            fee) + ', 时间: '+ order.order_time  #  + order.fill_time
                    elif diverse_direction == "Buy":
                        msg = "平仓成功, 平仓价: " + str(order.fillprice) + ', 平仓量: ' + str(
                            order.quantity) + ', 平仓方向: 多, 开仓价： ' + str(open_price) + ', 手续费: ' + str(
                            fee) + ', 时间: '+ order.order_time  #  + order.fill_time
                    LogHelper.debug(msg)

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
                        msg = holds[symbol][d].direction + ", quantity= " + str(
                            holds[symbol][d].quantity) + ", price=" + str(holds[symbol][d].averageprice)
                        LogHelper.warn(msg)
        return order

# 下单引擎实例
ibtradeengine =IBTradeEngine()

