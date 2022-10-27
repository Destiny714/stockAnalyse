# -*- coding: utf-8 -*-
# @Time    : 2022/10/11 23:49
# @Author  : Destiny_
# @File    : prepare.py
# @Software: PyCharm
import tushare

from api import config


class Prepare(object):
    def __init__(self, stocks: list[str] = None, aimDates: list[str] = None):
        self.stocks = stocks
        self.aimDates = aimDates

    def preTushare(self):
        token = config['tushareKey']
        tushare.set_token(token)
        print('tushare registered')

    def do(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'pre' in _]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                return True
