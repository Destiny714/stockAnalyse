# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 20:18
# @Author  : Destiny_
# @File    : dateHandler.py
# @Software: PyCharm

import time
import datetime
from api import databaseApi


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


def lastTradeDay(date=None):
    today = today2str() if date is None else date
    tradeDays = databaseApi.Mysql().selectTradeDate()
    count = 0
    while (today not in tradeDays) and count < 10000:
        count += 1
        today = str(int(today) - 1)
    return today


def week_day(day: datetime.datetime):
    weekday = day.weekday() + 1
    return weekday


def joinTimeToStamp(date: str, detail: str):
    result = datetime.datetime.strptime(f'{date[0:4]}-{date[4:6]}-{date[6:8]} {detail}', '%Y-%m-%d %H:%M:%S')
    return result.timestamp()


def timeDelta(start: str, end: str):
    startDate = datetime.datetime.strptime(start, '%Y%m%d')
    endDate = datetime.datetime.strptime(end, '%Y%m%d')
    delta = endDate - startDate
    return (delta.days * 86400).__abs__()