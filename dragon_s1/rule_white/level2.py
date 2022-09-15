# -*- coding: utf-8 -*-
# @Time    : 2022/6/21 00:05
# @Author  : Destiny_
# @File    : level2.py
# @Software: PyCharm
from common.dataOperation import *


class level2:
    def __init__(self, stock: str, data: list[dataModel]):
        self.level = 2
        self.data = data
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def rule1(self):
        data = self.data
        range5 = data[-5:]
        range6to10 = data[-10:-5]
        if sum([_.turnover() for _ in range5]) > 2 * sum([_.turnover() for _ in range6to10]):
            return True

    def rule2(self):
        data = self.data
        try:
            range60 = data[-60:]
            range220 = data[-220:]
            if max([_.turnover() for _ in range60]) > 5 * sum([_.turnover() for _ in range220]) / 220:
                return True
        except:
            return False

    def rule3(self):
        data = self.data
        stock = self.stock
        for i in range(5, 31):
            if t_limit(stock, data, i):
                return True

    def rule4(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        range10 = data[-11:-1]
        range30 = data[-31:-1]
        if sum(_.close() for _ in range10) / 10 > sum(_.close() for _ in range30) / 30:
            return True

    def rule5(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        range10 = data[-11:-1]
        range20 = data[-21:-1]
        if sum(_.close() for _ in range10) / 10 > sum(_.close() for _ in range20) / 20:
            return True

    def rule6(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        try:
            range20 = data[-21:-1]
            range30 = data[-31:-1]
            if sum(_.close() for _ in range20) / 20 > sum(_.close() for _ in range30) / 30:
                return True
        except Exception:
            return False

    def rule7(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        try:
            range30 = data[-31:-1]
            range60 = data[-61:-1]
            if sum(_.close() for _ in range30) / 30 > sum(_.close() for _ in range60) / 60:
                return True
        except Exception:
            return False

    def rule8(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        try:
            range60 = data[-61:-1]
            range120 = data[-121:-1]
            if sum(_.close() for _ in range60) / 60 > sum(_.close() for _ in range120) / 120:
                return True
        except:
            return False

    def rule9(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 3):
            return False
        high3 = max(data[-1].high(), data[-2].high(), data[-3].high())
        high220 = max([_.high() for _ in data[-223:-3]])
        if high3 > high220:
            return True

    def rule10(self):
        data = self.data
        if data[-3].turnover() < data[-2].turnover() < data[-1].turnover():
            if data[-3].close() < data[-2].close() < data[-1].close():
                return True

    def rule11(self):
        data = self.data
        if data[-4].turnover() < data[-3].turnover() < data[-2].turnover():
            if data[-4].close() < data[-3].close() < data[-2].close():
                return True

    def rule12(self):
        data = self.data
        if data[-5].turnover() < data[-4].turnover() < data[-3].turnover():
            if data[-5].close() < data[-4].close() < data[-3].close():
                return True

    def rule13(self):
        data = self.data
        if data[-5].turnover() < data[-3].turnover() < data[-2].turnover():
            if data[-5].close() < data[-3].close() < data[-2].close():
                return True

    def rule14(self):
        data = self.data
        if data[-5].turnover() < data[-4].turnover() < data[-2].turnover():
            if data[-5].close() < data[-4].close() < data[-2].close():
                return True

    def rule15(self):
        data = self.data
        try:
            count = 0
            for i in range(40):
                j = i + 1
                ma10 = [data[-_] for _ in range(j, j + 10)]
                ma20 = [data[-_] for _ in range(j, j + 20)]
                avg10 = sum(_.close() for _ in ma10) / len(ma10)
                avg20 = sum(_.close() for _ in ma20) / len(ma20)
                if avg10 > avg20:
                    count += 1
                if count >= 30:
                    return True
        except:
            return False

    def rule16(self):
        data = self.data
        try:
            count = 0
            for i in range(40):
                j = i + 1
                ma20 = [data[-_] for _ in range(j, j + 20)]
                ma30 = [data[-_] for _ in range(j, j + 30)]
                avg20 = sum(_.close() for _ in ma20) / len(ma20)
                avg30 = sum(_.close() for _ in ma30) / len(ma30)
                if avg20 > avg30:
                    count += 1
                if count >= 30:
                    return True
        except:
            return False

    def rule18(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 1):
            return False
        try:
            range1to5 = data[-6:-1]
            range1to10 = data[-11:-1]
            range1to20 = data[-21:-1]
            if sum([_.close() for _ in range1to5]) / 5 > sum([_.close() for _ in range1to20]) / 20:
                if data[-2].close() > sum([_.close() for _ in range1to10]) / 10:
                    return True
        except:
            return False

    def filter(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            ruleID = int(str(rule).replace('rule', ''))
            self.shot_rule.append(ruleID) if func() else self.fail_rule.append(ruleID)
        return self.result()
