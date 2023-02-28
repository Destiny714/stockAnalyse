# -*- coding: utf-8 -*-
# @Time    : 2023/1/9 19:01
# @Author  : Destiny_
# @File    : levelA6.py
# @Software: PyCharm
from utils.stockdata_util import model_1
from base.base_level_model import base_level
from models.stock_data_model import StockDataModel
from models.stock_detail_model import StockDetailModel


class levelA6(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex)

    def rule1(self):
        data = self.data
        d0 = data[-1]
        d1 = data[-2]
        return (d1.buy_elg_vol + d0.buy_elg_vol) / (d1.volume + d0.volume) > 0.8

    def rule2(self):
        data = self.data
        d0 = data[-1]
        d1 = data[-2]
        return (d1.buy_elg_vol + d0.buy_elg_vol) / (d1.volume + d0.volume) > 0.6

    def rule3(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data):
            return False
        d0 = data[-1]
        d1 = data[-2]
        return (d1.buy_elg_vol + d0.buy_elg_vol) / (d1.volume + d0.volume) > 0.45

    def rule4(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data):
            return False
        d0 = data[-1]
        d1 = data[-2]
        return (d1.buy_elg_vol + d0.buy_elg_vol) / (d1.volume + d0.volume) > 0.35

    def rule5(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data):
            return False
        d0 = data[-1]
        d1 = data[-2]
        return (d1.buy_elg_vol + d0.buy_elg_vol) / (d1.volume + d0.volume) > 0.25
