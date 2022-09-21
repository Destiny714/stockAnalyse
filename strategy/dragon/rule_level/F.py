# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : F.py
# @Software: PyCharm

from base.base_score_level_model import base_score_level


class ruleF(base_score_level):

    def __init__(self, scoreLevelData: dict):
        self.level = 'F'
        super().__init__(self.level, scoreLevelData)

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
