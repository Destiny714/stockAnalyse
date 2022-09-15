# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 18:52
# @Author  : Destiny_
# @File    : levelA1.py
# @Software: PyCharm

from common.dataOperation import dataModel


class levelA1:
    def __init__(self, stock: str, data: list[dataModel]):
        self.level = 'A1'
        self.data = data
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def rule1(self):
        data = self.data
        try:
            d = data[-1]
            if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.55:
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.7:
                    if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                            d.buy_elg_vol() + d.buy_lg_vol()) > 0.3:
                        return True
        except:
            pass

    def rule2(self):
        data = self.data
        try:
            d = data[-1]
            if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.45:
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.6:
                    if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                            d.buy_elg_vol() + d.buy_lg_vol()) > 0.2:
                        return True
        except:
            pass

    def rule3(self):
        data = self.data
        try:
            d = data[-1]
            if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.35:
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.5:
                    if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                            d.buy_elg_vol() + d.buy_lg_vol()) > 0.1:
                        return True
        except:
            pass

    def rule4(self):
        data = self.data
        try:
            d = data[-1]
            if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.3:
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.4:
                    if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                            d.buy_elg_vol() + d.buy_lg_vol()) > 0.05:
                        return True
        except:
            pass

    def rule5(self):
        data = self.data
        try:
            d = data[-2]
            if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.6:
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.5:
                    if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                            d.buy_elg_vol() + d.buy_lg_vol()) > 0.3:
                        d0 = data[-1]
                        if (d0.buy_elg_vol() - d0.sell_elg_vol()) / d0.buy_elg_vol() > 0.3:
                            return True
        except:
            pass

    def rule6(self):
        data = self.data
        try:
            d = data[-2]
            if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.5:
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.4:
                    if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                            d.buy_elg_vol() + d.buy_lg_vol()) > 0.2:
                        d0 = data[-1]
                        if (d0.buy_elg_vol() - d0.sell_elg_vol()) / d0.buy_elg_vol() > 0.3:
                            return True
        except:
            pass

    def rule7(self):
        data = self.data
        try:
            for i in range(2):
                d = data[-i - 1]
                if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() <= 0.5:
                    return False
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() <= 0.3:
                    return False
            return True
        except:
            pass

    def rule8(self):
        data = self.data
        try:
            for i in range(3):
                d = data[-i - 1]
                if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() <= 0.5:
                    return False
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() <= 0.25:
                    return False
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
