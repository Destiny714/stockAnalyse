# -*- coding: utf-8 -*-
# @Time    : 2022/8/21 17:32
# @Author  : Destiny_
# @File    : level6.py
# @Software: PyCharm

from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class level6(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex)

    def rule1(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(60):
                day1 = data[-i - 3]
                day2 = data[-i - 2]
                day3 = data[-i - 1]
                if model_1(stock, data, i + 2):
                    continue
                if not (1.2 * day1.volume < day2.volume < 2 * day1.volume):
                    continue
                if not (min(day2.open, day2.close) > day1.close):
                    continue
                if abs(t_open_pct(data, i + 1) - t_close_pct(data, i + 1)) > 0.03:
                    continue
                if not (day3.volume < 0.7 * day2.volume):
                    continue
                if day3.close > day1.close:
                    return True
        except:
            pass

    def rule2(self):
        data = self.data
        stock = self.stock
        for i in range(3, 33):
            if not 0.05 < t_high_pct(data, i - 1) < limit(stock) / 100:
                continue
            if t_close_pct(data, i - 1) <= 0.04:
                continue
            last5 = data[-i - 5:-i]
            flag = True
            count1 = 0
            count2 = 0
            for _ in last5:
                if data[-i].high <= _.high:
                    count1 += 1
                if count1 > 1:
                    flag = False
                    break
                if data[-i].low >= _.low:
                    count2 += 1
                if count2 > 1:
                    flag = False
                    break
            if flag:
                return True

    def rule3(self):
        data = self.data
        try:
            d0 = data[-1]
            if d0.limitOpenTime > 0:
                return False
            if (d0.buy_elg_vol + d0.buy_lg_vol - d0.sell_elg_vol - d0.sell_lg_vol) / (
                    d0.buy_elg_vol + d0.buy_lg_vol) <= 0.2:
                return False
            count = 0
            for i in range(5):
                d = data[-i - 1]
                j = i + 1
                prev6 = [data[-_] for _ in range(j, j + 6)]
                if d.close > sum([_.close for _ in prev6]) / len(prev6):
                    count += 1
            if count < 4:
                return False
            for i in range(30):
                if t_high_pct(data, i) <= 0.06:
                    continue
                d = data[-i - 1]
                j = i + 1
                prev5 = [data[-_] for _ in range(j + 1, j + 6)]
                if d.high <= max([_.high for _ in prev5]):
                    continue
                prev60 = [data[-_] for _ in range(j + 1, j + 61)]
                if d.close > max([_.close for _ in prev60]):
                    return True
        except:
            pass

    def rule4(self):
        data = self.data
        stock = self.stock
        try:
            d0 = data[-1]
            if d0.limitOpenTime > 0:
                return False
            if (d0.buy_elg_vol + d0.buy_lg_vol - d0.sell_elg_vol - d0.sell_lg_vol) / (
                    d0.buy_elg_vol + d0.buy_lg_vol) <= 0.2:
                return False
            count = 0
            for i in range(10):
                if t_limit(stock, data, i):
                    if t_limit(stock, data, i + 1):
                        return False
                j = i + 1
                d = data[-i - 1]
                prev60 = [data[-_] for _ in range(j + 1, j + 61)]
                if d.close > max([_.close for _ in prev60]):
                    count += 1
            if count >= 3:
                for i in range(30):
                    j = i + 1
                    d = data[-i - 1]
                    prev60 = [data[-_] for _ in range(j, j + 60)]
                    if d.close <= sum([_.close for _ in prev60]) / len(prev60):
                        return False
                return True
        except:
            pass

    def rule5(self):
        data = self.data
        stock = self.stock
        try:
            d0 = data[-1]
            if d0.limitOpenTime > 0:
                return False
            if (d0.buy_elg_vol + d0.buy_lg_vol - d0.sell_elg_vol - d0.sell_lg_vol) / (
                    d0.buy_elg_vol + d0.buy_lg_vol) <= 0.2:
                return False
            _flag = False
            for i in range(4, 21):
                if not t_limit(stock, data, i):
                    continue
                if t_limit(stock, data, i - 1):
                    continue
                if t_high_pct(data, i - 1) <= 0.07:
                    continue
                flag = False
                for n in range(i - 4, i):
                    if t_limit(stock, data, n):
                        flag = True
                        break
                if not flag:
                    return False
                for j in range(i):
                    k = j + 1
                    d = data[-j - 1]
                    if d.low <= data[-i - 2].low:
                        return False
                    prev10 = [data[-_] for _ in range(k, k + 10)]
                    if d.close <= sum([_.close for _ in prev10]) / len(prev10):
                        return False
                _flag = True
                break
            if not _flag:
                return False
            for i in range(30):
                j = i + 1
                d = data[-i - 1]
                prev60 = [data[-_] for _ in range(j, j + 60)]
                if d.close <= sum([_.close for _ in prev60]) / len(prev60):
                    return False
            return True
        except:
            pass

    def rule6(self):
        data = self.data
        stock = self.stock
        try:
            shot = False
            for i in range(1, 31):
                if not t_limit(stock, data, i):
                    continue
                d = data[-i - 1]
                if d.close <= max([_.close for _ in data[-i - 21:-i - 1]]):
                    continue
                after = [data[-_ - 1] for _ in range(1, i)]
                flag = True
                for index, t in enumerate(after):
                    No = index + 1
                    if t.close <= move_avg(data, 20, No):
                        flag = False
                        break
                if not flag:
                    continue
                if min([_.low for _ in after]) > d.close * 0.96:
                    shot = True
                    break
            if shot:
                for i in range(200):
                    if limit_height(stock, data, i) >= 4:
                        return False
                return True
        except:
            ...

    def rule7(self):
        data = self.data
        stock = self.stock
        if t_high_pct(data) >= limit(stock) / 100:
            return False
        return data[-1].CF > 25 and data[-1].CP > 10
