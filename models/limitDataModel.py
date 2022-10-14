# -*- coding: utf-8 -*-
# @Time    : 2022/9/18 00:20
# @Author  : Destiny_
# @File    : limitDataModel.py
# @Software: PyCharm


class limitDataModel:
    """stockLimit表 序列化"""

    def __init__(self, data):
        self.data = data

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]

    @property
    def date(self):
        return self.data[1]

    @property
    def stock(self):
        return self.data[2]

    @property
    def industry(self):
        return self.data[3]

    @property
    def open(self):
        return self.data[4]

    @property
    def close(self):
        return self.data[5]

    @property
    def preClose(self):
        return self.data[6]

    @property
    def pctChange(self):
        return self.data[7]

    def amount(self):
        return self.data[8]

    @property
    def turnover(self):
        return self.data[9]

    def fdAmount(self):
        return self.data[10]

    @property
    def firstLimitTime(self):
        return self.data[11]

    @property
    def lastLimitTime(self):
        return self.data[12]

    @property
    def limitOpenTime(self):
        return self.data[13]

    @property
    def upStat(self):
        return self.data[14]

    @property
    def limitHeight(self):
        return self.data[15]
