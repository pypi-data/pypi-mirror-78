# -*- encoding:utf-8 -*-
"""
    通用模块
"""

import datetime
from datetime import datetime
import time
import pytz

def complete_datetime(date_time):
    """ 
    补全时间
    :params date_time: 时间, str
    :return 补全后的时间, str
    """
    if len(date_time) == 10:    # 类似于2019-10-10
        data = datetime.strptime(date_time + " 00:00:00", '%Y-%m-%d %H:%M:%S')
        return datetime.strftime(data, '%Y-%m-%d %H:%M:%S')
    elif len(date_time) == 19:      # 类似于2019-10-10 08:00:00
        data = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        return datetime.strftime(data, '%Y-%m-%d %H:%M:%S')
    else:
        print("日期格式请按以下格式：%Y-%m-%d %H:%M:%S 或者 %Y-%m-%d")

def bar_to_second(value):
    """
    将相应的value转换成秒数
    :params value: 分钟精度, str
    :return 秒数: int
    """
    value = value.strip().lower()

    if value.endswith('s'):
        return int(value[0:-1])

    if value.endswith('m'):
        return int(value[0:-1]) * 60

    if value.endswith('h'):
        return int(value[0:-1]) * 60 * 60

    if value.endswith('d'):
        return int(value[0:-1]) * 60 * 60 * 24

    raise ValueError('仅支持s(秒)、m(分钟), h(小时), d(天) 结尾')

def str2datetime(d):
    """
    把字符串转成datetime类型
    :params d: 时间, str
    :return 时间, datetime
    """
    if len(d) == 8:
        return datetime.strptime(d, '%Y%m%d')
    if len(d) == 10:
        return datetime.strptime(d, '%Y-%m-%d')
    if len(d) == 17:  # 类似于 201707010 8:50:00
        return datetime.strptime(d, '%Y%m%d %H:%M:%S')
    if len(d) == 19:  # 类似于 2017-07-01 08:50:00
        return datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
    if len(d) == 23:  # 类似于 2017-07-01 08:50:00.000
        return datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f')  
    if len(d) == 26:  # 类似于 2017-07-01 08:50:00.000000
        return datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f')     
    return None

def convert_from_timeStamp(timeNum):
    """
    13位/10位时间戳转换成时间格式字符串
    :params timeNum:13位/10位时间戳, int
    :return otherStypeItem: 目标时间字符串, str
    """
    if len(str(int(timeNum))) == 13:
        timeStamp = float(int(timeNum)/1000)
    elif len(str(int(timeNum))) == 10:
        timeStamp = float(int(timeNum))
    otherStyleTime =  datetime.fromtimestamp(int(timeStamp), pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
    return otherStyleTime

def convert_to_timestamp(date_time):
    """
    将时间转换成13位时间戳
    :params date_time: 时间, str
    :return result: 时间戳, str
    """
    if len(date_time) == 26:
        date_time = date_time[:-3]
        date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=pytz.utc)
        result = str(int(date_time.timestamp() * 1000))
    else:
        # result = str(int(time.mktime(time.strptime(date_time, '%Y-%m-%d %H:%M:%S'))) * 1000)
        date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.utc)
        result = str(int(date_time.timestamp() * 1000))
    return result
