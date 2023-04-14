# -*- coding: utf-8 -*-
# @Time    : 2023/2/23 23:06
# @Author  : Destiny_
# @File    : level_rule.py
# @Software: PyCharm
from utils.date_util import getMinute
from models.stock_data_model import StockDataModel
from utils.stockdata_util import t_limit, t_close_pct, limit_height


class LevelRule(object):
    def __init__(self, params: dict):
        self.passes = []
        assert set(params.keys()) >= {'black', 'white', 'score', 'CF', 'TF', 'CP', 'TP', 'AJ', 'is1', 'height', 'day3elg', 'data'}, set(params.keys())
        self.CF: float = params['CF']
        self.TF: float = params['TF']
        self.CP: float = params['CP']
        self.TP: float = params['TP']
        self.AJ: float = params['AJ']
        self.stock = params['stock']
        self.is1: bool = params['is1']
        self.height = params['height']
        self.black: int = params['black']
        self.white: int = params['white']
        self.score: int = params['score']
        self.day3elg: float = params['day3elg']
        self.data: list[StockDataModel] = params['data']

    def k1(self):
        return self.white > 30

    def k2(self):
        return self.black == 0

    def k3(self):
        return self.CF > 50

    def k4(self):
        return self.TF > 80

    def k5(self):
        return self.CP > (65 if not self.is1 else 99)

    def k6(self):
        return self.TP > (40 if not self.is1 else 95)

    def k7(self):
        return self.score > 60

    def k8(self):
        return self.day3elg > 70

    def k9(self):
        return self.AJ < 0.11

    def k10(self):
        return getMinute(stamp=self.data[-1].firstLimitTime) < '0945'

    def j1(self):
        return self.k1()

    def j2(self):
        return self.k2()

    def j3(self):
        if t_limit(self.stock, self.data, 2):
            return False
        try:
            for i in range(1, 91):
                if t_close_pct(self.data, i) > 0.045:
                    return True
            return False
        except:
            return False

    def j4(self):
        return self.k4()

    def j5(self):
        return self.CP > (99 if self.is1 else 60)

    def j6(self):
        return self.TP > (95 if self.is1 else 35)

    def j7(self):
        return self.k7()

    def j8(self):
        try:
            for i in range(1, 81):
                if limit_height(self.stock, self.data, i) >= 3:
                    return False
            return True
        except:
            return False

    def j9(self):
        return self.k9()

    def j10(self):
        return getMinute(stamp=self.data[-1].firstLimitTime) > '0937'

    def filter(self):
        rule_key = 'j' if self.height == 1 else 'k'
        rules = [_ for _ in self.__class__.__dict__.keys() if _.startswith(rule_key)]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                self.passes.append(rule)

    @property
    def limitRank(self) -> str:
        if self.height == 1:
            if self.black < 2:
                if 8 <= len(self.passes) <= 10:
                    return 'S'
                if 6 <= len(self.passes) <= 7:
                    return 'A'
                if 4 <= len(self.passes) <= 5:
                    return 'B'
                if 0 <= len(self.passes) <= 3:
                    return 'F'
            else:
                if self.CP > (60 if not self.is1 else 90) and self.TP > (35 if not self.is1 else 95) and self.day3elg > 60 and getMinute(stamp=self.data[-1].firstLimitTime) > '0937':
                    return 'B'
                else:
                    return 'F'
        if self.height == 2 and self.black < 2:
            if 8 <= len(self.passes) <= 10:
                return 'S'
            if 6 <= len(self.passes) <= 7:
                return 'A'
            if 4 <= len(self.passes) <= 5:
                return 'B'
            if 0 <= len(self.passes) <= 3:
                return 'F'
        elif self.height == 2 and self.black >= 2:
            if self.CP > (65 if not self.is1 else 90) and self.TP > (40 if not self.is1 else 95) and self.day3elg > 60:
                return 'B'
            else:
                return 'F'
        elif self.height >= 3 and self.black < 2:
            if self.CP > (60 if not self.is1 else 80):
                if self.day3elg > 60:
                    return 'A'
                elif 50 <= self.day3elg <= 60:
                    return 'B'
                else:
                    return 'F'
            else:
                return 'F'
        elif self.height >= 3 and self.black >= 2:
            if self.CP > (60 if not self.is1 else 90):
                if self.day3elg > 70:
                    return 'A'
                elif 60 <= self.day3elg <= 70:
                    return 'B'
                else:
                    return 'F'
            else:
                return 'F'
