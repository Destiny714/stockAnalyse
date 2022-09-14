# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:25
# @Author  : Destiny_
# @File    : levelF3.py
# @Software: PyCharm

from typing import List

from common import dateHandler
from common.collect_data import t_low_pct, t_close_pct, t_open_pct, t_high_pct, limit, dataModel, model_1, model_t, \
    t_limit, limit_height, t_down_limit


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
    try:
        for i in range(1, 6):
            if not model_t(stock, data, i - 1):
                continue
            if t_low_pct(data, i - 1) >= 0.06:
                continue
            range10 = data[-10 - i:-i]
            if data[-i].volume() > 3 * max([_.volume() for _ in range10]):
                d = data[-i]
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                        d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
                    return True
    except:
        pass


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


def rule6(stock, data: List[dataModel], index: List[dataModel]):
    try:
        for i in range(1, 4):
            if t_low_pct(index, i - 1) <= -0.01:
                continue
            d = data[-i]
            if d.open() != d.close():
                continue
            if t_close_pct(data, i - 1) <= limit(stock) / 100:
                continue
            if t_low_pct(data, i - 1) >= 0.06:
                continue
            if data[-i].limitOpenTime() > 2:
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                        d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
                    return True
    except:
        pass


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
        if data[-2].close() / data[-5].close() > 1.1:
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


def rule11(stock, data: List[dataModel], index: List[dataModel]):
    try:
        if model_1(stock, data, 1):
            return False
        if not t_limit(stock, data, 1):
            return False
        if data[-1].turnover() <= 1.8 * data[-2].turnover():
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
        if data[-1].firstLimitTime() > matchTime and data[-1].lastLimitTime() > matchTime:
            time = data[-1].time()
            limitMinute = dateHandler.getMinute(data[-1].firstLimitTime())
            if time[limitMinute] < 100000:
                if t_low_pct(index) > -0.01:
                    return True
    except:
        pass


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
    for i in range(1, 21):
        if limit_height(stock, data, i) >= 3:
            return False
    if t_limit(stock, data, 1):
        return False
    if data[-1].turnover() > max([_.turnover() for _ in data[-31:-1]]) * 1.8:
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


def rule17(data: List[dataModel], index: List[dataModel]):
    try:
        for i in range(1, 5):
            if t_open_pct(data, i - 1) > 0.09 and t_low_pct(data, i - 1) < 0.03:
                if t_low_pct(index, i - 1) > -0.01:
                    d = data[-i]
                    if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() < 0.5 and d.buy_elg_vol() < d.sell_elg_vol():
                        if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                                d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
                            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.3:
                                return True
    except:
        pass


def rule18(stock, data: List[dataModel], index: List[dataModel]):
    try:
        if not t_limit(stock, data, 1):
            return False
        if model_1(stock, data, 1):
            return False
        if data[-1].limitOpenTime() <= 3:
            return False
        if data[-1].turnover() > 3 * data[-2].turnover():
            time = data[-1].time()
            limitMinute = dateHandler.getMinute(data[-1].firstLimitTime())
            if time[limitMinute] < 100000:
                if t_low_pct(index) > -0.01:
                    return True
    except:
        pass


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


def rule20(stock, data: List[dataModel], index: List[dataModel]):
    try:
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if data[-1].limitOpenTime() <= 2:
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
        if data[-1].firstLimitTime() <= matchTime:
            return False
        time = data[-1].time()
        limitMinute = dateHandler.getMinute(data[-1].firstLimitTime())
        if time[limitMinute] >= 100000:
            return False
        if t_low_pct(index) > -0.01:
            d = data[-1]
            if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() < 0.5 and d.buy_elg_vol() < d.sell_elg_vol():
                return True
    except:
        pass


def rule21(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    d = data[-1]
    if d.buy_elg_vol() / d.volume() >= 0.25:
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
    try:
        for i in range(-661, -120):
            range10 = data[i:i + 10]
            if range10[-1].close() / range10[0].close() > 1.8:
                return True
    except:
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


def rule26(stock, data: List[dataModel], index: List[dataModel]):
    for i in range(2):
        if not t_limit(stock, data, i + 1):
            return False
    if data[-2].limitOpenTime() <= 2:
        return False
    if t_low_pct(index, 1) > -0.01:
        return True


def rule27(stock, data: List[dataModel]):
    try:
        if not t_limit(stock, data):
            return False
        d = data[-1]
        if d.buy_elg_vol() / d.volume() >= 0.45:
            return False
        if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() >= 0.6:
            return False
        flag = False
        for i in range(30):
            j = i + 1
            ma30 = [data[-_] for _ in range(j, j + 30)]
            ma60 = [data[-_] for _ in range(j, j + 60)]
            avg30 = sum(_.close() for _ in ma30) / len(ma30)
            avg60 = sum(_.close() for _ in ma60) / len(ma60)
            if avg30 < avg60:
                flag = True
                break
        if not flag:
            return False
        for i in range(10, 51):
            if limit_height(stock, data, i) >= 3:
                return False
        count = 0
        range90 = data[-90:]
        highPrice = max([_.high() for _ in range90])
        if data[-1].close() >= highPrice:
            return False
        for i in range(3, 93):
            if not t_limit(stock, data, i):
                continue
            if t_limit(stock, data, i + 1):
                continue
            if t_limit(stock, data, i - 1):
                continue
            if t_limit(stock, data, i - 2):
                continue
            if t_open_pct(data, i - 1) < 0.045:
                count += 1
            if count >= 2:
                return True
    except:
        return False


def rule28(data: List[dataModel], index: List[dataModel]):
    count = 0
    for i in range(5):
        if t_open_pct(data, i) <= 0.09:
            continue
        if t_low_pct(data, i) >= 0.05:
            continue
        if t_low_pct(index, i) > -0.01:
            count += 1
        if count >= 2:
            return True


def rule29(stock, data: List[dataModel]):
    try:
        if t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        d = data[-1]
        if d.buy_elg_vol() / d.volume() < 0.3:
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.35:
                return True
    except:
        pass


def rule30(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if data[-1].concentration() - data[-2].concentration() > 2:
        return True


def rule31(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
    if data[-1].concentration() - data[-2].concentration() > 3.5:
        return True


def rule32(stock, data: List[dataModel]):
    try:
        if data[-1].turnover() <= 0.25 * data[-2].turnover():
            return False
        count = 0
        for i in range(3):
            if not t_limit(stock, data, i):
                return False
            matchTime = dateHandler.joinTimeToStamp(data[-i - 1].date(), '09:45:00')
            if data[-i - 1].firstLimitTime() >= matchTime:
                return False
            if t_open_pct(data, i) < limit(stock) / 100:
                count += 1
        return count >= 2
    except:
        pass


def rule33(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if data[-1].limitOpenTime() <= 1:
        return False
    if t_down_limit(stock, data):
        if data[-1].buy_elg_vol() / data[-1].volume() < 0.3:
            return True


def rule34(stock, data: List[dataModel]):
    for i in range(3):
        if not t_limit(stock, data, i):
            return False
        if t_open_pct(data, i) >= 0.05:
            return False
    return True


def rule35(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    for i in range(10, 61):
        if limit_height(stock, data, i) >= 3:
            return False
    plus = 0
    minus = 0
    for i in range(40):
        d = data[-i - 1]
        if d.close() > d.open():
            plus += 1
        else:
            minus += 1
    return plus < minus


def rule36(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
    for i in range(10, 61):
        if limit_height(stock, data, i) >= 3:
            return False
    plus = 0
    minus = 0
    for i in range(40):
        d = data[-i - 1]
        if d.close() > d.open():
            plus += 1
        else:
            minus += 1
    return plus < minus


def rule37(stock, data: List[dataModel], index: List[dataModel]):
    try:
        limitCount = 0
        for i in range(8):
            if t_limit(stock, data, i):
                limitCount += 1
        if limitCount >= 3:
            return False
        plus = 1
        minus = 1
        plusVol = 0
        minusVol = 0
        for i in range(8):
            if t_low_pct(index, i) <= -0.01:
                continue
            d = data[-i - 1]
            if d.close() > d.open():
                plusVol += data[-i - 1].volume()
                plus += 1
            else:
                minusVol += data[-i - 1].volume()
                minus += 1
        return plusVol / plus < minusVol / minus
    except:
        pass


def rule38(stock, data: List[dataModel], index: List[dataModel]):
    limitCount = 0
    for i in range(8):
        if t_limit(stock, data, i):
            limitCount += 1
    if limitCount >= 3:
        return False
    plus = 0
    minus = 0
    for i in range(8):
        if t_low_pct(index, i) <= -0.01:
            continue
        d = data[-i - 1]
        if d.close() > d.open():
            plus += 1
        else:
            minus += 1
    return plus < minus


class levelF3:
    def __init__(self, stock: str, data: List[dataModel], index: List[dataModel]):
        self.level = 'F3'
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
        self.shot_rule.append(3) if rule3(self.stock, self.data) else self.fail_rule.append(3)
        self.shot_rule.append(4) if rule4(self.stock, self.data) else self.fail_rule.append(4)
        self.shot_rule.append(5) if rule5(self.stock, self.data) else self.fail_rule.append(5)
        self.shot_rule.append(6) if rule6(self.stock, self.data, self.index) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.stock, self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.stock, self.data) else self.fail_rule.append(8)
        self.shot_rule.append(9) if rule9(self.stock, self.data) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.stock, self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.stock, self.data, self.index) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.stock, self.data) else self.fail_rule.append(12)
        self.shot_rule.append(13) if rule13(self.stock, self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.data) else self.fail_rule.append(14)
        self.shot_rule.append(15) if rule15(self.stock, self.data) else self.fail_rule.append(15)
        self.shot_rule.append(16) if rule16(self.stock, self.data) else self.fail_rule.append(16)
        self.shot_rule.append(17) if rule17(self.data, self.index) else self.fail_rule.append(17)
        self.shot_rule.append(18) if rule18(self.stock, self.data, self.index) else self.fail_rule.append(18)
        self.shot_rule.append(19) if rule19(self.stock, self.data) else self.fail_rule.append(19)
        self.shot_rule.append(20) if rule20(self.stock, self.data, self.index) else self.fail_rule.append(20)
        self.shot_rule.append(21) if rule21(self.stock, self.data) else self.fail_rule.append(21)
        self.shot_rule.append(22) if rule22(self.data) else self.fail_rule.append(22)
        self.shot_rule.append(23) if rule23(self.stock, self.data) else self.fail_rule.append(23)
        self.shot_rule.append(24) if rule24(self.stock, self.data) else self.fail_rule.append(24)
        self.shot_rule.append(25) if rule25(self.stock, self.data) else self.fail_rule.append(25)
        self.shot_rule.append(26) if rule26(self.stock, self.data, self.index) else self.fail_rule.append(26)
        self.shot_rule.append(27) if rule27(self.stock, self.data) else self.fail_rule.append(27)
        self.shot_rule.append(28) if rule28(self.data, self.index) else self.fail_rule.append(28)
        self.shot_rule.append(29) if rule29(self.stock, self.data) else self.fail_rule.append(29)
        self.shot_rule.append(30) if rule30(self.stock, self.data) else self.fail_rule.append(30)
        self.shot_rule.append(31) if rule31(self.stock, self.data) else self.fail_rule.append(31)
        self.shot_rule.append(32) if rule32(self.stock, self.data) else self.fail_rule.append(32)
        self.shot_rule.append(33) if rule33(self.stock, self.data) else self.fail_rule.append(33)
        self.shot_rule.append(34) if rule34(self.stock, self.data) else self.fail_rule.append(34)
        self.shot_rule.append(35) if rule35(self.stock, self.data) else self.fail_rule.append(35)
        self.shot_rule.append(36) if rule36(self.stock, self.data) else self.fail_rule.append(36)
        self.shot_rule.append(37) if rule37(self.stock, self.data, self.index) else self.fail_rule.append(37)
        self.shot_rule.append(38) if rule38(self.stock, self.data, self.index) else self.fail_rule.append(38)
        return self.result()
