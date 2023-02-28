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
        return True
