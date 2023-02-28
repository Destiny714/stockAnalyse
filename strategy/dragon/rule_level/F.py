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
        return True
