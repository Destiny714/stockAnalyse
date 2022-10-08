# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : S.py
# @Software: PyCharm
from base.base_score_level_model import base_score_level
from utils.stockdata_util import t_limit


class ruleS(base_score_level):

    def __init__(self, scoreLevelData: dict):
        self.level = 'S'
        super().__init__(self.level, scoreLevelData)

    def rule1(self):
        if self.height > 1 and self.T1S > 90 and self.black == 0:
            if self.b1 == 0 and self.b2 < 2:
                if self.S > 0:
                    return True

    def rule2(self):
        if self.height > 1 and self.white > 40 and self.black == 0:
            if self.S > 0:
                if self.b1 == 0 and self.b2 < 2:
                    return True

    def rule3(self):
        if self.height > 1 and self.S > 50:
            if self.T1S > self.score and self.black == 0:
                if self.b1 == 0 and self.b2 < 2:
                    return True

    def rule4(self):
        if self.height > 1 and self.score > 75:
            if self.T1S > self.score and self.black == 0:
                if self.S > 0:
                    if self.b1 == 0 and self.b2 < 2:
                        return True

    def rule5(self):
        if self.height == 1 and self.T1S - self.score > 10:
            if self.T1S > self.score and self.T1F > self.score:
                if self.black == 0 and self.white > 40:
                    if self.S > 0 and self.AJ < 15:
                        if self.b1 == 0 and self.b2 < 2:
                            return True

    def rule6(self):
        if self.height == 1 and self.score > 70:
            if self.T1S > self.score and self.T1F > self.score:
                if self.black == 0 and self.white > 25:
                    if self.S > 0 and self.AJ < 15:
                        if self.b1 == 0 and self.b2 < 2:
                            return True

    def rule7(self):
        if self.height == 1 and self.score > 50:
            if (self.T1S - self.score) > 20 and self.T1F > self.score:
                if self.white > 25 and self.black == 0:
                    if self.S > 0 and self.AJ < 15:
                        if self.b1 == 0 and self.b2 < 2:
                            return True

    def rule8(self):
        if self.height == 0 and self.score > 60:
            if (self.T1S - self.score) > 10 and self.T1F > self.score and self.T1F > 55:
                if self.black == 0 and self.white > 25:
                    if self.S > 0 and self.AJ < 15:
                        if self.b1 == 0 and self.b2 < 2:
                            return True

    def rule9(self):
        if self.height == 0 and self.score > 60:
            if (self.T1S - self.score) > 20 and self.T1F > self.score:
                if self.black == 0 and self.white > 25:
                    if not t_limit(self.stock, self.data, 1):
                        if not t_limit(self.stock, self.data, 2):
                            if self.AJ < 15 and self.S > 0:
                                if self.b1 == 0 and self.b2 < 2:
                                    return True

    def rule10(self):
        if self.height < 2 and self.S > 30:
            if self.white > 25 and self.score > 60:
                if self.T1S > self.score and self.T1F > self.score:
                    if not t_limit(self.stock, self.data, 1):
                        if not t_limit(self.stock, self.data, 2):
                            if self.AJ < 15 and self.black == 0:
                                if self.b1 == 0 and self.b2 < 2:
                                    return True

    def rule11(self):
        if self.height < 2 and self.S > 20:
            if self.white > 25 and self.black == 0:
                if self.T1S - self.score > 20 and self.T1F > self.score:
                    if not t_limit(self.stock, self.data, 1):
                        if not t_limit(self.stock, self.data, 2):
                            if self.AJ < 15:
                                if self.b1 == 0 and self.b2 < 2:
                                    return True

    def rule12(self):
        if self.height > 1:
            if self.white > 35 and self.black == 0:
                if self.b1 == 0 and self.b2 < 2:
                    return True

    def rule13(self):
        if self.height > 0 and self.black == 0:
            if self.white > 30:
                if 'A1' in self.details.keys():
                    if 1 in self.details['A1']:
                        if self.b1 == 0 and self.b2 < 2:
                            return True

    def rule14(self):
        if self.height > 0 and self.black == 0:
            if self.white > 25:
                if 'A1' in self.details.keys():
                    if 2 in self.details['A1']:
                        if self.b1 == 0 and self.b2 < 2:
                            return True
