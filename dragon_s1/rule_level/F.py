# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : F.py
# @Software: PyCharm

def rule1(height: int, score: int):
    if height > 1 and score < 0:
        return True


def rule2(height: int, score: int, T1S: int, black: int):
    if height > 1 and T1S < score:
        if black > 4:
            return True


def rule3(height: int, S: int, black: int):
    if height > 0 and S < -30:
        if black > 3:
            return True


def rule4(height: int, black: int):
    if height > 0 and black > 4:
        return True


def rule5(height: int, black: int):
    if height < 2 and black > 2:
        return True


def rule6(white: int, black: int):
    if white < 30 and black > 4:
        return True


def rule7(score: int, T1S: int, black: int):
    if score - T1S > 20 and black > 1:
        if score < 60:
            return True


class ruleF:

    def __init__(self, height: int, score: int, T1S: int, T1F: int, white: int, black: int, S: int):
        self.S = S
        self.height = height
        self.score = score
        self.T1S = T1S
        self.T1F = T1F
        self.white = white
        self.black = black

    def filter(self):
        if rule1(self.height, self.score):
            return True
        if rule2(self.height, self.score, self.T1S, self.black):
            return True
        if rule3(self.height, self.S, self.black):
            return True
        if rule4(self.height, self.black):
            return True
        if rule5(self.height, self.black):
            return True
        if rule6(self.white, self.black):
            return True
        if rule7(self.score, self.T1S, self.black):
            return True
