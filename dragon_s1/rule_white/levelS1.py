# -*- coding: utf-8 -*-
# @Time    : 2022/7/31 22:40
# @Author  : Destiny_
# @File    : levelS1.py
# @Software: PyCharm
from typing import List

from common.collect_data import dataModel, t_limit


def rule1(stock, data: List[dataModel]):
    try:
        for i in range(3):
            if not t_limit(stock, data, i):
                return False
        d = data[-1]
        if d.buy_elg_vol() / d.volume() <= 0.25:
            return False
        if d.buy_lg_vol() / d.volume() <= 0.15:
            return False
        if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() <= 0.4:
            return False
        if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() <= 0.5:
            return False
        if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                d.buy_elg_vol() + d.buy_lg_vol()) > 0.2:
            return True
    except:
        pass


def rule2(stock, data: List[dataModel]):
    try:
        for i in range(3):
            if not t_limit(stock, data, i):
                return False
        d = data[-1]
        if d.buy_elg_vol() / d.volume() <= 0.35:
            return False
        if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() <= 0.5:
            return False
        if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                d.buy_elg_vol() + d.buy_lg_vol()) > 0.2:
            return True
    except:
        pass


def rule3(stock, data: List[dataModel]):
    try:
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
        if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() <= 0.5:
            return False
        if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                d.buy_elg_vol() + d.buy_lg_vol()) > 0.2:
            return True
    except:
        pass


def rule4(stock, data: List[dataModel]):
    try:
        if t_limit(stock, data, 2):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        d = data[-1]
        if d.buy_elg_vol() / d.volume() <= 0.3:
            return False
        if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() <= 0.5:
            return False
        if d.buy_lg_vol() / d.volume() <= 0.18:
            return False
        if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() <= 0.5:
            return False
        if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                d.buy_elg_vol() + d.buy_lg_vol()) > 0.2:
            return True
    except:
        pass


class levelS1:
    def __init__(self, stock: str, data: List[dataModel]):
        self.level = 'S1'
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
