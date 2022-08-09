# -*- coding: utf-8 -*-
# @Time    : 2022/6/21 00:05
# @Author  : Destiny_
# @File    : level2.py
# @Software: PyCharm
from typing import List

from common import dateHandler
from common.collect_data import dataModel, t_limit, t_open_pct, t_low_pct


def rule1(data: List[dataModel]):
    range5 = data[-5:]
    range6to10 = data[-10:-5]
    if sum([_.turnover() for _ in range5]) > 2 * sum([_.turnover() for _ in range6to10]):
        return True


def rule2(data: List[dataModel]):
    err = None
    try:
        range60 = data[-60:]
        range220 = data[-220:]
        if max([_.turnover() for _ in range60]) > 5 * sum([_.turnover() for _ in range220]) / 220:
            return True
    except Exception as e:
        err = e
        return False


def rule3(stock, data: List[dataModel]):
    for i in range(1, 4):
        if not t_limit(stock, data, i - 1):
            return False
        if t_open_pct(data, i - 1) <= 0:
            return False
        if t_low_pct(data, i - 1) <= -0.01:
            return False
    return True


def rule4(data: List[dataModel]):
    range10 = data[-11:-1]
    range30 = data[-31:-1]
    if sum(_.close() for _ in range10) / 10 > sum(_.close() for _ in range30) / 30:
        return True


def rule5(data: List[dataModel]):
    range10 = data[-11:-1]
    range20 = data[-21:-1]
    if sum(_.close() for _ in range10) / 10 > sum(_.close() for _ in range20) / 20:
        return True


def rule6(data: List[dataModel]):
    try:
        range20 = data[-21:-1]
        range30 = data[-31:-1]
        if sum(_.close() for _ in range20) / 20 > sum(_.close() for _ in range30) / 30:
            return True
    except Exception:
        return False


def rule7(data: List[dataModel]):
    try:
        range30 = data[-31:-1]
        range60 = data[-61:-1]
        if sum(_.close() for _ in range30) / 30 > sum(_.close() for _ in range60) / 60:
            return True
    except Exception:
        return False


def rule8(data: List[dataModel]):
    try:
        range60 = data[-61:-1]
        range120 = data[-121:-1]
        if sum(_.close() for _ in range60) / 60 > sum(_.close() for _ in range120) / 120:
            return True
    except:
        return False


def rule9(data: List[dataModel]):
    high3 = max(data[-1].high(), data[-2].high(), data[-3].high())
    high220 = max([_.high() for _ in data[-223:-3]])
    if high3 > high220:
        return True


def rule10(data: List[dataModel]):
    if data[-3].turnover() < data[-2].turnover() < data[-1].turnover():
        if data[-3].close() < data[-2].close() < data[-1].close():
            return True


def rule11(data: List[dataModel]):
    if data[-4].turnover() < data[-3].turnover() < data[-2].turnover():
        if data[-4].close() < data[-3].close() < data[-2].close():
            return True


def rule12(data: List[dataModel]):
    if data[-5].turnover() < data[-4].turnover() < data[-3].turnover():
        if data[-5].close() < data[-4].close() < data[-3].close():
            return True


def rule13(data: List[dataModel]):
    if data[-5].turnover() < data[-3].turnover() < data[-2].turnover():
        if data[-5].close() < data[-3].close() < data[-2].close():
            return True


def rule14(data: List[dataModel]):
    if data[-5].turnover() < data[-4].turnover() < data[-2].turnover():
        if data[-5].close() < data[-4].close() < data[-2].close():
            return True


def rule15(data: List[dataModel]):
    range10 = data[-10:]
    range60 = data[-70:-10]
    if max([_.high() for _ in range10]) > max([_.high() for _ in range60]):
        return True


def rule16(data: List[dataModel]):
    range10 = data[-10:]
    range20 = data[-30:-10]
    if max([_.high() for _ in range10]) > max([_.high() for _ in range20]):
        return True


def rule17(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    matchTime1 = dateHandler.joinTimeToStamp(data[-1].date(), '09:40:00')
    matchTime2 = dateHandler.joinTimeToStamp(data[-1].date(), '10:00:00')
    if matchTime1 <= data[-1].firstLimitTime() <= matchTime2:
        return True


def rule18(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    try:
        range1to5 = data[-6:-1]
        range1to10 = data[-11:-1]
        range1to20 = data[-21:-1]
        if sum([_.close() for _ in range1to5]) / 5 > sum([_.close() for _ in range1to20]) / 20:
            if data[-2].close() > sum([_.close() for _ in range1to10]) / 10:
                return True
    except:
        return False


class level2:
    def __init__(self, stock: str, data: List[dataModel]):
        self.level = 2
        self.data = data
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def filter(self):
        self.shot_rule.append(1) if rule1(self.data) else self.fail_rule.append(1)
        self.shot_rule.append(2) if rule2(self.data) else self.fail_rule.append(2)
        self.shot_rule.append(3) if rule3(self.stock, self.data) else self.fail_rule.append(3)
        self.shot_rule.append(4) if rule4(self.data) else self.fail_rule.append(4)
        self.shot_rule.append(5) if rule5(self.data) else self.fail_rule.append(5)
        self.shot_rule.append(6) if rule6(self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.data) else self.fail_rule.append(8)
        self.shot_rule.append(9) if rule9(self.data) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.data) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.data) else self.fail_rule.append(12)
        self.shot_rule.append(13) if rule13(self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.data) else self.fail_rule.append(14)
        self.shot_rule.append(15) if rule15(self.data) else self.fail_rule.append(15)
        self.shot_rule.append(16) if rule16(self.data) else self.fail_rule.append(16)
        self.shot_rule.append(17) if rule17(self.stock, self.data) else self.fail_rule.append(17)
        self.shot_rule.append(18) if rule18(self.stock, self.data) else self.fail_rule.append(18)
        return self.result()
