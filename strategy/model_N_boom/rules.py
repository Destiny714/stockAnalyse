# -*- coding: utf-8 -*-
# @Time    : 2022/4/17 22:14
# @Author  : Destiny_
# @File    : rules.py
# @Software: PyCharm


from models.stock_data_model import StockDataModel
from utils.stockdata_util import t_limit, model_1, t_open_pct, t_close_pct, move_avg


def boom_model_rule(stock: str, data: list[StockDataModel]) -> int:
    SWING_LIMIT = 0.06
    assert len(data) >= 3
    for i in range(1):
        if not t_close_pct(data,1) >= 0.08:
            break
        if model_1(stock, data, 1):
            break
        day1 = data[-2]
        day2 = data[-1]
        if not (1.2 * day1.volume <= day2.volume <= 2 * day1.volume):
            break
        if not (day2.close >= day2.open):
            break
        if abs((t_open_pct(data) - t_close_pct(data))) <= SWING_LIMIT:
            return 2
    return 0
