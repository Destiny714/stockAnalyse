# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:25
# @Author  : Destiny_
# @File    : levelF1.py
# @Software: PyCharm
from common import dateHandler
from typing import List
from common.collect_data import t_low_pct, t_close_pct, t_open_pct, t_high_pct, dataModel, model_1, t_limit, limit, \
    collectData


def rule1(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if t_low_pct(data) < -0.005 and t_low_pct(data, 1) < -0.005:
        return True


def rule2(stock, data: List[dataModel]):
    if not model_1(stock, data):
        return False
    if not model_1(stock, data, 1):
        return False
    if data[-1].turnover() > 2.5 * data[-2].turnover():
        return True


def rule3(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 4):
        if t_open_pct(data, i - 1) >= -0.01:
            continue
        if t_close_pct(data, i - 1) > limit(stock) / 100:
            count += 1
            if count >= 2:
                return True
    return count >= 2


def rule4(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data, 2):
        return False
    if model_1(stock, data, 2):
        return False
    if t_low_pct(data, 1) > 0.07:
        if data[-2].turnover() > data[-3].turnover():
            if data[-2].firstLimitTime() > data[-3].firstLimitTime() + dateHandler.timeDelta(data[-3].date(),
                                                                                             data[-2].date()):
                return True


def rule5(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if model_1(stock, data, 1):
        return False
    if not model_1(stock, data):
        return False
    if data[-1].turnover() > data[-2].turnover() * 2:
        return True


def rule6(data: List[dataModel]):
    range91 = data[-121:-30]
    if range91[-1].close() / range91[0].close() > 2.2:
        return True


def rule7(stock, data: List[dataModel]):
    range50 = data[-52:-2]
    for d in range50:
        if d.pctChange() >= limit(stock):
            return False
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if model_1(stock, data):
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
    if data[-1].lastLimitTime() < matchTime:
        return True


def rule8(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data, 2):
        return False
    if data[-2].turnover() > 2 * data[-3].turnover():
        if data[-1].turnover() > 2 * data[-2].turnover():
            if not model_1(stock, data, 1):
                return True


def rule9(stock, data: List[dataModel], virtual=None):
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data, 2):
        return False
    for i in range(2, 4):
        if t_open_pct(data, i - 1) < -0.04:
            gemData = collectData('399006', dateRange=5, aimDate=data[-i if virtual is None else -i - 1].date())
            if t_low_pct(gemData) > -0.005:
                return True


def rule10(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 6):
        if t_low_pct(data, i - 1) < -0.055 and t_high_pct(data, i - 1) > limit(stock) / 100:
            count += 1
            if count >= 2:
                return True
    return count >= 2


def rule11(stock, data: List[dataModel]):
    for i in range(1, 4):
        if not t_limit(stock, data, i - 1):
            return False
        if t_open_pct(data, i - 1) >= 0.035:
            return False
    return True


def rule12(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if t_limit(stock, data, 3):
        return False
    if not t_limit(stock, data, 1):
        return False
    if model_1(stock, data, 1):
        return False
    if not model_1(stock, data):
        return False
    if data[-1].turnover() > 0.5 * data[-2].turnover():
        if data[-1].buy_elg_vol() < data[-1].sell_elg_vol():
            return True


def rule13(data: List[dataModel]):
    flag = True
    for i in range(1, 61):
        t1 = data[-i]
        t2 = data[-i - 1]
        t3 = data[-i - 2]
        if t3.turnover() < t2.turnover() < t1.turnover():
            if t3.close() < t2.close() < t1.close():
                flag = False
                break
    return flag


def rule14(data: List[dataModel]):
    try:
        for i in range(1, 31):
            if t_high_pct(data, i - 1) > 0.06:
                return False
        return True
    except:
        return False


def rule15(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if t_limit(stock, data, 1):
        return False
    if model_1(stock, data):
        return True


def rule16(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '10:00:00')
    if data[-1].firstLimitTime() > matchTime:
        d = data[-1]
        if (d.buy_elg_vol() + d.buy_lg_vol()) < (d.sell_elg_vol() + d.sell_lg_vol()):
            return True


def rule17(stock, data: List[dataModel]):
    changeRate = -1
    for i in range(4):
        if not t_limit(stock, data, i):
            return False
        if changeRate < data[-i - 1].turnover():
            changeRate = data[-i - 1].turnover()
        else:
            return False
    return True


def rule18(stock, data: List[dataModel]):
    if model_1(stock, data, 3):
        return False
    if model_1(stock, data, 2):
        return False
    if not t_limit(stock, data, 3):
        return False
    if not t_limit(stock, data, 2):
        return False
    if not model_1(stock, data, 1):
        return False
    if not model_1(stock, data):
        return False
    if data[-2].turnover() > (1 / 3) * data[-3].turnover():
        return True


def rule19(stock, data: List[dataModel]):
    if not t_limit(stock, data, 3):
        return False
    if not t_limit(stock, data, 2):
        return False
    if model_1(stock, data, 1):
        return False
    if not model_1(stock, data):
        return False
    if data[-1].turnover() > (1 / 3) * data[-2].turnover():
        return True


def rule20(stock, data: List[dataModel], virtual=None):
    if data[-1].turnover() <= data[-2].turnover() * 0.8:
        return False
    if not (t_open_pct(data) > t_open_pct(data, 1) > 0.05):
        return False
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if data[-1].lastLimitTime() > data[-2].lastLimitTime() + dateHandler.timeDelta(data[-2].date(), data[-1].date()):
        gemData = collectData('399006', dateRange=5, aimDate=data[-1 if virtual is None else -2].date())
        if t_low_pct(gemData) > -0.005:
            return True


def rule21(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-2].date(), '09:45:00')
    if data[-2].lastLimitTime() < matchTime:
        range2_20 = data[-21:-2]
        if data[-2].close() < max([_.close() for _ in range2_20]):
            return True


def rule22(stock, data: List[dataModel]):
    for i in range(1, 3):
        if t_open_pct(data, i) <= limit(stock) / 100:
            continue
        if t_low_pct(data, i) >= 0.05:
            continue
        if t_close_pct(data, i) <= limit(stock) / 100:
            continue
        matchTime = dateHandler.joinTimeToStamp(data[-i - 1].date(), '10:30:00')
        if data[-i - 1].lastLimitTime() > matchTime:
            return True


def rule23(data: List[dataModel]):
    try:
        range10 = data[-11:-1]
        range30 = data[-30:-1]
        if sum([_.close() for _ in range10]) / 10 < sum([_.close() for _ in range30]) / 30:
            return True
    except:
        return False


def rule24(data: List[dataModel]):
    try:
        range55 = data[-56:-1]
        avg55 = sum([_.close() for _ in range55]) / 55
        count = 0
        for i in range(1, 6):
            if data[-i - 1].close() < avg55:
                count += 1
            if count >= 2:
                return True
    except:
        return False


def rule25(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if data[-1].turnover() > 2 * data[-2].turnover():
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:37:00')
        if data[-1].lastLimitTime() < matchTime:
            return True


def rule26(data: List[dataModel]):
    range120 = data[-121:-1]
    count = 0
    for i in range120:
        if i.close() > data[-1].close():
            count += 1
        if count >= 20:
            return True


def rule27(data: List[dataModel]):
    range30 = data[-33:-3]
    count = 0
    for i in range30:
        if i.close() > data[-1].close() * 1.1:
            count += 1
        if count >= 3:
            return True


def rule28(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    range20 = data[-23:-3]
    count = 0
    for i in range20:
        if i.close() > data[-1].close():
            count += 1
        if count >= 3:
            return True


def rule29(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    range30 = data[-37:-7]
    count = 0
    for i in range30:
        if i.close() > data[-1].close():
            count += 1
        if count >= 3:
            return True


class levelF1:
    def __init__(self, stock: str, data: List[dataModel], virtual=None):
        self.level = 'F1'
        self.data = data
        self.stock = stock
        self.virtual = virtual
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule == []}

    def filter(self):
        self.shot_rule.append(1) if rule1(self.stock, self.data) else self.fail_rule.append(1)
        self.shot_rule.append(2) if rule2(self.stock, self.data) else self.fail_rule.append(2)
        self.shot_rule.append(3) if rule3(self.stock, self.data) else self.fail_rule.append(3)
        self.shot_rule.append(4) if rule4(self.stock, self.data) else self.fail_rule.append(4)
        self.shot_rule.append(5) if rule5(self.stock, self.data) else self.fail_rule.append(5)
        self.shot_rule.append(6) if rule6(self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.stock, self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.stock, self.data) else self.fail_rule.append(8)
        self.shot_rule.append(9) if rule9(self.stock, self.data, virtual=self.virtual) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.stock, self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.stock, self.data) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.stock, self.data) else self.fail_rule.append(12)
        self.shot_rule.append(13) if rule13(self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.data) else self.fail_rule.append(14)
        self.shot_rule.append(15) if rule15(self.stock, self.data) else self.fail_rule.append(15)
        self.shot_rule.append(16) if rule16(self.stock, self.data) else self.fail_rule.append(16)
        self.shot_rule.append(17) if rule17(self.stock, self.data) else self.fail_rule.append(17)
        self.shot_rule.append(18) if rule18(self.stock, self.data) else self.fail_rule.append(18)
        self.shot_rule.append(19) if rule19(self.stock, self.data) else self.fail_rule.append(19)
        self.shot_rule.append(20) if rule20(self.stock, self.data, virtual=self.virtual) else self.fail_rule.append(20)
        self.shot_rule.append(21) if rule21(self.stock, self.data) else self.fail_rule.append(21)
        self.shot_rule.append(22) if rule22(self.stock, self.data) else self.fail_rule.append(22)
        self.shot_rule.append(23) if rule23(self.data) else self.fail_rule.append(23)
        self.shot_rule.append(24) if rule24(self.data) else self.fail_rule.append(24)
        self.shot_rule.append(25) if rule25(self.stock, self.data) else self.fail_rule.append(25)
        self.shot_rule.append(26) if rule26(self.data) else self.fail_rule.append(26)
        self.shot_rule.append(27) if rule27(self.data) else self.fail_rule.append(27)
        self.shot_rule.append(28) if rule28(self.stock, self.data) else self.fail_rule.append(28)
        self.shot_rule.append(29) if rule29(self.stock, self.data) else self.fail_rule.append(29)
        return self.result()
