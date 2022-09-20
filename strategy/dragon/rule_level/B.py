# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : B.py
# @Software: PyCharm
from models.initDataModel import dataModel


class ruleB:

    def __init__(self, height: int, black: int, b1: int, b2: int, details: dict[str, list[int]]):
        self.b1 = b1
        self.b2 = b2
        self.black = black
        self.height = height
        self.details = details

    def rule1(self):
        if self.height > 1:
            if self.black - self.b1 > 3:
                if self.b1 < 3 and self.b2 < 4:
                    return True

    def rule2(self):
        if self.height > 0 and self.black > 4:
            if self.b1 < 3:
                if 'A1' in self.details.keys():
                    if 1 in self.details['A1']:
                        return True

    def filter(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                return True
