"""
    数据库辅助类
"""
from ..dbconn.mysqlconn import get_my_connection
import traceback

"""执行语句查询有结果返回结果没有返回0；增/删/改返回变更数据条数，没有返回0"""


class MySqLHelper(object):
    def __init__(self):
        self.db = get_my_connection()  # 从数据池中获取连接

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'inst'):  # 单例
            cls.inst = super(MySqLHelper, cls).__new__(cls, *args, **kwargs)
        return cls.inst

    # 封装执行命令
    def execute(self, sql, param=None, autoclose=False):
        """
        【主要判断是否有参数和是否执行完就释放连接】
        :param sql: 字符串类型，sql语句
        :param param: sql语句中要替换的参数"select %s from tab where id=%s" 其中的%s就是参数
        :param autoclose: 是否关闭连接
        :return: 返回连接conn和游标cursor
        """
        cursor, conn = self.db.getconn()  # 从连接池获取连接
        count = 0
        try:
            # count : 为改变的数据条数
            if param:
                count = cursor.execute(sql, param)
            else:
                count = cursor.execute(sql)
            conn.commit()
            if autoclose:
                self.close(cursor, conn)
        except Exception as e:
            print("插入数据库报错： " )
            print(e)
            traceback.print_exc()
        return cursor, conn, count

    # 释放连接
    def close(self, cursor, conn):
        """释放连接归还给连接池"""
        cursor.close()
        conn.close()

    # 查询所有
    def selectall(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            res = [d[0] for d in cursor.fetchall()]
            return res
        except Exception as e:
            print("从数据库中获取所有信息出错: ")
            print(sql)
            print(e)
            self.close(cursor, conn)
            traceback.print_exc()
            return count

    # 查询单条
    def selectone(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            res = cursor.fetchone()
            self.close(cursor, conn)
            return res
        except Exception as e:
            print("执行单条数据查询出错:"+ str(e.args))
            traceback.print_exc()
        finally:
            self.close(cursor, conn)
            return count

    # 增加
    def insertone(self, sql, param):
        try:
            cursor, conn, count = self.execute(sql, param)
            conn.commit()
            self.close(cursor, conn)
            return count
        except Exception as e:
            print("往数据库中插入数据时出错: ")
            print(sql)
            print(e)
            conn.rollback()
            traceback.print_exc()
            self.close(cursor, conn)
            return count

    # 增加多行
    def insertmany(self, sql, param):
        """
        :param sql:
        :param param: 必须是元组或列表[(),()]或（（），（））
        :return:
        """
        cursor, conn = self.db.getconn()
        try:
            count = cursor.executemany(sql, param)
            conn.commit()
            self.close(cursor, conn)
            return count
        except Exception as e:
            print("往数据库中插入数据时出错: ")
            print(sql)
            print(e.args)
            conn.rollback()
            traceback.print_exc()
            self.close(cursor, conn)

    # 删除
    def delete(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            self.close(cursor, conn)
            return count
        except Exception as e:
            print("删除数据库出错： "+ sql)
            print(e)
            conn.rollback()
            traceback.print_exc()
            self.close(cursor, conn)
            return count

    # 更新
    def update(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            conn.commit()
            self.close(cursor, conn)
            return count
        except Exception as e:
            print("更新数据库出错： "+ sql)
            print(e)
            conn.rollback()
            traceback.print_exc()
            self.close(cursor, conn)
            return count
