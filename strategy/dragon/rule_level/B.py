# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : B.py
# @Software: PyCharm

from prefs.params import *
from base.base_score_level_model import base_score_level


class ruleB(base_score_level):

    def __init__(self, scoreLevelData: dict):
        self.level = 'B'
        super().__init__(self.level, scoreLevelData)

    def rule1(self):
        if self.height > 0:
            if self.black - self.b1 > 4:
                return self.b1 < 2

    def rule2(self):
        if self.height > 0 and self.black > 4:
            if self.b1 < 3:
                if 'A1' in self.details.keys():
                    if 1 in self.details['A1']:
                        return True

    def rule3(self):
        if self.height > 1 and self.black > 4:
            if 'A1' in self.details.keys():
                if len(self.details['A1']) == len(Params.levelRuleDict['A1']):
                    return True

    def rule4(self):
        if self.height > 1 and self.black > 4:
            if 'A1' in self.details.keys():
                if {1, 2, 3, 4, 9} <= set(self.details['A1']):
                    return True
