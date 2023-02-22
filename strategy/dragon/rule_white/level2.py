# -*- coding: utf-8 -*-
# @Time    : 2022/6/21 00:05
# @Author  : Destiny_
# @File    : level2.py
# @Software: PyCharm

from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class level2(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel],
                 limitData: dict[str, list[LimitDataModel]]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex, limitData)

    def rule1(self):
        data = self.data
        range5 = data[-5:]
        range6to10 = data[-10:-5]
        if sum([_.turnover for _ in range5]) > 2 * sum([_.turnover for _ in range6to10]):
            return True

    def rule2(self):
        data = self.data
        try:
            range60 = data[-60:]
            range220 = data[-220:]
            if max([_.turnover for _ in range60]) > 5 * sum([_.turnover for _ in range220]) / 220:
                return True
        except:
            return False

    def rule3(self):
        if self.stock[:3] in ['002', '000']:
            return True

    def rule4(self):
        data = self.data
        stock = self.stock
        if not model_1(stock, data):
            return False
        return data[-1].turnover < data[-2].turnover / 10

    def rule5(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 4):
                if not data[-i - 1].close > move_avg(data, 60, i):
                    return False
            return True
        except:
            ...

    def rule6(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 1):
            return False
        if data[-1].limitOpenTime != 0:
            return False
        return data[-1].TP > 45 and getMinute(stamp=data[-1].firstLimitTime) > '0937'

    def rule7(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        return getMinute(stamp=data[-2].firstLimitTime) > '1100' and getMinute(stamp=data[-1].lastLimitTime) < '1015'

    def rule8(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 11):
                if i in range(1, 6):
                    if not (move_avg(data, 10, i) > move_avg(data, 20, i)):
                        return False
                if not (data[-i - 1].close > move_avg(data, 10, i)):
                    return False
            return True
        except:
            ...

    def rule9(self):
        data = self.data
        for i in range(1, 50):
            if t_limit(self.stock, data, i):
                if data[-1].close * 1.1 < data[-i].high:
                    return True
                else:
                    return False

    def rule10(self):
        data = self.data
        if data[-3].turnover < data[-2].turnover < data[-1].turnover:
            if data[-3].close < data[-2].close < data[-1].close:
                return True

    def rule11(self):
        data = self.data
        if data[-4].turnover < data[-3].turnover < data[-2].turnover:
            if data[-4].close < data[-3].close < data[-2].close:
                return True

    def rule12(self):
        data = self.data
        if data[-5].turnover < data[-4].turnover < data[-3].turnover:
            if data[-5].close < data[-4].close < data[-3].close:
                return True

    def rule13(self):
        data = self.data
        if data[-5].turnover < data[-3].turnover < data[-2].turnover:
            if data[-5].close < data[-3].close < data[-2].close:
                return True

    def rule14(self):
        data = self.data
        if data[-5].turnover < data[-4].turnover < data[-2].turnover:
            if data[-5].close < data[-4].close < data[-2].close:
                return True

    def rule15(self):
        data = self.data
        try:
            count = 0
            for i in range(40):
                j = i + 1
                ma10 = [data[-_] for _ in range(j, j + 10)]
                ma20 = [data[-_] for _ in range(j, j + 20)]
                avg10 = sum(_.close for _ in ma10) / len(ma10)
                avg20 = sum(_.close for _ in ma20) / len(ma20)
                if avg10 > avg20:
                    count += 1
                if count >= 30:
                    return True
        except:
            return False

    def rule16(self):
        data = self.data
        try:
            count = 0
            for i in range(40):
                j = i + 1
                ma20 = [data[-_] for _ in range(j, j + 20)]
                ma30 = [data[-_] for _ in range(j, j + 30)]
                avg20 = sum(_.close for _ in ma20) / len(ma20)
                avg30 = sum(_.close for _ in ma30) / len(ma30)
                if avg20 > avg30:
                    count += 1
                if count >= 30:
                    return True
        except:
            return False

    def rule17(self):
        if self.data[-1].close < self.data[-1].his_high / 3:
            return True

    def rule18(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data):
            return False
        if t_limit(stock, data, 1):
            return False
        try:
            range1to5 = data[-6:-1]
            range1to10 = data[-11:-1]
            range1to20 = data[-21:-1]
            if sum([_.close for _ in range1to5]) / 5 > sum([_.close for _ in range1to20]) / 20:
                if data[-2].close > sum([_.close for _ in range1to10]) / 10:
                    return True
        except:
            return False

    def rule19(self):
        flag = False
        limitCount = 0
        for i in range(5):
            if t_limit(self.stock, self.data, i):
                limitCount += 1
                if limitCount > 1:
                    return False
            if t_low_pct(self.data, i) < -0.05 and t_close_pct(self.data, i) > 0:
                flag = True
        return flag

    def rule20(self):
        try:
            for i in range(40):
                if self.data[-i - 1].close <= move_avg(self.data, 30, i):
                    return False
            return True
        except:
            pass

    def rule21(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(40):
                if not t_limit(stock, data, i):
                    continue
                if t_limit(stock, data, i + 1):
                    continue
                d = data[-i - 1]
                if d.buy_elg_vol / d.volume <= 0.5:
                    continue
                if d.turnover > 3 * sum([_.turnover for _ in data[-i - 6:-i - 1]]) / 5:
                    return True
        except:
            pass

    def rule22(self):
        data = self.data
        stock = self.stock
        return data[-1].limitOpenTime < 2 and data[-1].TP > 65 and data[-1].TF > 10

    def rule23(self):
        data = self.data
        stock = self.stock
        return day2elg(data) > 60 and day3elg(data) > 60

    def rule24(self):
        data = self.data
        stock = self.stock
        return data[-1].TP > 95 and t_limit(stock, data, 1)
