# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : A.py
# @Software: PyCharm
from base.base_score_level_model import base_score_level
from utils.stockdata_util import t_limit


class ruleA(base_score_level):

    def __init__(self, scoreLevelData: dict):
        self.level = 'A'
        super().__init__(self.level, scoreLevelData)

    def rule1(self):
        return True
