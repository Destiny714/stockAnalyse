# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 18:52
# @Author  : Destiny_
# @File    : levelA1.py
# @Software: PyCharm

from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class levelA1(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel],
                 limitData: dict[str, list[LimitDataModel]]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex, limitData)

    def rule1(self):
        data = self.data
        try:
            d = data[-1]
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume / weakenedIndex(self.shIndex) > 0.8:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol / weakenedIndex(self.shIndex) > 0.8:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) / weakenedIndex(self.shIndex) > 0.4:
                        return True
        except:
            pass

    def rule2(self):
        data = self.data
        try:
            d = data[-1]
            if d.CP / weakenedIndex(self.shIndex) > 65:
                if d.TF / weakenedIndex(self.shIndex) > 60:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) / weakenedIndex(self.shIndex) > 0.3:
                        return True
        except:
            pass

    def rule3(self):
        data = self.data
        try:
            d = data[-1]
            if d.CP / weakenedIndex(self.shIndex) > 50:
                if d.TF / weakenedIndex(self.shIndex) > 40:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) / weakenedIndex(self.shIndex) > 0.2:
                        return True
        except:
            pass

    def rule4(self):
        data = self.data
        try:
            d = data[-1]
            if d.CP / weakenedIndex(self.shIndex) > 40:
                if d.TF / weakenedIndex(self.shIndex) > 20:
                    if d.CF / weakenedIndex(self.shIndex) > -10:
                        return True
        except:
            pass

    def rule5(self):
        data = self.data
        try:
            d = data[-2]
            if d.CP / weakenedIndex(self.shIndex, 1) > 70:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol / weakenedIndex(self.shIndex, 1) > 0.6:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) / weakenedIndex(self.shIndex, 1) > 0.3:
                        d0 = data[-1]
                        if (d0.buy_elg_vol - d0.sell_elg_vol) / d0.buy_elg_vol / weakenedIndex(self.shIndex) > 0.4:
                            return True
        except:
            pass

    def rule6(self):
        data = self.data
        try:
            d = data[-2]
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume / weakenedIndex(self.shIndex, 1) > 0.6:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol / weakenedIndex(self.shIndex, 1) > 0.5:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) / weakenedIndex(self.shIndex, 1) > 0.2:
                        d0 = data[-1]
                        if (d0.buy_elg_vol - d0.sell_elg_vol) / d0.buy_elg_vol / weakenedIndex(self.shIndex) > 0.4:
                            return True
        except:
            pass

    def rule7(self):
        data = self.data
        try:
            for i in range(2):
                d = data[-i - 1]
                if (d.buy_elg_vol + d.buy_lg_vol) / d.volume / weakenedIndex(self.shIndex, i) <= 0.6:
                    return False
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol / weakenedIndex(self.shIndex, i) <= 0.5:
                    return False
            return True
        except:
            pass

    def rule8(self):
        data = self.data
        try:
            for i in range(3):
                d = data[-i - 1]
                if (d.buy_elg_vol + d.buy_lg_vol) / d.volume / weakenedIndex(self.shIndex, i) <= 0.6:
                    return False
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol / weakenedIndex(self.shIndex, i) <= 0.5:
                    return False
            return True
        except:
            pass

    def rule9(self):
        if model_1(self.stock, self.data):
            return False
        d = self.data[-1]
        return d.CF > 55 and d.TF > 80 and d.TP > 35

    def rule10(self):
        if t_down_limit(self.stock, self.data):
            return self.data[-1].TF > 60

    def rule11(self):
        data = self.data
        stock = self.stock
        if not model_1(stock, data):
            return False
        d = data[-2]
        if (d.buy_elg_vol + d.buy_lg_vol) / d.volume / weakenedIndex(self.shIndex, weak_degree=5) > 0.7:
            return d.TF / weakenedIndex(self.shIndex, weak_degree=5) > 50
