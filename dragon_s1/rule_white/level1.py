# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 21:30
# @Author  : Destiny_
# @File    : level1.py
# @Software: PyCharm
from typing import List

from common.collect_data import dataModel, limit, t_low_pct, t_limit, t_close_pct


def rule2(data: List[dataModel]):
    for i in range(1, 4):
        if t_low_pct(data, i - 1) <= -0.03:
            return False
    return True


def rule3(data: List[dataModel]):
    for i in range(1, 11):
        high60 = max([_.high() for _ in data[-60 - i:-i]])
        if data[-i].close() <= high60:
            return False
    return True


def rule4(stock, data: List[dataModel]):
    if data[-1].pctChange() <= limit(stock):
        return False
    if data[-2].pctChange() > limit(stock):
        return False
    for _ in data[-61:-1]:
        if _.pctChange() > limit(stock):
            return True


def rule5(data: List[dataModel]):
    if data[-1].low() <= data[-2].low():
        return False
    if data[-2].low() > data[-3].low():
        return True


def rule6(data: List[dataModel]):
    for i in range(1, 4):
        high20 = max([_.turnover() for _ in data[-20 - i:-i]])
        if data[-i].turnover() > high20:
            return True


def rule7(data: List[dataModel]):
    for i in range(1, 4):
        high30 = max([_.high() for _ in data[-30 - i:-i]])
        if data[-i].close() > high30:
            return True


def rule8(data: List[dataModel]):
    range5to20 = data[-21:-5]
    avgChangeRate = sum([(_.turnover()) for _ in range5to20]) / 16
    if avgChangeRate > 2.5:
        return True


def rule9(data: List[dataModel]):
    rangeData = data[-21:-10]
    volumeSum = sum([_.amount() for _ in rangeData])
    avgVolume = (volumeSum / 11) / 10
    if avgVolume > 50000:
        return True


def rule10(data: List[dataModel]):
    err = None
    try:
        range3month = data[-90:]
        range3year = data[-660:]
        if max([_.turnover() for _ in range3month]) > sum([_.turnover() for _ in range3year]) / 660:
            return True
    except Exception as e:
        err = e
        return False


class level1:
    def __init__(self, stock: str, data: List[dataModel]):
        self.level = 1
        self.data = data
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def filter(self):
        self.shot_rule.append(2) if rule2(self.data) else self.fail_rule.append(2)
        self.shot_rule.append(3) if rule3(self.data) else self.fail_rule.append(3)
        self.shot_rule.append(4) if rule4(self.stock, self.data) else self.fail_rule.append(4)
        self.shot_rule.append(5) if rule5(self.data) else self.fail_rule.append(5)
        self.shot_rule.append(6) if rule6(self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.data) else self.fail_rule.append(8)
        self.shot_rule.append(9) if rule9(self.data) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.data) else self.fail_rule.append(10)
        return self.result()
