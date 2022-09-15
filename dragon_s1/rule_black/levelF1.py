# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:25
# @Author  : Destiny_
# @File    : levelF1.py
# @Software: PyCharm
from common.dataOperation import *


class levelF1:
    def __init__(self, stock: str, data: list[dataModel], index: list[dataModel], industryLimitRank: list):
        self.level = 'F1'
        self.data = data
        self.index = index
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []
        self.industryLimitRank = industryLimitRank

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule == []}

    def rule1(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
                if t_low_pct(data, i) >= -0.01:
                    return False
                d = data[-i - 1]
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() >= 0.6:
                    return False
            return True
        except:
            pass

    def rule2(self):
        data = self.data
        stock = self.stock
        if not model_1(stock, data):
            return False
        if not model_1(stock, data, 1):
            return False
        if data[-1].turnover() > 2.5 * data[-2].turnover():
            return True

    def rule3(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(1, 4):
            if not t_limit(stock, data, i - 1):
                return False
            if t_open_pct(data, i - 1) >= -0.01:
                continue
            if t_close_pct(data, i - 1) > limit(stock) / 100:
                count += 1
        return count >= 2

    def rule4(self):
        data = self.data
        stock = self.stock
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
                if data[-2].firstLimitTime() > data[-3].firstLimitTime() + dateHandler.timeDelta(data[-3].date(), data[-2].date()):
                    return True

    def rule5(self):
        data = self.data
        stock = self.stock
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

    def rule6(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(30, 121):
            if t_limit(stock, data, i):
                count += 1
            if count >= 5:
                return False
        if data[-31].close() / data[-121].close() > 2.2:
            return True

    def rule7(self):
        data = self.data
        stock = self.stock
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
        matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '09:40:00')
        if data[-1].lastLimitTime() < matchTime:
            return True

    def rule8(self):
        data = self.data
        stock = self.stock
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

    def rule9(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data, 2):
            return False
        for i in range(1, 3):
            if t_open_pct(data, i) < -0.04:
                if t_low_pct(self.index, i) > -0.01:
                    return True

    def rule10(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(1, 6):
            if not t_limit(stock, data, i - 1):
                continue
            if t_low_pct(data, i - 1) < -0.055 and t_high_pct(data, i - 1) > limit(stock) / 100:
                count += 1
            if count >= 2:
                return True

    def rule11(self):
        data = self.data
        stock = self.stock
        for i in range(1, 4):
            if not t_limit(stock, data, i - 1):
                return False
            if t_open_pct(data, i - 1) >= 0.035:
                return False
        return True

    def rule12(self):
        data = self.data
        stock = self.stock
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

    def rule13(self):
        data = self.data
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

    def rule14(self):
        data = self.data
        try:
            for i in range(1, 31):
                if t_high_pct(data, i - 1) > 0.06:
                    return False
            return True
        except:
            return False

    def rule15(self):
        data = self.data
        stock = self.stock
        for i in range(2, 5):
            if t_limit(stock, data, i):
                return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if data[-2].turnover() > 3 * sum([_.turnover() for _ in data[-5:-2]]) / 3:
            if data[-1].turnover() > 3 * sum([_.turnover() for _ in data[-5:-2]]) / 3:
                return True

    def rule16(self):
        data = self.data
        stock = self.stock
        try:
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
                    if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.3:
                        return True
        except:
            pass

    def rule17(self):
        data = self.data
        stock = self.stock
        changeRate = -1
        for i in range(4):
            if not t_limit(stock, data, i):
                return False
            if changeRate < data[-i - 1].turnover():
                changeRate = data[-i - 1].turnover()
            else:
                return False
        return True

    def rule18(self):
        data = self.data
        stock = self.stock
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

    def rule19(self):
        data = self.data
        stock = self.stock
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

    def rule20(self):
        data = self.data
        stock = self.stock
        if data[-1].turnover() <= data[-2].turnover() * 0.8:
            return False
        if not (t_open_pct(data) > t_open_pct(data, 1) > 0.05):
            return False
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if data[-1].lastLimitTime() > data[-2].lastLimitTime() + dateHandler.timeDelta(data[-2].date(), data[-1].date()):
            if t_low_pct(self.index) > -0.01:
                return True

    def rule21(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        count = 0
        for i in range(2):
            if model_1(stock, data, i):
                count += 1
        if count > 1:
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-2].date(), '09:45:00')
        if data[-2].lastLimitTime() < matchTime:
            range2_20 = data[-21:-2]
            if data[-2].close() < max([_.close() for _ in range2_20]):
                return True

    def rule22(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 3):
                if t_open_pct(data, i) <= limit(stock) / 100:
                    continue
                if t_low_pct(data, i) >= 0.05:
                    continue
                if t_close_pct(data, i) <= limit(stock) / 100:
                    continue
                matchTime = dateHandler.joinTimeToStamp(data[-i - 1].date(), '10:30:00')
                if data[-i - 1].lastLimitTime() > matchTime:
                    d = data[-i]
                    if (d.buy_elg_vol() + d.buy_lg_vol()) / d.volume() < 0.5 and d.buy_elg_vol() < d.sell_elg_vol():
                        if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.3:
                            return True
        except:
            pass

    def rule23(self):
        data = self.data
        try:
            range10 = data[-11:-1]
            range30 = data[-30:-1]
            if sum([_.close() for _ in range10]) / 10 < sum([_.close() for _ in range30]) / 30:
                return True
        except:
            return False

    def rule25(self):
        data = self.data
        stock = self.stock
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

    def rule26(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if t_limit(stock, data, 1):
            return False
        if data[-1].turnover() > 16:
            matchTime = dateHandler.joinTimeToStamp(data[-1].date(), '13:30:00')
            if data[-1].firstLimitTime() > matchTime:
                return True

    def rule27(self):
        data = self.data
        stock = self.stock
        for i in range(3):
            if t_limit(stock, data, i + 2):
                return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if (data[-3].close() - data[-6].close()) / data[-6].close() > 0.1:
            return True

    def rule28(self):
        data = self.data
        stock = self.stock
        if not self.industryLimitRank:
            return False
        if not t_limit(stock, data):
            return False
        for i in range(20):
            if t_limit(stock, data, i):
                break
        else:
            return False
        if stock not in self.industryLimitRank[0].__iadd__([] if len(self.industryLimitRank) == 1 else self.industryLimitRank[1]):
            return True

    def rule29(self):
        data = self.data
        stock = self.stock
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

    def rule30(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data, 3):
            return False
        if not t_limit(stock, data):
            return False
        if t_limit(stock, data, 2):
            return False
        if t_limit(stock, data, 1):
            return False
        if data[-1].turnover() < data[-4].turnover() * 0.8:
            return True

    def rule32(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            if model_1(stock, data, i):
                return False
            d = data[-i - 1]
            matchTime = dateHandler.joinTimeToStamp(d.date(), '09:50:00')
            if d.firstLimitTime() >= matchTime:
                return False
        for i in range(3, 11):
            if not t_limit(stock, data, i):
                continue
            if not t_limit(stock, data, i - 1):
                return True

    def rule33(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data, 2):
            return False
        matchTime = dateHandler.joinTimeToStamp(data[-3].date(), '10:00:00')
        if data[-3].firstLimitTime() <= matchTime:
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            matchTime = dateHandler.joinTimeToStamp(data[-i - 1].date(), '09:50:00')
            if data[-i - 1].firstLimitTime() >= matchTime:
                return False
        return True

    def filter(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            ruleID = int(str(rule).replace('rule', ''))
            self.shot_rule.append(ruleID) if func() else self.fail_rule.append(ruleID)
        return self.result()
