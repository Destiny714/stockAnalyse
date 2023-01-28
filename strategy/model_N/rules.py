# -*- coding: utf-8 -*-
# @Time    : 2022/4/17 22:14
# @Author  : Destiny_
# @File    : rules.py
# @Software: PyCharm


from models.stock_data_model import StockDataModel
from utils.stockdata_util import t_limit, model_1, t_open_pct, t_close_pct


def n_model_rule(stock: str, data: list[StockDataModel]) -> int:
    SWING_LIMIT = 0.06
    assert len(data) == 3
    for i in range(1):
        if not t_limit(stock, data, 1):
            break
        if model_1(stock, data, 1):
            break
        day1 = data[-2]
        day2 = data[-1]
        if not (1.2 * day1.volume <= day2.volume <= 2 * day1.volume):
            break
        if not (day2.open >= day1.close and day2.close >= day1.close):
            break
        if not (day2.close >= day2.open):
            break
        if abs((t_open_pct(data) - t_close_pct(data))) <= SWING_LIMIT:
            return 2
    for i in range(1):
        if not t_limit(stock, data, 2):
            break
        day1 = data[-3]
        day2 = data[-2]
        day3 = data[-1]
        if model_1(stock, data, 2):
            break
        if not (1.2 * day1.volume <= day2.volume <= 2 * day1.volume):
            break
        if not (day2.open >= day1.close and day2.close >= day1.close):
            break
        if abs((t_open_pct(data, 1) - t_close_pct(data, 1))) > SWING_LIMIT:
            break
        if not (day2.close >= day2.open):
            break
        if day3.volume < 0.7 * day2.volume and day3.close > day1.close:
            return 3
    return 0
