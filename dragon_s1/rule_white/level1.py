# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 21:30
# @Author  : Destiny_
# @File    : level1.py
# @Software: PyCharm
from common.dataOperation import *


class level1:
    def __init__(self, stock: str, data: list[dataModel]):
        self.level = 1
        self.data = data
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def rule2(self):
        data = self.data
        for i in range(1, 4):
            if t_low_pct(data, i - 1) <= -0.03:
                return False
        return True

    def rule3(self):
        data = self.data
        for i in range(1, 11):
            high60 = max([_.high() for _ in data[-60 - i:-i]])
            if data[-i].close() <= high60:
                return False
        return True

    def rule4(self):
        data = self.data
        stock = self.stock
        if data[-1].pctChange() <= limit(stock):
            return False
        if data[-2].pctChange() > limit(stock):
            return False
        for _ in data[-61:-1]:
            if _.pctChange() > limit(stock):
                return True

    def rule5(self):
        data = self.data
        if data[-1].low() <= data[-2].low():
            return False
        if data[-2].low() > data[-3].low():
            return True

    def rule6(self):
        data = self.data
        for i in range(1, 4):
            high20 = max([_.turnover() for _ in data[-20 - i:-i]])
            if data[-i].turnover() > high20:
                return True

    def rule7(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 3):
            return False
        for i in range(1, 4):
            high30 = max([_.high() for _ in data[-30 - i:-i]])
            if data[-i].close() > high30:
                return True

    def rule8(self):
        data = self.data
        range5to20 = data[-21:-5]
        avgChangeRate = sum([(_.turnover()) for _ in range5to20]) / 16
        if avgChangeRate > 2.5:
            return True

    def rule9(self):
        data = self.data
        rangeData = data[-21:-10]
        volumeSum = sum([_.amount() for _ in rangeData])
        avgVolume = (volumeSum / 11) / 10
        if avgVolume > 50000:
            return True

    def rule10(self):
        data = self.data
        try:
            range3month = data[-90:]
            range3year = data[-660:]
            if max([_.turnover() for _ in range3month]) > sum([_.turnover() for _ in range3year]) / 660:
                return True
        except:
            return False

    def filter(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            ruleID = int(str(rule).replace('rule', ''))
            self.shot_rule.append(ruleID) if func() else self.fail_rule.append(ruleID)
        return self.result()
