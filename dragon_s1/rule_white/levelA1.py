# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 18:52
# @Author  : Destiny_
# @File    : levelA1.py
# @Software: PyCharm
from typing import List

from common.collect_data import dataModel


def rule1(data: List[dataModel]):
    try:
        d = data[-1]
        if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.65:
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.6:
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                        d.buy_elg_vol() + d.buy_lg_vol()) > 0.3:
                    return True
    except:
        pass


def rule2(data: List[dataModel]):
    try:
        d = data[-1]
        if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.55:
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.5:
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                        d.buy_elg_vol() + d.buy_lg_vol()) > 0.2:
                    return True
    except:
        pass


def rule3(data: List[dataModel]):
    try:
        d = data[-1]
        if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.45:
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.4:
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                        d.buy_elg_vol() + d.buy_lg_vol()) > 0.1:
                    return True
    except:
        pass


def rule4(data: List[dataModel]):
    try:
        d = data[-1]
        if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.4:
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.3:
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                        d.buy_elg_vol() + d.buy_lg_vol()) > 0.05:
                    return True
    except:
        pass


def rule5(data: List[dataModel]):
    try:
        d = data[-2]
        if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() > 0.55:
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.5:
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                        d.buy_elg_vol() + d.buy_lg_vol()) > 0.3:
                    d0 = data[-1]
                    if (d0.buy_elg_vol() - d0.sell_elg_vol()) / d0.buy_elg_vol() > 0.3:
                        return True
    except:
        pass


def rule6(data: List[dataModel]):
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


def rule7(data: List[dataModel]):
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


def rule8(data: List[dataModel]):
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
        self.shot_rule.append(5) if rule5(self.data) else self.fail_rule.append(5)
        self.shot_rule.append(6) if rule6(self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.data) else self.fail_rule.append(8)
        return self.result()
