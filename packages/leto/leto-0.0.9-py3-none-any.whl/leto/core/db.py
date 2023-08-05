# -*- coding: utf-8 -*-
# @author: leesoar

"""数据库操作

Usage:
    mysql = Mysql()

    sql = "select id, name from table_a"
    res = mysql.exec(sql)
    mysql.log.debug(res)
"""

import abc

import psycopg2
import pymysql
import redis

from ..util.decorator import mysql_dba, retry
from ..util.logger import Logger


class BaseDb(object, metaclass=abc.ABCMeta):
    """各数据库操作的基类"""

    def __new__(cls, *args, **kwargs):
        """限制客户端实例创建，避免建立多个客户端连接"""
        if not hasattr(cls, 'inst'):
            cls.inst = super().__new__(cls)
        return cls.inst

    def __init__(self):
        self.log = Logger(f"{__name__}.log").get_logger()


class Mysql(BaseDb):
    """MySQL的操作类"""

    def __init__(self, _config):
        super().__init__()
        self._config = _config
        self._conn = None
        self._cursor = None

    def _connect(self):
        return pymysql.connect(**self._config)

    def set_config(self, cfg):
        self._config = cfg

    @retry()
    @mysql_dba
    def exec(self, sql, data=None, is_dict=False):
        """执行sql

        对数据库的操作，返回元组、字典或None

        Usage:
            sql = "insert ignore into table_a(uid, name) values(%s, %s)"
            data = {"uid": "888", "name": "leesoar"}
            # or data = ["888", "leesoar"]
            # or data = ("888", "leesoar")
            mysql.exec(sql, data=data)
        Args:
            sql: 数据库语句(DDL, DML等)
            data: 插入时使用，默认为None。类型可为list, tuple, dict
            is_dict: 确定返回结果的类型。默认为False，即返回元组
        Returns:
            执行结果。tuple, dict or None
        """
        with self._conn.cursor(is_dict and pymysql.cursors.DictCursor) as cursor:
            self._cursor = cursor
            self._cursor.execute(sql, data)
            result = cursor.fetchall()
        return result

    @retry()
    @mysql_dba
    def exec_many(self, sql, data=None, is_dict=False):
        """执行sql

        对数据库的操作，返回元组、字典或None

        Usage:
            sql = "insert ignore into table_a(uid, name) values(%s, %s)"
            data = {"uid": "888", "name": "leesoar"}
            # or data = ["888", "leesoar"]
            # or data = ("888", "leesoar")
            mysql.exec(sql, data=data)
        Args:
            sql: 数据库语句(DDL, DML等)
            data: 插入时使用，默认为None。类型可为list, tuple, dict
            is_dict: 确定返回结果的类型。默认为False，即返回元组
        Returns:
            执行结果。tuple, dict or None
        """
        with self._conn.cursor(is_dict and pymysql.cursors.DictCursor) as cursor:
            self._cursor = cursor
            self._cursor.executemany(sql, data)
            result = cursor.fetchall()
        return result


class PostgreSql(BaseDb):
    """PostgreSQL的操作类"""

    def __init__(self, _config):
        super().__init__()
        self._config = _config
        self._conn = None
        self._cursor = None

    def _connect(self):
        return psycopg2.connect(**self._config)

    def set_config(self, cfg):
        self._config = cfg

    @retry()
    def exec(self, sql, *args):
        """执行sql"""
        with self._connect() as conn:
            self._conn = conn
            with conn.cursor() as cursor:
                if len(args) == 0:
                    cursor.execute(sql)
                elif len(args) != 1:
                    cursor.executemany(sql, args)
                else:
                    cursor.execute(sql, *args)

                try:
                    ret = cursor.fetchall()
                except psycopg2.ProgrammingError:
                    ret = None
        self._conn and self._conn.close()
        return ret


class Redis(BaseDb):
    """Redis的操作类"""

    def __init__(self, _config):
        super().__init__()
        self._conn = redis.Redis(connection_pool=redis.ConnectionPool(**_config))

    def get_client(self):
        return self._conn


if __name__ == "__main__":
    pass
