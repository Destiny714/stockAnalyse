# -*- coding: utf-8 -*-
# @Time    : 2022/8/3 17:41
# @Author  : Destiny_
# @File    : levelF5.py
# @Software: PyCharm

from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class levelF5(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel],
                 limitData: dict[str, list[LimitDataModel]]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex, limitData)

    def rule1(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data, 1):
                return False
            for i in range(2):
                if getMinute(stamp=data[-i - 1].firstLimitTime) <= '1000':
                    return False
            d = data[-2]
            if d.CF < 40:
                if d.TF < 50:
                    return True
        except:
            pass

    def rule2(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
            matchTime = joinTimeToStamp(data[-1].date, '10:00:00')
            if data[-1].firstLimitTime <= matchTime:
                return False
            d = data[-2]
            if d.CF < 40:
                if d.TF < 50:
                    return True
        except:
            pass

    def rule3(self):
        data = self.data
        try:
            for i in range(3):
                if t_close_pct(data, i) <= 0.06:
                    return False
                d = data[-i - 1]
                if d.CF >= 40:
                    return False
                if d.TF >= 50:
                    return False
                if d.CF >= 55:
                    return False
            return True
        except:
            pass

    def rule4(self):
        data = self.data
        stock = self.stock
        try:
            if data[-1].TF >= 50:
                return False
            for i in range(5):
                d = data[-i - 1]
                if d.turnover <= 4:
                    continue
                if model_1(stock, data, i):
                    return True
        except:
            pass

    def rule5(self):
        data = self.data
        try:
            if t_close_pct(data) <= 0.06:
                return False
            if t_low_pct(data) >= 0.05:
                return False
            d = data[-1]
            if d.TF < -10:
                if d.CF < -10:
                    return True
        except:
            pass

    def rule6(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
            d = data[-2]
            if d.CF < 40:
                if d.TF < 50:
                    if d.buy_lg_vol < d.sell_lg_vol:
                        matchTime = joinTimeToStamp(data[-1].date, '09:45:00')
                        if data[-1].firstLimitTime > matchTime:
                            return True
        except:
            pass

    def rule7(self):
        data = self.data
        stock = self.stock
        try:
            count = 0
            limitCount = 0
            if getMinute(stamp=data[-1].lastLimitTime) <= '1000':
                return False
            for i in range(5):
                if t_limit(stock, data, i):
                    limitCount += 1
                d = data[-i - 1]
                if d.CF < 40 and d.TF < 50:
                    count += 1
                if count >= 3 and limitCount >= 4:
                    return True
        except:
            pass

    def rule8(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
                d = data[-i - 1]
                if ((d.buy_elg_vol + d.buy_lg_vol) / d.volume) >= 0.5:
                    return False
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol >= 0.5:
                    return False
            return True
        except:
            pass

    def rule9(self):
        data = self.data
        try:
            for i in range(2):
                if t_close_pct(data, i) <= 0.05:
                    return False
            d0 = data[-1]
            d1 = data[-2]
            return (d1.buy_elg_vol + d0.buy_elg_vol - d1.sell_elg_vol - d0.sell_elg_vol) / (d1.buy_elg_vol + d0.buy_elg_vol) < 0.5 and (
                    d1.buy_elg_vol + d0.buy_elg_vol + d1.buy_lg_vol + d0.buy_lg_vol) / (d1.volume + d0.volume) < 0.6
        except:
            ...

    def rule10(self):
        data = self.data
        try:
            for i in range(2):
                if t_close_pct(data, i) <= 0.05:
                    return False
            if not t_limit(self.stock, data):
                return False
            if t_high_pct(data, 1) <= 0.05:
                return False
            if t_high_pct(data) > 0.05:
                d = data[-1]
                d1 = data[-2]
                if (d.buy_elg_vol + d1.buy_elg_vol - d.sell_elg_vol - d1.sell_elg_vol) / (
                        d.buy_elg_vol + d1.buy_elg_vol) < 0.4:
                    if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol < 0.4:
                        matchTime = joinTimeToStamp(data[-1].date, '09:50:00')
                        if data[-1].lastLimitTime > matchTime:
                            return True
        except:
            pass

    def rule11(self):
        data = self.data
        try:
            for i in range(2):
                if not t_limit(self.stock, data, i):
                    return False
                d = data[-i - 1]
                if t_high_pct(data, i) <= 0.05:
                    return False
                if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                        d.buy_elg_vol + d.buy_lg_vol) >= 0.2:
                    return False
                matchTime = joinTimeToStamp(d.date, '09:45:00')
                if d.firstLimitTime <= matchTime:
                    return False
            return True
        except:
            pass

    def rule12(self):
        data = self.data
        index = self.gemIndex
        try:
            if t_high_pct(data) <= 0.06:
                return False
            if t_low_pct(data) >= 0.05:
                return False
            if not t_limit(self.stock, data):
                return False
            d = data[-1]
            if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                    d.buy_elg_vol + d.buy_lg_vol) < 0.2:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol < 0.2:
                    matchTime = joinTimeToStamp(data[-1].date, '09:45:00')
                    if data[-1].lastLimitTime < matchTime:
                        if t_low_pct(index) > -0.01:
                            return True
        except:
            pass

    def rule13(self):
        data = self.data
        try:
            if not t_limit(self.stock, data):
                return False
            if not t_limit(self.stock, data, 1):
                return False
            d = data[-1]
            if t_high_pct(data) <= 0.06:
                return False
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol < 0.7:
                if d.buy_elg_vol / d.volume < 0.4:
                    matchTime = date_util.joinTimeToStamp(data[-1].date, '10:00:00')
                    if data[-1].firstLimitTime > matchTime:
                        return True
        except:
            pass

    def rule14(self):
        data = self.data
        try:
            if not t_limit(self.stock, data):
                return False
            for i in range(2):
                if t_close_pct(data, i) <= 0.05:
                    return False
            if data[-2].TF < 30:
                return data[-1].CP / weakenedIndex(self.shIndex, weak_degree=5) < 65
        except:
            pass
