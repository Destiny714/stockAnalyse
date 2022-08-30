# -*- coding: utf-8 -*-
# @Time    : 2022/8/30 19:28
# @Author  : Destiny_
# @File    : levelA4.py
# @Software: PyCharm
from typing import List

from common.collect_data import dataModel


def rule1(data: List[dataModel]):
    try:
        d1 = data[-2]
        d2 = data[-3]
        if (d2.buy_elg_vol() + d1.buy_elg_vol() - d2.sell_elg_vol() - d1.sell_elg_vol()) / (
                d2.buy_elg_vol() + d1.buy_elg_vol()) > 0.5:
            return True
    except:
        pass


def rule2(data: List[dataModel]):
    try:
        d0 = data[-1]
        d1 = data[-2]
        d2 = data[-3]
        if (d2.buy_elg_vol() + d1.buy_elg_vol() + d0.buy_elg_vol - d0.sell_elg_vol() - d1.sell_elg_vol()) / (
                d0.buy_elg_vol() + d1.buy_elg_vol()) > 0.3:
            return True
    except:
        pass


def rule3(data: List[dataModel]):
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


class levelA4:
    def __init__(self, stock: str, data: List[dataModel]):
        self.level = 'A4'
        self.data = data
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def filter(self):
        self.shot_rule.append(1) if rule1(self.data) else self.fail_rule.append(1)
        self.shot_rule.append(2) if rule2(self.data) else self.fail_rule.append(2)
        self.shot_rule.append(3) if rule3(self.data) else self.fail_rule.append(3)
        return self.result()
