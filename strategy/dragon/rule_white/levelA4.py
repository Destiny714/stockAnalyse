# -*- coding: utf-8 -*-
# @Time    : 2022/8/30 19:28
# @Author  : Destiny_
# @File    : levelA4.py
# @Software: PyCharm
from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class levelA4(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex)

    def rule1(self):
        data = self.data
        try:
            d0 = data[-1]
            d1 = data[-2]
            d2 = data[-3]
            return (d2.buy_elg_vol + d1.buy_elg_vol + d0.buy_elg_vol - d2.sell_elg_vol - d1.sell_elg_vol - d0.sell_elg_vol) / (
                    d2.buy_elg_vol + d1.buy_elg_vol + d0.buy_elg_vol) > 0.7
        except:
            pass

    def rule2(self):
        data = self.data
        try:
            d0 = data[-1]
            d1 = data[-2]
            d2 = data[-3]
            return (d2.buy_elg_vol + d1.buy_elg_vol + d0.buy_elg_vol - d2.sell_elg_vol - d1.sell_elg_vol - d0.sell_elg_vol) / (
                    d2.buy_elg_vol + d1.buy_elg_vol + d0.buy_elg_vol) > 0.6
        except:
            pass

    def rule3(self):
        data = self.data
        try:
            d0 = data[-1]
            d1 = data[-2]
            d2 = data[-3]
            return (d2.buy_elg_vol + d1.buy_elg_vol + d0.buy_elg_vol - d2.sell_elg_vol - d1.sell_elg_vol - d0.sell_elg_vol) / (
                    d2.buy_elg_vol + d1.buy_elg_vol + d0.buy_elg_vol) > 0.5
        except:
            pass

    def rule4(self):
        data = self.data
        try:
            d0 = data[-1]
            d1 = data[-2]
            d2 = data[-3]
            return (d2.buy_elg_vol + d1.buy_elg_vol + d0.buy_elg_vol - d2.sell_elg_vol - d1.sell_elg_vol - d0.sell_elg_vol) / (
                    d2.buy_elg_vol + d1.buy_elg_vol + d0.buy_elg_vol) > 0.4
        except:
            pass

    def rule5(self):
        data = self.data
        try:
            d0 = data[-1]
            d1 = data[-2]
            d2 = data[-3]
            return (d2.buy_elg_vol + d1.buy_elg_vol + d0.buy_elg_vol - d2.sell_elg_vol - d1.sell_elg_vol - d0.sell_elg_vol) / (
                    d2.buy_elg_vol + d1.buy_elg_vol + d0.buy_elg_vol) > 0.3
        except:
            pass
