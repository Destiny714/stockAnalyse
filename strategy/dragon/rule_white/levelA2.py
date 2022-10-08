# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 18:52
# @Author  : Destiny_
# @File    : levelA2.py
# @Software: PyCharm

from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stockDetailModel import stockDetailModel


class levelA2(base_level):
    def __init__(self, stockDetail: stockDetailModel, data: list[dataModel], index: list[dataModel], limitData: dict[str, list[limitDataModel]]):
        self.level = 'A2'
        super().__init__(self.level, stockDetail, data, index, limitData)

    def rule1(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
            d = data[-1]
            if d.buy_elg_vol / d.volume <= 0.4:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume <= 0.6:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                    d.buy_elg_vol + d.buy_lg_vol) <= 0.4:
                return False
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.7:
                return False
            d1 = data[-2]
            if (d1.buy_elg_vol - d1.sell_elg_vol) / d1.buy_elg_vol > 0.7:
                return True
        except:
            pass

    def rule2(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
            d = data[-1]
            if d.buy_elg_vol / d.volume <= 0.35:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume <= 0.55:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                    d.buy_elg_vol + d.buy_lg_vol) <= 0.35:
                return False
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.6:
                return False
            d1 = data[-2]
            if (d1.buy_elg_vol - d1.sell_elg_vol) / d1.buy_elg_vol > 0.6:
                return True
        except:
            pass

    def rule3(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
            d = data[-1]
            if d.buy_elg_vol / d.volume <= 0.35:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume <= 0.5:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                    d.buy_elg_vol + d.buy_lg_vol) <= 0.3:
                return False
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.5:
                return False
            d1 = data[-2]
            if (d1.buy_elg_vol - d1.sell_elg_vol) / d1.buy_elg_vol > 0.5:
                return True
        except:
            pass

    def rule4(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
            d = data[-1]
            if d.buy_elg_vol / d.volume <= 0.35:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume <= 0.45:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                    d.buy_elg_vol + d.buy_lg_vol) <= 0.2:
                return False
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.4:
                return False
            d1 = data[-2]
            if (d1.buy_elg_vol - d1.sell_elg_vol) / d1.buy_elg_vol > 0.4:
                return True
        except:
            pass

    def rule5(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
            d = data[-1]
            if d.buy_elg_vol / d.volume <= 0.35:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume <= 0.4:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                    d.buy_elg_vol + d.buy_lg_vol) <= 0.15:
                return False
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.3:
                return False
            d1 = data[-2]
            if (d1.buy_elg_vol - d1.sell_elg_vol) / d1.buy_elg_vol > 0.35:
                return True
        except:
            pass
