"""
awesome.helper
date, time 帮助类
"""
import time

ONE_SECOND = 1  # 一秒
MIN_SECOND = 60  # 一分钟的秒数
HOUR_SECOND = 3600  # 一个小时的秒数
DAY_SECOND = 86400  # 一天的秒数
WEE_SECOND = 604800  # 一周的秒数
MONTH_SECOND = 2592000  # 一个月的秒数
YEAR_SECOND = 31536000  # 一年的秒数


def now():
    """
    此时的时间戳
    :return:
    """
    return int(time.time())
