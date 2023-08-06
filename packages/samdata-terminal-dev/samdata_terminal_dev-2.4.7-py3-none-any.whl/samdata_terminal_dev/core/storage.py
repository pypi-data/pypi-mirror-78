# -*- encoding:utf-8 -*-
"""
    上下文：存储资金、持仓等信息
"""

import os
from datetime import datetime
import random
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..model.sql.tables import Position, PaperPosition
from ..core import env
from ..core.env import EModeType

# 上下文
class Context(object):
    def __init__(self,):
        self.cash = 0        # 可用资金
        self._temporary_now = None    # 记录当前时间
        self.holdings = {}           # 持仓量，key：品种名（str）、value：持仓量（dict, key 为 direction,value 为 Holding对象）
        self.total_cash = 0     # 总资产
        self.capital = 0     #  本金
        self.cumfee = 0     #  累计手续费
        self.leverage_multiple = 1    #  杠杆倍数
        self.open_percent = 1  # 开仓资金占用比例
        self.backtestid = None
        self.paperid = None
        self.strategyid = None
        self.api_key = None
        self.api_secret = None

        self.period = ''
        self.e = None

        self.websocketserver = None
        self.dataserver = None
        self.terminalserver = None
        self.orderserver = None

        self.mysql_conn = None
        self.pg_conn = None
        self.websocket_conn = None
        self.order_conn = None

        self.data_source_type = None

        self.is_reverse_operate = None

    def set_conn(self):
        self.dataserver = DataServer(self.pg_conn)
        self.terminalserver = TerminalServer(self.mysql_conn)
        self.websocketserver = WebSocket(self.websocket_conn)
        self.orderserver = IBOrder(self.order_conn)

class Holding(object):
    """
        持仓信息
    """
    def __init__(self, symbol, direction, quantity, averageprice, create_time, volumemultiple=0):
        """
        :param symbol: 交易对
        :param direction: 方向
        :param quantity: 数量
        :param averageprice: 平均成本价
        :param volumemultiple: 
        :param creat_time: 建仓时间        
        """
        self.symbol = symbol
        self.direction = direction
        self.quantity = quantity
        self.volumemultiple = volumemultiple
        self.averageprice = averageprice
        self.creat_time = create_time
        self.positionid = self.__create_position()
    
    def __create_position(self):
        """
        创建仓位
        """
        value = "PI" + datetime.strftime(datetime.utcnow(), "%Y%m%d") + ''.join(random.sample(string.ascii_letters + string.digits, 8))
        session = sessionmaker(bind = context.terminalserver.engine)()

        if env.get_mode == EModeType.BACKTEST:
            position = Position(PositionId = value, BacktestId = context.backtestid, Symbol = self.symbol, Direction = self.direction, CreatedAt = self.creat_time)
        else:
            position = PaperPosition(PositionId=value, PaperId=context.paperid, Symbol=self.symbol,
                                Direction=self.direction, CreatedAt=self.creat_time)
        session.add(position)
        session.commit()
        session.close()
        print("创建仓位信息, " + str(self.__dict__))
        return value

class TerminalServer(object):
    """
        终端数据库信息
    """
    server_url = None
    port = None
    username = None
    password = None

    def __init__(self, mysql_conn):
        if mysql_conn is None:
            self.get_conn_from_env()
        else:
            self.server_url = mysql_conn["url"]
            self.port = mysql_conn["port"]
            self.username = mysql_conn["username"]
            self.password = mysql_conn["pwd"]
        conn_str = 'mysql+pymysql://' + self.username + ':' + self.password + '@' + self.server_url + ':' + self.port + '/samdata_terminal'
        self.engine = create_engine(conn_str)
        print("连接的mysql_conn: " + str(self.__dict__))

    def get_conn_from_env(self):
        if "MySQL_Session" in os.environ:
            mysql_env = os.environ["MySQL_Session"].split(':')
            self.server_url = mysql_env[-2].split('@')[-1]
            self.port = mysql_env[-1]
            self.username = mysql_env[0]
            self.password = '@'.join(mysql_env[-2].split('@')[:-1])
        else:
            print("没有配置MySQL_Session环境变量")

class DataServer(object):
    """
        同步数据库信息
    """
    server_url = None
    port = None
    username = None
    password = None

    def __init__(self, pg_conn):
        if pg_conn is None:
            self.get_conn_from_env()
        else:
            self.server_url =pg_conn["url"]
            self.port = pg_conn["port"]
            self.username = pg_conn["username"]
            self.password = pg_conn["pwd"]
        print("连接的data_server: " + str(self.__dict__))

    def get_conn_from_env(self):
        if "PostgreSQL_Session" in os.environ:
            postgresql_env = os.environ["PostgreSQL_Session"].split(':')
            self.server_url = postgresql_env[-2].split('@')[-1]
            self.port = postgresql_env[-1]
            self.username = postgresql_env[0]
            self.password = '@'.join(postgresql_env[-2].split('@')[:-1])
        else:
            print("没有配置PostgreSQL_Session环境变量")

class WebSocket(object):
    server_url = None
    port = None

    def __init__(self, websocket_conn):
        if websocket_conn is None:
            self.get_conn_from_env()
        else:
            self.server_url = websocket_conn["url"]
            self.port = websocket_conn["port"]
        print("websocket的连接: "+ str(self.__dict__))

    def get_conn_from_env(self):
        if "Websocket" in os.environ:
            websocket_env = os.environ["Websocket"].split(":")
            self.server_url = websocket_env[0]
            self.port = websocket_env[1]
        else:
            print("没有配置Websocket环境变量")

class IBOrder(object):
    server_url = None
    port = None

    def __init__(self, order_conn):
        if order_conn is None:
            self.get_conn_from_env()
        else:
            self.server_url = order_conn["url"]
            self.port = order_conn["port"]
        print("连接的order_server: " + str(self.__dict__))

    def get_conn_from_env(self):
        if "Order_Server" in os.environ:
            order_env = os.environ["Order_Server"].split(":")
            self.server_url = order_env[0]
            self.port = order_env[1]

# 在整个策略运行过程中，唯一的上下文
context = Context()