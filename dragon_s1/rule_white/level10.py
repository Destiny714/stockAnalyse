# -*- coding: utf-8 -*-
# @Time    : 2022/7/31 22:40
# @Author  : Destiny_
# @File    : level10.py
# @Software: PyCharm
from typing import List

from common.collect_data import dataModel, t_limit


def rule1(stock, data: List[dataModel]):
    for i in range(3):
        if not t_limit(stock, data, i):
            return False
    d = data[-1]
    if d.buy_elg_vol() / d.volume() <= 0.15:
        return False
    if d.buy_lg_vol() / d.volume() <= 0.15:
        return False
    if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() <= 0.4:
        return False
    if (d.buy_elg_vol() + d.buy_lg_vol()) <= (d.sell_elg_vol() + d.sell_lg_vol()):
        return False
    return True


def rule2(stock, data: List[dataModel]):
    for i in range(3):
        if not t_limit(stock, data, i):
            return False
    d = data[-1]
    if d.buy_elg_vol() / d.volume() <= 0.35:
        return False
    if (d.buy_elg_vol() + d.buy_lg_vol()) <= (d.sell_elg_vol() + d.sell_lg_vol()):
        return False
    return True


def rule3(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
    d = data[-1]
    if d.buy_elg_vol() / d.volume() <= 0.35:
        return False
    if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() <= 0.6:
        return False
    if d.buy_elg_vol() <= d.sell_elg_vol():
        return False
    if (d.buy_elg_vol() + d.buy_lg_vol()) <= (d.sell_elg_vol() + d.sell_lg_vol()):
        return False
    return True


def rule4(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
    d = data[-1]
    if d.buy_elg_vol() / d.volume() <= 0.25:
        return False
    if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() <= 0.45:
        return False
    if d.buy_lg_vol() / d.volume() <= 0.18:
        return False
    if (d.buy_elg_vol() + d.buy_lg_vol()) <= (d.sell_elg_vol() + d.sell_lg_vol()):
        return False
    return True


def rule5(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if data[-1].buy_elg_vol() / data[-1].volume() <= 0.4:
        return False
    if data[-1].buy_elg_vol() <= data[-1].sell_elg_vol():
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) > (data[-1].sell_elg_vol() + data[-1].sell_lg_vol()):
        return True


def rule6(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) / data[-1].volume() <= 0.3:
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) > (data[-1].sell_elg_vol() + data[-1].sell_lg_vol()):
        return True


def rule7(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if data[-1].buy_elg_vol() / data[-1].volume() <= 0.2:
        return False
    if data[-1].buy_lg_vol() / data[-1].volume() <= 0.15:
        return False
    if data[-1].buy_elg_vol() <= data[-1].sell_elg_vol():
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) > (data[-1].sell_elg_vol() + data[-1].sell_lg_vol()):
        return True


def rule8(stock, data: List[dataModel]):
    if t_limit(stock, data):
        return False
    if data[-1].buy_elg_vol() / data[-1].volume() <= 0.4:
        return False
    if data[-1].buy_elg_vol() <= data[-1].sell_elg_vol():
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) > (data[-1].sell_elg_vol() + data[-1].sell_lg_vol()):
        return True


def rule9(stock, data: List[dataModel]):
    if t_limit(stock, data):
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) / data[-1].volume() <= 0.3:
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) > (data[-1].sell_elg_vol() + data[-1].sell_lg_vol()):
        return True


def rule10(stock, data: List[dataModel]):
    if t_limit(stock, data):
        return False
    if (data[-1].buy_elg_vol() + data[-1].buy_lg_vol()) / data[-1].volume() <= 0.2:
        return False
    if data[-1].buy_elg_vol() > data[-1].sell_elg_vol():
        if data[-1].buy_lg_vol() > data[-1].sell_lg_vol():
            return True


class level10:
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
        self.shot_rule.append(5) if rule5(self.stock, self.data) else self.fail_rule.append(5)
        self.shot_rule.append(6) if rule6(self.stock, self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.stock, self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.stock, self.data) else self.fail_rule.append(8)
        self.shot_rule.append(9) if rule9(self.stock, self.data) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.stock, self.data) else self.fail_rule.append(10)
        return self.result()
