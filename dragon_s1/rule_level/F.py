# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : F.py
# @Software: PyCharm

def rule1(score: int):
    if score < 0:
        return True


def rule2(height: int, score: int, T1S: int, T1F: int):
    if height > 0 and score / height < 12:
        if T1S / height < 10 and T1F / height < 8:
            return True


def rule3(height: int, score: int, black: int):
    if height > 0 and score / height < 12:
        if black > 5:
            return True


def rule4(score: int, black: int):
    if score < 40 and black > 6:
        return True


class ruleF:

    def __init__(self, height: int, score: int, T1S: int, T1F: int, black: int):
        self.height = height
        self.score = score
        self.T1S = T1S
        self.T1F = T1F
        self.black = black

    def filter(self):
        if rule1(self.score):
            return True
        if rule2(self.height, self.score, self.T1S, self.T1F):
            return True
        if rule3(self.height, self.score, self.black):
            return True
        if rule4(self.score, self.black):
            return True
