# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : A.py
# @Software: PyCharm


def rule1(height: int, T1S: int, black: int):
    if height > 1 and T1S > 80:
        if black < 2:
            return True


def rule2(height: int, white: int, black: int):
    if height > 1 and white > 30:
        if black < 2:
            return True


def rule3(height: int, score: int, T1S: int, black: int, S: int):
    if height > 1 and S > 40:
        if T1S > score and black < 2:
            return True


def rule4(height: int, score: int, T1S: int, black: int):
    if height > 1 and score > 65:
        if T1S > score and black < 2:
            return True


def rule5(height: int, score: int, T1S: int, T1F: int, black: int, white: int):
    if height == 1 and score > 55:
        if T1S > 70 and T1F > 45:
            if black == 0 and white > 20:
                return True


def rule6(height: int, score: int, T1S: int, T1F: int, black: int, white: int):
    if height == 1 and score > 60:
        if 50 < T1S < score and T1F > 40:
            if black < 2 and white > 20:
                return True


def rule7(height: int, score: int, T1S: int, black: int, white: int):
    if height == 1 and score > 55:
        if T1S > score and black == 0:
            if white > 20:
                return True


def rule8(height: int, score: int, T1S: int, T1F: int, black: int, white: int):
    if height == 0 and score > 60:
        if 50 < T1S < score and T1F > 40:
            if black < 2 and white > 20:
                return True


def rule9(height: int, score: int, T1S: int, T1F: int, black: int, white: int, t1isLimit: bool):
    if height == 0 and score > 55:
        if T1S > score and T1F > 45:
            if black == 0 and white > 20:
                if t1isLimit is False:
                    return True


class ruleA:

    def __init__(self, height: int, score: int, T1S: int, T1F: int, black: int, white: int, S: int, t1isLimit: bool):
        self.S = S
        self.height = height
        self.score = score
        self.T1S = T1S
        self.T1F = T1F
        self.black = black
        self.white = white
        self.t1isLimit = t1isLimit

    def filter(self):
        if rule1(self.height, self.T1S, self.black):
            return True
        if rule2(self.height, self.white, self.black):
            return True
        if rule3(self.height, self.score, self.T1S, self.black, self.S):
            return True
        if rule4(self.height, self.score, self.T1S, self.black):
            return True
        if rule5(self.height, self.score, self.T1S, self.T1F, self.black, self.white):
            return True
        if rule6(self.height, self.score, self.T1S, self.T1F, self.black, self.white):
            return True
        if rule7(self.height, self.score, self.T1S, self.black, self.white):
            return True
        if rule8(self.height, self.score, self.T1S, self.T1F, self.black, self.white):
            return True
        if rule9(self.height, self.score, self.T1S, self.T1F, self.black, self.white, self.t1isLimit):
            return True
