# -*- coding: utf-8 -*-
# @author: leesoar

"""something."""

import os

from ..common.const import Unit

# 爬虫
# 基本配置
REQ_TIMEOUT = int(os.getenv("SPIDER_TIMEOUT", Unit.ONE_SECOND * 10))   # 请求超时时间

# 睡眠时间
SLEEP_RANGE = [0.1, 0.5]   # 间隔随机范围(秒)
SLEEP_MAX = Unit.ONE_SECOND * 10   # 最大阻塞时间


# 日志
LOG_SAVE_DIR = "log"
LOG_LEVEL = "DEBUG"
LOG_FMT = "%(asctime)s %(levelname)s [%(process)d|%(threadName)s]" \
          " [%(filename)s > %(funcName)s > line:%(lineno)d]: %(message)s"
LOG_INTERVAL = 1   # 生成日志文件的时间间隔
LOG_UNIT = "D"   # 生成日志文件的间隔单位
LOG_BACKUP_COUNT = 3   # 日志备份文件个数（超过自动删除）
LOG_FILE_ENCODE = "utf-8"   # 日志文件编码


# 队列标记配置
FLAG_ORI = "ori"   # 种子源队列的后缀标志
FLAG_ENC = "sign"   # 加密队列的后缀标志
FLAG_FIN = "fin"   # 完成队列的后缀标志（存储结果），可选

# 队列最大长度
MAX_QUEUE_LEN = int(os.getenv("MAX_QUEUE_LEN", 10000))

# 清空队列保留率
STAY_RATE = 0.6
