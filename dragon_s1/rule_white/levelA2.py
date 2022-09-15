# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 18:52
# @Author  : Destiny_
# @File    : levelA2.py
# @Software: PyCharm

from common.dataOperation import *


class levelA2:
    def __init__(self, stock: str, data: list[dataModel]):
        self.level = 'A2'
        self.data = data
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

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
            if d.buy_elg_vol() / d.volume() <= 0.4:
                return False
            if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() <= 0.6:
                return False
            if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                    d.buy_elg_vol() + d.buy_lg_vol()) <= 0.4:
                return False
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() <= 0.7:
                return False
            d1 = data[-2]
            if (d1.buy_elg_vol() - d1.sell_elg_vol()) / d1.buy_elg_vol() > 0.5:
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
            if d.buy_elg_vol() / d.volume() <= 0.35:
                return False
            if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() <= 0.55:
                return False
            if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                    d.buy_elg_vol() + d.buy_lg_vol()) <= 0.35:
                return False
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() <= 0.6:
                return False
            d1 = data[-2]
            if (d1.buy_elg_vol() - d1.sell_elg_vol()) / d1.buy_elg_vol() > 0.45:
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
            if d.buy_elg_vol() / d.volume() <= 0.35:
                return False
            if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() <= 0.5:
                return False
            if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                    d.buy_elg_vol() + d.buy_lg_vol()) <= 0.3:
                return False
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() <= 0.5:
                return False
            d1 = data[-2]
            if (d1.buy_elg_vol() - d1.sell_elg_vol()) / d1.buy_elg_vol() > 0.4:
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
            if d.buy_elg_vol() / d.volume() <= 0.35:
                return False
            if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() <= 0.45:
                return False
            if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                    d.buy_elg_vol() + d.buy_lg_vol()) <= 0.2:
                return False
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() <= 0.4:
                return False
            d1 = data[-2]
            if (d1.buy_elg_vol() - d1.sell_elg_vol()) / d1.buy_elg_vol() > 0.35:
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
            if d.buy_elg_vol() / d.volume() <= 0.35:
                return False
            if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() <= 0.4:
                return False
            if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                    d.buy_elg_vol() + d.buy_lg_vol()) <= 0.15:
                return False
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() <= 0.3:
                return False
            d1 = data[-2]
            if (d1.buy_elg_vol() - d1.sell_elg_vol()) / d1.buy_elg_vol() > 0.3:
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
