# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 18:52
# @Author  : Destiny_
# @File    : levelA1.py
# @Software: PyCharm
from typing import List

from common.collect_data import dataModel, t_limit


def rule1(data: List[dataModel]):
    d = data[-1]
    if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.65:
        if d.buy_elg_vol() > d.sell_elg_vol():
            if d.buy_elg_vol() + d.buy_lg_vol() > d.sell_elg_vol() + d.sell_lg_vol():
                return True


def rule2(data: List[dataModel]):
    d = data[-1]
    if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.55:
        if d.buy_elg_vol() > d.sell_elg_vol():
            if d.buy_elg_vol() + d.buy_lg_vol() > d.sell_elg_vol() + d.sell_lg_vol():
                return True


def rule3(data: List[dataModel]):
    d = data[-1]
    if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.45:
        if d.buy_elg_vol() > d.sell_elg_vol():
            if d.buy_elg_vol() + d.buy_lg_vol() > d.sell_elg_vol() + d.sell_lg_vol():
                return True


def rule4(data: List[dataModel]):
    d = data[-1]
    if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.35:
        if d.buy_elg_vol() > d.sell_elg_vol():
            if d.buy_elg_vol() + d.buy_lg_vol() > d.sell_elg_vol() + d.sell_lg_vol():
                return True


class levelA1:
    def __init__(self, stock: str, data: List[dataModel]):
        self.level = 'A1'
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
        self.shot_rule.append(4) if rule4(self.data) else self.fail_rule.append(4)
        return self.result()
