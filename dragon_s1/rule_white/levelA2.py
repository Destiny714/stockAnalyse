# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 18:52
# @Author  : Destiny_
# @File    : levelA2.py
# @Software: PyCharm
from typing import List

from common.collect_data import dataModel, t_limit


def rule1(data: List[dataModel]):
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) / data[-1].volume() <= 0.5:
        return False
    if data[-1].buy_elg_vol() <= data[-1].sell_elg_vol():
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) > (data[-1].sell_elg_vol() + data[-1].sell_lg_vol()):
        return True


def rule2(data: List[dataModel]):
    if data[-1].buy_elg_vol() / data[-1].volume() <= 0.35:
        return False
    if data[-1].buy_elg_vol() <= data[-1].sell_elg_vol():
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) > (data[-1].sell_elg_vol() + data[-1].sell_lg_vol()):
        return True


class levelA2:
    def __init__(self, stock: str, data: List[dataModel]):
        self.level = 'A2'
        self.data = data
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def filter(self):
        self.shot_rule.append(1) if rule1(self.data) else self.fail_rule.append(1)
        self.shot_rule.append(2) if rule2(self.data) else self.fail_rule.append(2)
        return self.result()
