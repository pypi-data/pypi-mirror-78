# -*- coding: utf-8 -*-
# @author: leesoar

"""队列调度

Usage:
    queue = RedisQueue()

    key = "xxx"
    seed = queue.get_seed(key)
"""

import abc
import json
import queue as _queue

from ..common import config
from ..core.db import Redis
from ..util.base import extract
from ..util.decorator import daemon, retry
from ..util.logger import Logger


__all__ = ["RedisQueue", "MicroQueue", ]


class Queue(object, metaclass=abc.ABCMeta):
    """消息队列基类"""

    def __init__(self):
        self.log = Logger(f"{__name__}.log").get_logger()

    @abc.abstractmethod
    def get_seed(self, key, *, args):
        pass

    @abc.abstractmethod
    def set_seed(self, key, seed, args):
        pass

    @abc.abstractmethod
    def clear(self, key, *, args):
        pass


class MicroQueue(Queue):
    """微队列"""

    def __init__(self):
        super().__init__()
        self._pool = {}

    def get_seed(self, key, *args):
        queue_ = self._pool.get(key)

        assert queue_, \
            "The key has no queue."

        if queue_.empty():
            return
        return queue_.get()

    def set_seed(self, key, *seed):
        queue_ = self._pool.get(key)

        if not queue_:
            self._pool[key] = _queue.Queue()
            queue_ = self._pool[key]

        for s in seed:
            queue_.put(s)

    def clear(self, key, *args):
        self._pool[key].queue.clear()

    def qsize(self, key):
        return self._pool[key].qsize()


class RedisQueue(Queue):
    """redis消息队列"""

    def __init__(self, _config):
        super().__init__()
        self._redis = Redis(_config).get_client()

    def get_client(self):
        """返回redis client

        以便调用类里面未实现的操作
        """
        return self._redis

    @staticmethod
    def wear(key, mark):
        """为队列添加标志后缀"""
        return f"{key}:{mark.upper()}"

    @staticmethod
    def drop_mark(key):
        """去除队列标记"""
        return extract(key.rsplit(":", maxsplit=1))

    @daemon
    def get_seed(self, key, *, mark=config.FLAG_ENC, head=True):
        """获取并删除种子

        Args:
            key: 队列名
            mark: 队列标记
            head: 从队列头部获取并弹出，默认队列模式
        Returns:
            种子信息。None或dict
        """
        if head:
            seed = self._redis.lpop(self.wear(key, mark))
        else:
            seed = self._redis.rpop(self.wear(key, mark))
        try:
            return seed and json.loads(seed)
        except json.decoder.JSONDecodeError:
            return seed

    @daemon
    def get_seeds(self, key, size, *, mark=config.FLAG_ENC, head=True):
        """获取并删除多个种子

        一次弹出多个种子，节省网络和redis开销

        Args:
            key: 队列名
            size: 种子数
            mark: 队列标记
            head: 从队列头部获取并弹出，默认队列模式
        Returns:
            种子信息，type=list
        """
        pipeline = self._redis.pipeline()
        pipeline.multi()

        if head:
            pipeline.lrange(self.wear(key, mark), start=0, end=size - 1)
            pipeline.ltrim(self.wear(key, mark), start=size, end=-1)
        else:
            pipeline.lrange(self.wear(key, mark), start=-size, end=-1)
            pipeline.ltrim(self.wear(key, mark), start=0, end=-size - 1)

        seeds = extract(pipeline.execute())  # 获取lrange的结果

        try:
            return [json.loads(s) for s in seeds]
        except json.decoder.JSONDecodeError:
            return seeds

    @daemon
    def set_seed(self, key, *seed, mark=config.FLAG_ENC, head=False):
        """存储种子

        往Redis队列中存种子，期间会将dict转json字符串

        Args:
            key: 队列的key（队列名）
            mark: 队列标记
            seed: 种子
            head: 从队列尾部获取并弹出，默认队列模式
        Returns:
            包含存入和当前总量的队列信息，类型为dict
        """
        if not seed:
            return

        seed = [json.dumps(s, ensure_ascii=False) for s in seed]
        if head is False:
            all_seed_count = self._redis.rpush(self.wear(key, mark), *seed)
        else:
            all_seed_count = self._redis.lpush(self.wear(key, mark), *seed)
        return dict(now=len(seed), all=all_seed_count)

    @daemon
    def watch_seed(self, key, *, mark=config.FLAG_ORI, start=0, end=-1) -> list:
        """查看区间内的种子

        不会弹出种子，默认返回当前队列所有种子

        Usage:
            如需查看第2个及之后的所有种子:
                queue.watch_seed(key, start=1)
        Returns:
            种子组成的list
        """
        try:
            return [json.loads(s) for s in self._redis.lrange(self.wear(key, mark), start, end)]
        except json.decoder.JSONDecodeError:
            return self._redis.lrange(self.wear(key, mark), start, end)

    @daemon
    def deal_seed(self, key, *, mark=config.FLAG_ENC):
        """将失效种子转移至源种子队列"""
        seeds = [extract(seed['seed']) for seed in self.watch_seed(self.wear(key, mark))]

        if not seeds:
            return

        self.set_seed(self.wear(key, config.FLAG_ORI), *seeds)
        self.clear(self.wear(key, mark))

    @daemon
    def remove_seed(self, key, seed, *, mark=config.FLAG_ORI, count=0):
        """删除指定种子"""
        if isinstance(seed, str):
            self._redis.lrem(self.wear(key, mark), count, seed)
        else:
            self._redis.lrem(self.wear(key, mark), count, json.dumps(seed))

    @daemon
    def clear(self, key, *, mark=config.FLAG_ENC):
        """清空队列"""
        self._redis.delete(self.wear(key, mark))

    @retry()
    def check_and_clear(self, *keys, rate=config.STAY_RATE, threshold=config.MAX_QUEUE_LEN,
                        marks=(config.FLAG_ORI, config.FLAG_ENC), head=True):
        """检测并删去指定百分比的种子

        Args:
            keys: 要检测的队列名，支持传多个
            rate: 队列保留率，即删除 (1 - rate) * queue_len 的种子数
            threshold: 阀值，即最大队列长度
            marks: 要检测的队列标记，tuple or list
            head: 默认为True，即从头部删除
        """
        for key in keys:
            for mark in marks:
                queue_len = self._redis.llen(self.wear(key, mark=mark))
                self.log.debug(f"{key}:{mark.upper()}'s queue length: {queue_len}")

                if threshold < queue_len:
                    if head:  # 从头部删
                        self._redis.ltrim(self.wear(key, mark=mark), start=-int(threshold * rate), end=-1)
                    else:  # 从尾部删
                        self._redis.ltrim(self.wear(key, mark=mark), start=0, end=int(threshold * rate))


if __name__ == "__main__":
    pass
