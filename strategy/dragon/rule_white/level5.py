# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 09:18
# @Author  : Destiny_
# @File    : level5.py
# @Software: PyCharm

from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class level5(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel],
                 limitData: dict[str, list[LimitDataModel]]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex, limitData)

    def rule1(self):
        data = self.data
        stock = self.stock
        try:
            if data[-1].limitOpenTime >= 1:
                return False
            count1 = 0
            count2 = 0
            count3 = 0
            for i in range(1, 5):
                if data[-i].pctChange > limit(stock):
                    count1 += 1
                if t_open_pct(data, i - 1) > 0.065:
                    if t_low_pct(data, i - 1) > 0.035:
                        if t_close_pct(data, i - 1) > limit(stock) / 100:
                            count2 += 1
                if t_low_pct(data, i - 1) > 0.025:
                    count3 += 1
            if count1 >= 3 and count2 >= 2 and count3 >= 3:
                d = data[-1]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.3:
                    return True
        except:
            pass

    def rule2(self):
        data = self.data
        stock = self.stock
        try:
            if data[-1].limitOpenTime >= 1:
                return False
            count1 = 0
            count2 = 0
            count3 = 0
            for i in range(1, 6):
                if data[-i].pctChange > limit(stock):
                    if t_close_pct(data, i - 1) > limit(stock) / 100:
                        if t_low_pct(data, i - 1) > -0.01:
                            count1 += 1
                if t_low_pct(data, i - 1) > 0.035:
                    count2 += 1
                if t_open_pct(data, i - 1) > 0.06:
                    count3 += 1
            if count1 >= 4 and count2 >= 3 and count3 >= 2:
                d = data[-1]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.3:
                    return True
        except:
            pass

    def rule3(self):
        data = self.data
        try:
            d = data[-1]
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.8:
                if d.buy_elg_vol / d.volume > 0.5:
                    return True
        except:
            pass

    def rule4(self):
        data = self.data
        stock = self.stock
        if data[-1].limitOpenTime >= 1:
            return False
        count = 0
        for i in range(1, 4):
            if 0.055 < t_open_pct(data, i - 1) < limit(stock) / 100:
                count += 1
            if count >= 2:
                break
        if count < 2:
            return False
        matchTime = date_util.joinTimeToStamp(data[-1].date, '09:50:00')
        if data[-1].firstLimitTime < matchTime:
            return True

    def rule5(self):
        data = self.data
        try:
            d = data[-2]
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.8:
                if d.buy_elg_vol / d.volume > 0.5:
                    d = data[-1]
                    if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.6:
                        return True
        except:
            pass

    def rule6(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 3):
            return False
        try:
            if not t_limit(stock, data):
                return False
            if not t_limit(stock, data, 1):
                return False
            if data[-1].turnover > data[-2].turnover:
                if t_open_pct(data) > 0.07:
                    if t_low_pct(data) > 0.05:
                        if data[-2].turnover < 0.7 * data[-3].turnover:
                            d = data[-1]
                            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.3:
                                return True
        except:
            pass

    def rule7(self):
        data = self.data
        stock = self.stock
        try:
            if not model_1(stock, data, 1):
                return False
            if data[-2].turnover < data[-3].turnover / 3:
                if model_t(stock, data) and t_low_pct(data) > 0.07:
                    d = data[-1]
                    if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.4:
                        return True
        except:
            pass

    def rule8(self):
        data = self.data
        try:
            for i in range(1, 31):
                if limit_height(self.stock, data, i) >= 3:
                    return False
            for i in range(30, 121):
                d = data[-i - 1]
                if t_close_pct(data, i) <= 0.05:
                    continue
                ma20 = move_avg(data, 20, i)
                ma30 = move_avg(data, 30, i)
                ma60 = move_avg(data, 60, i)
                if d.low >= ma20:
                    continue
                if d.low >= ma30:
                    continue
                if d.low >= ma60:
                    continue
                if d.high <= ma20:
                    continue
                if d.high <= ma30:
                    continue
                if d.high <= ma60:
                    continue
                afterData = [_ for _ in range(30, i) if data[-_ - 1].close < d.low]
                if len(afterData) <= 3:
                    return True
        except:
            pass

    def rule9(self):
        data = self.data
        try:
            for i in range(1, 31):
                if limit_height(self.stock, data, i) >= 3:
                    return False
            for i in range(30, 121):
                d = data[-i - 1]
                if t_close_pct(data, i) <= 0.05:
                    continue
                ma10 = move_avg(data, 10, i)
                ma20 = move_avg(data, 20, i)
                ma30 = move_avg(data, 30, i)
                ma60 = move_avg(data, 60, i)
                if ma30 <= ma60:
                    continue
                if d.low >= ma20:
                    continue
                if d.low >= ma30:
                    continue
                if d.low >= ma60:
                    continue
                if d.close <= ma10:
                    continue
                if d.close <= ma20:
                    continue
                if d.close <= ma30:
                    continue
                afterData = [_ for _ in range(30, i) if data[-_ - 1].close < d.low]
                if len(afterData) <= 3:
                    return True
        except:
            pass

    def rule10(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 3):
                return False
            if not t_limit(stock, data):
                return False
            if not t_limit(stock, data, 1):
                return False
            if not (t_open_pct(data) > 0.05 and t_low_pct(data) > 0.03):
                return False
            if data[-1].turnover >= data[-2].turnover:
                return False
            range7 = data[-9:-2]
            if data[-2].turnover > max([_.turnover for _ in range7]):
                d = data[-1]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.3:
                    return True
        except:
            pass

    def rule13(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(4):
                if not t_limit(stock, data, i):
                    return False
            if not model_t(stock, data, 1):
                return False
            if data[-1].turnover >= data[-2].turnover:
                return False
            matchTime = joinTimeToStamp(data[-1].date, '09:50:00')
            if data[-1].lastLimitTime < matchTime:
                d = data[-1]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.3:
                    return True
        except:
            pass

    def rule14(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 4):
                if not t_limit(stock, data, i - 1):
                    return False
            if t_open_pct(data, 1) <= 0.05:
                return False
            matchTime = joinTimeToStamp(data[-2].date, '09:45:00')
            if data[-2].lastLimitTime >= matchTime:
                return False
            if data[-2].turnover >= data[-3].turnover:
                return False
            if data[-2].turnover >= data[-1].turnover:
                return False
            if t_open_pct(data) <= 0.07:
                return False
            matchTime = date_util.joinTimeToStamp(data[-1].date, '09:40:00')
            if data[-1].firstLimitTime < matchTime:
                d = data[-1]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.3:
                    return True
        except:
            pass
