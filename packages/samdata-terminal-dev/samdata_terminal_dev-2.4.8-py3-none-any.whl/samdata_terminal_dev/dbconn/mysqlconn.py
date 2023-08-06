from DBUtils.PooledDB import PooledDB
from .db_config import config
import traceback

"""
@功能：创建数据库连接池
"""

class MyConnectionPool(object):
    __pool = None

    # def __init__(self):
    #     self.conn = self.__getConn()
    #     self.cursor = self.conn.cursor()

    # 创建数据库连接conn和游标cursor
    def __enter__(self):
        self.conn = self.__getconn()
        self.cursor = self.conn.cursor()

    # 创建数据库连接池
    def __getconn(self):
        if self.__pool is None:
            self.__pool = PooledDB(
                creator=config.MYSQL_DB_CREATOR,
                mincached=config.DB_MIN_CACHED,
                maxcached=config.DB_MAX_CACHED,
                maxshared=config.DB_MAX_SHARED,
                maxconnections=config.DB_MAX_CONNECYIONS,
                blocking=config.DB_BLOCKING,
                maxusage=config.DB_MAX_USAGE,
                setsession=config.DB_SET_SESSION,
                host=config.MYSQL_DB_HOST,
                port=config.MYSQL_DB_PORT,
                user=config.MYSQL_DB_USER,
                passwd=config.MYSQL_DB_PASSWORD,
                db=config.MYSQL_DB_DBNAME,
                charset=config.DB_CHARSET
            )
        return self.__pool.connection()

    # 释放连接池资源
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    # 关闭连接归还给链接池
    def close(self):
         self.cursor.close()
         self.conn.close()

    # 从连接池中取出一个连接
    def getconn(self):
        try:
            conn = self.__getconn()
            cursor = conn.cursor()
            return cursor, conn
        except Exception as ex:
            print("连接mysql数据库失败")
            traceback.print_exc()

# 获取连接池,实例化
def get_my_connection():
    return MyConnectionPool()