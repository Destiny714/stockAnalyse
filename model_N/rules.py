# -*- coding: utf-8 -*-
# @Time    : 2022/4/17 22:14
# @Author  : Destiny_
# @File    : rules.py
# @Software: PyCharm

from api import databaseApi
from common import dateHandler


def twoDaySlideWindow(stock, aimDate=dateHandler.today2str()):
    mysql = databaseApi.Mysql()
    data = mysql.selectOneAllData(stock, aimDate=aimDate, dateRange=2)
    day1 = data[0]
    day2 = data[1]
    if not (9.8 <= day1[7] <= 10.2):  # pctChange
        return
    if day1[5] == day1[6]:
        return
    if not (day1[3] <= day2[2] <= day1[3] * 1.03):
        return
    if not (1.2 * day1[8] < day2[8] < 2 * day1[8]):
        return
    if day2[2] < day1[3] or day2[3] < day1[3]:
        return
    if day2[3] < day2[2]:
        return
    if max(day2[2], day2[3]) / min(day2[2], day2[3]) > 1.03:
        return
    return day2[1]


def threeDaySlideWindow(stock, aimDate=dateHandler.today2str()):
    mysql = databaseApi.Mysql()
    data = mysql.selectOneAllData(stock, aimDate=aimDate, dateRange=3)
    day1 = data[0]
    day2 = data[1]
    day3 = data[2]
    if not (9.8 <= day1[7] <= 10.2):  # pctChange
        return
    if day1[5] == day1[6]:
        return
    if not (day1[3] <= day2[2] <= day1[3] * 1.03):
        return
    if not (1.2 * day1[8] < day2[8] < 2 * day1[8]):
        return
    if day2[2] < day1[3] or day2[3] < day1[3]:
        return
    if day2[3] < day2[2]:
        return
    if max(day2[2], day2[3]) / min(day2[2], day2[3]) > 1.03:
        return
    if day3[8] >= 0.7 * day2[8]:
        return
    if day3[3] <= day1[3]:
        return
    return day3[1]
