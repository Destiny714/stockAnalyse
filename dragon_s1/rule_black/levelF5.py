# -*- coding: utf-8 -*-
# @Time    : 2022/8/3 17:41
# @Author  : Destiny_
# @File    : levelF5.py
# @Software: PyCharm

from common.dataOperation import *


class levelF5:
    def __init__(self, stock: str, data: list[dataModel], index: list[dataModel]):
        self.level = 'F5'
        self.data = data
        self.stock = stock
        self.index = index
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule == []}

    def rule1(self):
        data = self.data
        stock = self.stock
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

    def rule2(self):
        data = self.data
        stock = self.stock
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

    def rule3(self):
        data = self.data
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

    def rule4(self):
        data = self.data
        stock = self.stock
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

    def rule5(self):
        data = self.data
        try:
            if t_high_pct(data) <= 0.06:
                return False
            if t_low_pct(data) >= 0.05:
                return False
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0:
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (d.buy_elg_vol() + d.buy_lg_vol()) < 0:
                    return True
        except:
            pass

    def rule6(self):
        data = self.data
        stock = self.stock
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

    def rule7(self):
        data = self.data
        stock = self.stock
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

    def rule8(self):
        data = self.data
        stock = self.stock
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

    def rule9(self):
        data = self.data
        try:
            if t_high_pct(data) > 0.06:
                d = data[-1]
                if d.buy_elg_vol() / d.volume() >= 0.25:
                    return False
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.4:
                    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:45:00')
                    if data[-1].firstLimitTime() > matchTime:
                        return True
        except:
            pass

    def rule10(self):
        data = self.data
        try:
            if not t_limit(self.stock, data):
                return False
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

    def rule11(self):
        data = self.data
        try:
            for i in range(2):
                if not t_limit(self.stock, data, i):
                    return False
                d = data[-i - 1]
                if t_high_pct(data, i) <= 0.05:
                    return False
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                        d.buy_elg_vol() + d.buy_lg_vol()) >= 0.2:
                    return False
                matchTime = dateHandler.joinTimeToStamp(d.date(), '09:45:00')
                if d.firstLimitTime() <= matchTime:
                    return False
            return True
        except:
            pass

    def rule12(self):
        data = self.data
        index = self.index
        try:
            if t_high_pct(data) <= 0.06:
                return False
            if t_low_pct(data) >= 0.05:
                return False
            if not t_limit(self.stock, data):
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

    def rule13(self):
        data = self.data
        try:
            if not t_limit(self.stock, data):
                return False
            d = data[-1]
            if t_high_pct(data) <= 0.06:
                return False
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.6:
                if d.buy_elg_vol() / d.volume() < 0.4:
                    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '10:00:00')
                    if data[-1].firstLimitTime() > matchTime:
                        return True
        except:
            pass

    def rule14(self):
        data = self.data
        try:
            if not t_limit(self.stock, data):
                return False
            for i in range(2):
                if t_high_pct(data, i) <= 0.05:
                    return False
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.6:
                if d.buy_elg_vol() / d.volume() < 0.4:
                    matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '10:00:00')
                    if data[-1].firstLimitTime() > matchTime:
                        return True
        except:
            pass

    def filter(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            ruleID = int(str(rule).replace('rule', ''))
            self.shot_rule.append(ruleID) if func() else self.fail_rule.append(ruleID)
        return self.result()
