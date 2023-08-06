from ..core.storage import context

class DataSourceExcetion(Exception):
    def __init__(self):
        context.trader.stop()