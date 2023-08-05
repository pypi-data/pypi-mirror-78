# -*- coding: utf-8 -*-
# @author: leesoar

"""日志记录"""

import logging
import os
from logging import handlers

from ..common import config


__all__ = ["Logger", ]


class Logger:
    """将日志在屏幕输出的同时，保存在文件"""

    _level_map = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARN,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    _config = {
        "interval": config.LOG_INTERVAL,
        "when": config.LOG_UNIT,
        "backupCount": config.LOG_BACKUP_COUNT,
        "encoding": config.LOG_FILE_ENCODE,
    }

    def __new__(cls, *args, **kwargs):
        """限制实例创建"""
        if not hasattr(cls, 'inst'):
            cls.inst = super().__new__(cls)
        return cls.inst

    def __init__(self, filename, level=config.LOG_LEVEL, dump_log=False):
        self.filename = filename
        self.filepath = os.path.join(os.pardir, config.LOG_SAVE_DIR)
        self._dump_log = dump_log
        self._level = level

    @staticmethod
    def _mk_dir(filepath):
        """创建日志文件夹

        Args:
            filepath: 文件的绝对路径
        """
        if not os.path.exists(filepath):
            os.mkdir(filepath)

    def _init_logger(self):
        """初始化日志记录器"""
        self._logger = logging.getLogger(self.filename)
        self._fmt = logging.Formatter(config.LOG_FMT)
        if self._level.lower() in self._level_map:
            self._logger.setLevel(self._level_map[self._level.lower()])
        self._config.update(dict(filename=os.path.join(self.filepath, self.filename)))
        self._scr_hdl = logging.StreamHandler()  # 屏幕输出
        self._scr_hdl.setFormatter(self._fmt)

        if self._dump_log:
            self._mk_dir(self.filepath)
            self._file_hdl = handlers.TimedRotatingFileHandler(**self._config)  # 文件输出
            self._file_hdl.setFormatter(self._fmt)

        if not self._logger.handlers:
            self._logger.addHandler(self._scr_hdl)
            self._dump_log and self._logger.addHandler(self._file_hdl)

    def get_logger(self):
        """返回封装好的logger"""
        self._init_logger()
        return self._logger


if __name__ == "__main__":
    logger = Logger(filename="test.log", dump_log=True).get_logger()
    logger.info("test")
