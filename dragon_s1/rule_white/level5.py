# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 09:18
# @Author  : Destiny_
# @File    : level5.py
# @Software: PyCharm

from typing import List

from common import dateHandler
from common.collect_data import t_low_pct, t_close_pct, t_open_pct, limit, dataModel, model_1, model_t, \
    t_limit


def rule1(stock, data: List[dataModel]):
    try:
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
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.3:
                return True
    except:
        pass


def rule2(stock, data: List[dataModel]):
    try:
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
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.3:
                return True
    except:
        pass


def rule3(stock, limitTimeRank: list):
    if stock in limitTimeRank:
        return True


def rule4(stock, data: List[dataModel]):
    if data[-1].limitOpenTime() >= 1:
        return False
    count = 0
    for i in range(1, 4):
        if 0.055 < t_open_pct(data, i - 1) < limit(stock) / 100:
            count += 1
        if count >= 2:
            break
    if count < 2:
        return False
    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:50:00')
    if data[-1].firstLimitTime() < matchTime:
        return True


def rule5(stock, industryLimitRank: list):
    if stock in industryLimitRank:
        return True


def rule6(stock, data: List[dataModel]):
    if t_limit(stock, data, 3):
        return False
    try:
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if data[-1].turnover() > data[-2].turnover():
            if t_open_pct(data) > 0.07:
                if t_low_pct(data) > 0.05:
                    if data[-2].turnover() < 0.7 * data[-3].turnover():
                        d = data[-1]
                        if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.3:
                            return True
    except:
        pass


def rule7(stock, data: List[dataModel]):
    try:
        if not model_1(stock, data, 1):
            return False
        if data[-2].turnover() < data[-3].turnover() / 3:
            if model_t(stock, data) and t_low_pct(data) > 0.07:
                d = data[-1]
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.4:
                    return True
    except:
        pass


def rule10(stock, data: List[dataModel]):
    if t_limit(stock, data, 3):
        return False
    try:
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not (t_open_pct(data) > 0.05 and t_low_pct(data) > 0.03):
            return False
        if data[-1].turnover() >= data[-2].turnover():
            return False
        range7 = data[-9:-2]
        if data[-2].turnover() > max([_.turnover() for _ in range7]):
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.3:
                return True
    except:
        pass


def rule11(stock, data: List[dataModel]):
    try:
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        matchTime0 = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
        matchTime1 = dateHandler.joinTimeToStamp(data[-2].date(), '09:45:00')
        if data[-1].firstLimitTime() < matchTime0 and data[-2].firstLimitTime() > matchTime1:
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.3:
                return True
    except:
        pass


def rule12(stock, data: List[dataModel]):
    try:
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
        if data[-1].lastLimitTime() >= data[-2].lastLimitTime() + dateHandler.timeDelta(data[-2].date(),
                                                                                        data[-1].date()):
            return False
        if data[-1].lastLimitTime() < matchTime:
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.3:
                return True
    except:
        pass


def rule13(stock, data: List[dataModel]):
    try:
        for i in range(4):
            if not t_limit(stock, data, i):
                return False
        if not model_t(stock, data, 1):
            return False
        if data[-1].turnover() >= data[-2].turnover():
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:50:00')
        if data[-1].lastLimitTime() < matchTime:
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.3:
                return True
    except:
        pass


def rule14(stock, data: List[dataModel]):
    try:
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
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() > 0.3:
                return True
    except:
        pass


class level5:
    def __init__(self, stock: str, data: List[dataModel], index: List[dataModel], limitTimeRank: list,
                 industryLimitRank: list):
        self.level = 5
        self.data = data
        self.index = index
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []
        self.limitTimeRank: list = limitTimeRank
        self.industryLimitRank: list = industryLimitRank

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def filter(self):
        self.shot_rule.append(1) if rule1(self.stock, self.data) else self.fail_rule.append(1)
        self.shot_rule.append(2) if rule2(self.stock, self.data) else self.fail_rule.append(2)
        self.shot_rule.append(3) if rule3(self.stock, self.limitTimeRank) else self.fail_rule.append(3)
        self.shot_rule.append(4) if rule4(self.stock, self.data) else self.fail_rule.append(4)
        self.shot_rule.append(5) if rule5(self.stock, self.industryLimitRank) else self.fail_rule.append(5)
        self.shot_rule.append(6) if rule6(self.stock, self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.stock, self.data) else self.fail_rule.append(7)
        self.shot_rule.append(10) if rule10(self.stock, self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.stock, self.data) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.stock, self.data) else self.fail_rule.append(12)
        self.shot_rule.append(13) if rule13(self.stock, self.data) else self.fail_rule.append(13)
        self.shot_rule.append(14) if rule14(self.stock, self.data) else self.fail_rule.append(14)
        return self.result()
