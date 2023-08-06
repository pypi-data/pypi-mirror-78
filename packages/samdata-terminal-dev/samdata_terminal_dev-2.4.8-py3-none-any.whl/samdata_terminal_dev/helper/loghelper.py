# -*- encoding:utf-8 -*-
"""
    日志辅助类
"""

import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from ..core.storage import context
from ..core import env
from ..core.env import EModeType
from ..core.producer import LogProduce

level_num_dic = {"error":"0", "warn":"1", "info":"2", "debug":"3", "fatal":"4"}

class LogHelper:
    def __init__(self):
        self._pool = ThreadPoolExecutor(max_workers=10)

    @staticmethod
    def info(msg):
        log_info = "{0} {1}: {2}".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),'[INFO]',msg)
        print(log_info)
        level_num = level_num_dic["info"]
        logging.info(msg)
        now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

        if env.get_mode == EModeType.BACKTEST:
            LogProduce((context.backtestid, log_info, level_num, now_time, now_time))
        else:
            LogProduce((context.paperid, log_info, level_num, now_time, now_time))

    @staticmethod
    def error(msg):
        log_info = "{0} {1}: {2}".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),'[ERROR]',msg)
        print(log_info)
        level_num = level_num_dic["error"]
        logging.error(msg)
        now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

        if env.get_mode == EModeType.BACKTEST:
            LogProduce((context.backtestid, log_info, level_num, now_time, now_time))
        else:
            LogProduce((context.paperid, log_info, level_num, now_time, now_time))

    @staticmethod
    def debug(msg):
        log_info = "{0} {1}: {2}".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),'[DEBUG]',msg)
        print(log_info)
        level_num = level_num_dic["debug"]
        logging.debug(msg)
        now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

        if env.get_mode == EModeType.BACKTEST:
            LogProduce((context.backtestid, log_info, level_num, now_time, now_time))
        else:
            LogProduce((context.paperid, log_info, level_num, now_time, now_time))

    @staticmethod
    def warn(msg):
        log_info = "{0} {1}: {2}".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),'[WARN]',msg)
        print(log_info)
        level_num = level_num_dic["warn"]
        logging.warn(msg)
        now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

        if env.get_mode == EModeType.BACKTEST:
            LogProduce((context.backtestid, log_info, level_num, now_time, now_time))
        else:
            LogProduce((context.paperid, log_info, level_num, now_time, now_time))

    @staticmethod
    def fatal(msg):
        log_info = "{0} {1}: {2}".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),'[FATAL]',msg)
        print(log_info)
        level_num = level_num_dic["fatal"]
        logging.fatal(msg)
        now_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

        if env.get_mode == EModeType.BACKTEST:
            LogProduce((context.backtestid, log_info, level_num, now_time, now_time))
        else:
            LogProduce((context.paperid, log_info, level_num, now_time, now_time))