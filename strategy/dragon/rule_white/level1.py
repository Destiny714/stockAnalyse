# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 21:30
# @Author  : Destiny_
# @File    : level1.py
# @Software: PyCharm
from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stockDetailModel import stockDetailModel


class level1(base_level):
    def __init__(self, stockDetail: stockDetailModel, data: list[dataModel], index: list[dataModel], limitData: dict[str, list[limitDataModel]]):
        self.level = '1'
        super().__init__(self.level, stockDetail, data, index, limitData)

    def rule1(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 31):
                if limit_height(stock, data, i) >= 3:
                    return False
            for i in range(30, 121):
                d = data[-i - 1]
                if not t_limit(stock, data, i):
                    continue
                afterData = [_ for _ in range(30, i) if data[-_ - 1].close() < d.low()]
                if len(afterData) <= 3:
                    return True
        except:
            pass

    def rule2(self):
        data = self.data
        for i in range(1, 4):
            if t_low_pct(data, i - 1) <= -0.03:
                return False
        return True

    def rule3(self):
        data = self.data
        for i in range(1, 11):
            high60 = max([_.high() for _ in data[-60 - i:-i]])
            if data[-i].close() <= high60:
                return False
        return True

    def rule4(self):
        data = self.data
        stock = self.stock
        if data[-1].pctChange() <= limit(stock):
            return False
        if data[-2].pctChange() > limit(stock):
            return False
        for _ in data[-61:-1]:
            if _.pctChange() > limit(stock):
                return True

    def rule5(self):
        data = self.data
        if data[-1].low() <= data[-2].low():
            return False
        if data[-2].low() > data[-3].low():
            return True

    def rule6(self):
        data = self.data
        for i in range(1, 4):
            high20 = max([_.turnover() for _ in data[-20 - i:-i]])
            if data[-i].turnover() > high20:
                return True

    def rule7(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 3):
            return False
        for i in range(1, 4):
            high30 = max([_.high() for _ in data[-30 - i:-i]])
            if data[-i].close() > high30:
                return True

    def rule8(self):
        data = self.data
        range5to20 = data[-21:-5]
        avgChangeRate = sum([(_.turnover()) for _ in range5to20]) / 16
        if avgChangeRate > 2.5:
            return True

    def rule9(self):
        data = self.data
        rangeData = data[-21:-10]
        volumeSum = sum([_.amount() for _ in rangeData])
        avgVolume = (volumeSum / 11) / 10
        if avgVolume > 50000:
            return True

    def rule10(self):
        data = self.data
        try:
            range3month = data[-90:]
            range3year = data[-660:]
            if max([_.turnover() for _ in range3month]) > sum([_.turnover() for _ in range3year]) / 660:
                return True
        except:
            return False
