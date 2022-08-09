# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:25
# @Author  : Destiny_
# @File    : levelF3.py
# @Software: PyCharm

from typing import List

from common import dateHandler
from common.collect_data import t_low_pct, t_close_pct, t_open_pct, t_high_pct, limit, dataModel, model_1, model_t, \
    t_limit, \
    collectData


def rule1(stock, data: List[dataModel]):
    if not model_1(stock, data):
        return False
    if not model_1(stock, data, 1):
        return False
    if data[-1].turnover() > 1.5 * data[-2].turnover():
        return True


def rule2(stock, data: List[dataModel]):
    if data[-1].pctChange() <= limit(stock):
        return False
    if data[-2].pctChange() <= limit(stock):
        return False
    if model_1(stock, data, 1):
        return False
    if t_low_pct(data) <= 0.06:
        return False
    if data[-1].turnover() <= 1.5 * data[-2].turnover():
        return False
    if data[-1].firstLimitTime() > data[-2].firstLimitTime() + dateHandler.timeDelta(data[-2].date(), data[-1].date()):
        return True


def rule3(stock, data: List[dataModel]):
    for i in range(1, 6):
        if not model_t(stock, data, i - 1):
            continue
        if t_low_pct(data, i - 1) >= 0.06:
            continue
        range10 = data[-10 - i:-i]
        if data[-i].turnover() > 1.8 * max([_.turnover() for _ in range10]):
            d = data[-i]
            if (d.buy_elg_vol() + d.buy_lg_vol()) < (d.sell_elg_vol() + d.sell_lg_vol()):
                return True


def rule4(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if not model_1(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if t_open_pct(data) > limit(stock) / 100 and t_low_pct(data) < 0.05:
        return True


def rule5(stock, data: List[dataModel]):
    turnOver = data[-1].turnover() + 1
    for i in range(1, 4):
        d = data[-i]
        if d.pctChange() <= limit(stock):
            return False
        if model_1(stock, data, i - 1):
            return False
        if d.turnover() < turnOver:
            turnOver = d.turnover()
        else:
            return False
    if data[-1].firstLimitTime() <= data[-2].firstLimitTime() + dateHandler.timeDelta(data[-2].date(), data[-1].date()):
        return False
    if data[-2].firstLimitTime() <= data[-3].firstLimitTime() + dateHandler.timeDelta(data[-3].date(), data[-2].date()):
        return False
    return True


def rule6(stock, data: List[dataModel]):
    for i in range(1, 4):
        d = data[-i]
        if d.open() != d.close():
            continue
        if t_close_pct(data, i - 1) <= limit(stock) / 100:
            continue
        if t_low_pct(data, i - 1) >= 0.06:
            continue
        if data[-i].limitOpenTime() > 2:
            if (d.buy_elg_vol() + d.buy_lg_vol()) < (d.sell_elg_vol() + d.sell_lg_vol()):
                return True


def rule7(stock, data: List[dataModel]):
    if data[-4].pctChange() > limit(stock):
        return False
    if not model_1(stock, data, 2):
        return False
    if t_open_pct(data, 1) != t_close_pct(data, 1):
        return False
    if t_close_pct(data, 1) <= limit(stock) / 100:
        return False
    if t_low_pct(data, 1) < 0.07:
        return True


def rule8(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    for i in range(3):
        if t_limit(stock, data, i + 1):
            return False
    if data[-2].close() > data[-3].close() > data[-4].close():
        return True


def rule9(stock, data: List[dataModel]):
    if not model_1(stock, data, 1):
        return False
    if model_1(stock, data, 2):
        return False
    if not t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data, 3):
        return False
    if data[-2].turnover() > (1 / 3) * data[-3].turnover():
        t2Time = data[-3].lastLimitTime()
        t3Time = data[-4].lastLimitTime()
        if t2Time > t3Time + dateHandler.timeDelta(data[-4].date(), data[-3].date()):
            return True


def rule10(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 4):
        if data[-i].pctChange() <= limit(stock):
            return False
        if t_open_pct(data, i - 1) < 0.025:
            count += 1
    if count >= 2 and data[-1].turnover() > data[-2].turnover():
        if data[-1].limitOpenTime() > 0:
            return True


def rule11(stock, data: List[dataModel], virtual=None):
    if model_1(stock, data, 1):
        return False
    if not t_limit(stock, data, 1):
        return False
    if data[-1].turnover() <= 1.8 * data[-2].turnover():
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
    if data[-1].firstLimitTime() > matchTime and data[-1].lastLimitTime() > matchTime:
        gemData = collectData('399006', dateRange=5, aimDate=data[-1 if virtual is None else -2].date())
        if t_low_pct(gemData) > -0.005:
            return True


def rule12(stock, data: List[dataModel]):
    if data[-1].pctChange() <= limit(stock):
        return False
    if data[-2].pctChange() <= limit(stock):
        return False
    if t_open_pct(data, 1) >= 0.03:
        return False
    if t_open_pct(data) <= 0.05:
        return False
    if data[-1].turnover() <= 0.8 * data[-2].turnover():
        return False
    if data[-1].firstLimitTime() > data[-2].firstLimitTime() + dateHandler.timeDelta(data[-2].date(), data[-1].date()):
        return True


def rule13(stock, data: List[dataModel]):
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data, 2):
        return False
    if t_open_pct(data, 2) >= 0.03:
        return False
    if t_open_pct(data, 1) <= 0.05:
        return False
    if data[-2].turnover() <= 0.8 * data[-3].turnover():
        return False
    if data[-2].lastLimitTime() <= data[-3].lastLimitTime() + dateHandler.timeDelta(data[-3].date(), data[-2].date()):
        return False
    if data[-2].firstLimitTime() > data[-3].firstLimitTime() + dateHandler.timeDelta(data[-3].date(), data[-2].date()):
        return True


def rule14(data: List[dataModel]):
    range20 = data[-20:]
    range30 = data[-30:]
    if max([_.close() for _ in range20]) < sum([_.close() for _ in range30]) / 30:
        return True


def rule15(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    range20 = data[-21:-1]
    if data[-1].turnover() > max([_.turnover() for _ in range20]) * 4:
        return True


def rule16(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    range20 = data[-22:-2]
    avgRate = (sum([_.turnover() for _ in range20]) / 20) * 5
    if data[-1].turnover() > avgRate and data[-2].turnover() > avgRate:
        if data[-1].turnover() > 1.8 * data[-2].turnover():
            return True


def rule17(data: List[dataModel], virtual=None):
    for i in range(1, 5):
        if t_open_pct(data, i - 1) > 0.09 and t_low_pct(data, i - 1) < 0.03:
            gemData = collectData('399006', dateRange=5, aimDate=data[-i if virtual is None else -i - 1].date())
            if t_open_pct(gemData) > -0.005:
                return True


def rule18(stock, data: List[dataModel], virtual=None):
    if not t_limit(stock, data, 1):
        return False
    if model_1(stock, data, 1):
        return False
    if data[-1].limitOpenTime() <= 3:
        return False
    if data[-1].turnover() > 3 * data[-2].turnover():
        gemData = collectData('399006', dateRange=5, aimDate=data[-1 if virtual is None else -2].date())
        if t_low_pct(gemData) > -0.005:
            return True


def rule19(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 4):
        if data[-i].pctChange() < limit(stock):
            return False
        if t_open_pct(data, i - 1) >= 0.035:
            continue
        if t_low_pct(data, i - 1) < -0.045:
            count += 1
    if count >= 2:
        return True


def rule20(stock, data: List[dataModel], virtual):
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
    if data[-1].limitOpenTime() <= 2:
        return False
    gemData = collectData('399006', dateRange=5, aimDate=data[-1 if virtual is None else -2].date())
    if t_low_pct(gemData) > -0.005:
        return True


def rule21(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    range1 = data[-3:]
    range2 = data[-6:-3]
    if sum([_.turnover() for _ in range1]) < sum([_.turnover() for _ in range2]):
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:40:00')
        if data[-1].firstLimitTime() < matchTime:
            range20 = data[-21:-1]
            range30 = data[-31:-1]
            if sum([_.close() for _ in range20]) / 20 < sum([_.close() for _ in range30]) / 30:
                return True


def rule22(data: List[dataModel]):
    err = None
    try:
        for i in range(-661, -120):
            range10 = data[i:i + 10]
            if range10[-1].close() / range10[0].close() > 1.8:
                return True
    except Exception as e:
        err = e
        return False


def rule23(stock, data: List[dataModel]):
    if data[-1].turnover() <= 0.5 * data[-2].turnover():
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
    if data[-1].lastLimitTime() <= matchTime:
        return False
    count = 0
    for i in range(5):
        if t_high_pct(data, i) <= limit(stock) / 100:
            continue
        if t_open_pct(data, i) - t_low_pct(data, i) > 0.04:
            count += 1
    if count >= 3:
        return True


def rule24(stock, data: List[dataModel]):
    for i in range(2):
        if not (data[-i - 1].limitOpenTime() > 1 and t_open_pct(data, i) > limit(stock) / 100):
            return False
    return True


def rule25(stock, data: List[dataModel]):
    if data[-1].turnover() <= 0.5 * data[-2].turnover():
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
    if data[-1].lastLimitTime() <= matchTime:
        return False
    flag: bool = False
    for i in range(5):
        if t_open_pct(data, i) - t_low_pct(data, i) > 0.05:
            if t_high_pct(data, i) > limit(stock) / 100:
                matchTime = dateHandler.joinTimeToStamp(data[-i - 1].date(), '10:30:00')
                if data[-i - 1].lastLimitTime() > matchTime:
                    if flag:
                        return True
                    else:
                        flag = True
                        continue


def rule26(stock, data: List[dataModel], virtual=None):
    for i in range(2):
        if not t_limit(stock, data, i + 1):
            return False
    if data[-2].limitOpenTime() <= 2:
        return False
    gemData = collectData('399006', dateRange=5, aimDate=data[-2 if virtual is None else -3].date())
    if t_low_pct(gemData) > -0.005:
        return True


class levelF3:
    def __init__(self, stock: str, data: List[dataModel], virtual=None):
        self.level = 'F3'
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
        self.shot_rule.append(6) if rule6(self.stock, self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.stock, self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.stock, self.data) else self.fail_rule.append(8)
        self.shot_rule.append(9) if rule9(self.stock, self.data) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.stock, self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.stock, self.data, virtual=self.virtual) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.stock, self.data) else self.fail_rule.append(12)
        self.shot_rule.append(13) if rule13(self.stock, self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.data) else self.fail_rule.append(14)
        self.shot_rule.append(15) if rule15(self.stock, self.data) else self.fail_rule.append(15)
        self.shot_rule.append(16) if rule16(self.stock, self.data) else self.fail_rule.append(16)
        self.shot_rule.append(17) if rule17(self.data, self.virtual) else self.fail_rule.append(17)
        self.shot_rule.append(18) if rule18(self.stock, self.data, virtual=self.virtual) else self.fail_rule.append(18)
        self.shot_rule.append(19) if rule19(self.stock, self.data) else self.fail_rule.append(19)
        self.shot_rule.append(20) if rule20(self.stock, self.data, self.virtual) else self.fail_rule.append(20)
        self.shot_rule.append(21) if rule21(self.stock, self.data) else self.fail_rule.append(21)
        self.shot_rule.append(22) if rule22(self.data) else self.fail_rule.append(22)
        self.shot_rule.append(23) if rule23(self.stock, self.data) else self.fail_rule.append(23)
        self.shot_rule.append(24) if rule24(self.stock, self.data) else self.fail_rule.append(24)
        self.shot_rule.append(25) if rule25(self.stock, self.data) else self.fail_rule.append(25)
        self.shot_rule.append(26) if rule26(self.stock, self.data, self.virtual) else self.fail_rule.append(26)
        return self.result()
