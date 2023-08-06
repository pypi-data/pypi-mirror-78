# -*- encoding:utf-8 -*-
"""
    获取数据的各类方法模块
"""
import csv
import datetime
import os
import json
import requests
from urllib import parse
import platform
from datetime import datetime
from dateutil.parser import parse as dateparser
import zipfile
import re
import io

from dateutil.relativedelta import relativedelta
from samdata_terminal_dev.model.data_model import KlineData, DepthData, TickData
from samdata_terminal_dev.model.symbol import SymbolModel,FutureModel,IndexModel
from samdata_terminal_dev.core.utils import convert_from_timeStamp,convert_to_timestamp
from ..helper.mysqlhelper import MySqLHelper
from ..helper.pghelper import PgSqLHelper

user_path = ''
join_str = ''
if platform.system() == "Linux":   # 当前用户系统为linux
    user_path = os.path.expandvars('$HOME')
    join_str = "//"
elif platform.system() == "Windows":
    user_path = os.path.expanduser('~')
    join_str = "\\"
else:
    pass

default_count = 10000


def get_download_path():
    """
        获取csv文件下载路径
    """
    download_path = user_path + join_str + "samterminal" + join_str + "datasync"
    return download_path

def get_spot_kline_data(exchange, base_symbol, asset_symbol, period, starttime, endtime, count = default_count):
    """
    在csv文件路径下获取 现货 k线数据
    :params base_symbol: 基础币种, str
    :params asset_symbol: 计价币种, str
    :params period; 时间精度, str
    :params starttime: 开始时间,str 格式： %Y-%M-%d %H:%m-%s
    :params count: 返回的k线的数量
    :returns kline_data: k线数据, list（每个元素为KlineData对象）
    """
    file_dir = get_download_path()
    start_time = dateparser(starttime)
    end_time = dateparser(endtime)
    start_month = start_time
    data = []
    global join_str

    while start_month <= end_time:
        table_name = "Kline" + "_Spot_" + period + "_" + datetime.strftime(start_month, "%Y%m") + "_" + base_symbol.lower() + "_" + asset_symbol.lower() + "_" + exchange.upper() + ".csv"
        name_list = table_name.split('.')[0].split('_')
        file_path = file_dir + join_str + "Kline" + join_str + name_list[1] + join_str + name_list[-3] + '_' + name_list[-2] + '_' + name_list[-1] + join_str + table_name

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if "Time" not in row:
                        time = dateparser(row[1])
                        if time >= start_time and time <= end_time:
                            if len(data) < count:
                                data.append(KlineData(row[0], row[1], float(row[2]), float(row[3]), float(row[4]), float(row[5]),float(row[6]),float(row[7])))
                            else:
                                return data
                        elif time >= end_time:
                            return data
        else:
            print("文件不存在: " + file_path)
        start_month = start_month + relativedelta(months=1)

    return data


def get_future_kline_data(exchange, base_symbol, asset_symbol, future_type, period, starttime, endtime, count = default_count):
    """
    在csv文件路径下获取 期货 k线数据
    :params base_symbol: 基础币种, str
    :params asset_symbol: 计价币种, str
    :params future_type: 合约类型， str
    :params period; 时间精度, str
    :params starttime: 开始时间,str 格式： %Y-%M-%d %H:%m-%s
    :params count: 返回的k线的数量
    :returns kline_data: k线数据, list（每个元素为KlineData对象）
    """
    file_dir = get_download_path()
    start_time = dateparser(starttime)
    end_time = dateparser(endtime)
    start_month = start_time
    data = []
    global join_str

    while start_month <= end_time:
        table_name = "Kline" + "_" + future_type.upper() +"_" + period + "_" + datetime.strftime(start_month, "%Y%m") + "_" + base_symbol.lower() + "_" + asset_symbol.lower() + "_" + exchange.upper() + ".csv"
        name_list = table_name.split('.')[0].split('_')
        file_path = file_dir + join_str + "Kline" + join_str + name_list[1] + join_str + name_list[-3] + '_' + name_list[-2] + '_' + name_list[-1] + join_str + table_name

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if "Time" not in row:
                        time = dateparser(row[1])
                        if time >= start_time and time <= end_time:
                            if len(data) < count:
                                if len(row) == 8:
                                    data.append(KlineData(row[0], datetime.strftime(time, "%Y-%m-%d %H:%M:%S"), float(row[2]), float(row[3]), float(row[4]), float(row[5]),float(row[6]),float(row[7])))                            
                                else:
                                    data.append(KlineData(row[0], datetime.strftime(time, "%Y-%m-%d %H:%M:%S"), float(row[2]), float(row[3]), float(row[4]), float(row[5]),float(row[6])))
                            else:
                                return data
        else:
            print("文件不存在: " + file_path)
        start_month = start_month + relativedelta(months=1)

    return data

def get_spot_depth_data(exchange, base_symbol, asset_symbol, starttime, endtime, count = default_count):
    """
    在csv文件路径下获取 现货盘口 数据
    :params base_symbol: 基础币种, str
    :params asset_symbol: 计价币种, str
    :params starttime: 开始时间,str 格式： %Y-%M-%d %H:%m-%s
    :params count: 返回的盘口数据的数量
    :returns data: 盘口数据, list（每个元素为DepthData对象）
    """
    file_dir = get_download_path()
    start_time = dateparser(starttime)
    end_time = dateparser(endtime)
    start_month = start_time
    data = []
    global join_str

    while start_month <= end_time:
        zip_name = "Depth_Spot_" + datetime.strftime(start_month, "%Y%m") + "_" + base_symbol.lower() + "_" + asset_symbol.lower() + "_" + exchange.upper() + ".zip"
        name_list = zip_name.split('.')[0].split('_')
        zip_path = file_dir + join_str + "Depth" + join_str + name_list[1] + join_str + name_list[-3] + '_' + name_list[-2] + '_' + name_list[-1] + join_str + zip_name
        if os.path.exists(zip_path):
            import time 
            with zipfile.ZipFile(zip_path, mode='r') as zfile:
                for file_path in zfile.namelist():
                    if '.csv' in file_path:
                        file_name = file_path.split('/')[1]
                        table_date = datetime.strptime(re.search(r'[0-9]+',file_name).group(0) + ' 00:00:00', "%Y%m%d %H:%M:%S")

                        if table_date.date() >= start_month.date() and table_date.date() <= end_time.date():
                            for row in csv.reader(io.StringIO(zfile.open(file_path).read().decode('gbk'))):
                                if "DateTime" not in row:
                                        time = dateparser(row[0])
                                        if time >= start_time and time <= end_time:
                                            if len(data) < count: 
                                                depth_data = DepthData(row[1],row[0])
                                                depth_data.bids_price_list = [float(r) for r in row[2:22]]
                                                depth_data.bids_quantity_list = [float(r) for r in row[22:42]]
                                                depth_data.asks_price_list = [float(r) for r in row[42:62]]
                                                depth_data.asks_quantity_list = [float(r) for r in row[62:82]]
                                                data.append(depth_data)
                                            else:
                                                return data
                            
                        else:
                            return data
        else:
            print("文件不存在: " + zip_path)
        start_month = start_month + relativedelta(months=1)

    return data

def get_future_depth_data(exchange, base_symbol, asset_symbol, future_type, starttime, endtime, count = default_count):
    """
    在csv文件路径下获取 期货盘口 数据
    :params base_symbol: 基础币种, str
    :params asset_symbol: 计价币种, str
    :params starttime: 开始时间,str 格式： %Y-%M-%d %H:%m-%s
    :params count: 返回的盘口数据的数量
    :returns data: 盘口数据, list（每个元素为DepthData对象）
    """
    file_dir = get_download_path()
    start_time = dateparser(starttime)
    end_time = dateparser(endtime)
    start_month = start_time
    data = []
    bids_price_index= bids_quantity_index = asks_price_index = asks_qunatity_list = []
    global join_str
    
    while start_month <= end_time:
        zip_name = "Depth_" + future_type + "_" + datetime.strftime(start_month, "%Y%m") + "_" + base_symbol.lower() + "_" + asset_symbol.lower() + "_" + exchange.upper() + ".zip"
        name_list = zip_name.split('.')[0].split('_')
        zip_path = file_dir + join_str + "Depth" + join_str + name_list[1] + join_str + name_list[-3] + '_' + name_list[-2] + '_' + name_list[-1] + join_str + zip_name
        if os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path, mode='r') as zfile:
                fillename_list = [x for x in zfile.namelist() if '.csv' in x]    #  获取zip中的所有csv文件名
                for file_path in fillename_list:
                    file_name = file_path.split('/')[1]
                    table_date = datetime.strptime(re.search(r'[0-9]+',file_name).group(0) + ' 00:00:00', "%Y%m%d %H:%M:%S")
                    if table_date.date() >= start_month.date() and table_date.date() <= end_time.date():
                        for row in csv.reader(io.StringIO(zfile.open(file_path).read().decode('gbk'))):
                            if "DateTime" not in row:
                                    time = dateparser(row[0])
                                    if time >= start_time and time <= end_time:
                                        if len(data) < count:
                                            depth_data = DepthData(row[1],row[0])
                                            depth_data.bids_price_list = [float(row[i]) for i in bids_price_index]
                                            depth_data.bids_quantity_list = [float(row[i]) for i in bids_quantity_index]
                                            depth_data.asks_price_list = [float(row[i]) for i in asks_price_index]
                                            depth_data.asks_quantity_list = [float(row[i]) for i in asks_qunatity_list]                                            
                                            data.append(depth_data)
                                        else:
                                            return data
                            else:
                                asks_price_index = [row.index(x) for x in row if "AsksPrice" in x]
                                asks_qunatity_list = [row.index(x) for x in row if "AsksQuantity" in x]
                                bids_price_index = [row.index(x) for x in row if "BidsPrice" in x]
                                bids_quantity_index = [row.index(x) for x in row if "BidsQuantity" in x]
                    else:
                        return data
        else:
            print("文件不存在: " + zip_path)
        start_month = start_month + relativedelta(months=1)

    return data

def get_token(api_key, api_secret):
    '''
    通过api_key和api_secret获取用户token
    '''
    headers = {'content-type':'application/x-www-form-urlencoded'}
    url = "http://authd.matrixdata.io/api/user/token"
    data ={'grant_type':'client_credentials',
        'client_id':api_key,
        'client_secret':api_secret}
    request = requests.post(url, data=parse.urlencode(data), headers = headers)
    response = json.loads(request.text)
    token = ''

    if response["Head"]["Code"] == "200":
        token = response["Result"]["access_token"].split(' ')[1]

    return token

def get_history_kline_data_by_api(api_key, api_secret,symbol, period, starttime='', endtime='', count = default_count):
    '''
    通过api获取k线数据
    '''
    token = get_token(api_key, api_secret)
    headers = {'content-type':'application/json', 'Authorization':token}
    url = "https://dataapid.matrixdata.io/matrixdata/api/v2/barchart"
    datas = []
    start = ''
    end = ''
    if starttime != '':
        start = convert_to_timestamp(starttime)
    
    if endtime  != '':
        end = convert_to_timestamp(endtime) 

    if start == '' and end == '':
        data ={'symbol':symbol,
            'interval':period,
            'start':start,
            'end':end,
            'limit':200}

        request = requests.get(url, params=data, headers = headers)
        response = json.loads(request.text)
        datas = []

        if response["Head"]["Code"] == "200":
            if len(response["Result"]) != 0:
                for data in response["Result"]:
                    datas.append(KlineData(data["Symbol"],convert_from_timeStamp(data["Time"]), float(data["Open"]), float(data["High"]), \
                        float(data["Low"]), float(data["Close"]), float(data["QuoteVolume"]), float(data["QuoteAssetVolume"]), float(data["TradeNum"])))
            else:
                return datas
        else:
            return response["Result"]
    elif start != '' and end != '':
        current = int(start)
        end_time = int(end)

        while current < end_time:
            data ={'symbol':symbol,
                'interval':period,
                'start':str(current),
                'end':end,
                'limit':200}

            request = requests.get(url, params=data, headers = headers)
            
            if request.status_code == 200:
                response = json.loads(request.text)

                if response["Head"]["Code"] == "200":
                    if response["Result"] != None and len(response["Result"]) != 0:
                        for data in response["Result"]:
                            if len(data) < count:
                                datas.append(KlineData(data["Symbol"],convert_from_timeStamp(data["Time"]), float(data["Open"]), float(data["High"]), \
                                    float(data["Low"]), float(data["Close"]), float(data["QuoteVolume"]), float(data["QuoteAssetVolume"]), float(data["TradeNum"])))
                            else:
                                break
                    else:
                        return datas
                else:
                    return response["Result"]
                current = int(convert_to_timestamp(datas[len(datas)-1].bar_time)) + 1000
            else:
                return request.reason
        return datas
    else:
        return "不能只传end或只传start"

def get_spot_symbol_by_api(api_key, api_secret,exchange, symbol):
    '''
        通过api获取现货交易对信息
    '''
    token = get_token(api_key, api_secret)
    headers = {'content-type':'application/json', 'Authorization':token}
    url = "https://dataapid.matrixdata.io/matrixdata/api/v1/symbol/spot"
    data ={'exchange':exchange,
        'symbol':symbol}

    request = requests.get(url, params=data, headers = headers)
    response = json.loads(request.text)
    datas = []

    if response["Head"]["Code"] == "200" and len(response["Result"]) != 0:
        for data in response["Result"]:
            datas.append(SymbolModel(data["Symbol"], data["BaseAsset"], data["QuoteAsset"],\
                data["Type"]["SymbolType"], data["Type"]["SubSymbolType"], data["Status"],data["DisplaySymbol"], \
                data["TradeSymbol"], data["Exchange"], data["ListedTime"], data["DelistedTime"]))
    else:
        return response["Result"]
    
    return datas

def get_future_symbol_by_api(api_key, api_secret, exchange, symbol):
    '''
        通过api获取期货交易对信息
    '''
    token = get_token(api_key, api_secret)
    headers = {'content-type':'application/json', 'Authorization':token}
    url = "https://dataapid.matrixdata.io/matrixdata/api/v1/symbol/futures"
    data ={'exchange':exchange,
        'symbol':symbol}

    request = requests.get(url, params=data, headers = headers)
    response = json.loads(request.text)
    datas = []

    if response["Head"]["Code"] == "200" and response["Result"] != None:
        for data in response["Result"]:
            datas.append(FutureModel(data["Symbol"], data["BaseAsset"], data["QuoteAsset"],\
            data["ContractMultiple"], data["ContractMonth"], data["ListedTime"], \
            data["DeliveryDate"], data["DeliveryMonth"],data["DeliveryPrice"], data["MinPrice"], \
            data["Type"]["SymbolType"], data["Type"]["SubSymbolType"], data["Status"],data["DisplaySymbol"], \
            data["TradeSymbol"], data["Exchange"], data["LatestContract"]))
    else:
        return response["Result"]

    return datas

def get_index_symbol_by_api(api_key, api_secret,exchange, symbol):
    '''
        通过api获取指数交易对
    '''
    token = get_token(api_key, api_secret)
    headers = {'content-type':'application/json', 'Authorization':token}
    url = "https://dataapid.matrixdata.io/matrixdata/api/v1/symbol/index"
    data ={'exchange':exchange,
        'symbol':symbol}

    request = requests.get(url, params=data, headers = headers)
    response = json.loads(request.text)
    datas = []

    if response["Head"]["Code"] == "200" and len(response["Result"]) != 0:
        for data in response["Result"]:
            datas.append(IndexModel(data["Symbol"], data["BaseAsset"], data["QuoteAsset"],\
            data["Type"]["SymbolType"], data["Type"]["SubSymbolType"], data["Status"],data["DisplaySymbol"], \
            data["TradeSymbol"], data["Exchange"], data["ListedTime"], data["DelistedTime"]))
    else:
        return response["Result"]

    return datas

def get_option_symbol_by_api(api_key, api_secret, exchange, symbol):
    '''
    获取期权交易对
    :params api_key: api_key
    :params api_secret:
    :params exchange； 交易所
    :params symbol: 币种,格式为基础币种/计价币种
    :returns datas: 交易对信息
    '''
    token = get_token(api_key, api_secret)
    headers = {'content-type':'application/json', 'Authorization':token}
    url = "https://dataapid.matrixdata.io/matrixdata/api/v1/symbol/option"
    data ={'exchange':exchange,
        'symbol':symbol}

    request = requests.get(url, params=data, headers = headers)
    response = json.loads(request.text)
    datas = []

    if response["Head"]["Code"] == "200" and len(response["Result"]) != 0:
        for data in response["Result"]:
            datas.append(IndexModel(data["Symbol"], data["BaseAsset"], data["QuoteAsset"],\
            data["Type"]["SymbolType"], data["Type"]["SubSymbolType"], data["Status"],data["DisplaySymbol"], \
            data["TradeSymbol"], data["Exchange"], data["ListedTime"], data["DelistedTime"]))
    else:
        return response["Result"]
    return datas

def get_sync_spot_kline_data(exchange, base_symbol, asset_symbol, period, starttime, endtime,count = 5000):
    '''
    从本地数据库中获取同步 现货 k线数据
    :params base_symbol: 基础币种, str
    :params asset_symbol: 计价币种, str
    :params period; 时间精度, str
    :params starttime: 开始时间,str 格式： %Y-%M-%d %H:%m-%s
    :params count: 返回的k线的数量
    :returns kline_data: k线数据, list（每个元素为KlineData对象）
    '''
    symbol = (base_symbol + '/' + asset_symbol + '.' + exchange).upper() 
    sql = "select DataPacketId from (select * from datadetails d where Type = \'{0}\' and Symbol = \'{1}\' and DataType = \'{2}\' and Start <= \'{3}\' and d.Interval = \'{4}\' and TradeType = \'{5}\') a where ISNULL(a.End) or a.End <= \'{6}\'".format('DigitalCurrency', symbol, 'Kline', starttime, period, "Spot", endtime)
    data_ids = MySqLHelper().selectall(sql)

    kline_data = []

    if len(data_ids) != 0:
        for data_id in  data_ids:
            sql = "select a.symbol as symbol,  a.open as open, a.high as high,a.low as low, a.close as close, a.quotevolume as quotevolume,  a.quoteassetvolume as quoteassetvolume, (a.time AT TIME ZONE \'UTC\') as timezone from " +\
                "(select * from " + data_id +" where time >= TO_TIMESTAMP(" + convert_to_timestamp(starttime) + '::double precision / 1000) and time <= TO_TIMESTAMP(' + convert_to_timestamp(endtime) + '::double precision / 1000)) as a order by timezone limit ' + str(count)
            data = PgSqLHelper().selectall(sql)

            for row in data:
                kline_data.append(KlineData(row[0], datetime.strftime(row[7], "%Y-%m-%d %H:%M:%S"), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]),float(row[6])))
    else:
        if period != "1m": 
            sql = "select DataPacketId from (select * from datadetails d where Type = \'{0}\' and Symbol = \'{1}\' and DataType = \'{2}\' and Start <= \'{3}\' and d.Interval = \'{4}\' and TradeType = \'{5}\') a where ISNULL(a.End) or a.End <= \'{6}\'".format('DigitalCurrency', symbol, 'Kline', starttime, "1m", "Spot", endtime)
            one_min_data_ids = MySqLHelper().selectall(sql)

            if len(one_min_data_ids) != 0:
                for item in one_min_data_ids:
                    kline_data.extend(kline_integrate(period, item, starttime, endtime, count))

    return kline_data
        
def get_sync_future_kline_data(exchange, base_symbol, asset_symbol, future_type, period, starttime, endtime, count = default_count):
    '''
    从本地数据库中获取同步 期货 k线数据
    :params base_symbol: 基础币种, str
    :params asset_symbol: 计价币种, str
    :params future_type: 合约类型, str
    :params period; 时间精度, str
    :params starttime: 开始时间,str 格式： %Y-%M-%d %H:%m-%s
    :params count: 返回的k线的数量
    :returns kline_data: k线数据, list（每个元素为KlineData对象）
    '''
    symbol = (base_symbol + '/' + asset_symbol + '.' + exchange + "." + future_type).upper() 
    sql = "select DataPacketId  from (select * from datadetails d where Type = \'{0}\' and Symbol = \'{1}\' and DataType = \'{2}\' and Start <= \'{3}\' and d.Interval = \'{4}\' and TradeType = \'{5}\') a where ISNULL(a.End) or a.End <= \'{6}\'".format('DigitalCurrency', symbol, 'Kline', starttime, period, "Futures", endtime)
    data_ids = MySqLHelper().selectall(sql)

    kline_data = []

    if len(data_ids) !=0:
        for data_id in data_ids:
            sql = 'select a.symbol as symbol,  a.open as open, a.high as high,a.low as low, a.close as close, a.quotevolume as quotevolume,  a.quoteassetvolume as quoteassetvolume, (a.time AT TIME ZONE \'UTC\') as timezone from ' + \
                '(select * from ' + data_id +' where time >= TO_TIMESTAMP(' + convert_to_timestamp(starttime) + '::double precision / 1000) and time <= TO_TIMESTAMP(' + convert_to_timestamp(endtime) + '::double precision / 1000)) as a order by timezone'
            data = PgSqLHelper().selectall(sql)

            for row in data:
                kline_data.extend(KlineData(row[0], datetime.strftime(row[7], "%Y-%m-%d %H:%M:%S"), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]),float(row[6])))
    else:
        if period != "1m":        
            sql = "select DataPacketId from (select * from datadetails d where Type = \'{0}\' and Symbol = \'{1}\' and DataType = \'{2}\' and Start <= \'{3}\' and d.Interval = \'{4}\' and TradeType = \'{5}\') a where ISNULL(a.End) or a.End <= \'{6}\'".format('DigitalCurrency', symbol, 'Kline', starttime, "1m", "Futures", endtime)
            one_min_data_ids = MySqLHelper().selectall(sql)

            if len(one_min_data_ids) != 0:
                for item in one_min_data_ids:
                    kline_data.extend(kline_integrate(period, item, starttime, endtime, count))

    return kline_data

def get_sync_forex_tick_data(base_symbol, asset_symbol, starttime, endtime, count = default_count):
    """
    从本地数据库中获取同步 外汇 tick数据
    :params base_symbol: 基础币种, str
    :params asset_symbol: 计价币种, str
    :params starttime: 开始时间,str 格式： %Y-%M-%d %H:%m-%s
    :params count: 返回的k线的数量
    :returns tick_data: tick数据, list（每个元素为TickData对象）
    """
    symbol = (base_symbol + asset_symbol).upper() 
    sql = "select DataPacketId from datadetails where Type = \'{0}\' and Symbol = \'{1}\' and DataType = \'{2}\' and Start <= \'{3}\'".format('Forex', symbol, 'Tick', starttime)
    data_ids = MySqLHelper().selectall(sql)

    tick_data = []

    if len(data_ids) != 0:
        for data_id in data_ids:
            sql = 'select symbol as symbol, bid as bid, ask as ask, (time AT TIME ZONE \'UTC\') as timezone from ' + \
            '(select * from ' + data_id +' where time >= TO_TIMESTAMP(' + convert_to_timestamp(starttime) + '::double precision / 1000) and time <= TO_TIMESTAMP(' + convert_to_timestamp(endtime) + '::double precision / 1000)) as a order by timezone' + ' limit ' + str(count)
            data = PgSqLHelper().selectall(sql)

            for row in data:
                tick_data.append(TickData(row[0],datetime.strftime(row[3], "%Y-%m-%d %H:%M:%S.%f"), float(row[1]), float(row[2])))
    return tick_data   

def get_sync_forex_kline_data(base_symbol, asset_symbol, period, starttime, endtime, count = default_count):
    """
    从本地数据库中获取同步 外汇 kline数据,如果没有相应的k线数据，则用tick数据聚合
    :params base_symbol: 基础币种, str
    :params asset_symbol: 计价币种, str
    :params period; 时间精度, str
    :params starttime: 开始时间,str 格式： %Y-%M-%d %H:%m-%s
    :params count: 返回的k线的数量
    :returns kline_data: k线数据, list（每个元素为KlineData对象）
    """

    symbol = (base_symbol + asset_symbol).upper() 
    sql = "select DataPacketId from datadetails a where Type = \'{0}\' and Symbol = \'{1}\' and DataType = \'{2}\' and Start <= \'{3}\' and a.Interval = \'{4}\'".format('Forex', symbol, 'Kline', starttime, period)
    data_ids = MySqLHelper().selectall(sql)

    kline_data = []

    if len(data_ids) != 0:
        for data_id in data_ids:
            sql = 'select a.symbol as symbol,  a.open as open, a.high as high,a.low as low, a.close as close, (a.time AT TIME ZONE \'UTC\') as timezone from ' + \
                '(select * from ' + data_id +' where time >= TO_TIMESTAMP(' + convert_to_timestamp(starttime) + '::double precision / 1000) and time <= TO_TIMESTAMP(' + convert_to_timestamp(endtime) + '::double precision / 1000)) as a order by timezone limit ' + str(count)
            data = PgSqLHelper().selectall(sql)

            if len(data) != 0:
                for row in data:
                    kline_data.append(KlineData(bar_time = datetime.strftime(row[5], "%Y-%m-%d %H:%M:%S"), symbol = row[0], open = float(row[1]), high = float(row[2]), low = float(row[3]), close = float(row[4])))
            else:
                sql = "select DataPacketId from datadetails where Type = \'{0}\' and Symbol = \'{1}\' and DataType = \'{2}\' and Start <= \'{3}\'".format(
                    'Forex', symbol, 'Tick', starttime)
                tick_data_ids = MySqLHelper().selectall(sql)

                if len(tick_data_ids) != 0:
                    for d in tick_data_ids:
                        multiple_time_data = tick_integrate(period, d, starttime, endtime, count)
                        for m in multiple_time_data:
                            kline_data.append(m)
    else:
        if period != "1m":        
            sql = "select DataPacketId from datadetails a where Type = \'{0}\' and Symbol = \'{1}\' and DataType = \'{2}\' and Start <= \'{3}\' and a.Interval = \'{4}\'".format('Forex', symbol, 'Kline', starttime, "1m")
            one_min_data_ids = MySqLHelper().selectall(sql)

            if len(one_min_data_ids) != 0:
                for d in one_min_data_ids:
                    multiple_time_data = forex_kline_integrate(period, d, starttime, endtime, count)
                    for m in multiple_time_data:
                        kline_data.append(m)
        else:
            sql = "select DataPacketId from datadetails where Type = \'{0}\' and Symbol = \'{1}\' and DataType = \'{2}\' and Start <= \'{3}\'".format('Forex', symbol, 'Tick', starttime)
            tick_data_ids = MySqLHelper().selectall(sql)

            if len(tick_data_ids) != 0:
                for d in tick_data_ids:
                    multiple_time_data = tick_integrate(period, d, starttime, endtime, count)
                    for m in multiple_time_data:
                        kline_data.append(m)
            
    return kline_data   

def kline_integrate(period, data_id, starttime , endtime, count):
    """
    用1分钟k线数据合成其他时间精度数据
    :parmas period: 时间精度, str
    :params data_id: 存放在本地数据库中的数据库表名
    :params starttime: 开始时间, str
    :params endtime: 结束时间, str
    :params count: 数量
    :returns kline_integrate_data: k线数据, list（每个元素为KlineData对象）
    """
    kline_integrate_data = [] 
    period_num = re.search('[0-9]+', period).group(0)
    period_type = ''

    if 'm' in period:
        period_type = 'minutes'
    elif 'h' in period:
        period_type = 'hours'
    elif 'd' in period:
        period_type = 'days'

    sql_base = 'select * from ' + data_id + " where time >= TO_TIMESTAMP(" + convert_to_timestamp(starttime) + '::double precision / 1000) and time <= TO_TIMESTAMP(' + convert_to_timestamp(endtime)  + '::double precision / 1000)'
    sql_bucket = " SELECT a.symbol AS symbol, first(a.open,a.time) AS open, max(a.high) AS high, min(a.low) AS low, last(a.close,a.time) AS close, " + \
            "sum(a.quotevolume) AS quotevolume, sum(a.quoteassetvolume) AS quoteassetvolume , time_bucket(\'" + period_num + " " + period_type + "\', a.time AT TIME ZONE \'UTC\') AS multiple_time FROM (" + sql_base + \
            ") as a GROUP BY multiple_time, symbol  ORDER BY multiple_time limit " + str(count)
    data = PgSqLHelper().selectall(sql_bucket)

    for row in data:
        kline_integrate_data.append(KlineData(row[0], datetime.strftime(row[7], "%Y-%m-%d %H:%M:%S"), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]),float(row[6])))

    return kline_integrate_data

def forex_kline_integrate(period, data_id, starttime , endtime, count):
    """
    用 外汇1分钟 k线数据 合成其他时间精度数据
    :parmas period: 时间精度, str
    :params data_id: 存放在本地数据库中的数据库表名
    :params starttime: 开始时间, str
    :params endtime: 结束时间, str
    :params count: 数量
    :returns kline_integrate_data: k线数据, list（每个元素为KlineData对象）
    """
    kline_integrate_data = [] 
    period_num = re.search('[0-9]+', period).group(0)
    period_type = ''

    if 'm' in period:
        period_type = 'minutes'
    elif 'h' in period:
        period_type = 'hours'
    elif 'd' in period:
        period_type = 'days'

    sql_base = 'select * from ' + data_id + " where time >= TO_TIMESTAMP(" + convert_to_timestamp(starttime) + '::double precision / 1000) and time <= TO_TIMESTAMP(' + convert_to_timestamp(endtime)  + '::double precision / 1000)'
    sql_bucket = " SELECT a.symbol AS symbol, first(a.open,time) AS open, max(a.high) AS high, min(a.low) AS low, last(a.close,time) AS close, " + \
            "time_bucket(\'" + period_num + " " + period_type + "\', a.time AT TIME ZONE \'UTC\') AS multiple_time FROM (" + sql_base + \
            ") as a GROUP BY multiple_time, symbol  ORDER BY multiple_time limit " + str(count)
    data = PgSqLHelper().selectall(sql_bucket)

    for row in data:
        kline_integrate_data.append(KlineData(row[0], datetime.strftime(row[5], "%Y-%m-%d %H:%M:%S"), float(row[1]), float(row[2]), float(row[3]), float(row[4])))        

    return kline_integrate_data

def tick_integrate(period, data_id, starttime , endtime, count):
    """
    用 外汇tick数据 整合成其他分钟精度数据
    :parmas period: 时间精度, str
    :params data_id: 存放在本地数据库中的数据库表名
    :params starttime: 开始时间, str
    :params endtime: 结束时间, str
    :params count: 数量
    :returns kline_integrate_data: k线数据, list（每个元素为KlineData对象）
    """
    kline_integrate_data = [] 
    period_num = re.search('[0-9]+', period).group(0)
    period_type = ''

    if 'm' in period:
        period_type = 'minutes'
    elif 'h' in period:
        period_type = 'hours'
    elif 'd' in period:
        period_type = 'days'
    elif 's' in period:
        period_type = 'seconds'
    else:
        pass

    sql_base = 'select * from ' + data_id + " where time >= TO_TIMESTAMP(" + convert_to_timestamp(starttime) + '::double precision / 1000) and time <= TO_TIMESTAMP(' + convert_to_timestamp(endtime)  + '::double precision / 1000)'
    sql_bucket = " SELECT a.symbol AS symbol, first(a.bid,time) AS open, max(a.bid) AS high, min(a.bid) AS low, last(a.bid,time) AS close, " + \
            "time_bucket(\'" + period_num + " " + period_type + "\', a.time AT TIME ZONE \'UTC\') AS multiple_time FROM (" + sql_base + \
            ") as a GROUP BY multiple_time, symbol  ORDER BY multiple_time limit " + str(count)
    data = PgSqLHelper().selectall(sql_bucket)

    for row in data:
        kline_integrate_data.append(KlineData(row[0], datetime.strftime(row[5], "%Y-%m-%d %H:%M:%S"), float(row[1]), float(row[2]), float(row[3]), float(row[4])))        

    return kline_integrate_data