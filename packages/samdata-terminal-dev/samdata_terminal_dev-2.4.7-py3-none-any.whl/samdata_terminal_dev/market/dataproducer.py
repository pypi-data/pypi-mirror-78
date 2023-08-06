import threading
from dateutil.parser import parse as dateparser
import time

from ..core import env
from ..core.env import EDataSourceType
from ..exceptions.dataexception import DataSourceExcetion

from .datafeed import CsvKlineApi, CsvDepthApi,ApiKlineApi, DbKlineApi, DbTickApi

data_time_count = 0

max_size = 10000

class DataProducer(threading.Thread):
    """
    单个交易对数据生产者
    """
    def __init__(self, t_name, symbol, period, starttime, endtime, data_type, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue
        self.symbol = symbol
        self.period = period
        self.data_type = data_type
        self.endtime = endtime
        self.starttime = starttime
        self.last_data = None
        self._stop_event = threading.Event()

    def run(self):
        """
        往数据队列中存放指定数据
        """
        try:
            source = None

            # 获取数据源类
            if env.get_private_data_source is None:
            # 没有设置私有源
                if env.get_public_data_source == EDataSourceType.E_DATA_SOURCE_CSV:
                    if self.data_type == "kline":
                        source = CsvKlineApi
                    elif self.data_type == "depth":
                        source = CsvDepthApi
                elif env.get_public_data_source == EDataSourceType.E_DATA_SOURCE_API:
                    if self.data_type == "kline":
                        source = ApiKlineApi
                elif env.get_public_data_source == EDataSourceType.E_DATA_SOURCE_DB:
                    if self.data_type == "kline":
                        source = DbKlineApi
                    elif self.data_type == "tick":
                        source = DbTickApi
            else:
                # 设置数据源
                source = env.get_private_data_source

            if source is None:
                print("数据源无效， 请检查该数据源是否存在")
                raise DataSourceExcetion

            start = self.starttime
            if self.data_type == "kline":
                temp_source = source(self.symbol, self.period)
            else:
                temp_source= source(self.symbol)

            is_end = False          # 是否结束生产数据
            is_load_data = False    # 是否下载数据

            while not is_end and not self._stop_event.is_set():
                if dateparser(start) < dateparser(self.endtime) and start != None:
                    if not is_load_data:
                        global  max_size
                        if self.data.qsize() <= int(max_size * 0.5)  or self.data.qsize() == 0:
                            is_load_data = True
                            d = temp_source.get_data(start, self.endtime)

                            if self.last_data is not None and d[0] == self.last_data:
                                d = d[1:]

                            if len(d) != 0:
                                for item in d:
                                    if dateparser(item.bar_time) < dateparser(self.endtime):
                                        kline_data = {}
                                        kline_data[self.symbol] = []
                                        kline_data[self.symbol].append(item)
                                        self.data.put(kline_data)

                                start = d[-1].bar_time
                                self.last_data = d[-1]
                            else:
                                break

                            is_load_data = False
                        else:
                            is_end = True
                            # time.sleep(0.002)
                else:
                    time.sleep(0.002)
                    is_end = True
            self.data.put("finish")
        except BaseException as e:
            print(e.args)

    def stop(self):
        self._stop_event.set()

