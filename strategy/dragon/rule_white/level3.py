# -*- coding: utf-8 -*-
# @Time    : 2022/6/21 15:16
# @Author  : Destiny_
# @File    : level3.py
# @Software: PyCharm

from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class level3(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex)

    def rule1(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        if data[-1].pctChange <= limit(stock):
            return False
        if data[-2].pctChange <= limit(stock):
            return False
        if data[-1].turnover <= data[-2].turnover:
            return False
        range10 = data[-11:-1]
        if data[-1].turnover < 1.8 * max([_.turnover for _ in range10]):
            return True

    def rule2(self):
        data = self.data
        stock = self.stock
        if data[-1].pctChange <= limit(stock):
            return False
        if data[-2].pctChange <= limit(stock):
            return False
        if data[-1].turnover >= data[-2].turnover:
            return False
        if t_open_pct(data, 0) <= t_open_pct(data, 1):
            return False
        if data[-2].turnover > data[-3].turnover:
            return True

    def rule3(self):
        data = self.data
        stock = self.stock
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if data[-1].turnover >= data[-2].turnover:
            return False
        if t_open_pct(data) > 0.035:
            return t_open_pct(data) > t_open_pct(data, 1)

    def rule4(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(3, 51):
                if not t_limit(stock, data, i):
                    continue
                d = data[-i - 1]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.8:
                    if d.buy_elg_vol / d.volume > 0.5:
                        return True
        except:
            pass

    def rule5(self):
        data = self.data
        stock = self.stock
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if data[-1].turnover >= data[-2].turnover:
            return False
        matchTime = joinTimeToStamp(data[-1].date, '09:45:00')
        if data[-1].firstLimitTime < matchTime:
            matchTime = joinTimeToStamp(data[-2].date, '09:40:00')
            return data[-2].firstLimitTime > matchTime

    def rule6(self):
        data = self.data
        try:
            for i in range(40):
                j = i + 1
                ma30 = [data[-_] for _ in range(j, j + 30)]
                ma60 = [data[-_] for _ in range(j, j + 60)]
                avg30 = sum(_.close for _ in ma30) / len(ma30)
                avg60 = sum(_.close for _ in ma60) / len(ma60)
                if avg30 <= avg60:
                    return False
        except:
            return False

    def rule7(self):
        data = self.data
        stock = self.stock
        limit1 = 0.11 if stock[0:3] == '300' else 0.055
        if data[-1].pctChange <= limit(stock):
            return False
        if data[-2].pctChange <= limit(stock):
            return False
        if data[-3].pctChange > limit(stock):
            return False
        if t_open_pct(data) > limit1:
            return True

    def rule8(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data):
                return False
            range5to25 = data[-26:-5]
            if data[-1].close <= 1.2 * max(_.close for _ in range5to25):
                range10 = data[-11:-1]
                if data[-1].turnover < 1.5 * max([_.turnover for _ in range10]):
                    range440 = data[-441:-1]
                    if data[-1].close > max([_.high for _ in range440]):
                        return True
        except:
            return False

    def rule9(self):
        data = self.data
        stock = self.stock
        if data[-2].turnover <= data[-1].turnover:
            return False
        if not (t_open_pct(data) > 0.05 and t_close_pct(data) > limit(stock) / 100):
            return False
        range10 = data[-12:-2]
        if data[-2].turnover > max([_.turnover for _ in range10]):
            return True

    def rule10(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if t_limit(stock, data, 2):
            return False
        if t_open_pct(data, 0) >= 0.045:
            if t_low_pct(data, 0) > 0.005:
                return True

    def rule11(self):
        data = self.data
        stock = self.stock
        try:
            range10 = data[-10:]
            range60 = data[-60:]
            range220 = data[-220:]
            if sum([_.close for _ in range10]) / 10 > sum([_.close for _ in range220]) / 220:
                if sum([_.close for _ in range60]) / 60 > sum([_.close for _ in range220]) / 220:
                    if max([_.turnover for _ in range60]) > 5 * sum([_.turnover for _ in range220]) / 220:
                        for i in range(1, 61):
                            if data[-i].pctChange > limit(stock):
                                return True
        except:
            return False

    def rule12(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data):
            return False
        if t_limit(stock, data, 1):
            return False
        try:
            range220 = data[-221:-1]
            flag = max([_.close for _ in range220])
            for i in range(20):
                if data[-i - 1].close * 1.1 > flag:
                    return True
        except:
            return False

    def rule13(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        try:
            for i in range(1, 61):
                if data[-i].close > max([_.close for _ in data[-i - 440:-i]]):
                    return True
        except:
            pass

    def rule14(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        try:
            flag = False
            for i in range(1, 31):
                if t_close_pct(data, i - 1) > 0.06:
                    flag = True
                    break
            if flag:
                range220 = data[-221:-1]
                if data[-1].close > 0.95 * max([_.high for _ in range220]):
                    return True
        except:
            return False

    def rule15(self):
        data = self.data
        avg4 = sum([data[-5].close, data[-4].close, data[-3].close, data[-2].close]) / 4
        if not (data[-1].close > avg4 and data[-2].close > avg4):
            return False
        for i in range(1, 3):
            range220 = data[-i - 220:-i]
            if data[-i].close > max([_.high for _ in range220]):
                return True

    def rule16(self):
        data = self.data
        try:
            if data[-1].concentration < 9:
                return True
        except:
            pass

    def rule17(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data, 1):
            range5 = data[-6:-1]
            avg = sum([_.turnover for _ in range5]) / 5
            if avg < 5:
                return True

    def rule18(self):
        data = self.data
        if 4 < data[-1].close < 12:
            if 1.5 < data[-1].turnover < 6:
                return True

    def rule19(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if 4 < data[-1].close < 12:
            if 3 < data[-1].turnover < 9:
                return True

    def rule20(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        matchTime = joinTimeToStamp(data[-1].date, '09:40:00')
        if data[-1].firstLimitTime > matchTime:
            return True

    def rule21(self):
        data = self.data
        try:
            for i in range(10):
                j = i + 1
                ma10 = [data[-_] for _ in range(j, j + 10)]
                ma20 = [data[-_] for _ in range(j, j + 20)]
                avg10 = sum(_.close for _ in ma10) / len(ma10)
                avg20 = sum(_.close for _ in ma20) / len(ma20)
                if avg10 <= avg20:
                    return False
            return True
        except:
            return False

    def rule22(self):
        data = self.data
        stock = self.stock
        index = self.gemIndex
        if not t_limit(stock, data):
            return False
        if t_low_pct(data) <= -0.05:
            return False
        if t_open_pct(data) > 0.01:
            if t_close_pct(index) < -0.01:
                return True

    def rule23(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 4):
            return False
        try:
            for i in range(10):
                j = i + 1
                ma = [data[-_] for _ in range(j, j + 10)]
                avg = sum(_.close for _ in ma) / len(ma)
                if data[-i - 1].close <= avg:
                    return False
            return True
        except:
            return False

    def rule24(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 4):
            return False
        try:
            for i in range(20):
                j = i + 1
                ma = [data[-_] for _ in range(j, j + 20)]
                avg = sum(_.close for _ in ma) / len(ma)
                if data[-i - 1].close <= avg:
                    return False
            return True
        except:
            return False

    def rule25(self):
        data = self.data
        try:
            for i in range(30):
                j = i + 1
                ma = [data[-_] for _ in range(j, j + 30)]
                avg = sum(_.close for _ in ma) / len(ma)
                if data[-i - 1].close <= avg:
                    return False
            return True
        except:
            return False

    def rule26(self):
        data = self.data
        try:
            if data[-1].concentration < data[-2].concentration:
                if data[-1].concentration < 13:
                    return True
        except:
            pass

    def rule27(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data):
            return False
        if t_limit(stock, data, 2):
            return False
        if t_open_pct(data) <= 0.05:
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        matchTime = joinTimeToStamp(data[-1].date, '09:45:00')
        if data[-1].firstLimitTime < matchTime:
            return True

    def rule28(self):
        data = self.data
        stock = self.stock
        limitCount = 0
        for i in range(3):
            if t_limit(stock, data, i):
                limitCount += 1
            if limitCount > 1:
                return False
        range10 = data[-11:-1]
        range20 = data[-21:-1]
        count = 0
        for i in range10:
            if i.close > sum([_.close for _ in range20]) / 20:
                count += 1
            if count >= 8:
                return True

    def rule29(self):
        data = self.data
        try:
            for i in range(30):
                j = i + 1
                day1 = data[-j - 2]
                day2 = data[-j - 1]
                day3 = data[-j]
                if day1.close > day2.close > day3.close:
                    if day1.volume < day2.volume < day3.volume:
                        return True
        except:
            pass

    def rule30(self):
        data = self.data
        stock = self.stock
        try:
            plus = []
            minus = []
            for i in range(1, 21):
                if t_limit(stock, data, i):
                    return False
                if t_close_pct(data, i) > 0:
                    plus.append(data[-i - 1].volume)
                else:
                    minus.append(data[-i - 1].volume)
            if sum(plus) / len(plus) > sum(minus) / len(minus):
                return True
        except:
            pass

    def rule31(self):
        data = self.data
        stock = self.stock
        if not model_1(stock, data):
            return False
        if model_1(stock, data, 1):
            return False
        if data[-1].turnover < 0.25 * data[-2].turnover:
            return True

    def rule32(self):
        data = self.data
        stock = self.stock
        if not model_1(stock, data, 1):
            return False
        if model_1(stock, data, 2):
            return False
        if data[-2].turnover < 0.25 * data[-3].turnover:
            return True

    def rule33(self):
        data = self.data
        try:
            badCount = 0
            for i in range(50):
                j = i + 1
                ma = [data[-_] for _ in range(j, j + 60)]
                avg = sum(_.close for _ in ma) / len(ma)
                if data[-i - 1].close <= avg:
                    badCount += 1
                if badCount > 2:
                    return False
            return True
        except:
            return False

    def rule34(self):
        data = self.data
        try:
            badCount = 0
            for i in range(40):
                j = i + 1
                ma = [data[-_] for _ in range(j, j + 30)]
                avg = sum(_.close for _ in ma) / len(ma)
                if data[-i - 1].close <= avg:
                    badCount += 1
                if badCount > 3:
                    return False
            return True
        except:
            return False

    def rule35(self):
        data = self.data
        try:
            for i in range(30):
                j = i + 1
                ma20 = [data[-_] for _ in range(j, j + 20)]
                ma30 = [data[-_] for _ in range(j, j + 30)]
                avg20 = sum(_.close for _ in ma20) / len(ma20)
                avg30 = sum(_.close for _ in ma30) / len(ma30)
                if avg20 <= avg30:
                    return False
            return True
        except:
            return False

    def rule36(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(20):
                if t_limit(stock, data, i):
                    if t_limit(stock, data, i + 1):
                        return False
            badCount = 0
            for i in range(15):
                if t_limit(stock, data, i):
                    continue
                j = i + 1
                ma = [data[-_] for _ in range(j, j + 20)]
                avg = sum(_.close for _ in ma) / len(ma)
                if data[-i - 1].close < avg:
                    badCount += 1
                if badCount > 1:
                    return False
            return True
        except:
            return False

    def rule37(self):
        data = self.data
        stock = self.stock
        for i in range(30):
            j = i + 1
            day1 = data[-j - 2]
            day2 = data[-j - 1]
            day3 = data[-j]
            for _ in range(i, i + 3):
                if t_limit(stock, data, _):
                    return False
            if day1.close < day2.close < day3.close:
                if day1.volume < day2.volume < day3.volume:
                    return True

    def rule38(self):
        data = self.data
        stock = self.stock
        try:
            if model_1(stock, data):
                return False
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
            v1 = data[-1].timeVol(minute='0930')
            v2 = data[-2].timeVol(minute='0930')
            if v1 > v2:
                return True
        except:
            pass

    def rule39(self):
        data = self.data
        try:
            if model_1(self.stock, data):
                return False
            v1 = data[-1].timeVol(minute='0930')
            v2 = data[-2].timeVol(minute='0930')
            v3 = data[-3].timeVol(minute='0930')
            if v1 > v2 > v3:
                return True
        except:
            pass

    def rule40(self):
        data = self.data
        stock = self.stock
        try:
            if t_open_pct(data) > limit(stock) / 100:
                return False
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
            v1 = data[-1].timeVol(timeStamp=data[-1].firstLimitTime)
            v2 = data[-2].timeVol(timeStamp=data[-2].firstLimitTime)
            if v1 > v2:
                return True
        except:
            pass

    def rule41(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data, 1):
                return False
            if model_1(stock, data, 1):
                return False
            d = data[-2]
            if d.timeVol(timeStamp=d.firstLimitTime) <= d.volume * 0.1:
                return False
            if d.timeVol(timeStamp=d.firstLimitTime) > d.timeVol(minute=prevMinute(getMinute(stamp=d.firstLimitTime))) * 10:
                return True
        except:
            pass

    def rule42(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(2, 22):
                if not t_limit(stock, data, i):
                    continue
                if t_limit(stock, data, i - 1):
                    continue
                if not t_limit(stock, data, i - 2):
                    continue
                nxt_nxt = data[-i + 1]
                if (nxt_nxt.buy_elg_vol - nxt_nxt.sell_elg_vol) / nxt_nxt.buy_elg_vol > 0.6:
                    if nxt_nxt.buy_elg_vol / nxt_nxt.volume > 0.4:
                        return True
        except:
            pass

    def rule43(self):
        try:
            d = self.data[-1]
            if d.close < 0.25 * d.his_high:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol > 0.6:
                    if d.buy_elg_vol / d.volume > 0.4:
                        return True
        except:
            pass

    def rule44(self):
        data = self.data
        if data[-1].concentration < data[-2].concentration < data[-3].concentration:
            return True

    def rule45(self):
        data = self.data
        stock = self.stock
        try:
            count = 0
            limitCount = 0
            for i in range(3):
                if t_limit(stock, data, i):
                    limitCount += 1
                    if limitCount > 1:
                        return False
                highestClose = max([data[-_ - 1].close for _ in range(5, 91)])
                if data[-i - 1].close > highestClose:
                    count += 1
            return limitCount <= 1 and count >= 2
        except:
            pass

    def rule46(self):
        # TODO
        data = self.data
        stock = self.stock
        if not model_1(stock, data):
            return False
        if t_limit(stock, data, 1):
            return False
        return data[-1].turnover < data[-2].turnover * 0.4

    def rule47(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        return t_open_pct(data) > 0.05 and t_low_pct(data) > 0.035

    def rule49(self):
        data = self.data
        stock = self.stock
        if data[-1].CP <= 65:
            return False
        try:
            for i in range(10, 81):
                if t_limit(stock, data, i):
                    return True
        except:
            pass

    def rule50(self):
        data = self.data
        stock = self.stock
        if data[-1].limitOpenTime > 0:
            return False
        if data[-1].turnover <= 3 * sum([data[-i - 1].turnover for i in range(1, 11)]) / 10:
            return False
        try:
            for i in range(10, 81):
                if t_limit(stock, data, i):
                    return True
        except:
            pass

    def rule51(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 6):
                if not data[-i - 1].close > move_avg(data, 20, i):
                    return False
            avgClose1to5 = sum([data[-_ - 1].close for _ in range(1, 6)]) / 5
            for i in range(2, 31):
                if not t_limit(stock, data, i):
                    continue
                if data[-i - 1].close * 0.96 < avgClose1to5:
                    return True
        except:
            ...
