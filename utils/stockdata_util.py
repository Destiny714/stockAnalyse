# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 19:55
# @Author  : Destiny_
# @File    : stockdata_util.py
# @Software: PyCharm
from utils.date_util import *
from functools import lru_cache
from models.stock_data_model import *


def queryIndexData(index, dateRange: int = 500, aimDate=None) -> list[StockDataModel]:
    if not aimDate:
        aimDate = lastTradeDay()
    mysql = db.Stock_Database()
    allData = mysql.selectOneAllData(stock=index, dateRange=dateRange, aimDate=aimDate)
    res = [StockDataModel(allData[i]) for i in range(len(allData))]
    mysql.close()
    return res


@lru_cache(maxsize=None)
def queryData(stock, dateRange: int = 800, aimDate='', after=False) -> list[StockDataModel]:
    if aimDate == '':
        aimDate = lastTradeDay()
    mysql = db.Stock_Database()
    allData = mysql.selectOneAllData(stock=stock, dateRange=dateRange, aimDate=aimDate, after=after)
    res = [StockDataModel(_) for _ in allData]
    mysql.close()
    return res


def t_low_pct(data: list[StockDataModel], plus: int = 0) -> float:
    return (data[-plus - 1].low / data[-plus - 2].close) - 1


def t_high_pct(data: list[StockDataModel], plus: int = 0) -> float:
    return (data[-plus - 1].high / data[-plus - 2].close) - 1


def t_close_pct(data: list[StockDataModel], plus: int = 0) -> float:
    return (data[-plus - 1].close / data[-plus - 2].close) - 1


def t_open_pct(data: list[StockDataModel], plus: int = 0) -> float:
    return (data[-plus - 1].open / data[-plus - 2].close) - 1


@lru_cache(maxsize=None)
def limit(stock: str) -> float:
    return 19.6 if stock[0:2] in ['30', '68'] else 9.8


def model_1(stock: str, data: list[StockDataModel], plus: int = 0) -> bool:
    d = data[-plus - 1]
    if (d.close == d.low) and (d.open == d.high) and (d.open == d.close):
        if d.pctChange > limit(stock):
            return True


def model_t(stock: str, data: list[StockDataModel], plus: int = 0) -> bool:
    open_p = t_open_pct(data, plus)
    close_p = t_close_pct(data, plus)
    if open_p != close_p:
        return False
    if close_p <= limit(stock) / 100:
        return False
    if t_low_pct(data, plus) < limit(stock) / 100:
        return True


def t_limit(stock: str, data: list[StockDataModel], plus: int = 0) -> bool:
    return data[-plus - 1].pctChange >= limit(stock)


def t_down_limit(stock: str, data: list[StockDataModel], plus: int = 0) -> bool:
    return data[-plus - 1].pctChange < - limit(stock)


def limit_height(stock: str, data: list[StockDataModel], plus: int = 0) -> int:
    height = 0
    for i in range(20):
        if t_limit(stock, data, i + plus):
            height += 1
        else:
            return height
    return height


def move_avg(data: list[StockDataModel], dateRange: int, plus: int = 0) -> float:
    """
    计算移动平均值
    :param data: list[dataModel]
    :param dateRange: ma(x)
    :param plus: 指定 t - (plus) 日
    :return:
    """
    j = plus + 1
    return sum([data[-_].close for _ in range(j, j + dateRange)]) / dateRange


def weakenedIndex(indexData: list[StockDataModel], plus: int = 0, weak_degree: int = 10):
    return 1 + t_close_pct(indexData, plus) * weak_degree


def day2elg(data: list[StockDataModel]):
    try:
        t0 = data[-1]
        t1 = data[-2]
        return round(((t0.buy_elg_vol + t1.buy_elg_vol - t0.sell_elg_vol - t1.sell_elg_vol) / (t0.buy_elg_vol + t1.buy_elg_vol)) * 100, 2)
    except:
        return 0


def day3elg(data: list[StockDataModel]):
    try:
        t0 = data[-1]
        t1 = data[-2]
        t2 = data[-3]
        return round(((t0.buy_elg_vol + t1.buy_elg_vol + t2.buy_elg_vol - t0.sell_elg_vol - t1.sell_elg_vol - t2.sell_elg_vol) / (
                t0.buy_elg_vol + t1.buy_elg_vol + t2.buy_elg_vol)) * 100, 2)
    except:
        return 0
