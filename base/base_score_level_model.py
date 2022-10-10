# -*- coding: utf-8 -*-
# @Time    : 2022/9/20 00:01
# @Author  : Destiny_
# @File    : base_score_level_model.py
# @Software: PyCharm

from prefs.params import *


class base_score_level(object):
    def __init__(self, level: str, scoreLevelData: dict):
        assert {'S', 'AJ', 'T1S', 'T1F', 'data', 'black', 'white', 'stock', 'score', 'height', 'details', 'b1', 'b2', 'CF', 'TF', 'TP'} <= set(
            scoreLevelData.keys()), '评级数据缺失'
        self.level = level
        self.S = scoreLevelData['S']
        self.b1 = scoreLevelData['b1']
        self.b2 = scoreLevelData['b2']
        self.CF = scoreLevelData['CF']
        self.TF = scoreLevelData['TF']
        self.TP = scoreLevelData['TP']
        self.AJ = scoreLevelData['AJ']
        self.T1S = scoreLevelData['T1S']
        self.T1F = scoreLevelData['T1F']
        self.data = scoreLevelData['data']
        self.black = scoreLevelData['black']
        self.white = scoreLevelData['white']
        self.stock = scoreLevelData['stock']
        self.score = scoreLevelData['score']
        self.height = scoreLevelData['height']
        self.details = scoreLevelData['details']
        if level not in scoreRuleDict.keys():
            scoreRuleDict[level] = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]

    def filter(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                return True
