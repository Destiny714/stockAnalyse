# -*- coding: utf-8 -*-
# @Time    : 2022/10/14 21:40
# @Author  : Destiny_
# @File    : column_model.py
# @Software: PyCharm


class ColumnModel(object):
    placeholder = 'N/A'
    __cols__ = [
        '回测日期', '当日上证指数收盘价涨幅', '当日评级', '当日评级股票名称', '当日连板height值', '当日+1上证指数收盘价涨幅', '当日+1开盘价涨幅', '当日+1最高价涨幅',
        '当日+1最低价涨幅', '当日+1收盘价涨幅', '当日+1是否涨停', '当日+2上证指数收盘价涨幅', '当日+2开盘价涨幅', '当日+2最高价涨幅', '当日+2最低价涨幅',
        '当日+2收盘价涨幅', '当日+2是否涨停', '当日+3上证指数收盘价涨幅', '当日+3开盘价涨幅', '当日+3最高价涨幅', '当日+3最低价涨幅', '当日+3收盘价涨幅', '当日+3是否涨停'
    ]

    def __init__(self, resultDict=None):
        if resultDict is None:
            resultDict = {}
        self.backTraceDate = self.placeholder
        self.shIndexClosePCT_0 = self.placeholder
        self.level = self.placeholder
        self.name = self.placeholder
        self.height = self.placeholder
        self.shIndexClosePCT_1 = self.placeholder
        self.openPCT_1 = self.placeholder
        self.highPCT_1 = self.placeholder
        self.lowPCT_1 = self.placeholder
        self.closePCT_1 = self.placeholder
        self.isLimit_1 = self.placeholder
        self.shIndexClosePCT_2 = self.placeholder
        self.openPCT_2 = self.placeholder
        self.highPCT_2 = self.placeholder
        self.lowPCT_2 = self.placeholder
        self.closePCT_2 = self.placeholder
        self.isLimit_2 = self.placeholder
        self.shIndexClosePCT_3 = self.placeholder
        self.openPCT_3 = self.placeholder
        self.highPCT_3 = self.placeholder
        self.lowPCT_3 = self.placeholder
        self.closePCT_3 = self.placeholder
        self.isLimit_3 = self.placeholder
        for key in resultDict.keys():
            if key in self.__dict__.keys():
                self.__dict__[key] = resultDict[key]
