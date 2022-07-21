# -*- coding: utf-8 -*-
# @Time    : 2022/6/21 00:05
# @Author  : Destiny_
# @File    : level2.py
# @Software: PyCharm
from typing import List

from common import dateHandler
from common.collect_data import dataModel, t_limit


def rule1(data: List[dataModel]):
    range5 = data[-5:]
    range6to10 = data[-10:-5]
    if sum([_.volume() for _ in range5]) > 2 * sum([_.volume() for _ in range6to10]):
        return True


def rule2(data: List[dataModel]):
    err = None
    try:
        range60 = data[-60:]
        range220 = data[-220:]
        if max([_.volume() for _ in range60]) > 5 * sum([_.volume() for _ in range220]) / 220:
            return True
    except Exception as e:
        err = e
        return False


def rule4(data: List[dataModel]):
    range10 = data[-10:]
    range30 = data[-30:]
    if max(_.close() for _ in range10) > sum(_.close() for _ in range30) / 30:
        return True


def rule9(data: List[dataModel]):
    high3 = max(data[-1].high(), data[-2].high(), data[-3].high())
    high220 = max([_.high() for _ in data[-223:-3]])
    if high3 > high220:
        return True


def rule10(data: List[dataModel]):
    if data[-3].volume() < data[-2].volume() < data[-1].volume():
        if data[-3].close() < data[-2].close() < data[-1].close():
            return True


def rule11(data: List[dataModel]):
    if data[-4].volume() < data[-3].volume() < data[-2].volume():
        if data[-4].close() < data[-3].close() < data[-2].close():
            return True


def rule12(data: List[dataModel]):
    if data[-5].volume() < data[-4].volume() < data[-3].volume():
        if data[-5].close() < data[-4].close() < data[-3].close():
            return True


def rule13(data: List[dataModel]):
    if data[-5].volume() < data[-3].volume() < data[-2].volume():
        if data[-5].close() < data[-3].close() < data[-2].close():
            return True


def rule14(data: List[dataModel]):
    if data[-5].volume() < data[-4].volume() < data[-2].volume():
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
        self.shot_rule.append(4) if rule4(self.data) else self.fail_rule.append(4)
        self.shot_rule.append(9) if rule9(self.data) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.data) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.data) else self.fail_rule.append(12)
        self.shot_rule.append(13) if rule13(self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.data) else self.fail_rule.append(14)
        self.shot_rule.append(15) if rule15(self.data) else self.fail_rule.append(15)
        self.shot_rule.append(16) if rule16(self.data) else self.fail_rule.append(16)
        self.shot_rule.append(17) if rule17(self.stock, self.data) else self.fail_rule.append(17)
        return self.result()