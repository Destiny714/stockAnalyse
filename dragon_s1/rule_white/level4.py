# -*- coding: utf-8 -*-
# @Time    : 2022/6/21 16:26
# @Author  : Destiny_
# @File    : level4.py
# @Software: PyCharm

from typing import List
from common.dateHandler import timeDelta, getMinute, lastMinute
from common.collect_data import t_low_pct, t_close_pct, t_open_pct, limit, dataModel, model_t, t_limit, model_1


def rule1(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    try:
        range1to5 = data[-6:-1]
        range1to10 = data[-10:-1]
        range1to20 = data[-21:-1]
        range1to30 = data[-31:-1]
        range1to60 = data[-61:-1]
        if sum([_.close() for _ in range1to5]) / 5 > sum([_.close() for _ in range1to20]) / 20:
            if sum([_.close() for _ in range1to20]) / 20 > sum([_.close() for _ in range1to60]) / 60:
                if sum([_.close() for _ in range1to30]) / 30 > sum([_.close() for _ in range1to60]) / 60:
                    if data[-1].close() > sum([_.close() for _ in range1to10]) / 10:
                        return True
    except:
        return False


def rule2(stock, data: List[dataModel]):
    err = None
    try:
        if not t_limit(stock, data):
            return False
        if t_low_pct(data) <= 0.06:
            return False
        if t_close_pct(data) <= limit(stock) / 100:
            return False
        if not (0.08 < t_open_pct(data) < limit(stock) / 100):
            return False
        range220 = data[-221:-1]
        if data[-1].close() > max([_.high() for _ in range220]):
            return True
    except Exception as e:
        err = e
        return False


def rule3(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if data[-1].turnover() <= data[-2].turnover():
        return False
    if data[-1].turnover() < 1.5 * data[-2].turnover():
        if data[-2].turnover() < 0.7 * data[-3].turnover():
            return True


def rule4(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if model_1(stock, data):
        return False
    if model_1(stock, data, 1):
        return False
    if t_low_pct(data, 1) < -0.02:
        return False
    if t_open_pct(data) <= 0.05:
        return False
    if t_low_pct(data) < 0.035:
        return False
    if data[-1].turnover() < 0.8 * data[-2].turnover():
        return True


def rule5(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if t_open_pct(data, 1) <= 0.05:
        return False
    if t_low_pct(data, 1) <= 0.02:
        return False
    tLowPct = t_low_pct(data)
    if 0.07 < tLowPct < limit(stock) / 100:
        return True
    if t_open_pct(data) <= 0.07:
        return False
    if tLowPct <= 0.04:
        return False
    if data[-1].turnover() < 20:
        return True


def rule6(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if t_limit(stock, data, 2):
        return False
    if not (0.06 < t_open_pct(data) < 0.09):
        return False
    if not (data[-1].turnover() < 0.7 * data[-2].turnover()):
        return False
    if t_low_pct(data) <= 0.005:
        return False
    range120 = data[-121:-1]
    if data[-1].close() > max([_.high() for _ in range120]):
        return True


def rule7(stock, data: List[dataModel]):
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if model_1(stock, data):
        return False
    if 4 < data[-1].close() < 12:
        if 3 < data[-1].turnover() < 9:
            return True


def rule8(data: List[dataModel]):
    if data[-1].concentration() < 0.115:
        if data[-1].concentration() < data[-2].concentration():
            return True


def rule9(stock, data: List[dataModel]):
    if model_1(stock, data):
        return False
    if data[-1].turnover() <= 1.5 * data[-2].turnover():
        range10 = data[-11:-1]
        if data[-1].turnover() < 0.25 * max([_.turnover() for _ in range10]):
            return True


def rule10(stock, data: List[dataModel]):
    try:
        for i in range(1, 11):
            if not t_limit(stock, data, i):
                continue
            if t_limit(stock, data, i + 1):
                continue
            if t_open_pct(data, i - 1) <= 0.045:
                continue
            time = data[-i].time()
            if time['0930'] > data[-i - 1].volume() / 12:
                return True
    except:
        return False


def rule11(stock, data: List[dataModel]):
    for i in range(1, 4):
        if not t_limit(stock, data, i - 1):
            return False
        if model_1(stock, data, i - 1):
            return False
        if data[-i].open() == data[-i].close():
            if t_close_pct(data, i - 1) <= limit(stock) / 100:
                continue
            if t_low_pct(data, i - 1) > 0.075:
                return True


def rule12(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data, 2):
        return False
    if data[-2].turnover() > 4 * data[-3].turnover():
        if t_open_pct(data, 0) > 1.04:
            return True


def rule13(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data, 2):
        return False
    if not (data[-3].turnover() < data[-2].turnover()):
        return False
    if not (data[-1].turnover() < data[-2].turnover()):
        return False
    if t_open_pct(data, 2) > 0.035:
        if t_open_pct(data) > 0.01:
            if data[-3].turnover() < data[-4].turnover() < data[-2].turnover():
                return True


def rule14(stock, data: List[dataModel]):
    try:
        if model_1(stock, data, 1):
            return False
        if not t_limit(stock, data, 1):
            return False
        limitTime = data[-2].firstLimitTime()
        limitMinute = getMinute(limitTime)
        limitMinuteLast = lastMinute(limitMinute)
        time = data[-2].time()
        if time[limitMinute] > time[limitMinuteLast] * 3:
            if data[-2].limitOpenTime() == 0:
                return True
    except:
        return False


def rule15(stock, data: List[dataModel]):
    try:
        if model_1(stock, data):
            return False
        if not t_limit(stock, data):
            return False
        limitTime = data[-1].firstLimitTime()
        limitMinute = getMinute(limitTime)
        limitMinuteLast = lastMinute(limitMinute)
        time = data[-1].time()
        if time[limitMinute] > time[limitMinuteLast] * 10:
            return True
    except:
        return False


def rule16(stock, data: List[dataModel]):
    err = None
    try:
        for i in range(1, 3):
            if not t_limit(stock, data, i - 1):
                continue
            if t_low_pct(data, i - 1) <= 0.055:
                continue
            if t_close_pct(data, i - 1) <= limit(stock) / 100:
                continue
            if 0.07 < t_open_pct(data, i - 1) < limit(stock) / 100:
                range120 = data[-i - 120:-i]
                if data[-i].close() > max([_.high() for _ in range120]):
                    return True
    except Exception as e:
        err = e
        return False


def rule17(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 4):
        if t_open_pct(data, i - 1) <= 0.035:
            continue
        if t_low_pct(data, i - 1) <= 0.01:
            continue
        if t_close_pct(data, i - 1) > limit(stock) / 100:
            count += 1
            if count >= 2:
                return True
    return count >= 2


def rule18(stock, data: List[dataModel]):
    for i in range(1, 4):
        if not model_t(stock, data, i - 1):
            continue
        if 0.08 < t_low_pct(data, i - 1) < limit(stock) / 100:
            return True


def rule19(stock, data: List[dataModel]):
    count1 = 0
    count2 = 0
    for i in range(1, 5):
        if t_open_pct(data, i - 1) > 0.035:
            count2 += 1
        if t_limit(stock, data, i - 1):
            if t_close_pct(data, i - 1) > limit(stock) / 100:
                if t_low_pct(data, i - 1) > -0.01:
                    count1 += 1
    return count1 >= 3 and count2 >= 2


def rule20(stock, data: List[dataModel]):
    err = None
    try:
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if model_1(stock, data):
            return False
        if data[-1].turnover() >= 0.7 * data[-2].turnover():
            return False
        if t_open_pct(data) <= 0.065:
            return False
        if t_low_pct(data) <= 0.05:
            return False
        range90 = data[-91:-1]
        if data[-1].close() > max([_.high() for _ in range90]):
            return True
    except Exception as e:
        err = e
        return False


def rule21(data: List[dataModel]):
    if t_close_pct(data) > 0.06:
        if data[-1].concentration() < 0.11:
            if data[-1].concentration() - data[-2].concentration() < 0.015:
                return True


def rule22(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if data[-3].turnover() > data[-2].turnover() > data[-1].turnover():
        if data[-1].lastLimitTime() < data[-2].lastLimitTime() + timeDelta(data[-2].date(), data[-1].date()):
            if data[-2].lastLimitTime() < data[-3].lastLimitTime() + timeDelta(data[-3].date(), data[-2].date()):
                return True


def rule23(stock, data: List[dataModel]):
    if not model_t(stock, data):
        return False
    if data[-1].concentration() - data[-2].concentration() < 0:
        return True


def rule24(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 5):
        if data[-i].pctChange() <= limit(stock):
            return False
        if t_low_pct(data, i - 1) <= -0.01:
            return False
        if t_open_pct(data, i - 1) > 0.035:
            count += 1
    if count >= 2:
        return True


def rule25(stock, data: List[dataModel]):
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
        if data[-i - 1].limitOpenTime() >= 2:
            return False
    if data[-1].concentration() - data[-2].concentration() < 0.02:
        return True


def rule26(data: List[dataModel]):
    if data[-1].close() < data[-1].his_high() / 3:
        return True


def rule29(data: List[dataModel]):
    for i in range(3):
        d = data[-i - 1]
        if not ((d.buy_elg_vol() + d.buy_lg_vol()) > (d.sell_elg_vol() + d.sell_lg_vol())):
            return False
    return True


def rule30(data: List[dataModel]):
    try:
        for i in range(30):
            j = i + 1
            ma20 = [data[-_] for _ in range(j, j + 20)]
            ma30 = [data[-_] for _ in range(j, j + 30)]
            ma60 = [data[-_] for _ in range(j, j + 60)]
            avg20 = sum(_.close() for _ in ma20) / len(ma20)
            avg30 = sum(_.close() for _ in ma30) / len(ma30)
            avg60 = sum(_.close() for _ in ma60) / len(ma60)
            if not (avg30 > avg60):
                return False
            if not (avg20 > avg30):
                return False
        return True
    except:
        return False


class level4:
    def __init__(self, stock: str, data: List[dataModel]):
        self.level = 4
        self.data = data
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def filter(self):
        self.shot_rule.append(2) if rule2(self.stock, self.data) else self.fail_rule.append(2)
        self.shot_rule.append(3) if rule3(self.stock, self.data) else self.fail_rule.append(3)
        self.shot_rule.append(4) if rule4(self.stock, self.data) else self.fail_rule.append(4)
        self.shot_rule.append(5) if rule5(self.stock, self.data) else self.fail_rule.append(5)
        self.shot_rule.append(6) if rule6(self.stock, self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.stock, self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.data) else self.fail_rule.append(8)
        self.shot_rule.append(9) if rule9(self.stock, self.data) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.stock, self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.stock, self.data) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.stock, self.data) else self.fail_rule.append(12)
        self.shot_rule.append(13) if rule13(self.stock, self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.stock, self.data) else self.fail_rule.append(14)
        self.shot_rule.append(15) if rule15(self.stock, self.data) else self.fail_rule.append(15)
        self.shot_rule.append(16) if rule16(self.stock, self.data) else self.fail_rule.append(16)
        self.shot_rule.append(17) if rule17(self.stock, self.data) else self.fail_rule.append(17)
        self.shot_rule.append(18) if rule18(self.stock, self.data) else self.fail_rule.append(18)
        self.shot_rule.append(19) if rule19(self.stock, self.data) else self.fail_rule.append(19)
        self.shot_rule.append(20) if rule20(self.stock, self.data) else self.fail_rule.append(20)
        self.shot_rule.append(21) if rule21(self.data) else self.fail_rule.append(21)
        self.shot_rule.append(22) if rule22(self.stock, self.data) else self.fail_rule.append(22)
        self.shot_rule.append(23) if rule23(self.stock, self.data) else self.fail_rule.append(23)
        self.shot_rule.append(24) if rule24(self.stock, self.data) else self.fail_rule.append(24)
        self.shot_rule.append(25) if rule25(self.stock, self.data) else self.fail_rule.append(25)
        self.shot_rule.append(26) if rule26(self.data) else self.fail_rule.append(26)
        self.shot_rule.append(29) if rule29(self.data) else self.fail_rule.append(29)
        self.shot_rule.append(30) if rule30(self.data) else self.fail_rule.append(30)
        return self.result()
