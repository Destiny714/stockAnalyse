# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : F.py
# @Software: PyCharm

class ruleF:

    def __init__(self, height: int, score: int, T1S: int, T1F: int, white: int, black: int, S: int, details: dict[str, list[int]]):
        self.S = S
        self.T1S = T1S
        self.T1F = T1F
        self.white = white
        self.black = black
        self.score = score
        self.height = height
        self.details = details

    def rule1(self):
        if self.height > 1 and self.score < 0:
            return True

    def rule2(self):
        if self.height > 1 and self.T1S < self.score:
            if self.black > 4:
                return True

    def rule3(self):
        if self.height > 0 and self.S < -30:
            if self.black > 4:
                return True

    def rule4(self):
        if self.height > 0 and self.black > 4:
            return True

    def rule5(self):
        if self.height < 2 and self.black > 3:
            return True

    def rule6(self):
        if self.white < 30 and self.black > 4:
            return True

    def rule7(self):
        if self.score - self.T1S > 20 and self.black > 1:
            if self.score < 60:
                return True

    def rule8(self):
        if self.height > 0:
            if self.score / self.height < 15 and self.T1S / self.height < 15:
                return True

    def rule9(self):
        if 'F5' in self.details.keys():
            if len(self.details['F5']) >= 4:
                return True

    def rule10(self):
        if self.height > 1 and self.score > self.T1S:
            for _ in ['A1', 'A2', 'S1', 'S2']:
                if _ in self.details.keys():
                    return False
            return True

    def filter(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                return True
