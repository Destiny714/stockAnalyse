# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : S.py
# @Software: PyCharm

def rule1(height: int, score: int, T1S: int, T1F: int, black: int):
    if height > 1 and score / height > 15:
        if T1S > score and T1F / height > 12:
            if black == 0:
                return True


def rule2(height: int, score: int, T1S: int, black: int):
    if height > 1 and score / height > 12:
        if T1S > score and black == 0:
            return True


def rule3(height: int, score: int, T1S: int, black: int):
    if height > 1 and score / height > 12:
        if T1S * 0.8 < score < T1S:
            if black == 0:
                return True


def rule4(height: int, score: int, T1S: int, T1F: int, black: int):
    if height > 1 and score / height > 12:
        if T1S / height > 10 and T1F / height > 8:
            if black == 0:
                return True


def rule5(height: int, score: int, T1S: int, black: int):
    if height > 1 and 10 < score / height < 12:
        if T1S > score and black == 0:
            return True


def rule6(height: int, score: int, T1S: int, T1F: int, black: int):
    if height > 1 and score > 50:
        if T1S / height > 10 and T1F / height > 8:
            if black == 0:
                return True


def rule7(height: int, score: int, T1S: int, T1F: int, black: int):
    if height == 1 and score > 25:
        if T1S > 25 and T1F > 20:
            if black == 0:
                return True


def rule8(height: int, score: int, T1S: int, T1F: int, black: int):
    if height == 1 and score > 30:
        if 20 < T1S < score and T1F > 20:
            if black == 0:
                return True


def rule9(height: int, score: int, T1S: int, T1F: int, black: int):
    if height == 0 and score > 30:
        if 20 < T1S < score and T1F > 20:
            if black == 0:
                return True


def rule10(height: int, score: int, T1S: int, T1F: int, black: int):
    if height == 0 and score > 25:
        if T1S > 25 and T1F > 20:
            if black == 0:
                return True


class ruleS:

    def __init__(self, height: int, score: int, T1S: int, T1F: int, black: int):
        self.height = height
        self.score = score
        self.T1S = T1S
        self.T1F = T1F
        self.black = black

    def filter(self):
        if rule1(self.height, self.score, self.T1S, self.T1F, self.black):
            return True
        if rule2(self.height, self.score, self.T1S, self.black):
            return True
        if rule3(self.height, self.score, self.T1S, self.black):
            return True
        if rule4(self.height, self.score, self.T1S, self.T1F, self.black):
            return True
        if rule5(self.height, self.score, self.T1S, self.black):
            return True
        if rule6(self.height, self.score, self.T1S, self.T1F, self.black):
            return True
        if rule7(self.height, self.score, self.T1S, self.T1F, self.black):
            return True
        if rule8(self.height, self.score, self.T1S, self.T1F, self.black):
            return True
        if rule9(self.height, self.score, self.T1S, self.T1F, self.black):
            return True
        if rule10(self.height, self.score, self.T1S, self.T1F, self.black):
            return True
