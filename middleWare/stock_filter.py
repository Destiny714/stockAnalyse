# -*- coding: utf-8 -*-
# @Time    : 2022/9/14 21:45
# @Author  : Destiny_
# @File    : stock_filter.py
# @Software: PyCharm
from api import tushare_api


class stockFilter:
    def __init__(self, stocks: list):
        self.stocks = stocks

    def baseFilter(self, stocks: list):
        return [_ for _ in stocks if int(_[0]) in [0, 3, 6]]

    def endStocksFilter(self, stocks: list):
        endStocks = tushare_api.Tushare().allEndStocks()
        return [_ for _ in stocks if _ not in endStocks]

    def result(self):
        filters = [_ for _ in stockFilter.__dict__.keys() if 'Filter' in _]
        stocks = self.stocks.copy()
        for _filter in filters:
            func = getattr(self,_filter)
            stocks = func(stocks)
        return stocks
