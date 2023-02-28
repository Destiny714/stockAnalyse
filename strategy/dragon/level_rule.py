# -*- coding: utf-8 -*-
# @Time    : 2023/2/23 23:06
# @Author  : Destiny_
# @File    : level_rule.py
# @Software: PyCharm


class LevelRule(object):
    def __init__(self, params: dict):
        self.ks = []
        assert set(params.keys()) >= {'black', 'white', 'score', 'CF', 'TF', 'CP', 'TP', 'AJ', 'is1', 'height', 'day3elg'}, '评级数据缺失'
        self.CF: float = params['CF']
        self.TF: float = params['TF']
        self.CP: float = params['CP']
        self.TP: float = params['TP']
        self.AJ: float = params['AJ']
        self.is1: bool = params['is1']
        self.height = params['height']
        self.black: int = params['black']
        self.white: int = params['white']
        self.score: int = params['score']
        self.day3elg: float = params['day3elg']

    def k1(self):
        return self.white > 30

    def k2(self):
        return self.black == 0

    def k3(self):
        return self.CF > 50

    def k4(self):
        return self.TF > 80

    def k5(self):
        return self.CP > (65 if not self.is1 else 99)

    def k6(self):
        return self.TP > (40 if not self.is1 else 95)

    def k7(self):
        return self.score > 60

    def k8(self):
        return self.day3elg > 70

    def k9(self):
        return self.AJ < 0.11

    def filter(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if _.startswith('k')]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                self.ks.append(rule)

    def limitRank(self) -> str:
        if self.height < 3 and self.black < 2:
            if 8 <= len(self.ks) <= 9:
                return 'S'
            if 6 <= len(self.ks) <= 7:
                return 'A'
            if 4 <= len(self.ks) <= 5:
                return 'B'
            if 0 <= len(self.ks) <= 3:
                return 'F'
        elif self.height < 3 and self.black >= 2:
            if self.CP > (65 if not self.is1 else 90) and self.TP > (40 if not self.is1 else 95) and self.day3elg > 60:
                return 'B'
            else:
                return 'F'
        elif self.height >= 3 and self.black < 2:
            if self.CP > (60 if not self.is1 else 80):
                if self.day3elg > 60:
                    return 'A'
                elif 50 <= self.day3elg <= 60:
                    return 'B'
                else:
                    return 'F'
            else:
                return 'F'
        elif self.height >= 3 and self.black >= 2:
            if self.CP > (60 if not self.is1 else 90):
                if self.day3elg > 70:
                    return 'A'
                elif 60 <= self.day3elg <= 70:
                    return 'B'
                else:
                    return 'F'
            else:
                return 'F'
