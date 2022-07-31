# -*- coding: utf-8 -*-
# @Time    : 2022/7/31 22:40
# @Author  : Destiny_
# @File    : level11.py
# @Software: PyCharm
from typing import List

from common.collect_data import dataModel, t_limit


def rule1(stock, data: List[dataModel]):
    for i in range(3):
        if not t_limit(stock, data, i):
            return False
    if data[-1].buy_elg_vol() / data[-1].volume() <= 0.45:
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) / data[-1].volume() <= 0.65:
        return False
    if data[-1].buy_elg_vol() <= data[-1].sell_elg_vol():
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) > (data[-1].sell_elg_vol() + data[-1].sell_lg_vol()):
        return True


def rule2(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
    if data[-1].buy_elg_vol() / data[-1].volume() <= 0.4:
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) / data[-1].volume() <= 0.7:
        return False
    if data[-1].buy_elg_vol() <= data[-1].sell_elg_vol():
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) > (data[-1].sell_elg_vol() + data[-1].sell_lg_vol()):
        return True


def rule3(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if data[-1].buy_elg_vol() / data[-1].volume() <= 0.4:
        return False
    if data[-1].buy_lg_vol() / data[-1].volume() <= 0.18:
        return False
    if data[-1].buy_elg_vol() <= data[-1].sell_elg_vol():
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) > (data[-1].sell_elg_vol() + data[-1].sell_lg_vol()):
        return True


def rule4(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) / data[-1].volume() <= 0.55:
        return False
    if data[-1].buy_elg_vol() <= data[-1].sell_elg_vol():
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) > (data[-1].sell_elg_vol() + data[-1].sell_lg_vol()):
        return True


class level11:
    def __init__(self, stock: str, data: List[dataModel]):
        self.level = 1
        self.data = data
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def filter(self):
        self.shot_rule.append(1) if rule1(self.stock, self.data) else self.fail_rule.append(1)
        self.shot_rule.append(2) if rule2(self.stock, self.data) else self.fail_rule.append(2)
        self.shot_rule.append(3) if rule3(self.stock, self.data) else self.fail_rule.append(3)
        self.shot_rule.append(4) if rule4(self.stock, self.data) else self.fail_rule.append(4)
        return self.result()
