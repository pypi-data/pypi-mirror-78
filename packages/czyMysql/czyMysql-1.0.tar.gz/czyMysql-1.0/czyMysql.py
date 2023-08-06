'''
@File       : czyMysql.py
@Copyright  : rainbol
@Date       : 2020/9/7
@Desc       :
'''
import threading

import pymysql
from DBUtils.PooledDB import PooledDB

MYSQL_INFO = {
    'host': '<>',
    'user': 'root',
    'password': 'root',
    'db': '<>',
    'port': 3306,
    'charset': 'utf8',
    'autocommit': True  # 自动commit
}

# mysql连接池
POOL_INFO = {
    'host': '<>',  # ip
    'user': 'root',  # username
    'password': 'root',  # password
    'db': '<>',  # database
    'port': 3306,  # port
    'charset': 'utf8',  # coded set
    'creator': pymysql,  # 选择pymysql
    'maxconnections': 20,  # 数据库连接池最大连接数
    'mincached': 5,  # 数据库连接池最小缓存数
    'maxcached': 5,  # 数据库连接池最大缓存数
    'cursorclass': pymysql.cursors.DictCursor,  # 返回方式dict形式
    'blocking': True,  # 当连接数达到最大的连接数时，在请求连接的时候，
    # 如果这个值是True，请求连接的程序会一直等待，直到当前连接数小于最大连接数，如果这个值是False，会报错
    'maxshared': 20  # 当连接数达到这个数，新请求的连接会分享已经分配出去的连接
}


class Singleton(object):
    '''线程安全——单例模式'''
    _instance = None
    lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        if cls._instance:
            return cls._instance
        with cls.lock:
            if not cls._instance:
                cls._instance = object.__new__(cls)
            return cls._instance


class MySQL(Singleton):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, p=False):  # 选择是否使用普通连接或者连接池
        self.p = p
        if not self.p:
            try:
                self.conn = pymysql.connect(**MYSQL_INFO)
            except Exception as e:
                print("Failed to connect to the database, please view the configuration file,%s" % e)
            else:
                self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        else:
            try:
                self.pool_db = PooledDB(**POOL_INFO)
            except Exception as e:
                print(
                    "Failed to connect to the database or can't create connect pool,"
                    "please view the configuration file,%s" % e)
            else:
                self.__pool = self.pool_db.connection()
                self.cur = self.__pool.cursor()

    def execute_one(self, sql):
        try:
            self.cur.execute(sql)
        except Exception as e:
            print("Execute error, please check the SQL statement\n%s" % e)
        else:
            return self.cur.fetchone()

    def execute_many(self, sql):
        try:
            self.cur.execute(sql)
        except Exception as e:
            print("Execute error, please check the SQL statement\n%s" % e)
        else:
            return self.cur.fetchall()

    def __del__(self):
        self.cur.close()
        if self.p:
            self.__pool.close()
