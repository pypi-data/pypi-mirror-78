# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     database
   Description :
   Author :        Asdil
   date：          2020/8/24
-------------------------------------------------
   Change Activity:
                   2020/8/28:
-------------------------------------------------
"""
__author__ = 'Asdil'
import psycopg2
from psycopg2 import pool
from DBUtils.PersistentDB import PersistentDB
import pymysql


class Psycopg:
    """
    Psycopg类用于链接Psycopg
    """

    def __init__(self, host, port, user, password, database, minconn=2, maxconn=10):
        """__init__(self):方法用于

        Parameters
        ----------
        host : str
            host地址
        port : int
            端口
        user : str
            用户名
        password : str
            密码
        database : str
            数据库名称
        minconn : int
            最小连接数
        maxconn : int
            最大连接数

        Returns
        ----------
        """
        try:
            self.connectPool = pool.ThreadedConnectionPool(minconn, maxconn, host=host, port=port,
                                                           user=user, password=password,
                                                           database=database)

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)

    def get_connect(self):
        """getConnect方法用于生成新连接"""
        conn = self.connectPool.getconn()
        cursor = conn.cursor()
        return conn, cursor

    def close_connect(self, conn, cursor):
        """closeConnect方法用于关闭连接

        Parameters
        ----------
        cursor : object
            游标
        conn : object
            连接
        Returns
        ----------
        """
        cursor.close()
        self.connectPool.putconn(conn)

    def close_all(self):
        """close_all方法用于断开连接

        Parameters
        ----------
        param : str

        Returns
        ----------
        """
        self.connectPool.closeall()

    def select_one(self, sql, args=None):
        """select_one方法用于查找一条数据

        Parameters
        ----------
        sql : str
            查询语句
        args : list or None
            参数
        Returns
        ----------
        """
        conn, cursor = self.get_connect()
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        result = cursor.fetchone()
        self.close_connect(conn, cursor)
        return result

    def select_all(self, sql, args):
        """select_all方法用于查找所有记录

        Parameters
        ----------
        sql : str
            sql语句
        args : list or None
            参数
        Returns
        ----------
        """
        conn, cursor = self.get_connect()
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        result = cursor.fetchall()
        self.close_connect(conn, cursor)
        return result

    def excute(self, sql, value=None):
        """excute方法用于增删查改

        Parameters
        ----------
        sql : str
            sql 语句
        value : list or None
            值列表
        Returns
        ----------
        """
        conn, cursor = self.get_connect()
        try:
            res = cursor.execute(sql, value)
            conn.commit(conn, cursor)
            self.close_connect(conn, cursor)
            return res
        except Exception as e:
            conn.rollock()
            raise e


class Mysql:
    """
    Mysql类用于mysql连接池操作
    """
    def __init__(self, host, port, user, password, database):
        """__init__(self):方法用于

        Parameters
        ----------
        host : str
            host地址
        port : int
            端口
        user : str
            用户名
        password : str
            密码
        database : str
            数据库名称

        Returns
        ----------
        """
        self.pool = PersistentDB(
            creator=pymysql,  # 使用连接数据库模块
            maxusage=None,  # 连接超时时间
            setsession=[],  # 开始会话前执行的操作
            ping=0,  # ping服务器端查看是否可用
            closeable=False,  # 实际上被忽略，供下次使用，再线程关闭时，才会自动关闭链接。如果为True时， conn.close()则关闭链接，
            # 那么再次调用pool.connection时就会报错，因为已经真的关闭了连接（pool.steady_connection()可以获取一个新的链接
            threadlocal=None,  # 本线程独享值得对象，用于保存链接对象，如果链接对象被重置
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8')

    def select_one(self, sql, args=None):
        """select_one方法用于查询一条数据

        Parameters
        ----------
        sql : str
            sql 语句
        args : list or tuple
            参数
        Returns
        ----------
        """
        conn = self.pool.connection(shareable=False)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def select_all(self, sql, args=None):
        """select_all方法用于查询所有数据

        Parameters
        ----------
        sql : str
            sql 语句
        args : list or tuple or None
            参数
        Returns
        ----------
        """
        if not args:
            args = tuple(args)
        conn = self.pool.connection(shareable=False)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        conn.close()
        return result

    def excute(self, sql, args=None):
        """excute方法用于增删查改

        Parameters
        ----------
        param : str

        Returns
        ----------
        """
        if not args:
            args = tuple(args)
        conn = self.pool.connection(shareable=False)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        conn.commit()
        conn.close()


def optimize_expression(sql, params):
    """optimize_expression方法用于优化sql表达式
    使用方法:
        sql = "select * from table1 where age=%s and name in (%s)"
        params = [10, ['Tom', 'Jim']]
        sql, params = optimize_expression(sql, params)
    Parameters
    ----------
    sql : str
        sql语句
    params ： 参数列表

    Returns
    ----------
    """
    new_params = []
    codes = []
    for param in params:
        if isinstance(param, list):
            new_params.extend(list(map(str, param)))
            codes.append(','.join(['%s']*len(param)))
        else:
            new_params.append(param)
            codes.append('%s')
    sql = sql % tuple(codes)
    return sql, new_params


