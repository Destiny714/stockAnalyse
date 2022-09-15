# -*- coding: utf-8 -*-
# @Time    : 2022/8/30 19:28
# @Author  : Destiny_
# @File    : levelA4.py
# @Software: PyCharm
from common.dataOperation import dataModel


class levelA4:
    def __init__(self, stock: str, data: list[dataModel]):
        self.level = 'A4'
        self.data = data
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def rule1(self):
        data = self.data
        try:
            d1 = data[-2]
            d2 = data[-3]
            if (d2.buy_elg_vol() + d1.buy_elg_vol() - d2.sell_elg_vol() - d1.sell_elg_vol()) / (
                    d2.buy_elg_vol() + d1.buy_elg_vol()) > 0.5:
                return True
        except:
            pass

    def rule2(self):
        data = self.data
        try:
            d0 = data[-1]
            d1 = data[-2]
            d2 = data[-3]
            if (d2.buy_elg_vol() + d1.buy_elg_vol() + d0.buy_elg_vol - d0.sell_elg_vol() - d1.sell_elg_vol()) / (
                    d0.buy_elg_vol() + d1.buy_elg_vol()) > 0.3:
                return True
        except:
            pass

    def rule3(self):
        data = self.data
        try:
            d0 = data[-1]
            d1 = data[-2]
            d2 = data[-3]
            if (
                    d2.buy_elg_vol() + d1.buy_elg_vol() + d0.buy_elg_vol() - d2.sell_elg_vol() - d1.sell_elg_vol() - d0.sell_elg_vol()) / (
                    d2.buy_elg_vol() + d1.buy_elg_vol() + d0.buy_elg_vol()) > 0.4:
                return True
        except:
            pass

    def filter(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            ruleID = int(str(rule).replace('rule', ''))
            self.shot_rule.append(ruleID) if func() else self.fail_rule.append(ruleID)
        return self.result()
