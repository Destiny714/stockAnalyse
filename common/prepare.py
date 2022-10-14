# -*- coding: utf-8 -*-
# @Time    : 2022/10/11 23:49
# @Author  : Destiny_
# @File    : prepare.py
# @Software: PyCharm


class Prepare(object):
    def __init__(self, stocks: list[str], aimDates: list[str]):
        self.stocks = stocks
        self.aimDates = aimDates

    def do(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'pre' in _]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                return True
