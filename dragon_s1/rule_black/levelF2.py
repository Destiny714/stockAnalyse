# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:25
# @Author  : Destiny_
# @File    : levelF2.py
# @Software: PyCharm
from typing import List
from common import dateHandler
from common.collect_data import t_low_pct, t_open_pct, t_close_pct, t_high_pct, limit, dataModel, model_1, t_limit, \
    t_down_limit


def rule1(stock, data: List[dataModel]):
    count = 0
    if not (data[-3].turnover() < data[-2].turnover() < data[-1].turnover()):
        return False
    for i in range(3):
        if not t_limit(stock, data, i):
            return False
        if data[-i - 1].limitOpenTime() > 2:
            count += 1
        if count >= 2:
            return True


def rule2(stock, data: List[dataModel]):
    for i in range(3):
        if not t_limit(stock, data, i):
            return False
        if model_1(stock, data, i):
            return False
    if data[-1].turnover() > 1.5 * data[-2].turnover():
        if data[-2].turnover() > 1.5 * data[-3].turnover():
            return True


def rule3(stock, data: List[dataModel], index: List[dataModel]):
    try:
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
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
        if data[-1].firstLimitTime() <= matchTime:
            return False
        time = data[-1].time()
        limitMinute = dateHandler.getMinute(data[-1].firstLimitTime())
        if time[limitMinute] < 100000:
            if t_low_pct(index) > -0.01:
                return True
    except:
        pass


def rule4(stock, data: List[dataModel]):
    for i in range(4):
        if not t_limit(stock, data, i):
            return False
    if model_1(stock, data):
        return False
    if model_1(stock, data, 1):
        return False
    if data[-1].turnover() < data[-2].turnover() < data[-3].turnover():
        if data[-2].turnover() < data[-4].turnover():
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
        if t_open_pct(data, 1) < 0.06 and t_open_pct(data) < 0.06:
            return True


def rule6(stock, data: List[dataModel]):
    if not model_1(stock, data, 0):
        return False
    range10 = data[-11:-1]
    if data[-1].turnover() > 1.8 * max([_.turnover() for _ in range10]):
        return True


def rule7(stock, data: List[dataModel]):
    limitCount = 0
    for i in range(3):
        if t_limit(stock, data, i + 1):
            limitCount += 1
    if limitCount < 2:
        return False
    range30 = data[-34:-4]
    for d in range30:
        if d.pctChange() >= limit(stock):
            return False
    if not (data[-4].turnover() > data[-3].turnover() > data[-2].turnover()):
        return False
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
    try:
        for i in range(1, 4):
            if not t_limit(stock, data, i - 1):
                return False
        for i in range(2):
            d = data[- i - 1]
            if data[-i - 1].limitOpenTime() <= 1:
                continue
            if t_close_pct(data, i) <= limit(stock) / 100:
                continue
            if t_open_pct(data, i) < -0.025 or t_low_pct(data, i) < -0.045:
                if (d.buy_elg_vol() + d.buy_lg_vol()) < (d.sell_elg_vol() + d.sell_lg_vol()):
                    if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.3:
                        return True
    except:
        pass


def rule10(stock, data: List[dataModel]):
    count = 0
    for i in range(1, 4):
        if data[-i].pctChange() < limit(stock):
            return False
        if t_low_pct(data, i - 1) < -0.06:
            matchTime = dateHandler.joinTimeToStamp(data[-i].date(), '10:30:00')
            if data[-i].firstLimitTime() != 0 and data[-i].firstLimitTime() > matchTime:
                if data[-i].limitOpenTime() > 0:
                    count += 1
    return count >= 1


def rule11(stock, data: List[dataModel]):
    for i in range(1, 5):
        if not t_limit(stock, data, i - 1):
            continue
        if not t_limit(stock, data, i):
            continue
        if t_open_pct(data, i - 1) < -0.03:
            matchTime = dateHandler.joinTimeToStamp(data[-i].date(), '10:30:00')
            if data[-i].lastLimitTime() > matchTime:
                return True


def rule12(stock, data: List[dataModel]):
    if not t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data, ):
        return False
    if t_limit(stock, data, 1):
        return False
    if data[-2].turnover() * 0.7 > data[-1].turnover():
        if data[-2].high() > data[-1].high():
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


def rule15(stock, data: List[dataModel]):
    plus = []
    minus = []
    for i in range(3, 33):
        if t_limit(stock, data, i):
            return False
        if t_down_limit(stock, data, i):
            return False
        if t_close_pct(data, i) > 0:
            plus.append(data[-i - 1].volume())
        else:
            minus.append(data[-i - 1].volume())
    if sum(plus) / len(plus) < sum(minus) / len(minus):
        return True


def rule16(data: List[dataModel]):
    range15 = data[-15:]
    range60 = data[-60:]
    avg15 = sum([_.close() for _ in range15]) / 15
    avg60 = sum([_.close() for _ in range60]) / 60
    if avg15 < avg60:
        return True


def rule17(stock, data: List[dataModel]):
    flag = False
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
        if t_low_pct(data, i) >= -0.05:
            continue
        matchTime = dateHandler.joinTimeToStamp(data[-i - 1].date(), '13:00:00')
        if data[-i - 1].lastLimitTime() > matchTime:
            flag = True
    return flag


def rule18(stock, data: List[dataModel]):
    try:
        if not t_limit(stock, data):
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '10:00:00')
        if data[-1].lastLimitTime() <= matchTime:
            return False
        count = 0
        for i in range(5):
            d = data[-i - 1]
            if t_open_pct(data, i) - t_low_pct(data, i) > 0.07 and t_high_pct(data, i) > 0.06:
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                        d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
                    count += 1
            if count >= 2:
                return True
    except:
        pass


def rule19(stock, data: List[dataModel]):
    try:
        count = 0
        for i in range(3):
            if not t_limit(stock, data, i):
                return False
            if model_1(stock, data, i):
                return False
            matchTime = dateHandler.joinTimeToStamp(data[-i - 1].date(), '09:47:00')
            if data[-i - 1].firstLimitTime() >= matchTime:
                return False
            d = data[-i - 1]
            if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                    d.sell_elg_vol() + d.sell_lg_vol()) < 0.2:
                count += 1
        return count >= 2
    except:
        pass


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


def rule22(stock, data: List[dataModel]):
    for i in range(3):
        if not t_limit(stock, data, i):
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-i - 1].date(), '10:00:00')
        if data[-i - 1].firstLimitTime() <= matchTime:
            return False
        if data[-i - 1].lastLimitTime() <= matchTime:
            return False
    return True


def rule23(stock, data: List[dataModel]):
    for i in range(2):
        if t_limit(stock, data, i):
            return False
    if data[-1].concentration() - data[-2].concentration() > 0.02:
        return True


def rule24(stock, data: List[dataModel]):
    try:
        for i in range(3):
            if t_limit(stock, data, i + 1):
                return False
        if not t_limit(stock, data):
            return False
        if model_1(stock, data):
            return False
        d = data[-1]
        if d.buy_elg_vol() / d.volume() >= 0.4:
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:40:00')
        if data[-1].firstLimitTime() < matchTime:
            if data[-1].timeVol(timeStamp=data[-1].firstLimitTime()) < 100000:
                return True
    except:
        pass


def rule25(stock, data: List[dataModel]):
    for i in range(2, 4):
        if t_limit(stock, data, i):
            return False
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
    if data[-4].turnover() > data[-3].turnover() > data[-2].turnover() > data[-1].turnover():
        return True


def rule26(stock, data: List[dataModel]):
    if model_1(stock, data):
        return False
    if not t_limit(stock, data, 1):
        if t_limit(stock, data):
            matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:40:00')
            if data[-1].firstLimitTime() < matchTime:
                return True


def rule27(stock, data: List[dataModel]):
    if model_1(stock, data, 1):
        return False
    if not t_limit(stock, data, 2):
        if t_limit(stock, data, 1):
            matchTime = dateHandler.joinTimeToStamp(data[-2].date(), '09:40:00')
            if data[-2].firstLimitTime() < matchTime:
                return True


def rule28(stock, data: List[dataModel]):
    flag = False
    for i in range(4, 13):
        if t_limit(stock, data, i):
            if t_limit(stock, data, i + 1):
                if t_limit(stock, data, i + 2):
                    flag = True
                    break
    if not flag:
        return False
    if t_limit(stock, data, 3):
        return False
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
    if data[-2].turnover() >= sum(_.turnover() for _ in data[-6:-3]) / 3:
        return False
    if data[-1].turnover() > data[-2].turnover():
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '10:00:00')
        if data[-1].firstLimitTime() > matchTime:
            return True


def rule29(stock, data: List[dataModel]):
    flag = False
    for i in range(4, 13):
        if t_limit(stock, data, i):
            if t_limit(stock, data, i + 1):
                if t_limit(stock, data, i + 2):
                    flag = True
                    break
    if not flag:
        return False
    if t_limit(stock, data, 3):
        return False
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-i - 1].date(), '09:40:00')
        if data[-i - 1].firstLimitTime() >= matchTime:
            return False
    if data[-2].turnover() >= 0.6 * sum(_.turnover() for _ in data[-6:-3]) / 3:
        return False
    if data[-1].turnover() < 0.6 * sum(_.turnover() for _ in data[-6:-3]) / 3:
        return True


def rule30(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if t_low_pct(data) < -0.04:
        return True


class levelF2:
    def __init__(self, stock: str, data: List[dataModel], index: List[dataModel]):
        self.level = 'F2'
        self.data = data
        self.index = index
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule == []}

    def filter(self):
        self.shot_rule.append(1) if rule1(self.stock, self.data) else self.fail_rule.append(1)
        self.shot_rule.append(2) if rule2(self.stock, self.data) else self.fail_rule.append(2)
        self.shot_rule.append(3) if rule3(self.stock, self.data, self.index) else self.fail_rule.append(3)
        self.shot_rule.append(4) if rule4(self.stock, self.data) else self.fail_rule.append(4)
        self.shot_rule.append(5) if rule5(self.stock, self.data) else self.fail_rule.append(5)
        self.shot_rule.append(6) if rule6(self.stock, self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.stock, self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.stock, self.data) else self.fail_rule.append(8)
        self.shot_rule.append(9) if rule9(self.stock, self.data) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.stock, self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.stock, self.data) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.stock, self.data) else self.fail_rule.append(12)
        self.shot_rule.append(13) if rule13(self.stock, self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.stock, self.data) else self.fail_rule.append(14)
        self.shot_rule.append(15) if rule15(self.stock, self.data) else self.fail_rule.append(15)
        self.shot_rule.append(16) if rule16(self.data) else self.fail_rule.append(16)
        self.shot_rule.append(17) if rule17(self.stock, self.data) else self.fail_rule.append(17)
        self.shot_rule.append(18) if rule18(self.stock, self.data) else self.fail_rule.append(18)
        self.shot_rule.append(19) if rule19(self.stock, self.data) else self.fail_rule.append(19)
        self.shot_rule.append(20) if rule20(self.stock, self.data) else self.fail_rule.append(20)
        self.shot_rule.append(21) if rule21(self.stock, self.data) else self.fail_rule.append(21)
        self.shot_rule.append(22) if rule22(self.stock, self.data) else self.fail_rule.append(22)
        self.shot_rule.append(23) if rule23(self.stock, self.data) else self.fail_rule.append(23)
        self.shot_rule.append(24) if rule24(self.stock, self.data) else self.fail_rule.append(24)
        self.shot_rule.append(25) if rule25(self.stock, self.data) else self.fail_rule.append(25)
        self.shot_rule.append(26) if rule26(self.stock, self.data) else self.fail_rule.append(26)
        self.shot_rule.append(27) if rule27(self.stock, self.data) else self.fail_rule.append(27)
        self.shot_rule.append(28) if rule28(self.stock, self.data) else self.fail_rule.append(28)
        self.shot_rule.append(29) if rule29(self.stock, self.data) else self.fail_rule.append(29)
        self.shot_rule.append(30) if rule30(self.stock, self.data) else self.fail_rule.append(30)
        return self.result()
