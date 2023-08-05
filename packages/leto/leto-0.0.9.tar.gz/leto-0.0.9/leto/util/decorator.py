# -*- coding: utf-8 -*-
# @author: leesoar

"""装饰器"""

import functools
import traceback

import pymysql
import retrying

from ..common import config, const
from ..util.base import extract, random_ip
from ..util.logger import Logger


log = Logger(f"{__name__}.log").get_logger()


def retry(max_retries=3, min_wait=0, max_wait=1):
    """函数重试器

    Args:
        max_retries: 最大重试次数，默认3次
        min_wait: 最小间隔时间。默认为0。单位：秒（sec）
        max_wait: 最大间隔时间。默认为1
    Returns:
        被装饰函数的返回结果
    """
    def decorator(func):
        @retrying.retry(stop_max_attempt_number=max_retries,
                        wait_random_min=min_wait * const.Unit.ONE_SEC_AS_MS,
                        wait_random_max=max_wait * const.Unit.ONE_SEC_AS_MS)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


def mysql_dba(func):
    """MySQL的装饰器

    提供事务提交、异常捕获、回滚、连接断开等功能

    """
    @functools.wraps(func)
    def wrapper(cls, *args, **kwargs):
        try:
            cls._conn = cls._connect()
            cls.log.debug("【Start】Start transaction...")
            cls._conn.begin()
            # cls.log.debug(f"【SQL】{kwargs.get('sql') or args[0]}")   # 打印sql模版
            res = func(cls, *args, **kwargs)
            cls.log.debug(f"【SQL】{cls._cursor._executed}")   # 打印解析后的sql
        except pymysql.err.Error as e:
            cls.log.error(f"【Plain】{e}")
            config.TRACEBACK and cls.logging.error(f"【Error】\n{traceback.format_exc()}\n\t【Error's end】\n\n")
            cls.log.debug("【Rollback】Rollback...")
            cls._conn.rollback()
            cls.log.debug("【Rollback】Rollback was done.")
        else:
            cls._conn.commit()
            cls.log.debug("【Success】Transaction was committed.")
            return res
        finally:
            cls._conn.close()
            cls.log.debug("【Finish】Connection was closed.")
    return wrapper


def daemon(func):
    """守护队列操作

    提供队列日志打印及异常重试

    """
    @retry()
    @functools.wraps(func)
    def wrapper(cls, *args, **kwargs):
        try:
            cls.log.debug(f"操作：{func.__name__}")
            cls.log.debug(f"队列：{cls.wear(extract(args), kwargs.get('mark') or func.__kwdefaults__['mark'])}")
            res = func(cls, *args, **kwargs)
            try:
                if "set" in func.__name__:
                    cls.log.debug(f"结果：当前存储{res['now']}个种子，库中共有{res['all']}个种子。")
                elif "get" in func.__name__:
                    cls.log.debug(f"结果：{len(res) if isinstance(res, (tuple, list)) else res}")
                else:
                    cls.log.debug("结果：success")
            except TypeError:   # 无种子时捕获异常
                cls.log.warn("结果：fail, no seed")
        except (KeyboardInterrupt, SystemExit) as e:
            cls.log.warn("捕获到主动退出，取消重试，一切正常。")
            raise e
        else:
            return res
    return wrapper


def ninja(func):
    """针对普通代理伪装头信息"""
    def wrapper(cls, *args, **kwargs):
        if cls.ninja_mode is not True:
            return func(cls, *args, **kwargs)

        headers = kwargs.get("headers", {})
        ip = random_ip()
        headers.update({"x-forward-for": ip, "client-ip": ip})
        kwargs['headers'] = headers
        res = func(cls, *args, **kwargs)
        return res
    return wrapper


def bit_bucket(filters=(), callback=None, *call_args, **call_kwargs):
    """位桶，捕获并吞噬一切异常

    Args:
        filters: 字符串组成的容器。在过滤器中的异常，不会被捕获（重新raise）
        callback: 异常回调函数
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                ret = func(*args, **kwargs)
            except Exception as e:
                if e.__class__.__name__ in filters:
                    raise e

                # 异常回调
                if hasattr(bit_bucket, "callback"):
                    bit_bucket.callback()
                elif hasattr(callback, '__call__'):
                    callback(*call_args, **call_kwargs)
            else:
                return ret
        return wrapper
    return decorator
