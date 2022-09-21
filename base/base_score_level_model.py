# -*- coding: utf-8 -*-
# @Time    : 2022/9/20 00:01
# @Author  : Destiny_
# @File    : base_score_level_model.py
# @Software: PyCharm


class base_score_level(object):
    def __init__(self, level: str, scoreLevelData: dict):
        assert {'S', 'aj', 'T1S', 'T1F', 'data', 'black', 'white', 'stock', 'score', 'height', 'details', 'b1', 'b2'} <= set(
            scoreLevelData.keys()), '评级数据缺失'
        self.level = level
        self.S = scoreLevelData['S']
        self.b1 = scoreLevelData['b1']
        self.b2 = scoreLevelData['b2']
        self.aj = scoreLevelData['aj']
        self.T1S = scoreLevelData['T1S']
        self.T1F = scoreLevelData['T1F']
        self.data = scoreLevelData['data']
        self.black = scoreLevelData['black']
        self.white = scoreLevelData['white']
        self.stock = scoreLevelData['stock']
        self.score = scoreLevelData['score']
        self.height = scoreLevelData['height']
        self.details = scoreLevelData['details']

    def filter(self):
        if self.level in ['A', 'S'] and 'A1' not in self.details.keys():
            return False
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                return True