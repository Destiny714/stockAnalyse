# -*- coding: utf-8 -*-
# @Time    : 2022/8/22 18:39
# @Author  : Destiny_
# @File    : levelA3.py
# @Software: PyCharm
from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class levelA3(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex)

    def rule1(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(3):
                if not t_limit(stock, data, i):
                    return False
            d = data[-1]
            if d.buy_elg_vol / d.volume > 0.65:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.8:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) > 0.4:
                        return data[-2].TP > 50
        except:
            pass

    def rule2(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(3):
                if not t_limit(stock, data, i):
                    return False
            d = data[-1]
            if d.buy_elg_vol / d.volume > 0.55:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.7:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) > 0.3:
                        return data[-2].TP > 40
        except:
            pass

    def rule3(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(3):
                if not t_limit(stock, data, i):
                    return False
            d = data[-1]
            if d.buy_elg_vol / d.volume > 0.4:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.6:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) > 0.2:
                        return data[-2].TP > 30
        except:
            pass

    def rule4(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(3):
                if not t_limit(stock, data, i):
                    return False
            for i in range(2):
                d = data[-i - 1]
                if d.buy_elg_vol / d.volume <= 0.4:
                    return False
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.65:
                    return False
                if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                        d.buy_elg_vol + d.buy_lg_vol) <= 0.3:
                    return False
            return True
        except:
            pass

    def rule5(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(3):
                if not t_limit(stock, data, i):
                    return False
                d = data[-i - 1]
                if d.buy_elg_vol / d.volume <= 0.35:
                    return False
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.5:
                    return False
                if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                        d.buy_elg_vol + d.buy_lg_vol) <= 0.25:
                    return False
            return True
        except:
            pass
