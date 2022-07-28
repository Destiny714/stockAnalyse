# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:25
# @Author  : Destiny_
# @File    : level9.py
# @Software: PyCharm

from typing import List

from common import dateHandler
from common.collect_data import t_low_pct, t_close_pct, t_open_pct, limit, dataModel, model_1, model_t, t_limit


def rule1(stock, data: List[dataModel]):
    if data[-1].turnover() <= 1:
        return False
    count = 0
    for i in range(1, 6):
        if t_open_pct(data, i - 1) >= -0.01:
            continue
        if t_close_pct(data, i - 1) > limit(stock) / 100:
            count += 1
    if count >= 2:
        return True


def rule2(stock, data: List[dataModel]):
    if data[-1].limitOpenTime() <= 1:
        return False
    for i in range(1, 6):
        if t_low_pct(data, i - 1) >= -0.06:
            continue
        if t_close_pct(data, i - 1) > limit(stock) / 100:
            return True


def rule3(data: List[dataModel]):
    count = 0
    for i in range(1, 6):
        if t_open_pct(data, i - 1) <= 0.08:
            continue
        matchTime = dateHandler.joinTimeToStamp(data[-i].date(), '10:00:00')
        if data[-i].lastLimitTime() > matchTime:
            count += 1
        if count >= 2:
            return True


def rule4(stock, data: List[dataModel]):
    if model_1(stock, data, 1):
        return False
    if not model_1(stock, data):
        return False
    if data[-1].turnover() > data[-2].turnover() / 3:
        return True


def rule5(data: List[dataModel]):
    if sum([data[-1].turnover(), data[-2].turnover(), data[-3].turnover()]) <= 40:
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '10:00:00')
    if data[-1].firstLimitTime() > matchTime and data[-1].lastLimitTime() > matchTime:
        return True


def rule6(stock, data: List[dataModel]):
    if data[-5].pctChange() > limit(stock):
        return False
    if data[-4].pctChange() > limit(stock):
        return False
    if model_1(stock, data, 2):
        return False
    if data[-3].pctChange() <= limit(stock):
        return False
    if not model_1(stock, data, 1):
        return False
    if t_open_pct(data) < limit(stock) / 100:
        return False
    if t_low_pct(data) >= limit(stock) / 100:
        return False
    if not model_t(stock, data):
        return False
    if data[-1].turnover() > 1.8 * max([_.turnover() for _ in data[-6:-1]]):
        return True


def rule7(data: List[dataModel]):
    if data[-1].turnover() <= 1.5 * data[-2].turnover():
        return False
    standard = (sum([data[-_].turnover() for _ in range(3, 8)]) / 5) * 3
    if data[-1].turnover() > standard and data[-2].turnover() > standard:
        return True


def rule8(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if data[-1].turnover() > 3 * data[-2].turnover():
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '11:00:00')
        if data[-1].firstLimitTime() > matchTime and data[-1].lastLimitTime() > matchTime:
            return True


def rule10(data: List[dataModel]):
    if data[-1].turnover() <= 10:
        return False
    range20 = data[-21:-1]
    if data[-1].turnover() > 2.5 * max([_.turnover() for _ in range20]):
        return True


def rule11(stock, data: List[dataModel]):
    if not model_1(stock, data):
        return False
    if not model_1(stock, data, 1):
        return False
    if (data[-1].turnover() + data[-2].turnover()) / 2 > 0.25 * max([_.turnover() for _ in data[-20:]]):
        return True


def rule14(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 5):
        if not t_limit(stock, data, i - 1):
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-i].date(), '10:15:00')
        if data[-i].lastLimitTime() > matchTime and data[-i].firstLimitTime() > matchTime:
            count += 1
    return count >= 3


def rule16(stock, data: List[dataModel]):
    for i in range(5):
        if t_open_pct(data, i) <= limit(stock) / 100:
            continue
        if t_low_pct(data, i) >= 0.06:
            continue
        if not t_limit(stock, data, i):
            continue
        if data[-i - 1].limitOpenTime() > 3:
            return True


def rule17(stock, data: List[dataModel]):
    for i in range(1, 4):
        if not t_limit(stock, data, i - 1):
            return False
    if t_open_pct(data, 1) >= 0.03:
        return False
    if t_open_pct(data) >= 0.03:
        return False
    return True


def rule18(data: List[dataModel]):
    matchTime0 = dateHandler.joinTimeToStamp(data[-1].date(), '10:15:00')
    matchTime1 = dateHandler.joinTimeToStamp(data[-2].date(), '10:15:00')
    if data[-1].firstLimitTime() > matchTime0 and data[-2].firstLimitTime() > matchTime1:
        return True


def rule19(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if model_1(stock, data):
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
    if data[-1].lastLimitTime() < matchTime:
        return True


def rule20(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if data[-1].turnover() < 0.5 * data[-2].turnover():
        return True


def rule21(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if data[-1].firstLimitTime() > data[-2].firstLimitTime() + dateHandler.timeDelta(data[-2].date(), data[-1].date()):
        return True


def rule22(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '10:30:00')
    if data[-1].firstLimitTime() > matchTime and data[-1].lastLimitTime() > matchTime:
        return True


def rule23(stock, data: List[dataModel]):
    for i in range(1, 4):
        if not t_limit(stock, data, i - 1):
            return False
    if data[-2].turnover() >= data[-3].turnover():
        return False
    if data[-1].turnover() <= data[-2].turnover():
        return False
    if t_low_pct(data) >= 0.03:
        return False
    if data[-1].limitOpenTime() <= 2:
        return False
    if t_open_pct(data, 2) < t_open_pct(data, 1) < t_open_pct(data, 0):
        return True


def rule24(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if data[-2].limitOpenTime() <= 1:
        return False
    if data[-1].lastLimitTime() > data[-2].lastLimitTime() + dateHandler.timeDelta(data[-2].date(), data[-1].date()):
        return True


def rule25(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 6):
        if not t_limit(stock, data, i - 1):
            continue
        if data[-i].limitOpenTime() > 5:
            count += 1
        if count >= 2:
            return True


class level9:
    def __init__(self, stock: str, data: List[dataModel]):
        self.level = 9
        self.data = data
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule == []}

    def filter(self):
        self.shot_rule.append(1) if rule1(self.stock, self.data) else self.fail_rule.append(1)
        self.shot_rule.append(2) if rule2(self.stock, self.data) else self.fail_rule.append(2)
        self.shot_rule.append(3) if rule3(self.data) else self.fail_rule.append(3)
        self.shot_rule.append(4) if rule4(self.stock, self.data) else self.fail_rule.append(4)
        self.shot_rule.append(5) if rule5(self.data) else self.fail_rule.append(5)
        self.shot_rule.append(6) if rule6(self.stock, self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.stock, self.data) else self.fail_rule.append(8)
        self.shot_rule.append(10) if rule10(self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.stock, self.data) else self.fail_rule.append(11)
        self.shot_rule.append(14) if rule14(self.stock, self.data) else self.fail_rule.append(14)
        self.shot_rule.append(16) if rule16(self.stock, self.data) else self.fail_rule.append(16)
        self.shot_rule.append(17) if rule17(self.stock, self.data) else self.fail_rule.append(17)
        self.shot_rule.append(18) if rule18(self.data) else self.fail_rule.append(18)
        self.shot_rule.append(19) if rule19(self.stock, self.data) else self.fail_rule.append(19)
        self.shot_rule.append(20) if rule20(self.stock, self.data) else self.fail_rule.append(20)
        self.shot_rule.append(21) if rule21(self.stock, self.data) else self.fail_rule.append(21)
        self.shot_rule.append(22) if rule22(self.stock, self.data) else self.fail_rule.append(22)
        self.shot_rule.append(23) if rule23(self.stock, self.data) else self.fail_rule.append(23)
        self.shot_rule.append(24) if rule24(self.stock, self.data) else self.fail_rule.append(24)
        self.shot_rule.append(25) if rule25(self.stock, self.data) else self.fail_rule.append(25)
        return self.result()
