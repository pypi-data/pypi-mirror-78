# -*- coding: utf-8 -*-
# @author: leesoar

"""clone.py"""
import itertools
import os
import threading


__all__ = ["ThreadPool", ]


class ThreadPool:
    """线程池

    Usage:
        def test1():
            sleep(2, 5)
            print("HoLa")

        def test2():
            sleep(1, 3)
            print("Hello")

        pool = ThreadPool()
        pool.set_task(test1, workers=2)
        pool.set_task(test2, workers=3)
        pool.start()
    """
    _counter = itertools.count().__next__

    def __init__(self, max_workers=(os.cpu_count() or 1) * 5, prefix=None):
        if max_workers <= 0:
            raise ValueError("max_workers需大于0")

        self._max_workers = max_workers
        self._thread_pool = []
        self._prefix = prefix or f"Leto-Thread"

    @staticmethod
    def _start_thread(threads, join=True):
        for t in threads:
            t.start()

        if join is False:
            return

        for t in threads:
            t.join()

    def get_remain(self):
        """获取剩余线程数"""
        return self._max_workers - len(self._thread_pool)

    def set_task(self, target, workers: int, now=False, join=True, args=(), kwargs=None):
        """设置（启动）线程任务等

        配置线程任务，默认不直接启动（需调用cls.start()）

        Args:
            target: 要执行的任务
            workers: 目标任务所需线程数
            now: 是否立即启动。默认False，当now=True时，无需调用cls.start()
            join: 是否阻塞主线程。默认为True
            args: 任务所需普通参数
            kwargs: 任务所需关键字参数
        """
        if workers <= 0:
            raise ValueError("workers需大于0")

        if self._max_workers < len(self._thread_pool) + workers:
            remain = self.get_remain()
            raise ValueError(f"【workers={workers}】线程数超出max_workers，还可创建{remain}个线程")

        threads = [threading.Thread(target=target, args=args, kwargs=kwargs,
                                    name=f"{self._prefix}-{str(self._counter())}") for _ in range(workers)]
        self._thread_pool.extend(threads)
        now and self._start_thread(threads, join)

    def start(self, join=True):
        """启动线程池中的线程"""
        self._start_thread(self._thread_pool, join)

    def __len__(self):
        return len(self._thread_pool)

    def __str__(self):
        return f"ThreadPool(max_workers={self._max_workers}, current_workers={len(self._thread_pool)})"

    __repr__ = __str__
