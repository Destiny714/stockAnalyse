# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : A.py
# @Software: PyCharm


def rule1(height: int, score: int, black: int):
    if height > 1 and 10 < score / height < 15:
        if black < 3:
            return True


def rule2(height: int, score: int, T1S: int, T1F: int, black: int):
    if height > 1 and score > 50:
        if T1S / height > 12 and 8 < T1F / height < 10:
            if black < 3:
                return True


def rule3(height: int, score: int, T1S: int, T1F: int):
    if height > 1 and 10 < score / height < 15:
        if T1S > score and T1F > score:
            return True


def rule4(height: int, score: int, T1S: int, T1F: int):
    if height > 1 and score / height > 15:
        if T1S / height > 12 and (10 < T1F / height < 12):
            return True


def rule5(height: int, score: int, T1S: int, T1F: int, black: int):
    if height == 1 and score > 25:
        if T1S > 25 and T1F > 25:
            if black < 2:
                return True


def rule6(height: int, score: int, T1S: int, T1F: int, black: int):
    if height == 0 and score > 25:
        if T1S > 25 and T1F > 25:
            if black < 2:
                return True


def rule7(height: int, T1S: int, T1F: int, black: int):
    if height == 0 and black < 2:
        if T1S > 30 and T1F > 30:
            return True


class ruleA:

    def __init__(self, height: int, score: int, T1S: int, T1F: int, black: int):
        self.height = height
        self.score = score
        self.T1S = T1S
        self.T1F = T1F
        self.black = black

    def filter(self):
        if rule1(self.height, self.score, self.black):
            return True
        if rule2(self.height, self.score, self.T1S, self.T1F, self.black):
            return True
        if rule3(self.height, self.score, self.T1S, self.T1F):
            return True
        if rule4(self.height, self.score, self.T1S, self.T1F):
            return True
        if rule5(self.height, self.score, self.T1S, self.T1F, self.black):
            return True
        if rule6(self.height, self.score, self.T1S, self.T1F, self.black):
            return True
        if rule7(self.height, self.T1S, self.T1F, self.black):
            return True
