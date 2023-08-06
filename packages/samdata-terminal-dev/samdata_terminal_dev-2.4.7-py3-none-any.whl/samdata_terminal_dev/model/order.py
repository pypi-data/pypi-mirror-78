# -*- encoding:utf-8 -*-

class Order(object):
    """
        订单类
    """
    def __init__(self, symbol, direction, order_time, quantity, 
            open_or_close, order_type, fillprice, limit_price=0, order_id = 0):
        """
        初始化
        :params symbol: 品种名, str
        :params direction: 方向("Buy":多，"Sell":空), str
        :params order_time: 下单时间, str
        :params quantity: 数量, int
        :params open_or_close：开仓("Open")/平仓("Close"), str
        :params order_type: 
        :params fillprice: 成交价, float
        :params limitprice: 限价，float
        """
        self.order_id = None
        self.symbol = symbol
        self.direction = direction
        self.order_time = order_time
        self.fill_time = None
        self.quantity = quantity
        self.open_or_close = open_or_close
        self.fillprice = fillprice
        self.limit_price = limit_price
        self.order_type = order_type
        self.positionid = None
        self.close_profit = None
        self.close_profit_ratio = None
        self.status = None
        self.cach = 0
        self.fee = 0
        self.order_result = None

class PaperOrder(object):
    """
        订单类
    """
    def __init__(self, symbol, direction, order_time, quantity,
            open_or_close, order_type, fillprice, limit_price=0, order_id = None):
        """
        初始化
        :params symbol: 品种名, str
        :params direction: 方向("Buy":多，"Sell":空), str
        :params order_time: 下单时间, str
        :params quantity: 数量, int
        :params open_or_close：开仓("Open")/平仓("Close"), str
        :params order_type:
        :params fillprice: 成交价, float
        :params limitprice: 限价，float
        """
        self.order_id = order_id
        self.symbol = symbol
        self.direction = direction
        self.order_time = order_time
        self.fill_time = None
        self.quantity = quantity
        self.open_or_close = open_or_close
        self.fillprice = fillprice
        self.limit_price = limit_price
        self.order_type = order_type
        self.positionid = None
        self.close_profit = None
        self.close_profit_ratio = None
        self.status = None
        self.cach = 0
        self.fee = 0
        self.order_result = None
