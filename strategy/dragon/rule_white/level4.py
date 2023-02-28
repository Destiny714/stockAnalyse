# -*- coding: utf-8 -*-
# @Time    : 2022/6/21 16:26
# @Author  : Destiny_
# @File    : level4.py
# @Software: PyCharm

from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class level4(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex)

    def rule1(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 1):
            return False
        try:
            range1to5 = data[-6:-1]
            range1to10 = data[-10:-1]
            range1to20 = data[-21:-1]
            range1to30 = data[-31:-1]
            range1to60 = data[-61:-1]
            if sum([_.close for _ in range1to5]) / 5 > sum([_.close for _ in range1to20]) / 20:
                if sum([_.close for _ in range1to20]) / 20 > sum([_.close for _ in range1to60]) / 60:
                    if sum([_.close for _ in range1to30]) / 30 > sum([_.close for _ in range1to60]) / 60:
                        if data[-1].close > sum([_.close for _ in range1to10]) / 10:
                            return True
        except:
            return False

    def rule2(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        try:
            for i in range(30):
                if not t_limit(stock, data, i):
                    continue
                if t_low_pct(data, i) <= 0.06:
                    continue
                if not (0.08 < t_open_pct(data, i) < limit(stock) / 100):
                    continue
                range220 = data[-221 - i:-1 - i]
                if data[-i - 1].close > max([_.high for _ in range220]):
                    return True
        except:
            return False

    def rule3(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if data[-1].turnover <= data[-2].turnover:
            return False
        if data[-1].turnover < 1.5 * data[-2].turnover:
            if data[-2].turnover < 0.7 * data[-3].turnover:
                return True

    def rule4(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if model_1(stock, data):
            return False
        if model_1(stock, data, 1):
            return False
        if t_low_pct(data, 1) < -0.02:
            return False
        if t_open_pct(data) <= 0.05:
            return False
        if t_low_pct(data) < 0.035:
            return False
        if data[-1].turnover < 0.8 * data[-2].turnover:
            return True

    def rule5(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if t_open_pct(data, 1) <= 0.05:
            return False
        if t_low_pct(data, 1) <= 0.02:
            return False
        tLowPct = t_low_pct(data)
        if 0.07 < tLowPct < limit(stock) / 100:
            return True
        if t_open_pct(data) <= 0.07:
            return False
        if tLowPct <= 0.04:
            return False
        if data[-1].turnover < 20:
            return True

    def rule6(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if t_limit(stock, data, 2):
            return False
        if not (0.06 < t_open_pct(data) < 0.09):
            return False
        if not (data[-1].turnover < 0.7 * data[-2].turnover):
            return False
        if t_low_pct(data) <= 0.005:
            return False
        range120 = data[-121:-1]
        if data[-1].close > max([_.high for _ in range120]):
            return True

    def rule7(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if model_1(stock, data):
            return False
        if 4 < data[-1].close < 12:
            if 3 < data[-1].turnover < 9:
                return True

    def rule8(self):
        data = self.data
        if data[-1].concentration < 9:
            if data[-1].concentration < data[-2].concentration:
                return True

    def rule9(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data):
            return False
        if data[-1].turnover <= 1.5 * data[-2].turnover:
            range10 = data[-11:-1]
            if data[-1].turnover < 0.25 * max([_.turnover for _ in range10]):
                return True

    def rule10(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 11):
                if not t_limit(stock, data, i):
                    continue
                if t_limit(stock, data, i + 1):
                    continue
                if t_open_pct(data, i - 1) <= 0.045:
                    continue
                if data[-i].timeVol(minute='0930') > data[-i - 1].volume / 12:
                    return True
        except:
            return False

    def rule11(self):
        data = self.data
        stock = self.stock
        count1 = 0
        count2 = 0
        try:
            for i in range(1, 4):
                if not t_limit(stock, data, i - 1):
                    return False
                if model_1(stock, data, i - 1):
                    return False
                if data[-i].open == data[-i].close:
                    if t_close_pct(data, i - 1) > limit(stock) / 100:
                        if t_low_pct(data, i - 1) > 0.075:
                            count1 += 1
                d = data[-i]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.5:
                    count2 += 1
                if count1 == 1 and count2 >= 2:
                    return True
        except:
            pass

    def rule12(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data, 2):
            return False
        if data[-2].turnover > 4 * data[-3].turnover:
            if t_open_pct(data, 0) > 1.04:
                return True

    def rule13(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data, 2):
            return False
        if not (data[-3].turnover < data[-2].turnover):
            return False
        if not (data[-1].turnover < data[-2].turnover):
            return False
        if t_open_pct(data, 2) > 0.035:
            if t_open_pct(data) > 0.01:
                if data[-3].turnover < data[-4].turnover < data[-2].turnover:
                    return True

    def rule14(self):
        data = self.data
        stock = self.stock
        try:
            if model_1(stock, data, 1):
                return False
            if not t_limit(stock, data, 1):
                return False
            limitTime = data[-2].firstLimitTime
            limitMinute = getMinute(stamp=limitTime)
            limitMinuteLast = prevMinute(limitMinute)
            if data[-2].timeVol(minute=limitMinute) > data[-2].timeVol(minute=limitMinuteLast) * 3:
                if data[-2].limitOpenTime == 0:
                    return True
        except:
            return False

    def rule15(self):
        data = self.data
        stock = self.stock
        try:
            if model_1(stock, data):
                return False
            if not t_limit(stock, data):
                return False
            limitTime = data[-1].firstLimitTime
            limitMinute = getMinute(stamp=limitTime)
            limitMinuteLast = prevMinute(limitMinute)
            if data[-1].timeVol(minute=limitMinute) <= data[-1].timeVol(minute=limitMinuteLast) * 10:
                return False
            if data[-1].timeVol(timeStamp=data[-1].firstLimitTime) > data[-1].volume * 0.1:
                return True
        except:
            return False

    def rule16(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 3):
                if not t_limit(stock, data, i - 1):
                    continue
                if t_low_pct(data, i - 1) <= 0.055:
                    continue
                if t_close_pct(data, i - 1) <= limit(stock) / 100:
                    continue
                if 0.07 < t_open_pct(data, i - 1) < limit(stock) / 100:
                    range120 = data[-i - 120:-i]
                    if data[-i].close > max([_.high for _ in range120]):
                        return True
        except:
            return False

    def rule18(self):
        data = self.data
        stock = self.stock
        for i in range(1, 4):
            if not model_t(stock, data, i - 1):
                continue
            if 0.08 < t_low_pct(data, i - 1) < limit(stock) / 100:
                return True

    def rule19(self):
        data = self.data
        stock = self.stock
        try:
            count1 = 0
            count2 = 0
            count3 = 0
            for i in range(1, 5):
                if t_open_pct(data, i - 1) > 0.035:
                    count2 += 1
                if t_limit(stock, data, i - 1):
                    if t_close_pct(data, i - 1) > limit(stock) / 100:
                        if t_low_pct(data, i - 1) > -0.01:
                            count1 += 1
                d = data[-i]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.5:
                    count3 += 1
                if count1 >= 3 and count2 >= 2 and count3 >= 2:
                    return True
        except:
            pass

    def rule20(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        try:
            if not t_limit(stock, data):
                return False
            if not t_limit(stock, data, 1):
                return False
            if model_1(stock, data):
                return False
            if data[-1].turnover >= 0.7 * data[-2].turnover:
                return False
            if t_open_pct(data) <= 0.065:
                return False
            if t_low_pct(data) <= 0.05:
                return False
            range90 = data[-91:-1]
            if data[-1].close > max([_.high for _ in range90]):
                return True
        except:
            return False

    def rule21(self):
        data = self.data
        if t_close_pct(data) > 0.06:
            con1 = data[-1].concentration
            con2 = data[-2].concentration
            if con1 < 0.09:
                if (con1 - con2) / con2 < 0.1:
                    return True

    def rule22(self):
        data = self.data
        stock = self.stock
        try:
            count = 0
            for i in range(3):
                d = data[-i - 1]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.5:
                    count += 1
            if count < 2:
                return False
            if not t_limit(stock, data):
                return False
            if not t_limit(stock, data, 1):
                return False
            if data[-3].turnover > data[-2].turnover > data[-1].turnover:
                if getMinute(stamp=data[-1].lastLimitTime) < getMinute(stamp=data[-2].lastLimitTime) < getMinute(stamp=data[-3].lastLimitTime):
                    return True
        except:
            pass

    def rule23(self):
        data = self.data
        stock = self.stock
        if not model_t(stock, data):
            return False
        if data[-1].concentration - data[-2].concentration < 0:
            if data[-1].concentration < 18:
                return True

    def rule24(self):
        data = self.data
        stock = self.stock
        try:
            count = 0
            count1 = 0
            for i in range(1, 5):
                if data[-i].pctChange <= limit(stock):
                    return False
                if t_low_pct(data, i - 1) <= -0.01:
                    return False
                if t_open_pct(data, i - 1) > 0.045:
                    count += 1
                d = data[-i]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.5:
                    count1 += 1
                if count >= 2 and count1 >= 3:
                    return True
        except:
            pass

    def rule25(self):
        data = self.data
        stock = self.stock
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            if data[-i - 1].limitOpenTime >= 2:
                return False
        con1 = data[-1].concentration
        con2 = data[-2].concentration
        if (con1 - con2) / con2 < 0.09:
            return True

    def rule26(self):
        data = self.data
        try:
            d = data[-1]
            if d.close >= d.his_high / 3:
                return False
            if d.buy_elg_vol / d.volume <= 0.5:
                return False
            for i in range(20):
                if data[-i - 1].close <= move_avg(data, 30, i):
                    return False
            return True
        except:
            pass

    def rule27(self):
        data = self.data
        try:
            for i in range(1, 3):
                if t_low_pct(data, i - 1) <= -0.02:
                    continue
                if t_open_pct(data, i - 1) > 0:
                    if t_open_pct(self.gemIndex, i - 1) < -0.02:
                        d = data[-1]
                        if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.5:
                            return True
        except:
            pass

    def rule28(self):
        data = self.data
        stock = self.stock
        try:
            count = 0
            for i in range(1, 5):
                if not t_limit(stock, data, i - 1):
                    return False
                if data[-i].limitOpenTime < 2:
                    count += 1
            d = data[-1]
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol <= 0.5:
                return False
            return count >= 3
        except:
            pass

    def rule29(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data):
                return False
            if model_1(stock, data):
                return False
            if data[-1].timeVol(timeStamp=data[-1].firstLimitTime) > 120000:
                d = data[-1]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.5:
                    return True
        except:
            pass

    def rule30(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 3):
            return False
        try:
            for i in range(30):
                j = i + 1
                ma20 = [data[-_] for _ in range(j, j + 20)]
                ma30 = [data[-_] for _ in range(j, j + 30)]
                ma60 = [data[-_] for _ in range(j, j + 60)]
                avg20 = sum(_.close for _ in ma20) / len(ma20)
                avg30 = sum(_.close for _ in ma30) / len(ma30)
                avg60 = sum(_.close for _ in ma60) / len(ma60)
                if not (avg30 > avg60):
                    return False
                if not (avg20 > avg30):
                    return False
            return True
        except:
            return False

    def rule31(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 51):
                if not t_limit(stock, data, i):
                    continue
                d = data[-i - 1]
                range20 = data[-i - 21:-i - 1]
                if d.close <= max([_.close for _ in range20]):
                    continue
                if t_limit(stock, data, i - 1):
                    continue
                if t_open_pct(data, i - 1) <= 0.035:
                    continue
                if t_high_pct(data, i - 1) <= 0.07:
                    continue
                flag = True
                for _i in range(-i, 0):
                    j = _i + 1
                    _range20 = [data[_] for _ in range(j - 20, j)]
                    if data[_i].close <= sum([_.close for _ in _range20]) / len(_range20):
                        flag = False
                        break
                if flag:
                    return True
        except:
            pass

    def rule33(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            if not t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            matchTime0 = joinTimeToStamp(data[-1].date, '09:45:00')
            matchTime1 = joinTimeToStamp(data[-2].date, '09:45:00')
            if data[-1].firstLimitTime < matchTime0 and data[-2].firstLimitTime > matchTime1:
                d = data[-1]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.5:
                    return True
        except:
            pass

    def rule34(self):
        data = self.data
        stock = self.stock
        try:
            if data[-1].limitOpenTime >= 1:
                return False
            if not t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            if data[-2].turnover <= data[-3].turnover:
                return False
            if data[-2].turnover <= data[-1].turnover:
                return False
            matchTime = joinTimeToStamp(data[-1].date, '09:55:00')
            if data[-1].lastLimitTime >= data[-2].lastLimitTime + timeDelta(data[-2].date, data[-1].date):
                return False
            if data[-1].lastLimitTime < matchTime:
                d = data[-1]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.3:
                    return True
        except:
            pass

    def rule36(self):
        data = self.data
        if data[-1].concentration >= 9:
            return False
        cons = [data[-i - 1].concentration for i in range(1, 5)]
        maxCon = max(cons)
        minCon = min(cons)
        if (maxCon - minCon) / minCon < 0.08:
            return True

    def rule37(self):
        data = self.data
        if data[-1].concentration < data[-2].concentration < data[-3].concentration > data[-4].concentration:
            return True

    def rule38(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if (data[-1].concentration - data[-2].concentration) / data[-2].concentration < 0.1:
            return True

    def rule39(self):
        data = self.data
        try:
            for i in range(10):
                ma10 = move_avg(data, 10, i)
                ma20 = move_avg(data, 20, i)
                ma30 = move_avg(data, 30, i)
                ma60 = move_avg(data, 60, i)
                if not (ma10 > ma20 > ma30 > ma60):
                    return False
            return True
        except:
            pass

    def rule41(self):
        data = self.data
        stock = self.stock
        try:
            flag = False
            turnover = 0
            for i in range(1, 31):
                turnover = max(turnover, data[-i - 1].turnover)
                if t_limit(stock, data, i):
                    return False
                if flag is False and t_high_pct(data, i) > 0.06:
                    flag = True
            return flag is True and data[-1].turnover > turnover
        except:
            ...

    def rule42(self):
        data = self.data
        stock = self.stock
        try:
            d = data[-1]
            if not t_limit(stock, data):
                return False
            for i in range(1, 11):
                if t_limit(stock, data, i):
                    return False
            return getMinute(stamp=d.firstLimitTime) > '1030' and d.TP > 50 and d.amount * 1000 > 5e8
        except:
            ...

    def rule43(self):
        data = self.data
        stock = self.stock
        try:
            d = data[-1]
            if not t_limit(stock, data):
                return False
            for i in range(1, 11):
                if t_limit(stock, data, i):
                    return False
            return getMinute(stamp=d.firstLimitTime) > '1030' and d.CP > 70 and d.limitOpenTime == 0
        except:
            ...
