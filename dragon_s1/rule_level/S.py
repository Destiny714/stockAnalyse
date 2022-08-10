# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : S.py
# @Software: PyCharm

def rule1(height: int, T1S: int, black: int, S: int):
    if height > 1 and T1S > 90 and black == 0:
        if S > 0:
            return True


def rule2(height: int, white: int, black: int, S: int):
    if height > 1 and white > 40 and black == 0:
        if S > 0:
            return True


def rule3(height: int, score: int, T1S: int, black: int, S: int):
    if height > 1 and S > 50:
        if T1S > score and black == 0:
            return True


def rule4(height: int, score: int, T1S: int, black: int, S: int):
    if height > 1 and score > 75:
        if T1S > score and black == 0:
            if S > 0:
                return True


def rule5(height: int, score: int, T1S: int, T1F: int, black: int, white: int, S: int):
    if height == 1 and score > 65:
        if T1S > 80 and T1F > 60:
            if black == 0 and white > 25:
                if S > 0:
                    return True


def rule6(height: int, score: int, T1S: int, T1F: int, black: int, white: int, S: int):
    if height == 1 and score > 70:
        if 60 < T1S < score and T1F > 55:
            if black == 0 and white > 25:
                if S > 0:
                    return True


def rule7(height: int, score: int, T1S: int, black: int, white: int, S: int):
    if height == 1 and score > 65:
        if (T1S - score) > 10 and black == 0:
            if white > 25 and S > 0:
                return True


def rule8(height: int, score: int, T1S: int, T1F: int, black: int, white: int, S: int):
    if height == 0 and score > 70:
        if 60 < T1S < score and T1F > 55:
            if black == 0 and white > 25:
                if S > 0:
                    return True


def rule9(height: int, score: int, T1S: int, black: int, white: int, t1isLimit: bool, S: int):
    if height == 0 and score > 65:
        if T1S > score and S > 0:
            if black == 0 and white > 25:
                if t1isLimit is False:
                    return True


def rule10(height: int, score: int, T1S: int, black: int, white: int, t1isLimit: bool, S: int):
    if height < 2 and S > 30:
        if white > 25 and score > 60:
            if T1S > score and black == 0:
                return not t1isLimit


def rule11(height: int, score: int, T1S: int, black: int, white: int, t1isLimit: bool, S: int):
    if height < 2 and S > 20:
        if white > 25 and T1S - score > 20:
            if black == 0:
                return not t1isLimit


def rule12(height: int, score: int, black: int, white: int):
    if height > 3 and score > 80:
        if white > 30 and black == 0:
            return True


class ruleS:

    def __init__(self, height: int, score: int, T1S: int, T1F: int, black: int, white: int, S: int, t1isLimit: bool):
        self.S = S
        self.T1S = T1S
        self.T1F = T1F
        self.black = black
        self.white = white
        self.score = score
        self.height = height
        self.t1isLimit = t1isLimit

    def filter(self):
        if rule1(self.height, self.T1S, self.black, self.S):
            return True
        if rule2(self.height, self.white, self.black, self.S):
            return True
        if rule3(self.height, self.score, self.T1S, self.black, self.S):
            return True
        if rule4(self.height, self.score, self.T1S, self.black, self.S):
            return True
        if rule5(self.height, self.score, self.T1S, self.T1F, self.black, self.white, self.S):
            return True
        if rule6(self.height, self.score, self.T1S, self.T1F, self.black, self.white, self.S):
            return True
        if rule7(self.height, self.score, self.T1S, self.black, self.white, self.S):
            return True
        if rule8(self.height, self.score, self.T1S, self.T1F, self.black, self.white, self.S):
            return True
        if rule9(self.height, self.score, self.T1S, self.black, self.white, self.t1isLimit, self.S):
            return True
        if rule10(self.height, self.score, self.T1S, self.black, self.white, self.t1isLimit, self.S):
            return True
        if rule11(self.height, self.score, self.T1S, self.black, self.white, self.t1isLimit, self.S):
            return True
        if rule12(self.height, self.score, self.black, self.white):
            return True
