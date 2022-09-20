# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : S.py
# @Software: PyCharm
from utils.stockdata_util import dataModel, t_limit


class ruleS:

    def __init__(self, height: int, score: int, T1S: int, T1F: int, black: int, white: int, S: int,
                 data: list[dataModel], stock: str, aj: float, details: dict[str, list[int]]):
        self.S = S
        self.aj = aj
        self.T1S = T1S
        self.T1F = T1F
        self.data = data
        self.stock = stock
        self.black = black
        self.white = white
        self.score = score
        self.height = height
        self.details = details

    def rule1(self):
        if self.height > 1 and self.T1S > 90 and self.black == 0:
            if self.S > 0:
                return True

    def rule2(self):
        if self.height > 1 and self.white > 40 and self.black == 0:
            if self.S > 0:
                return True

    def rule3(self):
        if self.height > 1 and self.S > 50:
            if self.T1S > self.score and self.black == 0:
                return True

    def rule4(self):
        if self.height > 1 and self.score > 75:
            if self.T1S > self.score and self.black == 0:
                if self.S > 0:
                    return True

    def rule5(self):
        if self.height == 1 and self.T1S - self.score > 10:
            if self.T1S > self.score and self.T1F > self.score:
                if self.black == 0 and self.white > 40:
                    if self.S > 0 and self.aj < 15:
                        return True

    def rule6(self):
        if self.height == 1 and self.score > 70:
            if self.T1S > self.score and self.T1F > self.score:
                if self.black == 0 and self.white > 25:
                    if self.S > 0 and self.aj < 15:
                        return True

    def rule7(self):
        if self.height == 1 and self.score > 50:
            if (self.T1S - self.score) > 20 and self.T1F > self.score:
                if self.white > 25 and self.black == 0:
                    if self.S > 0 and self.aj < 15:
                        return True

    def rule8(self):
        if self.height == 0 and self.score > 60:
            if (self.T1S - self.score) > 10 and self.T1F > self.score and self.T1F > 55:
                if self.black == 0 and self.white > 25:
                    if self.S > 0 and self.aj < 15:
                        return True

    def rule9(self):
        if self.height == 0 and self.score > 60:
            if (self.T1S - self.score) > 20 and self.T1F > self.score:
                if self.black == 0 and self.white > 25:
                    if not t_limit(self.stock, self.data, 1):
                        if not t_limit(self.stock, self.data, 2):
                            if self.aj < 15 and self.S > 0:
                                return True

    def rule10(self):
        if self.height < 2 and self.S > 30:
            if self.white > 25 and self.score > 60:
                if self.T1S > self.score and self.T1F > self.score:
                    if not t_limit(self.stock, self.data, 1):
                        if not t_limit(self.stock, self.data, 2):
                            if self.aj < 15 and self.black == 0:
                                return True

    def rule11(self):
        if self.height < 2 and self.S > 20:
            if self.white > 25 and self.black == 0:
                if self.T1S - self.score > 20 and self.T1F > self.score:
                    if not t_limit(self.stock, self.data, 1):
                        if not t_limit(self.stock, self.data, 2):
                            if self.aj < 15:
                                return True

    def rule12(self):
        if self.height > 1:
            if self.white > 35 and self.black == 0:
                return True

    def rule13(self):
        if self.height > 0 and self.black == 0:
            if self.white > 30:
                if 'A1' in self.details.keys():
                    if 1 in self.details['A1']:
                        return True

    def rule14(self):
        if self.height > 0 and self.black == 0:
            if self.white > 25:
                if 'A1' in self.details.keys():
                    if 2 in self.details['A1']:
                        return True

    def filter(self):
        if 'A1' not in self.details.keys():
            return False
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                return True
