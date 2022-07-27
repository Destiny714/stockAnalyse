# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:25
# @Author  : Destiny_
# @File    : level7.py
# @Software: PyCharm
from typing import List
from common import dateHandler
from common.collect_data import t_low_pct, t_open_pct, t_close_pct, t_high_pct, limit, dataModel, model_1, t_limit


def rule1(stock, data: List[dataModel]):
    if t_limit(stock, data, 3):
        return False
    if t_limit(stock, data, 4):
        return False
    if not t_limit(stock, data):
        return False
    if model_1(stock, data):
        return False
    flag = False
    for i in range(2, 4):
        if model_1(stock, data, i - 1):
            flag = not flag
    return flag


def rule2(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data, 2):
        return False
    if data[-1].turnover() > 1.5 * data[-2].turnover():
        if data[-2].turnover() > 1.5 * data[-3].turnover():
            return True


def rule3(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if model_1(stock, data):
        return False
    if model_1(stock, data, 1):
        return False
    if data[-1].turnover() <= 3 * data[-2].turnover():
        return False
    if data[-1].firstLimitTime() > data[-2].firstLimitTime() + dateHandler.timeDelta(data[-2].date(), data[-1].date()):
        return True


def rule4(stock, data: List[dataModel]):
    for i in range(4):
        if not t_limit(stock, data, i):
            return False
    if model_1(stock, data):
        return False
    if model_1(stock, data, 1):
        return False
    if data[-1].turnover() < data[-2].turnover() < data[-3].turnover():
        return True


def rule5(stock, data: List[dataModel]):
    count1 = 0
    count2 = 0
    for i in range(1, 5):
        if t_limit(stock, data, i - 1):
            count1 += 1
        if model_1(stock, data, i - 1):
            count2 += 1
    if count2 > 1:
        return False
    if count1 < 3:
        return False
    if data[-4].turnover() < data[-3].turnover() < data[-2].turnover() < data[-1].turnover():
        return True


def rule6(stock, data: List[dataModel]):
    if not model_1(stock, data, 0):
        return False
    range10 = data[-11:-1]
    if data[-1].turnover() > 1.8 * max([_.turnover() for _ in range10]):
        return True


def rule7(stock, data: List[dataModel]):
    if not (data[-4].turnover() > data[-3].turnover() > data[-2].turnover()):
        return False
    flag = False
    for i in range(2, 5):
        if t_limit(stock, data, i - 1):
            flag = True
            break
    if flag:
        if model_1(stock, data, 1):
            return False
        if model_1(stock, data, 3):
            return False
        return True


def rule8(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 5):
        if data[-i].pctChange() < limit(stock):
            return False
        if t_open_pct(data, i - 1) < 0.03:
            count += 1
    if count >= 3:
        return True


def rule9(stock, data: List[dataModel]):
    flag = False
    for i in range(1, 4):
        if not t_limit(stock, data, i - 1):
            return False
        if i in range(1, 3) and flag is False:
            if t_close_pct(data, i - 1) <= limit(stock) / 100:
                continue
            if t_open_pct(data, i - 1) < -0.025 or t_low_pct(data, i - 1) < -0.045:
                flag = True
    return flag


def rule10(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 4):
        if data[-i].pctChange() < limit(stock):
            return False
        if t_low_pct(data, i - 1) < -0.06:
            matchTime = dateHandler.joinTimeToStamp(data[-i].date(), '10:30:00')
            if data[-i].firstLimitTime() != 0 and data[-i].firstLimitTime() > matchTime:
                count += 1
    return count >= 1


def rule11(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 5):
        if data[-i].pctChange() < limit(stock):
            return False
        if t_open_pct(data, i - 1) < -0.03:
            matchTime = dateHandler.joinTimeToStamp(data[-i].date(), '10:30:00')
            if data[-i].lastLimitTime() != 0 and data[-i].lastLimitTime() > matchTime:
                count += 1
    return count >= 1


def rule12(data: List[dataModel]):
    start = data[-9].close()
    close = data[-1].close()
    if (close - start) / start > 0.9:
        return True


def rule13(stock, data: List[dataModel]):
    flag = False
    for i in range(1, 6):
        if model_1(stock, data, i - 1):
            flag = True
            break
    if flag:
        allVol = [_.turnover() for _ in data[-5:]]
        if min(allVol) > (1 / 3) * max(allVol):
            return True


def rule14(stock, data: List[dataModel]):
    if t_limit(stock, data, 3):
        return False
    if t_limit(stock, data, 2):
        return False
    if not model_1(stock, data, 1):
        return False
    if not model_1(stock, data):
        return True


def rule15(data: List[dataModel]):
    range10 = data[-10:]
    range30 = data[-30:]
    avg10 = sum([_.close() for _ in range10]) / 10
    avg30 = sum([_.close() for _ in range30]) / 30
    if avg10 < avg30:
        return True


def rule16(data: List[dataModel]):
    range15 = data[-15:]
    range60 = data[-60:]
    avg15 = sum([_.close() for _ in range15]) / 15
    avg60 = sum([_.close() for _ in range60]) / 60
    if avg15 < avg60:
        return True


def rule17(stock, data: List[dataModel]):
    for i in range(5):
        if data[-i - 1].turnover() <= 4:
            continue
        if model_1(stock, data, i):
            return True


def rule18(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '10:00:00')
    if data[-1].lastLimitTime() <= matchTime:
        return False
    count = 0
    for i in range(5):
        if t_open_pct(data, i) - t_low_pct(data, i) > 0.07:
            count += 1
        if count >= 2:
            return True


def rule19(stock, data: List[dataModel]):
    for i in range(3):
        if not t_limit(stock, data, i):
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-i - 1].date(), '09:47:00')
        if data[-i - 1].firstLimitTime() >= matchTime:
            return False
    return True


def rule20(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if t_open_pct(data) >= 0.04:
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '10:30:00')
    if data[-1].firstLimitTime() > matchTime:
        return True


def rule21(stock, data: List[dataModel]):
    count = 0
    for i in range(4):
        if t_open_pct(data, i) - t_low_pct(data, i) > 0.07:
            if t_high_pct(data, i) > limit(stock) / 100:
                count += 1
        if count >= 3:
            return True


class level7:
    def __init__(self, stock: str, data: List[dataModel]):
        self.level = 7
        self.data = data
        self.stock = stock
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
        self.shot_rule.append(11) if rule11(self.stock, self.data) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.data) else self.fail_rule.append(12)
        self.shot_rule.append(13) if rule13(self.stock, self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.stock, self.data) else self.fail_rule.append(14)
        self.shot_rule.append(15) if rule15(self.data) else self.fail_rule.append(15)
        self.shot_rule.append(16) if rule16(self.data) else self.fail_rule.append(16)
        self.shot_rule.append(17) if rule17(self.stock, self.data) else self.fail_rule.append(17)
        self.shot_rule.append(18) if rule18(self.stock, self.data) else self.fail_rule.append(18)
        self.shot_rule.append(19) if rule19(self.stock, self.data) else self.fail_rule.append(19)
        self.shot_rule.append(20) if rule20(self.stock, self.data) else self.fail_rule.append(20)
        self.shot_rule.append(21) if rule21(self.stock, self.data) else self.fail_rule.append(21)
        return self.result()
