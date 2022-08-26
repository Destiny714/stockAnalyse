# -*- coding: utf-8 -*-
# @Time    : 2022/8/3 17:41
# @Author  : Destiny_
# @File    : levelF5.py
# @Software: PyCharm
from typing import List

from common import dateHandler
from common.collect_data import dataModel, model_1, t_limit, t_high_pct, t_low_pct


def rule1(stock, data: List[dataModel]):
    try:
        if not t_limit(stock, data, 1):
            return False
        d = data[-2]
        if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.2:
                matchTime = dateHandler.joinTimeToStamp(d.date(), '10:00:00')
                if d.firstLimitTime() > matchTime:
                    return True
    except:
        pass


def rule2(stock, data: List[dataModel]):
    try:
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '10:00:00')
        if data[-1].firstLimitTime() <= matchTime:
            return False
        d = data[-2]
        if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.2:
                return True
    except:
        pass


def rule3(data: List[dataModel]):
    try:
        for i in range(3):
            d = data[-i - 1]
            if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                    d.buy_elg_vol() + d.buy_lg_vol()) >= 0.2:
                return False
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() >= 0.3:
                return False
        return True
    except:
        pass


def rule4(stock, data: List[dataModel]):
    try:
        if (data[-1].buy_elg_vol() - data[-1].sell_elg_vol()) / data[-1].buy_elg_vol() >= 0.2:
            return False
        for i in range(5):
            d = data[-i - 1]
            if d.turnover() <= 4:
                continue
            if model_1(stock, data, i):
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.2:
                    return True
    except:
        pass


def rule5(data: List[dataModel]):
    if t_high_pct(data) <= 0.05:
        return False
    d = data[-1]
    if d.buy_elg_vol() + d.buy_lg_vol() < d.sell_elg_vol():
        return True
    if d.buy_elg_vol() + d.buy_lg_vol() < d.sell_lg_vol():
        return True


def rule6(stock, data: List[dataModel]):
    try:
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        d = data[-2]
        if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.2:
                if d.buy_lg_vol() < d.sell_lg_vol():
                    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
                    if data[-1].firstLimitTime() > matchTime:
                        return True
    except:
        pass


def rule7(stock, data: List[dataModel]):
    try:
        count = 0
        limitCount = 0
        for i in range(5):
            if t_limit(stock, data, i):
                limitCount += 1
            d = data[-i - 1]
            if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                    d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.2:
                    count += 1
            if count >= 3 and limitCount >= 4:
                return True
    except:
        pass


def rule8(stock, data: List[dataModel]):
    try:
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            d = data[-i - 1]
            if ((d.buy_elg_vol() + d.buy_lg_vol()) / d.volume()) >= 0.45:
                return False
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() >= 0.3:
                return False
        return True
    except:
        pass


def rule9(data: List[dataModel]):
    try:
        if t_high_pct(data) > 0.06:
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.4:
                matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
                if data[-1].firstLimitTime() > matchTime:
                    return True
    except:
        pass


def rule10(data: List[dataModel]):
    try:
        if t_high_pct(data, 1) <= 0.05:
            return False
        if t_high_pct(data) > 0.05:
            d = data[-1]
            d1 = data[-2]
            if (d.buy_elg_vol() + d1.buy_elg_vol() - d.sell_elg_vol() - d1.sell_elg_vol()) / (
                    d.buy_elg_vol() + d1.buy_elg_vol()) < 0.3:
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.4:
                    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
                    if data[-1].lastLimitTime() > matchTime:
                        return True
    except:
        pass


def rule11(data: List[dataModel]):
    try:
        if t_high_pct(data) <= 0.05:
            return False
        for i in range(2):
            d = data[-i - 1]
            if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                    d.buy_elg_vol() + d.buy_lg_vol()) >= 0.2:
                return False
            matchTime = dateHandler.joinTimeToStamp(d.date(), '09:45:00')
            if d.firstLimitTime() <= matchTime:
                return False
        return True
    except:
        pass


def rule12(data: List[dataModel], index: List[dataModel]):
    try:
        if t_high_pct(data) <= 0.05:
            return False
        d = data[-1]
        if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.2:
                matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
                if data[-1].lastLimitTime() < matchTime:
                    if t_low_pct(index) > -0.01:
                        return True
    except:
        pass


class levelF5:
    def __init__(self, stock: str, data: List[dataModel], index: List[dataModel]):
        self.level = 'F5'
        self.data = data
        self.stock = stock
        self.index = index
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule == []}

    def filter(self):
        self.shot_rule.append(1) if rule1(self.stock, self.data) else self.fail_rule.append(1)
        self.shot_rule.append(2) if rule2(self.stock, self.data) else self.fail_rule.append(2)
        self.shot_rule.append(3) if rule3(self.data) else self.fail_rule.append(3)
        self.shot_rule.append(4) if rule4(self.stock, self.data) else self.fail_rule.append(4)
        self.shot_rule.append(5) if rule5(self.data) else self.fail_rule.append(5)
        self.shot_rule.append(6) if rule6(self.stock, self.data) else self.fail_rule.append(6)
        self.shot_rule.append(7) if rule7(self.stock, self.data) else self.fail_rule.append(7)
        self.shot_rule.append(8) if rule8(self.stock, self.data) else self.fail_rule.append(8)
        self.shot_rule.append(9) if rule9(self.data) else self.fail_rule.append(9)
        self.shot_rule.append(10) if rule10(self.data) else self.fail_rule.append(10)
        self.shot_rule.append(11) if rule11(self.data) else self.fail_rule.append(11)
        self.shot_rule.append(12) if rule12(self.data, self.index) else self.fail_rule.append(12)
        return self.result()
