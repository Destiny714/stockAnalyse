# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 09:18
# @Author  : Destiny_
# @File    : level5.py
# @Software: PyCharm

from typing import List

from common import dateHandler
from common.collect_data import t_low_pct, t_close_pct, t_open_pct, limit, dataModel, model_1, model_t, t_limit, \
    collectData


def rule1(stock, data: List[dataModel]):
    if data[-1].limitOpenTime() >= 1:
        return False
    count1 = 0
    count2 = 0
    count3 = 0
    for i in range(1, 5):
        if data[-i].pctChange() > limit(stock):
            count1 += 1
        if t_open_pct(data, i - 1) > 0.065:
            if t_low_pct(data, i - 1) > 0.035:
                if t_close_pct(data, i - 1) > limit(stock) / 100:
                    count2 += 1
        if t_low_pct(data, i - 1) > 0.025:
            count3 += 1
    if count1 >= 3 and count2 >= 2 and count3 >= 3:
        return True


def rule2(stock, data: List[dataModel]):
    if data[-1].limitOpenTime() >= 1:
        return False
    count1 = 0
    count2 = 0
    count3 = 0
    for i in range(1, 6):
        if data[-i].pctChange() > limit(stock):
            if t_close_pct(data, i - 1) > limit(stock) / 100:
                if t_low_pct(data, i - 1) > -0.01:
                    count1 += 1
        if t_low_pct(data, i - 1) > 0.035:
            count2 += 1
        if t_open_pct(data, i - 1) > 0.06:
            count3 += 1
    if count1 >= 4 and count2 >= 3 and count3 >= 2:
        return True


def rule3(data: List[dataModel], virtual=None):
    for i in range(1, 3):
        if t_low_pct(data, i - 1) <= -0.02:
            continue
        if t_open_pct(data, i - 1) > 0:
            gemData = collectData('399006', dateRange=5, aimDate=data[-i if virtual is None else -i - 1].date())
            if t_open_pct(gemData, i - 1) < -0.02:
                return True


def rule4(stock, data: List[dataModel]):
    if data[-1].limitOpenTime() >= 1:
        return False
    count = 0
    for i in range(1, 4):
        if 0.035 < t_open_pct(data, i - 1) < limit(stock) / 100:
            count += 1
        if count >= 2:
            break
    if count < 2:
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:50:00')
    if data[-1].firstLimitTime() < matchTime:
        return True


def rule6(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if data[-1].turnover() > data[-2].turnover():
        if t_open_pct(data) > 0.07:
            if t_low_pct(data) > 0.05:
                if data[-2].turnover() < 0.7 * data[-3].turnover():
                    return True


def rule7(stock, data: List[dataModel]):
    if not model_1(stock, data, 1):
        return False
    if not model_1(stock, data, 2):
        return False
    if data[-2].turnover() < 1.5 * data[-3].turnover():
        if model_t(stock, data) and t_low_pct(data) > 0.07:
            return True


def rule10(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not (t_open_pct(data, 1) > 0.05 and t_low_pct(data, 1) > 0.03):
        return False
    if data[-1].turnover() >= data[-2].turnover():
        return False
    range7 = data[-9:-2]
    if data[-2].turnover() > max([_.turnover() for _ in range7]):
        return True


def rule11(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if data[-1].turnover() <= data[-2].turnover():
        return False
    matchTime0 = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
    matchTime1 = dateHandler.joinTimeToStamp(data[-2].date(), '09:45:00')
    if data[-1].firstLimitTime() < matchTime0 and data[-2].firstLimitTime() > matchTime1:
        return True


def rule12(stock, data: List[dataModel]):
    if data[-1].limitOpenTime() >= 1:
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if data[-2].turnover() <= data[-3].turnover():
        return False
    if data[-2].turnover() <= data[-1].turnover():
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:55:00')
    if data[-1].lastLimitTime() >= data[-2].lastLimitTime() + dateHandler.timeDelta(data[-2].date(), data[-1].date()):
        return False
    if data[-1].lastLimitTime() < matchTime:
        return True


def rule13(stock, data: List[dataModel]):
    for i in range(4):
        if not t_limit(stock, data, i):
            return False
    if not model_t(stock, data, 1):
        return False
    if data[-1].turnover() >= data[-2].turnover():
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:50:00')
    if data[-1].lastLimitTime() < matchTime:
        return True


def rule14(stock, data: List[dataModel]):
    for i in range(1, 4):
        if not t_limit(stock, data, i - 1):
            return False
    if t_open_pct(data, 1) <= 0.05:
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-2].date(), '09:45:00')
    if data[-2].lastLimitTime() >= matchTime:
        return False
    if data[-2].turnover() >= data[-3].turnover():
        return False
    if data[-2].turnover() >= data[-1].turnover():
        return False
    if t_open_pct(data) <= 0.07:
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:40:00')
    if data[-1].firstLimitTime() < matchTime:
        return True


def rule15(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 5):
        if not t_limit(stock, data, i - 1):
            return False
        if data[-i].limitOpenTime() < 2:
            count += 1
    return count >= 3


class level5:
    def __init__(self, stock: str, data: List[dataModel], virtual=None):
        self.level = 5
        self.data = data
        self.stock = stock
        self.virtual = virtual
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def filter(self):
        self.shot_rule.append(1) if rule1(self.stock, self.data) else self.fail_rule.append(1)
        self.shot_rule.append(2) if rule2(self.stock, self.data) else self.fail_rule.append(2)
        self.shot_rule.append(3) if rule3(self.data, self.virtual) else self.fail_rule.append(3)
        self.shot_rule.append(4) if rule4(self.stock, self.data) else self.fail_rule.append(4)
        self.shot_rule.append(6) if rule6(self.stock, self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.stock, self.data) else self.fail_rule.append(7)
        self.shot_rule.append(10) if rule10(self.stock, self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.stock, self.data) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.stock, self.data) else self.fail_rule.append(12)
        self.shot_rule.append(13) if rule13(self.stock, self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.stock, self.data) else self.fail_rule.append(14)
        self.shot_rule.append(15) if rule15(self.stock, self.data) else self.fail_rule.append(15)
        return self.result()
