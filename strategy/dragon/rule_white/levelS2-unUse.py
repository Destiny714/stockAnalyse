# -*- coding: utf-8 -*-
# @Time    : 2022/7/31 22:40
# @Author  : Destiny_
# @File    : levelS2-unUse.py
# @Software: PyCharm

from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class levelS2(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel],
                 limitData: dict[str, list[LimitDataModel]]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex, limitData)

    def rule1(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(3):
                if not t_limit(stock, data, i):
                    return False
            d = data[-1]
            if d.buy_elg_vol / d.volume <= 0.45:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume <= 0.65:
                return False
            if d.buy_elg_vol <= d.sell_elg_vol:
                return False
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.5:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                    d.buy_elg_vol + d.buy_lg_vol) > 0.2:
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
            if d.buy_elg_vol / d.volume <= 0.4:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume <= 0.7:
                return False
            if d.buy_elg_vol <= d.sell_elg_vol:
                return False
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.5:
                return False
            if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                    d.buy_elg_vol + d.buy_lg_vol) > 0.2:
                return True
        except:
            pass

    def rule3(self):
        data = self.data
        try:
            for i in range(2):
                d = data[-i - 1]
                if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                        d.buy_elg_vol + d.buy_lg_vol) <= 0.2:
                    return False
                if (d.buy_elg_vol + d.buy_lg_vol) / d.volume <= 0.5:
                    return False
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.5:
                    return False
            return True
        except:
            pass
