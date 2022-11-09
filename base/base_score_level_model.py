# -*- coding: utf-8 -*-
# @Time    : 2022/9/20 00:01
# @Author  : Destiny_
# @File    : base_score_level_model.py
# @Software: PyCharm

from prefs.params import *
from models.stock_data_model import StockDataModel


class base_score_level(object):
    def __init__(self, level: str, scoreLevelData: dict):
        assert {'S', 'AJ', 'T1S', 'T1F', 'data', 'black', 'white', 'stock', 'score', 'height', 'details', 'b1', 'b2', 'CF', 'TF', 'TP'} <= set(
            scoreLevelData.keys()), '评级数据缺失'
        self.level: str = level
        self.S: int = scoreLevelData['S']
        self.b1: int = scoreLevelData['b1']
        self.b2: int = scoreLevelData['b2']
        self.CF: float = scoreLevelData['CF']
        self.TF: float = scoreLevelData['TF']
        self.TP: float = scoreLevelData['TP']
        self.AJ: float = scoreLevelData['AJ']
        self.T1S: int = scoreLevelData['T1S']
        self.T1F: int = scoreLevelData['T1F']
        self.data: list[StockDataModel] = scoreLevelData['data']
        self.black: int = scoreLevelData['black']
        self.white: int = scoreLevelData['white']
        self.stock: str = scoreLevelData['stock']
        self.score: int = scoreLevelData['score']
        self.height: int = scoreLevelData['height']
        self.details: dict = scoreLevelData['details']
        if level not in Params.scoreRuleDict.keys():
            Params.scoreRuleDict[level] = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]

    def filter(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                return True
