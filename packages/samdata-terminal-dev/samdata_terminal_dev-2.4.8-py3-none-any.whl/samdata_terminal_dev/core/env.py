# -*- encoding:utf-8 -*-
"""
    全局环境配置模块
"""

from enum import Enum

class EDataSourceType(Enum):
    """
        数据源，当数据获取不可靠时，可尝试切换数据源，更可连接私有的数据源
    """
    """本地csv路径"""
    E_DATA_SOURCE_CSV= 1
    """api"""
    E_DATA_SOURCE_API= 2
    """同步数据库"""
    E_DATA_SOURCE_DB= 3
    """自定义数据源"""
    E_DATA_SOURCE_CUSTOMIZE = 4
    """IB实时数据源"""
    E_DATA_SOURCE_LIVE_IB = 5
    """Lamx实时数据源"""
    E_DATA_SOURCE_LIVE_LAMX = 6

class EMarketType(Enum):
    """
        市场类型
    """
    """ 数字货币 """
    E_MARKET_TYPE_DigitalCurrency = "DigitalCurrency"
    """外汇数据"""
    E_MARKET_TYPE_Forex = "Forex"

class EDataType(Enum):
    """
        数据类型
    """
    """k线"""
    E_Data_Kline = 0
    """盘口"""
    E_Data_Depth = 1
    """Tick"""
    E_Data_Tick = 2

class EModeType(Enum):
    """
        策略模式
    """
    """ 回测模式 """
    BACKTEST = "backtest"
    """ 实盘模式 """
    LIVE = "live"

"""默认设置数据源使用E_MARKET_SOURCE_csv"""
get_public_data_source = EDataSourceType.E_DATA_SOURCE_CSV
"""私有数据源"""
get_private_data_source = None
"""市场类型设置"""
get_market_type = None
"""策略模式设置"""
get_mode = None


class EMarketDataSplitMode(Enum):
    """
        ABuSymbolPd中请求参数，关于是否需要与基准数据对齐切割
    """
    """直接取出所有data，不切割，即外部需要切割"""
    E_DATA_SPLIT_UNDO = 0
    """内部根据start，end取切割data"""
    E_DATA_SPLIT_SE = 1