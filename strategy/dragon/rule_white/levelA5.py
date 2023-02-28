# -*- coding: utf-8 -*-
# @Time    : 2022/11/8 21:13
# @Author  : Destiny_
# @File    : levelA5.py
# @Software: PyCharm
from utils.stockdata_util import (t_limit)
from base.base_level_model import base_level
from models.limit_data_model import LimitDataModel
from models.stock_data_model import StockDataModel
from models.stock_detail_model import StockDetailModel


class levelA5(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex)

    def rule1(self):
        data = self.data
        try:
            if not t_limit(self.stock, data, 1):
                return False
            d0 = data[-1]
            d1 = data[-2]
            return (d1.buy_elg_vol + d0.buy_elg_vol - d1.sell_elg_vol - d0.sell_elg_vol) / (d1.buy_elg_vol + d0.buy_elg_vol) > 0.7
        except:
            ...

    def rule2(self):
        data = self.data
        try:
            if not t_limit(self.stock, data, 1):
                return False
            d0 = data[-1]
            d1 = data[-2]
            return (d1.buy_elg_vol + d0.buy_elg_vol - d1.sell_elg_vol - d0.sell_elg_vol) / (d1.buy_elg_vol + d0.buy_elg_vol) > 0.6
        except:
            ...

    def rule3(self):
        data = self.data
        try:
            if not t_limit(self.stock, data, 1):
                return False
            d0 = data[-1]
            d1 = data[-2]
            return (d1.buy_elg_vol + d0.buy_elg_vol - d1.sell_elg_vol - d0.sell_elg_vol) / (d1.buy_elg_vol + d0.buy_elg_vol) > 0.5
        except:
            ...

    def rule4(self):
        data = self.data
        try:
            if not t_limit(self.stock, data, 1):
                return False
            d0 = data[-1]
            d1 = data[-2]
            return (d1.buy_elg_vol + d0.buy_elg_vol - d1.sell_elg_vol - d0.sell_elg_vol) / (d1.buy_elg_vol + d0.buy_elg_vol) > 0.4
        except:
            ...

    def rule5(self):
        data = self.data
        try:
            if not t_limit(self.stock, data, 1):
                return False
            d0 = data[-1]
            d1 = data[-2]
            return (d1.buy_elg_vol + d0.buy_elg_vol - d1.sell_elg_vol - d0.sell_elg_vol) / (d1.buy_elg_vol + d0.buy_elg_vol) > 0.3
        except:
            ...
