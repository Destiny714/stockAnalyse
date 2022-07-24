# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 19:55
# @Author  : Destiny_
# @File    : collect_data.py
# @Software: PyCharm
from typing import List
from api import databaseApi
from common import dateHandler


class dataModel:
    def __init__(self, data):
        self.data = data

    def date(self):
        return self.data[1]

    def open(self):
        return self.data[2]

    def close(self):
        return self.data[3]

    def preClose(self):
        return self.data[4]

    def high(self):
        return self.data[5]

    def low(self):
        return self.data[6]

    def pctChange(self):
        return self.data[7]

    def volume(self):
        return self.data[8]

    def amount(self):
        return self.data[9]

    def turnover(self):
        return self.data[10]

    def firstLimitTime(self):
        return self.data[11]

    def lastLimitTime(self):
        return self.data[12]

    def limitOpenTime(self):
        return self.data[13]


def collectData(stock, dateRange: int = 800, aimDate=dateHandler.lastTradeDay(), virtual=None) -> List[dataModel]:
    mysql = databaseApi.Mysql()
    allData = mysql.selectOneAllData(stock=stock, dateRange=dateRange, aimDate=aimDate)
    res = [dataModel(_) for _ in allData]
    if virtual is None:
        pass
    elif virtual == 's':
        modifyData = res[-1]
        nextDate = mysql.selectNextTradeDay(modifyData.date())
        virtualData = [8888,
                       nextDate,
                       modifyData.close() * 1.08,
                       modifyData.close() * (1 + (limit(stock) / 100)),
                       modifyData.close(),
                       modifyData.close() * (1 + (limit(stock) / 100)),
                       modifyData.close() * 1.07,
                       limit(stock),
                       modifyData.volume() * 0.6,
                       modifyData.amount() * 0.6,
                       modifyData.turnover() * 0.6,
                       dateHandler.joinTimeToStamp(nextDate, '09:45:00'),
                       dateHandler.joinTimeToStamp(nextDate, '09:45:00'),
                       0]
        res.append(dataModel(virtualData))
    elif virtual == 'f':
        modifyData = res[-1]
        nextDate = mysql.selectNextTradeDay(modifyData.date())
        plus = 1 if modifyData.pctChange() > limit(stock) else 0
        virtualData = [8888,
                       nextDate,
                       modifyData.close() * 1.04,
                       modifyData.close() * (1 + (limit(stock) / 100)),
                       modifyData.close(),
                       modifyData.close() * (1 + (limit(stock) / 100)),
                       modifyData.close(),
                       limit(stock),
                       modifyData.volume() * 1.4,
                       modifyData.amount() * 1.4,
                       modifyData.turnover() * 1.4,
                       dateHandler.joinTimeToStamp(nextDate, '10:45:00'),
                       dateHandler.joinTimeToStamp(nextDate, '14:30:00'),
                       1]
        res.append(dataModel(virtualData))
    return res


def t_low_pct(data: List[dataModel], plus: int = 0):
    return data[-plus - 1].low() / data[-plus - 2].close() - 1


def t_high_pct(data: List[dataModel], plus: int = 0):
    return data[-plus - 1].high() / data[-plus - 2].close() - 1


def t_close_pct(data: List[dataModel], plus: int = 0):
    return data[-plus - 1].close() / data[-plus - 2].close() - 1


def t_open_pct(data: List[dataModel], plus: int = 0):
    return data[-plus - 1].open() / data[-plus - 2].close() - 1


def limit(stock: str) -> float:
    return 19.6 if stock[0:2] in ['30', '68'] else 9.8


def model_1(stock: str, data: List[dataModel], plus: int = 0):
    if (data[-plus - 1].close() == data[-plus - 1].low()) and (data[-plus - 1].open() == data[-plus - 1].high()) and (
            data[-plus - 1].open() == data[-plus - 1].close()):
        if data[-plus - 1].pctChange() > limit(stock):
            return True


def model_t(stock: str, data: List[dataModel], plus: int = 0):
    open_p = t_open_pct(data, plus)
    close_p = t_close_pct(data, plus)
    if open_p != close_p:
        return False
    if close_p <= limit(stock) / 100:
        return False
    if t_low_pct(data, plus) < limit(stock) / 100:
        return True


def t_limit(stock: str, data: List[dataModel], plus: int = 0):
    return data[-plus - 1].pctChange() > limit(stock)


def limit_height(stock: str, data: List[dataModel]):
    height = 0
    for i in range(20):
        if t_limit(stock, data, i):
            height += 1
        else:
            return height
    return height
