# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:25
# @Author  : Destiny_
# @File    : levelF4.py
# @Software: PyCharm

from typing import List

from common import dateHandler
from common.collect_data import t_low_pct, t_close_pct, t_open_pct, limit, dataModel, model_1, model_t, t_limit, \
    limit_height, t_high_pct


def rule1(stock, data: List[dataModel]):
    if data[-1].limitOpenTime() <= 1:
        return False
    count = 0
    limitCount = 0
    for i in range(1, 6):
        if t_limit(stock, data, i - 1):
            limitCount += 1
        if t_open_pct(data, i - 1) >= -0.01:
            continue
        if t_close_pct(data, i - 1) > limit(stock) / 100:
            count += 1
    if count >= 2 and limitCount >= 3:
        return True


def rule2(stock, data: List[dataModel]):
    if data[-1].limitOpenTime() <= 1:
        return False
    limitCount = 0
    for i in range(5):
        if t_limit(stock, data, i):
            limitCount += 1
    if limitCount < 3:
        return False
    for i in range(3):
        if t_low_pct(data, i) < -0.06 and t_close_pct(data, i) > limit(stock) / 100:
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
        if data[-1].buy_elg_vol() < data[-1].sell_elg_vol():
            return True


def rule5(stock, data: List[dataModel]):
    try:
        for i in range(3):
            if not t_limit(stock, data, i):
                return False
        if sum([data[-1].turnover(), data[-2].turnover(), data[-3].turnover()]) <= 40:
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '10:00:00')
        if data[-1].firstLimitTime() > matchTime and data[-1].lastLimitTime() > matchTime:
            d = data[-1]
            if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                    d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
                return True
    except:
        pass


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


def rule7(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if data[-1].turnover() <= 1.8 * data[-2].turnover():
        return False
    standard = (sum([data[-_].turnover() for _ in range(3, 8)]) / 5) * 3
    if data[-1].turnover() > standard and data[-2].turnover() > standard:
        return True


def rule8(stock, data: List[dataModel]):
    try:
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if data[-1].turnover() > 3 * data[-2].turnover():
            matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '11:00:00')
            if data[-1].firstLimitTime() > matchTime and data[-1].lastLimitTime() > matchTime:
                d = data[-1]
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                        d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
                    return True
    except:
        pass


def rule9(stock, data: List[dataModel]):
    for i in range(20):
        if not model_1(stock, data, i):
            continue
        if model_1(stock, data, i + 1):
            continue
        if data[-i - 1].turnover() > 1:
            if data[-i - 1].turnover() > max([_.turnover() for _ in data[-i - 6:-i - 1]]) / 2:
                return True


def rule10(data: List[dataModel]):
    if data[-1].turnover() <= 10:
        return False
    try:
        range60 = data[-61:-1]
        if data[-1].turnover() > 2.5 * max([_.turnover() for _ in range60]):
            return True
    except:
        return False


def rule11(stock, data: List[dataModel]):
    if not model_1(stock, data):
        return False
    if not model_1(stock, data, 1):
        return False
    if (data[-1].turnover() + data[-2].turnover()) / 2 > 0.25 * max([_.turnover() for _ in data[-20:]]):
        return True


def rule12(stock, data: List[dataModel], index: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '14:30:00')
    if data[-1].lastLimitTime() <= matchTime:
        return False
    if data[-1].limitOpenTime() > 3:
        if t_low_pct(index) > -0.01:
            return True


def rule13(stock, data: List[dataModel]):
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-i - 1].date(), '09:40:00')
        if data[-i - 1].firstLimitTime() >= matchTime:
            return False
        if data[-i - 1].limitOpenTime() <= 2:
            return False
        if data[-i - 1].turnover() <= data[-3].turnover():
            return False
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


def rule15(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    range5 = data[-6:-1]
    if data[-1].turnover() > 2 * (sum([_.turnover() for _ in range5]) / 5):
        return True


def rule16(stock, data: List[dataModel], index: List[dataModel]):
    for i in range(5):
        if t_open_pct(data, i) <= limit(stock) / 100:
            continue
        if t_low_pct(data, i) >= 0.06:
            continue
        if not t_limit(stock, data, i):
            continue
        if data[-i - 1].limitOpenTime() > 3:
            d = data[-i - 1]
            if (d.buy_elg_vol() + d.buy_lg_vol()) < (d.sell_elg_vol() + d.sell_lg_vol()):
                if t_low_pct(index, i) > -0.01:
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


def rule18(stock, data: List[dataModel]):
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
    matchTime0 = dateHandler.joinTimeToStamp(data[-1].date(), '10:15:00')
    matchTime1 = dateHandler.joinTimeToStamp(data[-2].date(), '10:15:00')
    if data[-1].firstLimitTime() > matchTime0 and data[-2].firstLimitTime() > matchTime1:
        return True


def rule19(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    for i in range(2):
        matchTime = dateHandler.joinTimeToStamp(data[-i - 1].date(), '13:00:00')
        if data[-i - 1].lastLimitTime() <= matchTime:
            return False
    if data[-1].turnover() > data[-3].turnover() * 5:
        if data[-2].turnover() > data[-3].turnover() * 5:
            return True


def rule20(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if model_1(stock, data):
        return False
    if data[-1].turnover() < 0.5 * data[-2].turnover():
        d = data[-1]
        if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.5:
            return True


def rule21(stock, data: List[dataModel], index: List[dataModel]):
    try:
        if data[-1].limitOpenTime() == 0:
            return False
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if data[-1].firstLimitTime() <= data[-2].firstLimitTime() + dateHandler.timeDelta(data[-2].date(),
                                                                                          data[-1].date()):
            return False
        if data[-1].lastLimitTime() <= data[-2].lastLimitTime() + dateHandler.timeDelta(data[-2].date(),
                                                                                        data[-1].date()):
            return False
        if t_low_pct(index) > -0.01:
            time = data[-1].time()
            limitMinute = dateHandler.getMinute(data[-1].firstLimitTime())
            if time[limitMinute] < 100000:
                return True
    except:
        pass


def rule22(stock, data: List[dataModel]):
    try:
        if data[-1].limitOpenTime() == 0:
            return False
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '10:30:00')
        if data[-1].firstLimitTime() > matchTime and data[-1].lastLimitTime() > matchTime:
            time = data[-1].time()
            limitMinute = dateHandler.getMinute(data[-1].firstLimitTime())
            if time[limitMinute] < 100000:
                return True
    except:
        pass


def rule23(stock, data: List[dataModel], index: List[dataModel]):
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
        if t_low_pct(index) > -0.01:
            return True


def rule24(stock, data: List[dataModel], index: List[dataModel]):
    try:
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if data[-2].limitOpenTime() <= 1:
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
        if data[-1].firstLimitTime() <= matchTime:
            return False
        time = data[-1].time()
        limitMinute = dateHandler.getMinute(data[-1].firstLimitTime())
        if time[limitMinute] >= 100000:
            return False
        if data[-1].lastLimitTime() > data[-2].lastLimitTime() + dateHandler.timeDelta(data[-2].date(),
                                                                                       data[-1].date()):
            if t_low_pct(index) > -0.01:
                return True
    except:
        pass


def rule25(stock, data: List[dataModel]):
    try:
        count = 0
        for i in range(1, 6):
            if not t_limit(stock, data, i - 1):
                continue
            if data[-i].limitOpenTime() > 5:
                d = data[-i]
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                        d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
                    count += 1
            if count >= 2:
                return True
    except:
        pass


def rule26(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if data[-1].turnover() <= data[-2].turnover():
        return False
    range10 = data[-12:-2]
    if data[-2].turnover() > 3 * (sum([_.turnover() for _ in range10]) / 10):
        if t_open_pct(data) < 0.03:
            return True


def rule28(stock, data: List[dataModel]):
    for i in range(3):
        if not t_limit(stock, data, i):
            return False
    if data[-1].turnover() > data[-2].turnover() > data[-3].turnover() > 15:
        return True


def rule29(stock, data: List[dataModel]):
    try:
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if data[-1].turnover() <= data[-2].turnover():
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
        if data[-1].firstLimitTime() <= matchTime:
            return False
        time = data[-1].time()
        limitMinute = dateHandler.getMinute(data[-1].firstLimitTime())
        if time[limitMinute] >= 100000:
            return False
        d = data[-1]
        if (d.buy_elg_vol() - d.sell_elg_vol()) / (d.buy_elg_vol()) < 0.3:
            if t_low_pct(data) < t_open_pct(data):
                return True
    except:
        pass


def rule30(stock, data: List[dataModel]):
    try:
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if data[-1].turnover() <= data[-2].turnover() * 0.8:
            return False
        if t_open_pct(data) >= 0.045:
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:50:00')
        if data[-1].firstLimitTime() > matchTime:
            time = data[-1].time()
            limitMinute = dateHandler.getMinute(data[-1].firstLimitTime())
            if time[limitMinute] < 100000:
                if t_low_pct(data) < t_open_pct(data):
                    return True
    except:
        pass


def rule31(stock, data: List[dataModel]):
    try:
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if data[-1].turnover() <= data[-2].turnover():
            return False
        range5 = data[-7:-2]
        if data[-2].turnover() > 3 * (sum([_.turnover() for _ in range5]) / 5):
            time = data[-1].time()
            limitMinute = dateHandler.getMinute(data[-1].firstLimitTime())
            if time[limitMinute] < 100000:
                return True
    except:
        pass


def rule32(stock, data: List[dataModel]):
    try:
        d = data[-1]
        if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() >= 0.3:
            return False
        for i in range(10, 51):
            if limit_height(stock, data, i) >= 2:
                return False
        for i in range(3, 153):
            if not t_limit(stock, data, i):
                continue
            if t_limit(stock, data, i - 1):
                continue
            if t_limit(stock, data, i + 1):
                continue
            if data[-i].turnover() > 1.5 * data[-1].turnover():
                if data[-i].high() * 1.02 > data[-1].close():
                    if t_limit(stock, data):
                        return True
    except:
        return False


def rule33(stock, data: List[dataModel]):
    try:
        if t_limit(stock, data, 2):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            if t_open_pct(data, i) >= 0.03:
                return False
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
        if data[-1].firstLimitTime() <= matchTime:
            return False
        time = data[-1].time()
        limitMinute = dateHandler.getMinute(data[-1].firstLimitTime())
        if time[limitMinute] >= 100000:
            return False
        if data[-1].turnover() > data[-2].turnover():
            return True
    except:
        pass


def rule34(stock, data: List[dataModel]):
    if t_low_pct(data) >= 0.05:
        return False
    if t_limit(stock, data, 2):
        return False
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
    if data[-1].turnover() > data[-2].turnover():
        matchTime = dateHandler.joinTimeToStamp(data[-2].date(), '09:40:00')
        if data[-2].firstLimitTime() < matchTime:
            if t_low_pct(data) < t_open_pct(data):
                return True


def rule35(stock, data: List[dataModel]):
    try:
        for i in range(3, 153):
            if not t_limit(stock, data, i):
                continue
            if t_limit(stock, data, i - 1):
                continue
            if data[-i].turnover() > 1.5 * data[-1].turnover() and data[-i].turnover() > 1.5 * data[-2].turnover():
                if data[-i].high() * 1.02 > data[-1].close():
                    if not t_limit(stock, data):
                        continue
                    if t_limit(stock, data, 1):
                        continue
                    if data[-1].limitOpenTime() > 3:
                        return True
    except:
        return False


def rule36(stock, data: List[dataModel]):
    try:
        if t_open_pct(data) >= t_open_pct(data, 1):
            return False
        if t_low_pct(data) >= 0.05:
            return False
        flag = False
        for i in range(3, 153):
            if not t_limit(stock, data, i):
                continue
            if t_limit(stock, data, i - 1):
                continue
            if data[-i].turnover() > 1.5 * data[-1].turnover() and data[-i].turnover() > 1.5 * data[-2].turnover():
                if data[-i].high() * 1.02 > data[-2].close():
                    flag = True
                    break
        if not flag:
            return False
        if not t_limit(stock, data, 1):
            return False
        if t_limit(stock, data, 2):
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-2].date(), '09:50:00')
        if data[-2].firstLimitTime() < matchTime:
            return True
    except:
        return False


def rule37(data: List[dataModel]):
    try:
        d = data[-1]
        if d.buy_elg_vol() / d.volume() >= 0.35:
            return False
        if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() >= 0.6:
            return False
        badCount = 0
        for i in range(50):
            j = i + 1
            ma30 = [data[-_] for _ in range(j, j + 30)]
            ma60 = [data[-_] for _ in range(j, j + 60)]
            avg30 = sum(_.close() for _ in ma30) / len(ma30)
            avg60 = sum(_.close() for _ in ma60) / len(ma60)
            if avg30 < avg60:
                badCount += 1
            if badCount >= 15:
                return True
    except:
        return False


def rule38(stock, data: List[dataModel]):
    try:
        if model_1(stock, data):
            return False
        if not t_limit(stock, data):
            return False
        limitTime = data[-1].firstLimitTime()
        limitMinute = dateHandler.getMinute(limitTime)
        limitMinuteLast = dateHandler.lastMinute(limitMinute)
        time = data[-1].time()
        if time[limitMinute] < time[limitMinuteLast] * 3:
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.4:
                if t_low_pct(data) < t_open_pct(data):
                    return True
    except:
        return False


def rule40(data: List[dataModel], index: List[dataModel]):
    try:
        badCount10 = 0
        badCount30 = 0
        for i in range(30):
            j = i + 1
            if i in range(10):
                ma20 = [data[-_] for _ in range(j, j + 20)]
                avg20 = sum(_.close() for _ in ma20) / len(ma20)
                if data[-i - 1].close() < avg20:
                    if t_low_pct(index, i) > -0.01:
                        badCount10 += 1
            ma60 = [data[-_] for _ in range(j, j + 60)]
            avg60 = sum(_.close() for _ in ma60) / len(ma60)
            if data[-i - 1].close() < avg60:
                badCount30 += 1
            if badCount10 >= 2 and badCount30 >= 3:
                return True
    except:
        return False


def rule41(stock, data: List[dataModel]):
    try:
        for i in range(10, 51):
            if limit_height(stock, data, i) >= 3:
                return False
        for i in range(3, 153):
            if not t_limit(stock, data, i):
                continue
            if t_limit(stock, data, i - 1):
                continue
            nxt = data[-i]
            if nxt.turnover() > data[-1].turnover() * 1.5 and nxt.turnover() > data[-2].turnover() * 1.5:
                if nxt.high() * 1.02 > data[-1].close():
                    if t_open_pct(data, i - 1) < 0.04 and t_high_pct(data, i - 1) < 0.06:
                        return True
    except:
        pass


def rule42(data: List[dataModel], index: List[dataModel]):
    try:
        badCount1 = 0
        badCount2 = 0
        for i in range(40):
            j = i + 1
            ma60 = [data[-_] for _ in range(j, j + 60)]
            avg60 = sum(_.close() for _ in ma60) / len(ma60)
            if data[-i - 1].close() < avg60:
                if t_low_pct(index, i) > -0.01:
                    badCount1 += 1
            if i in range(10) and badCount2 == 0:
                ma10 = [data[-_] for _ in range(j, j + 10)]
                ma30 = [data[-_] for _ in range(j, j + 30)]
                avg10 = sum(_.close() for _ in ma10) / len(ma10)
                avg30 = sum(_.close() for _ in ma30) / len(ma30)
                if avg10 < avg30 < avg60:
                    badCount2 += 1
            if badCount1 >= 3 and badCount2 > 0:
                return True
    except:
        return False


def rule43(stock, data: List[dataModel], index: List[dataModel]):
    try:
        for i in range(10, 51):
            if limit_height(stock, data, i) >= 3:
                return False
        badCount = 0
        for i in range(10):
            j = i + 1
            ma = [data[-_] for _ in range(j, j + 30)]
            avg = sum(_.close() for _ in ma) / len(ma)
            if data[-i - 1].close() < avg:
                if t_low_pct(index, i) > -0.01:
                    badCount += 1
            if badCount >= 2:
                return True
    except:
        return False


def rule44(data: List[dataModel], index: List[dataModel]):
    try:
        badCount10 = 0
        badCount40 = 0
        for i in range(40):
            j = i + 1
            if t_low_pct(index, i) <= -0.01:
                continue
            if i in range(10):
                ma20 = [data[-_] for _ in range(j, j + 20)]
                avg20 = sum(_.close() for _ in ma20) / len(ma20)
                if data[-i - 1].close() < avg20:
                    badCount10 += 1
            ma60 = [data[-_] for _ in range(j, j + 60)]
            avg60 = sum(_.close() for _ in ma60) / len(ma60)
            if data[-i - 1].close() < avg60:
                badCount40 += 1
            if badCount10 >= 2 and badCount40 >= 3:
                return True
    except:
        return False


def rule45(stock, data: List[dataModel]):
    for i in range(3, 153):
        if not t_limit(stock, data, i):
            continue
        if t_limit(stock, data, i - 1):
            continue
        if t_high_pct(data, i - 1) > max([_.high() for _ in data[-5:]]):
            return True


class levelF4:
    def __init__(self, stock: str, data: List[dataModel], index: List[dataModel]):
        self.level = 'F4'
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
        self.shot_rule.append(3) if rule3(self.data) else self.fail_rule.append(3)
        self.shot_rule.append(4) if rule4(self.stock, self.data) else self.fail_rule.append(4)
        self.shot_rule.append(5) if rule5(self.stock, self.data) else self.fail_rule.append(5)
        self.shot_rule.append(6) if rule6(self.stock, self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.stock, self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.stock, self.data) else self.fail_rule.append(8)
        self.shot_rule.append(9) if rule9(self.stock, self.data) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.stock, self.data) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.stock, self.data, self.index) else self.fail_rule.append(12)
        self.shot_rule.append(13) if rule13(self.stock, self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.stock, self.data) else self.fail_rule.append(14)
        self.shot_rule.append(15) if rule15(self.stock, self.data) else self.fail_rule.append(15)
        self.shot_rule.append(16) if rule16(self.stock, self.data, self.index) else self.fail_rule.append(16)
        self.shot_rule.append(17) if rule17(self.stock, self.data) else self.fail_rule.append(17)
        self.shot_rule.append(18) if rule18(self.stock, self.data) else self.fail_rule.append(18)
        self.shot_rule.append(19) if rule19(self.stock, self.data) else self.fail_rule.append(19)
        self.shot_rule.append(20) if rule20(self.stock, self.data) else self.fail_rule.append(20)
        self.shot_rule.append(21) if rule21(self.stock, self.data, self.index) else self.fail_rule.append(21)
        self.shot_rule.append(22) if rule22(self.stock, self.data) else self.fail_rule.append(22)
        self.shot_rule.append(23) if rule23(self.stock, self.data, self.index) else self.fail_rule.append(23)
        self.shot_rule.append(24) if rule24(self.stock, self.data, self.index) else self.fail_rule.append(24)
        self.shot_rule.append(25) if rule25(self.stock, self.data) else self.fail_rule.append(25)
        self.shot_rule.append(26) if rule26(self.stock, self.data) else self.fail_rule.append(26)
        self.shot_rule.append(28) if rule28(self.stock, self.data) else self.fail_rule.append(28)
        self.shot_rule.append(29) if rule29(self.stock, self.data) else self.fail_rule.append(29)
        self.shot_rule.append(30) if rule30(self.stock, self.data) else self.fail_rule.append(30)
        self.shot_rule.append(31) if rule31(self.stock, self.data) else self.fail_rule.append(31)
        self.shot_rule.append(32) if rule32(self.stock, self.data) else self.fail_rule.append(32)
        self.shot_rule.append(33) if rule33(self.stock, self.data) else self.fail_rule.append(33)
        self.shot_rule.append(34) if rule34(self.stock, self.data) else self.fail_rule.append(34)
        self.shot_rule.append(35) if rule35(self.stock, self.data) else self.fail_rule.append(35)
        self.shot_rule.append(36) if rule36(self.stock, self.data) else self.fail_rule.append(36)
        self.shot_rule.append(37) if rule37(self.data) else self.fail_rule.append(37)
        self.shot_rule.append(38) if rule38(self.stock, self.data) else self.fail_rule.append(38)
        self.shot_rule.append(40) if rule40(self.data, self.index) else self.fail_rule.append(40)
        self.shot_rule.append(41) if rule41(self.stock, self.data) else self.fail_rule.append(41)
        self.shot_rule.append(42) if rule42(self.data, self.index) else self.fail_rule.append(42)
        self.shot_rule.append(43) if rule43(self.stock, self.data, self.index) else self.fail_rule.append(43)
        self.shot_rule.append(44) if rule44(self.data, self.index) else self.fail_rule.append(44)
        self.shot_rule.append(45) if rule45(self.stock, self.data) else self.fail_rule.append(45)
        return self.result()
