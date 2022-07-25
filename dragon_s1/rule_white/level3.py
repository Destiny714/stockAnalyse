# -*- coding: utf-8 -*-
# @Time    : 2022/6/21 15:16
# @Author  : Destiny_
# @File    : level3.py
# @Software: PyCharm
from common import dateHandler
from typing import List
from common.collect_data import limit, dataModel, t_open_pct, t_close_pct, t_low_pct, t_limit, collectData


def rule1(stock, data: List[dataModel]):
    if data[-1].pctChange() <= limit(stock):
        return False
    if data[-2].pctChange() <= limit(stock):
        return False
    if data[-1].turnover() <= data[-2].turnover():
        return False
    range10 = data[-11:-1]
    if data[-1].turnover() < 1.8 * max([_.turnover() for _ in range10]):
        return True


def rule2(stock, data: List[dataModel]):
    if data[-1].pctChange() <= limit(stock):
        return False
    if data[-2].pctChange() <= limit(stock):
        return False
    if data[-1].turnover() >= data[-2].turnover():
        return False
    if t_open_pct(data, 0) <= t_open_pct(data, 1):
        return False
    if data[-2].turnover() > data[-3].turnover():
        return True


def rule3(stock, data: List[dataModel]):
    if data[-1].pctChange() <= limit(stock):
        return False
    if data[-2].pctChange() <= limit(stock):
        return False
    if data[-1].turnover() >= data[-2].turnover():
        return False
    if t_open_pct(data) > 0.035:
        return True


def rule4(stock, data: List[dataModel]):
    if data[-1].pctChange() <= limit(stock):
        return False
    if data[-2].pctChange() <= limit(stock):
        return False
    if data[-3].pctChange() > limit(stock):
        return False
    if data[-4].pctChange() > limit(stock):
        return False
    if 0.035 < t_open_pct(data) < 0.09:
        return True


def rule5(stock, data: List[dataModel]):
    if data[-1].pctChange() <= limit(stock):
        return False
    if data[-2].pctChange() <= limit(stock):
        return False
    if data[-1].turnover() >= data[-2].turnover():
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
    if data[-1].firstLimitTime() < matchTime:
        return True


def rule6(data: List[dataModel]):
    range5 = data[-5:]
    range20 = data[-20:]
    range60 = data[-60:]
    if sum(_.close() for _ in range5) / 5 > sum(_.close() for _ in range20) / 20:
        if sum(_.close() for _ in range20) / 20 > sum(_.close() for _ in range60) / 60:
            return True


def rule7(stock, data: List[dataModel]):
    limit1 = 0.11 if stock[0:3] == '300' else 0.055
    if data[-1].pctChange() <= limit(stock):
        return False
    if data[-2].pctChange() <= limit(stock):
        return False
    if data[-3].pctChange() > limit(stock):
        return False
    if t_open_pct(data) > limit1:
        return True


def rule8(stock, data: List[dataModel]):
    err = None
    try:
        if not t_limit(stock, data):
            return False
        range5to25 = data[-26:-5]
        if data[-1].close() <= 1.2 * max(_.close() for _ in range5to25):
            range10 = data[-11:-1]
            if data[-1].turnover() < 1.5 * max([_.turnover() for _ in range10]):
                range440 = data[-441:-1]
                if data[-1].close() > max([_.high() for _ in range440]):
                    return True
    except Exception as e:
        err = e
        return False


def rule9(stock, data: List[dataModel]):
    if data[-2].turnover() <= data[-1].turnover():
        return False
    if not (t_open_pct(data) > -0.01 and t_close_pct(data) > limit(stock) / 100):
        return False
    range10 = data[-12:-2]
    if data[-2].turnover() > max([_.turnover() for _ in range10]):
        return True


def rule10(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if t_open_pct(data, 0) >= 0.05 and t_open_pct(data, 1) >= 0.05:
        if t_low_pct(data, 0) > 0.01 and t_low_pct(data, 1) > 0.01:
            return True


def rule11(stock, data: List[dataModel]):
    err = None
    try:
        range10 = data[-10:]
        range60 = data[-60:]
        range220 = data[-220:]
        if sum([_.close() for _ in range10]) / 10 > sum([_.close() for _ in range220]) / 220:
            if sum([_.close() for _ in range60]) / 60 > sum([_.close() for _ in range220]) / 220:
                if max([_.turnover() for _ in range60]) > 5 * sum([_.turnover() for _ in range220]) / 220:
                    for i in range(1, 61):
                        if data[-i].pctChange() > limit(stock):
                            return True
    except Exception as e:
        err = e
        return False


def rule13(data: List[dataModel]):
    for i in range(1, 3):
        if data[-i].close() > max([_.close() for _ in data[-i - 440:-i]]):
            return True


def rule14(data: List[dataModel]):
    err = None
    try:
        flag = False
        for i in range(1, 3):
            if t_close_pct(data, i - 1) > 0.06:
                flag = True
                break
        if flag:
            range220 = data[-221:-1]
            if data[-1].close() > 0.95 * max([_.high() for _ in range220]):
                return True
    except Exception as e:
        err = e
        return False


def rule15(data: List[dataModel]):
    avg4 = sum([data[-5].close(), data[-4].close(), data[-3].close(), data[-2].close()]) / 4
    if not (data[-1].close() > avg4 and data[-2].close() > avg4):
        return False
    for i in range(1, 3):
        range220 = data[-i - 220:-i]
        if data[-i].close() > max([_.high() for _ in range220]):
            return True


def rule21(data: List[dataModel]):
    range5 = data[-5:]
    range10 = data[-10:]
    range20 = data[-20:]
    range30 = data[-30:]
    range60 = data[-60:]
    if max([_.close() for _ in range10]) > sum([_.close() for _ in range30]) / 30:
        if sum([_.close() for _ in range5]) / 5 > sum([_.close() for _ in range20]) / 20:
            if sum([_.close() for _ in range20]) / 20 > sum([_.close() for _ in range60]) / 60:
                return True


def rule22(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if t_low_pct(data) <= -0.05:
        return False
    if t_open_pct(data) > 0.01:
        gemData = collectData('399006', dateRange=5, aimDate=data[-1].date())
        if t_close_pct(gemData) < -0.02:
            return True


def rule23(stock, data: List[dataModel]):
    err = None
    try:
        for i in range(1, 3):
            d = data[-i]
            if not t_limit(stock, data, i - 1):
                continue
            if t_low_pct(data, i - 1) <= -0.01:
                continue
            if d.turnover() > 1.8 * max([_.turnover() for _ in data[-10 - i:-i]]):
                continue
            if d.close() > max([_.close() for _ in data[-440 - i:-i]]):
                return True
    except Exception as e:
        err = e
        return False


def rule24(stock, data: List[dataModel]):
    if (data[-3].high() - data[-4].close()) / data[-4].close() <= 0.07:
        return False
    for i in range(1, 3):
        if not t_limit(stock, data, i - 1):
            continue
        if t_open_pct(data, i - 1) > 0.06 and t_low_pct(data, i - 1) > 0.035:
            return True


class level3:
    def __init__(self, stock: str, data: List[dataModel]):
        self.level = 3
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
        self.shot_rule.append(6) if rule6(self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.stock, self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.stock, self.data) else self.fail_rule.append(8)
        self.shot_rule.append(9) if rule9(self.stock, self.data) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.stock, self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.stock, self.data) else self.fail_rule.append(11)
        self.shot_rule.append(13) if rule13(self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.data) else self.fail_rule.append(14)
        self.shot_rule.append(15) if rule15(self.data) else self.fail_rule.append(15)
        self.shot_rule.append(21) if rule21(self.data) else self.fail_rule.append(21)
        self.shot_rule.append(22) if rule22(self.stock, self.data) else self.fail_rule.append(22)
        self.shot_rule.append(23) if rule23(self.stock, self.data) else self.fail_rule.append(23)
        self.shot_rule.append(24) if rule24(self.stock, self.data) else self.fail_rule.append(24)
        return self.result()
