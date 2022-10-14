# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 21:30
# @Author  : Destiny_
# @File    : level1.py
# @Software: PyCharm
from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stockDetailModel import stockDetailModel


class level1(base_level):
    def __init__(self, stockDetail: stockDetailModel, data: list[dataModel], gemIndex: list[dataModel], shIndex: list[dataModel],
                 limitData: dict[str, list[limitDataModel]]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex, limitData)

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
                afterData = [_ for _ in range(30, i) if data[-_ - 1].close < d.low]
                if len(afterData) <= 3:
                    return True
        except:
            pass

    def rule2(self):
        data = self.data
        for i in range(3):
            if t_low_pct(data, i) / (1 + t_close_pct(self.shIndex, i) * 10) <= -0.03:
                return False
        return True

    def rule3(self):
        data = self.data
        for i in range(1, 11):
            high60 = max([_.high for _ in data[-60 - i:-i]])
            if data[-i].close <= high60:
                return False
        return True

    def rule4(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data):
                return False
            if t_limit(stock, data, 1):
                return False
            for i in range(60):
                if t_limit(stock, data, i):
                    return True
        except:
            pass

    def rule5(self):
        data = self.data
        if t_limit(self.stock, data, 1):
            return False
        if data[-1].low <= data[-2].low:
            return False
        if data[-2].low > data[-3].low:
            return True

    def rule6(self):
        data = self.data
        try:
            for i in range(1, 21):
                prev120 = data[-i - 1 - 120:-i - 1]
                if data[-i - 1].volume > max([_.volume for _ in prev120]):
                    return True
        except:
            pass

    def rule7(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 3):
            return False
        for i in range(1, 4):
            high30 = max([_.high for _ in data[-30 - i:-i]])
            if data[-i].close > high30:
                return True

    def rule8(self):
        data = self.data
        range5to20 = data[-21:-5]
        avgChangeRate = sum([_.turnover for _ in range5to20]) / 16
        if 2.5 < avgChangeRate < 5:
            return True

    def rule9(self):
        data = self.data
        rangeData = data[-21:-10]
        avgAmount = 1000 * sum([_.amount for _ in rangeData]) / 11
        if 5 * 1e7 < avgAmount < 2 * 1e8:
            return True

    def rule10(self):
        data = self.data
        try:
            range3month = data[-90:]
            range3year = data[-660:]
            if sum([_.volume for _ in range3month]) / 90 > sum([_.volume for _ in range3year]) / 660:
                return True
        except:
            return False
