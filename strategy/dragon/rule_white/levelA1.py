# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 18:52
# @Author  : Destiny_
# @File    : levelA1.py
# @Software: PyCharm

from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stockDetailModel import stockDetailModel


class levelA1(base_level):
    def __init__(self, stockDetail: stockDetailModel, data: list[dataModel], gemIndex: list[dataModel], shIndex: list[dataModel],
                 limitData: dict[str, list[limitDataModel]]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex, limitData)

    def rule1(self):
        data = self.data
        try:
            d = data[-1]
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume > 0.6:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.8:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) > 0.4:
                        return True
        except:
            pass

    def rule2(self):
        data = self.data
        try:
            d = data[-1]
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume > 0.5:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.7:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) > 0.3:
                        return True
        except:
            pass

    def rule3(self):
        data = self.data
        try:
            d = data[-1]
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume > 0.4:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.6:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) > 0.2:
                        return True
        except:
            pass

    def rule4(self):
        data = self.data
        try:
            d = data[-1]
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume > 0.35:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.5:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) > 0.05:
                        return True
        except:
            pass

    def rule5(self):
        data = self.data
        try:
            d = data[-2]
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume > 0.6:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.5:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) > 0.3:
                        d0 = data[-1]
                        if (d0.buy_elg_vol - d0.sell_elg_vol) / d0.buy_elg_vol > 0.4:
                            return True
        except:
            pass

    def rule6(self):
        data = self.data
        try:
            d = data[-2]
            if (d.buy_elg_vol + d.buy_lg_vol) / d.volume > 0.5:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.4:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) > 0.2:
                        d0 = data[-1]
                        if (d0.buy_elg_vol - d0.sell_elg_vol) / d0.buy_elg_vol > 0.4:
                            return True
        except:
            pass

    def rule7(self):
        data = self.data
        try:
            for i in range(2):
                d = data[-i - 1]
                if (d.buy_elg_vol + d.buy_lg_vol) / d.volume <= 0.5:
                    return False
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.5:
                    return False
            return True
        except:
            pass

    def rule8(self):
        data = self.data
        try:
            for i in range(3):
                d = data[-i - 1]
                if (d.buy_elg_vol + d.buy_lg_vol) / d.volume <= 0.5:
                    return False
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.5:
                    return False
            return True
        except:
            pass

    def rule9(self):
        d = self.data[-1]
        return d.CF > 55 and d.TF > 80 and d.TP > 35
