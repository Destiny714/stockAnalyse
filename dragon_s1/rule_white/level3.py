# -*- coding: utf-8 -*-
# @Time    : 2022/6/21 15:16
# @Author  : Destiny_
# @File    : level3.py
# @Software: PyCharm
from common import dateHandler
from typing import List
from common.collect_data import limit, dataModel, t_open_pct, t_close_pct, t_low_pct, t_limit, model_1


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
    except:
        return False


def rule9(stock, data: List[dataModel]):
    if data[-2].turnover() <= data[-1].turnover():
        return False
    if not (t_open_pct(data) > 0.05 and t_close_pct(data) > limit(stock) / 100):
        return False
    range10 = data[-12:-2]
    if data[-2].turnover() > max([_.turnover() for _ in range10]):
        return True


def rule10(stock, data: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if not t_limit(stock, data, 1):
        return False
    if t_limit(stock, data, 2):
        return False
    if t_open_pct(data, 0) >= 0.045:
        if t_low_pct(data, 0) > 0.005:
            return True


def rule11(stock, data: List[dataModel]):
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
    except:
        return False


def rule12(stock, data: List[dataModel]):
    if t_limit(stock, data):
        return False
    if t_limit(stock, data, 1):
        return False
    try:
        range220 = data[-221:-1]
        flag = max([_.close() for _ in range220])
        for i in range(20):
            if data[-i - 1].close() * 1.1 > flag:
                return True
    except:
        return False


def rule13(data: List[dataModel]):
    try:
        for i in range(1, 61):
            if data[-i].close() > max([_.close() for _ in data[-i - 440:-i]]):
                return True
    except:
        pass


def rule14(data: List[dataModel]):
    try:
        flag = False
        for i in range(1, 31):
            if t_close_pct(data, i - 1) > 0.06:
                flag = True
                break
        if flag:
            range220 = data[-221:-1]
            if data[-1].close() > 0.95 * max([_.high() for _ in range220]):
                return True
    except:
        return False


def rule15(data: List[dataModel]):
    avg4 = sum([data[-5].close(), data[-4].close(), data[-3].close(), data[-2].close()]) / 4
    if not (data[-1].close() > avg4 and data[-2].close() > avg4):
        return False
    for i in range(1, 3):
        range220 = data[-i - 220:-i]
        if data[-i].close() > max([_.high() for _ in range220]):
            return True


def rule16(data: List[dataModel]):
    try:
        if data[-1].concentration() < 0.14:
            return True
    except:
        pass


def rule17(stock, data: List[dataModel]):
    if not t_limit(stock, data, 1):
        range5 = data[-6:-1]
        avg = sum([_.turnover() for _ in range5]) / 5
        if avg < 5:
            return True


def rule18(stock, data: List[dataModel]):
    if 4 < data[-1].close() < 12:
        if 1.5 < data[-1].turnover() < 6:
            return True


def rule19(stock, data: List[dataModel]):
    if t_limit(stock, data, 2):
        return False
    if not t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    if 4 < data[-1].close() < 12:
        if 3 < data[-1].turnover() < 9:
            return True


def rule20(stock, data: List[dataModel]):
    if t_limit(stock, data, 1):
        return False
    if not t_limit(stock, data):
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:40:00')
    if data[-1].firstLimitTime() > matchTime:
        return True


def rule22(stock, data: List[dataModel], index: List[dataModel]):
    if not t_limit(stock, data):
        return False
    if t_low_pct(data) <= -0.05:
        return False
    if t_open_pct(data) > 0.01:
        if t_close_pct(index) < -0.02:
            return True


def rule23(data: List[dataModel]):
    try:
        for i in range(10):
            j = i + 1
            ma = [data[-_] for _ in range(j, j + 10)]
            avg = sum(_.close() for _ in ma) / len(ma)
            if data[-i - 1].close() <= avg:
                return False
        return True
    except:
        return False


def rule24(data: List[dataModel]):
    try:
        for i in range(20):
            j = i + 1
            ma = [data[-_] for _ in range(j, j + 20)]
            avg = sum(_.close() for _ in ma) / len(ma)
            if data[-i - 1].close() <= avg:
                return False
        return True
    except:
        return False


def rule25(data: List[dataModel]):
    try:
        for i in range(30):
            j = i + 1
            ma = [data[-_] for _ in range(j, j + 30)]
            avg = sum(_.close() for _ in ma) / len(ma)
            if data[-i - 1].close() <= avg:
                return False
        return True
    except:
        return False


def rule26(data: List[dataModel]):
    try:
        if data[-1].concentration() < data[-2].concentration():
            if data[-1].concentration() < 0.15:
                return True
    except:
        pass


def rule27(stock, data: List[dataModel]):
    for i in range(2):
        if not t_limit(stock, data, i):
            return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
    if data[-1].firstLimitTime() < matchTime:
        return True


def rule28(stock, data: List[dataModel]):
    limitCount = 0
    for i in range(3):
        if t_limit(stock, data, i):
            limitCount += 1
        if limitCount > 1:
            return False
    range10 = data[-11:-1]
    range20 = data[-21:-1]
    count = 0
    for i in range10:
        if i.close() > sum([_.close() for _ in range20]) / 20:
            count += 1
        if count >= 8:
            return True


def rule29(data: List[dataModel]):
    try:
        for i in range(30):
            j = i + 1
            day1 = data[-j - 2]
            day2 = data[-j - 1]
            day3 = data[-j]
            if day1.close() > day2.close() > day3.close():
                if day1.volume() < day2.volume() < day3.volume():
                    return True
    except:
        pass


def rule30(stock, data: List[dataModel]):
    plus = []
    minus = []
    for i in range(1, 21):
        if t_limit(stock, data, i):
            return False
        if t_close_pct(data, i) > 0:
            plus.append(data[-i - 1].volume())
        else:
            minus.append(data[-i - 1].volume())
    if sum(plus) / len(plus) > sum(minus) / len(minus):
        return True


def rule31(stock, data: List[dataModel]):
    if not model_1(stock, data):
        return False
    if model_1(stock, data, 1):
        return False
    if data[-1].turnover() < 0.25 * data[-2].turnover():
        return True


def rule32(stock, data: List[dataModel]):
    if not model_1(stock, data, 1):
        return False
    if model_1(stock, data, 2):
        return False
    if data[-2].turnover() < 0.25 * data[-3].turnover():
        return True


def rule33(data: List[dataModel]):
    try:
        badCount = 0
        for i in range(50):
            j = i + 1
            ma = [data[-_] for _ in range(j, j + 60)]
            avg = sum(_.close() for _ in ma) / len(ma)
            if data[-i - 1].close() <= avg:
                badCount += 1
            if badCount > 2:
                return False
        return True
    except:
        return False


def rule34(data: List[dataModel]):
    try:
        badCount = 0
        for i in range(40):
            j = i + 1
            ma = [data[-_] for _ in range(j, j + 30)]
            avg = sum(_.close() for _ in ma) / len(ma)
            if data[-i - 1].close() <= avg:
                badCount += 1
            if badCount > 3:
                return False
        return True
    except:
        return False


def rule36(stock, data: List[dataModel]):
    try:
        for i in range(20):
            if t_limit(stock, data, i):
                if t_limit(stock, data, i + 1):
                    return False
        badCount = 0
        for i in range(15):
            if t_limit(stock, data, i):
                continue
            j = i + 1
            ma = [data[-_] for _ in range(j, j + 20)]
            avg = sum(_.close() for _ in ma) / len(ma)
            if data[-i - 1].close() < avg:
                badCount += 1
            if badCount > 1:
                return False
        return True
    except:
        return False


def rule37(stock, data: List[dataModel]):
    for i in range(30):
        j = i + 1
        day1 = data[-j - 2]
        day2 = data[-j - 1]
        day3 = data[-j]
        for _ in range(i, i + 3):
            if t_limit(stock, data, _):
                return False
        if day1.close() < day2.close() < day3.close():
            if day1.volume() < day2.volume() < day3.volume():
                return True


def rule38(data: List[dataModel]):
    v1 = data[-1].timeVol(minute='0930')
    v2 = data[-2].timeVol(minute='0930')
    if v1 > v2:
        return True


def rule39(data: List[dataModel]):
    v1 = data[-1].timeVol(minute='0930')
    v2 = data[-2].timeVol(minute='0930')
    v3 = data[-3].timeVol(minute='0930')
    if v1 > v2 > v3:
        return True


def rule40(stock, data: List[dataModel]):
    try:
        if t_open_pct(data) > limit(stock):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        v1 = data[-1].timeVol(timeStamp=data[-1].firstLimitTime())
        v2 = data[-2].timeVol(timeStamp=data[-2].firstLimitTime())
        if v1 > v2:
            return True
    except:
        pass


def rule41(stock, data: List[dataModel]):
    try:
        if not t_limit(stock, data, 1):
            return False
        if model_1(stock, data, 1):
            return False
        d = data[-2]
        if d.timeVol(timeStamp=d.firstLimitTime()) <= 100000:
            return False
        if d.timeVol(timeStamp=d.firstLimitTime()) > d.timeVol(timeStamp=d.firstLimitTime() - 60) * 10:
            return True
    except:
        pass


class level3:
    def __init__(self, stock: str, data: List[dataModel], index: List[dataModel]):
        self.level = 3
        self.data = data
        self.index = index
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
        self.shot_rule.append(7) if rule7(self.stock, self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.stock, self.data) else self.fail_rule.append(8)
        self.shot_rule.append(9) if rule9(self.stock, self.data) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.stock, self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.stock, self.data) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.stock, self.data) else self.fail_rule.append(12)
        self.shot_rule.append(13) if rule13(self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.data) else self.fail_rule.append(14)
        self.shot_rule.append(15) if rule15(self.data) else self.fail_rule.append(15)
        self.shot_rule.append(16) if rule16(self.data) else self.fail_rule.append(16)
        self.shot_rule.append(17) if rule17(self.stock, self.data) else self.fail_rule.append(17)
        self.shot_rule.append(18) if rule18(self.stock, self.data) else self.fail_rule.append(18)
        self.shot_rule.append(19) if rule19(self.stock, self.data) else self.fail_rule.append(19)
        self.shot_rule.append(20) if rule20(self.stock, self.data) else self.fail_rule.append(20)
        self.shot_rule.append(22) if rule22(self.stock, self.data, self.index) else self.fail_rule.append(22)
        self.shot_rule.append(23) if rule23(self.data) else self.fail_rule.append(23)
        self.shot_rule.append(24) if rule24(self.data) else self.fail_rule.append(24)
        self.shot_rule.append(25) if rule25(self.data) else self.fail_rule.append(25)
        self.shot_rule.append(26) if rule26(self.data) else self.fail_rule.append(26)
        self.shot_rule.append(27) if rule27(self.stock, self.data) else self.fail_rule.append(27)
        self.shot_rule.append(28) if rule28(self.stock, self.data) else self.fail_rule.append(28)
        self.shot_rule.append(29) if rule29(self.data) else self.fail_rule.append(29)
        self.shot_rule.append(30) if rule30(self.stock, self.data) else self.fail_rule.append(30)
        self.shot_rule.append(31) if rule31(self.stock, self.data) else self.fail_rule.append(31)
        self.shot_rule.append(32) if rule32(self.stock, self.data) else self.fail_rule.append(32)
        self.shot_rule.append(33) if rule33(self.data) else self.fail_rule.append(33)
        self.shot_rule.append(34) if rule34(self.data) else self.fail_rule.append(34)
        self.shot_rule.append(36) if rule36(self.stock, self.data) else self.fail_rule.append(36)
        self.shot_rule.append(37) if rule37(self.stock, self.data) else self.fail_rule.append(37)
        self.shot_rule.append(38) if rule38(self.data) else self.fail_rule.append(38)
        self.shot_rule.append(39) if rule39(self.data) else self.fail_rule.append(39)
        self.shot_rule.append(40) if rule40(self.stock, self.data) else self.fail_rule.append(40)
        self.shot_rule.append(41) if rule41(self.stock, self.data) else self.fail_rule.append(41)
        return self.result()
