# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 18:20
# @Author  : Destiny_
# @File    : A.py
# @Software: PyCharm
from typing import List

from common.collect_data import dataModel, t_limit


def rule1(height: int, T1S: int, black: int):
    if height > 1 and T1S > 80:
        if black < 2:
            return True


def rule2(height: int, white: int, black: int):
    if height > 1 and white > 30:
        if black < 2:
            return True


def rule3(height: int, T1S: int, black: int, S: int):
    if height > 1 and S > 40:
        if T1S > 80 and black < 2:
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
        if T1S - score > 10 and black == 0:
            if white > 20:
                return True


def rule8(height: int, score: int, T1S: int, T1F: int, black: int, white: int, aj: float):
    if height == 0 and score > 60:
        if 50 < T1S < score and T1F > 40:
            if black < 2 and white > 20:
                if aj < 20:
                    return True


def rule9(height: int, score: int, T1S: int, T1F: int, black: int, white: int, data: List[dataModel], stock: str,
          aj: float):
    if height == 0 and score > 50:
        if T1S > score and T1F > 40:
            if black == 0 and white > 20:
                if not t_limit(stock, data, 1):
                    if not t_limit(stock, data, 2):
                        if aj < 20:
                            return True


def rule10(height: int, score: int, T1S: int, black: int, white: int, data: List[dataModel], S: int, stock: str,
           aj: float):
    if height < 2 and S > 30:
        if white > 20 and score > 50:
            if T1S > score and black < 2:
                if not t_limit(stock, data, 1):
                    if not t_limit(stock, data, 2):
                        if aj < 20:
                            return True


def rule11(height: int, score: int, T1S: int, black: int, white: int, data: List[dataModel], S: int, stock: str,
           aj: float):
    if height < 2 and S > 20:
        if white > 20 and T1S - score > 10:
            if black < 2:
                if not t_limit(stock, data, 1):
                    if not t_limit(stock, data, 2):
                        if aj < 20:
                            return True


def rule12(height: int, score: int, black: int, white: int):
    if height > 3 and score > 70:
        if white > 25 and black < 2:
            return True


class ruleA:

    def __init__(self, height: int, score: int, T1S: int, T1F: int, black: int, white: int, S: int,
                 data: List[dataModel], stock: str, aj: float):
        self.S = S
        self.aj = aj
        self.T1S = T1S
        self.T1F = T1F
        self.data = data
        self.stock = stock
        self.black = black
        self.white = white
        self.score = score
        self.height = height

    def filter(self):
        if rule1(self.height, self.T1S, self.black):
            return True
        if rule2(self.height, self.white, self.black):
            return True
        if rule3(self.height, self.T1S, self.black, self.S):
            return True
        if rule4(self.height, self.score, self.T1S, self.black):
            return True
        if rule5(self.height, self.score, self.T1S, self.T1F, self.black, self.white):
            return True
        if rule6(self.height, self.score, self.T1S, self.T1F, self.black, self.white):
            return True
        if rule7(self.height, self.score, self.T1S, self.black, self.white):
            return True
        if rule8(self.height, self.score, self.T1S, self.T1F, self.black, self.white, self.aj):
            return True
        if rule9(self.height, self.score, self.T1S, self.T1F, self.black, self.white, self.data, self.stock, self.aj):
            return True
        if rule10(self.height, self.score, self.T1S, self.black, self.white, self.data, self.S, self.stock, self.aj):
            return True
        if rule11(self.height, self.score, self.T1S, self.black, self.white, self.data, self.S, self.stock, self.aj):
            return True
        if rule12(self.height, self.score, self.black, self.white):
            return True
