# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 20:18
# @Author  : Destiny_
# @File    : date_util.py
# @Software: PyCharm

import time
import datetime
from functools import lru_cache

from database import db


def str2date(date: str):
    assert len(date) == 8
    year = date[:4]
    month = date[4:6]
    day = date[6:]
    new_date = f'{year}-{month}-{day}'
    format_date = time.strptime(new_date, '%Y-%m-%d')
    final_date = datetime.datetime(format_date[0], format_date[1], format_date[2])
    return final_date


def date2str(date: datetime.datetime):
    month = f'{0 if date.month < 10 else ""}{date.month}'
    day = f'{0 if date.day < 10 else ""}{date.day}'
    date_str = f'{date.year}-{month}-{day}'
    return date_str


def today2str():
    today = datetime.datetime.today()
    return date2str(today).replace('-', '')


@lru_cache(maxsize=None)
def lastTradeDay(date=None):
    today = today2str() if date is None else date
    client = db.Stock_Database()
    tradeDays = client.selectTradeDate()
    if today in tradeDays:
        matchTime = joinTimeToStamp(today, '15:30:00')
        if time.time() < matchTime:
            return client.selectPrevTradeDate(today)
        else:
            return today
    count = 0
    while (today not in tradeDays) and count < 10000:
        count += 1
        today = str(int(today) - 1)
    client.close()
    return today


def allTradeDay():
    client = db.Stock_Database()
    alDays = client.selectTradeDate()
    client.close()
    return alDays


@lru_cache(maxsize=None)
def prevTradeDay(date: str):
    client = db.Stock_Database()
    prev = client.selectPrevTradeDate(date)
    client.close()
    return prev


@lru_cache(maxsize=None)
def nextTradeDay(date: str):
    client = db.Stock_Database()
    nxt = client.selectNextTradeDay(date)
    client.close()
    return nxt


@lru_cache(maxsize=None)
def lastXTradeDay(date=None, x: int = 1):
    client = db.Stock_Database()
    date = lastTradeDay(date)
    res = client.selectTradeDateByDuration(date, x)
    client.close()
    return res


@lru_cache(maxsize=None)
def nextXTradeDay(date=None, x: int = 1):
    client = db.Stock_Database()
    date = lastTradeDay(date)
    res = client.selectNextXTradeDay(date, x)
    client.close()
    return res


def week_day(day: datetime.datetime):
    weekday = day.weekday() + 1
    return weekday


@lru_cache(maxsize=None)
def joinTimeToStamp(date: str, detail: str):
    """
    将标准日期格式与hh:mm:ss时间格式合并获得当时的时间戳
    :param date: YYMMDD
    :param detail: hh:mm:ss
    :return: timestamp (s)
    """
    result = datetime.datetime.strptime(f'{date[0:4]}-{date[4:6]}-{date[6:8]} {detail}', '%Y-%m-%d %H:%M:%S')
    return result.timestamp()


@lru_cache(maxsize=None)
def timeDelta(start: str, end: str):
    """
    求时间差 返回秒数
    :param start: 开始日期
    :param end: 结束日期
    :return: 返回两日期相差的秒数绝对值
    """
    startDate = datetime.datetime.strptime(start, '%Y%m%d')
    endDate = datetime.datetime.strptime(end, '%Y%m%d')
    delta = endDate - startDate
    return (delta.days * 86400).__abs__()


@lru_cache(maxsize=None)
def getMinute(stamp: int = None, timeStr: str = None):
    """
    通过时间戳或者标准时间格式获取当时的hhmm
    :param stamp: 时间戳
    :param timeStr: YY-MM-DD hh:mm:ss
    :return: hhmm
    """
    assert (stamp is not None or timeStr is not None)
    if stamp:
        res = datetime.datetime.fromtimestamp(stamp)
    else:
        res = datetime.datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
    hour = res.hour
    minute = res.minute
    return f'{0 if hour < 10 else ""}{hour}{0 if minute < 10 else ""}{minute}'


def nextMinute(now: str):
    if now == '1130':
        nxt = datetime.datetime.strptime(f'2022-02-22 13:01:00', '%Y-%m-%d %H:%M:%S')
    elif now == '1500':
        nxt = datetime.datetime.strptime(f'2022-02-22 15:00:00', '%Y-%m-%d %H:%M:%S')
    else:
        result = datetime.datetime.strptime(f'2022-02-22 {now[0:2]}:{now[2:4]}:00', '%Y-%m-%d %H:%M:%S')
        nxt = result + datetime.timedelta(minutes=1)
    hour = nxt.hour
    minute = nxt.minute
    return f'{0 if hour < 10 else ""}{hour}{0 if minute < 10 else ""}{minute}'


def prevMinute(now: str):
    if now in ['1300', '1301']:
        nxt = datetime.datetime.strptime(f'2022-02-22 11:30:00', '%Y-%m-%d %H:%M:%S')
    elif now == '0930':
        nxt = datetime.datetime.strptime(f'2022-02-22 09:30:00', '%Y-%m-%d %H:%M:%S')
    else:
        result = datetime.datetime.strptime(f'2022-02-22 {now[0:2]}:{now[2:4]}:00', '%Y-%m-%d %H:%M:%S')
        nxt = result - datetime.timedelta(minutes=1)
    hour = nxt.hour
    minute = nxt.minute
    return f'{0 if hour < 10 else ""}{hour}{0 if minute < 10 else ""}{minute}'
