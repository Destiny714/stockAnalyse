# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:25
# @Author  : Destiny_
# @File    : levelF3.py
# @Software: PyCharm

from common.tool_box import skip
from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class levelF3(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel],
                 shIndex: list[StockDataModel]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex)

    def rule1(self):
        data = self.data
        try:
            if data[-1].TP / weakenedIndex(self.shIndex) >= 35:
                return False
            if data[-1].turnover <= data[-2].turnover / 4:
                return False
            count = 0
            for i in range(6):
                if t_high_pct(data, i) > 0.07 and t_close_pct(data, i) < 0.045:
                    count += 1
                if count >= 2:
                    return True
        except:
            ...

    def rule2(self):
        data = self.data
        stock = self.stock
        if data[-1].pctChange <= limit(stock):
            return False
        if data[-2].pctChange <= limit(stock):
            return False
        if model_1(stock, data, 1):
            return False
        if t_low_pct(data) <= 0.06:
            return False
        if data[-1].turnover <= 1.5 * data[-2].turnover:
            return False
        if data[-1].firstLimitTime > data[-2].firstLimitTime + timeDelta(data[-2].date, data[-1].date):
            return True

    def rule3(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 6):
                if not model_t(stock, data, i - 1):
                    continue
                if t_low_pct(data, i - 1) >= 0.06:
                    continue
                if data[-i - 1].CP >= 55:
                    continue
                range10 = data[-10 - i:-i]
                if data[-i].volume > 3 * max([_.volume for _ in range10]):
                    d = data[-i]
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) < 0.2:
                        return True
        except:
            pass

    def rule4(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        if not model_1(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if t_open_pct(data) > limit(stock) / 100 and t_low_pct(data) < 0.05:
            return True

    def rule5(self):
        data = self.data
        stock = self.stock
        turnOver = data[-1].turnover + 1
        for i in range(1, 4):
            d = data[-i]
            if d.pctChange <= limit(stock):
                return False
            if model_1(stock, data, i - 1):
                return False
            if d.turnover < turnOver:
                turnOver = d.turnover
            else:
                return False
        if data[-1].firstLimitTime <= data[-2].firstLimitTime + timeDelta(data[-2].date, data[-1].date):
            return False
        if data[-2].firstLimitTime <= data[-3].firstLimitTime + date_util.timeDelta(data[-3].date, data[-2].date):
            return False
        return True

    def rule6(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 4):
                if t_low_pct(self.gemIndex, i - 1) <= -0.01:
                    continue
                d = data[-i]
                if d.open != d.close:
                    continue
                if t_close_pct(data, i - 1) <= limit(stock) / 100:
                    continue
                if t_low_pct(data, i - 1) >= 0.06:
                    continue
                if data[-i].limitOpenTime > 2:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) < 0.2:
                        return True
        except:
            pass

    def rule7(self):
        data = self.data
        stock = self.stock
        if data[-1].TP >= 50:
            return False
        if data[-2].TP >= 35:
            return False
        if data[-4].pctChange > limit(stock):
            return False
        if not model_1(stock, data, 2):
            return False
        if t_open_pct(data, 1) != t_close_pct(data, 1):
            return False
        if t_close_pct(data, 1) <= limit(stock) / 100:
            return False
        if t_low_pct(data, 1) < 0.07:
            return True

    def rule8(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        for i in range(3):
            if t_limit(stock, data, i + 1):
                return False
        if data[-2].close > data[-3].close > data[-4].close:
            if data[-2].close / data[-5].close > 1.13:
                return True

    def rule9(self):
        data = self.data
        stock = self.stock
        if not model_1(stock, data, 1):
            return False
        if model_1(stock, data, 2):
            return False
        if not t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 3):
            return False
        if data[-2].turnover > (1 / 3) * data[-3].turnover:
            t2Time = data[-3].lastLimitTime
            t3Time = data[-4].lastLimitTime
            if t2Time > t3Time + timeDelta(data[-4].date, data[-3].date):
                return True

    def rule10(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(1, 4):
            if data[-i].pctChange <= limit(stock):
                return False
            if t_open_pct(data, i - 1) < 0.035:
                count += 1
        if count >= 2 and data[-1].turnover > data[-2].turnover:
            if data[-1].limitOpenTime > 0:
                return True

    def rule11(self):
        data = self.data
        stock = self.stock
        try:
            if model_1(stock, data, 1):
                return False
            if not t_limit(stock, data, 1):
                return False
            if data[-1].turnover <= 1.8 * data[-2].turnover:
                return False
            matchTime = joinTimeToStamp(data[-1].date, '09:45:00')
            if data[-1].firstLimitTime > matchTime and data[-1].lastLimitTime > matchTime:
                if data[-1].timeVol(timeStamp=data[-1].firstLimitTime) < data[-1].volume * 0.1:
                    if t_low_pct(self.gemIndex) > -0.01:
                        return True
        except:
            pass

    def rule12(self):
        data = self.data
        stock = self.stock
        if data[-1].pctChange <= limit(stock):
            return False
        if data[-2].pctChange <= limit(stock):
            return False
        if t_open_pct(data, 1) >= 0.03:
            return False
        if t_open_pct(data) <= 0.05:
            return False
        if data[-1].turnover <= 0.8 * data[-2].turnover:
            return False
        if data[-1].firstLimitTime > data[-2].firstLimitTime + timeDelta(data[-2].date, data[-1].date):
            return True

    def rule13(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data, 2):
            return False
        if t_open_pct(data, 2) >= 0.03:
            return False
        if t_open_pct(data, 1) <= 0.05:
            return False
        if data[-2].turnover <= 0.8 * data[-3].turnover:
            return False
        if getMinute(stamp=data[-2].lastLimitTime) <= '0935':
            return False
        if data[-2].lastLimitTime <= data[-3].lastLimitTime + timeDelta(data[-3].date, data[-2].date):
            return False
        if data[-2].firstLimitTime > data[-3].firstLimitTime + timeDelta(data[-3].date, data[-2].date):
            return True

    def rule14(self):
        data = self.data
        range20 = data[-20:]
        range30 = data[-30:]
        if max([_.close for _ in range20]) < sum([_.close for _ in range30]) / 30:
            return True

    def rule15(self):
        data = self.data
        stock = self.stock
        try:
            if not data[-1].TP < 40:
                return False
            if not data[-1].pctChange < 16:
                return False
            if data[-1].CP / weakenedIndex(self.shIndex, weak_degree=5) >= 60:
                return False
            for i in range(1, 21):
                if limit_height(stock, data, i) >= 3:
                    return False
            if t_limit(stock, data, 1):
                return False
            if data[-1].turnover > max([_.turnover for _ in data[-31:-1]]) * 1.8:
                return True
        except:
            pass

    def rule16(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        range20 = data[-22:-2]
        avgRate = (sum([_.turnover for _ in range20]) / 20) * 5
        if data[-1].turnover > avgRate and data[-2].turnover > avgRate:
            if data[-1].turnover > 1.8 * data[-2].turnover:
                return True

    def rule17(self):
        data = self.data
        try:
            for i in range(1, 5):
                if t_open_pct(data, i - 1) > 0.09 and t_low_pct(data, i - 1) < 0.03:
                    if t_low_pct(self.gemIndex, i - 1) > -0.01:
                        d = data[-i]
                        if (d.buy_elg_vol + d.buy_lg_vol) / d.volume < 0.5 and d.buy_elg_vol < d.sell_elg_vol:
                            if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                                    d.buy_elg_vol + d.buy_lg_vol) < 0.2:
                                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol < 0.3:
                                    return True
        except:
            pass

    def rule18(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data, 1):
                return False
            if model_1(stock, data, 1):
                return False
            if data[-1].limitOpenTime <= 3:
                return False
            if data[-1].turnover > 3 * data[-2].turnover:
                if data[-1].timeVol(timeStamp=data[-1].firstLimitTime) < 100000:
                    if t_low_pct(self.gemIndex) > -0.01:
                        return True
        except:
            pass

    def rule19(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(1, 4):
            if data[-i].pctChange < limit(stock):
                return False
            if t_open_pct(data, i - 1) >= 0.035:
                continue
            if t_low_pct(data, i - 1) < -0.045:
                count += 1
        if count >= 2:
            return True

    def rule20(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
            if data[-1].limitOpenTime <= 2:
                return False
            matchTime = joinTimeToStamp(data[-1].date, '09:45:00')
            if data[-1].firstLimitTime <= matchTime:
                return False
            if data[-1].timeVol(timeStamp=data[-1].firstLimitTime) >= data[-1].volume * 0.1:
                return False
            if t_low_pct(self.gemIndex) > -0.01:
                d = data[-1]
                if (d.buy_elg_vol + d.buy_lg_vol) / d.volume < 0.5 and d.buy_elg_vol < d.sell_elg_vol:
                    return True
        except:
            pass

    def rule21(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        d = data[-1]
        if d.buy_elg_vol / d.volume >= 0.25:
            return False
        range1 = data[-3:]
        range2 = data[-6:-3]
        if sum([_.turnover for _ in range1]) < sum([_.turnover for _ in range2]):
            matchTime = joinTimeToStamp(data[-1].date, '09:40:00')
            if data[-1].firstLimitTime < matchTime:
                range20 = data[-21:-1]
                range30 = data[-31:-1]
                if sum([_.close for _ in range20]) / 20 < sum([_.close for _ in range30]) / 30:
                    return True

    def rule22(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            if model_1(stock, data):
                return False
            if data[-1].TP >= 50:
                return False
            for i in range(2):
                if not t_limit(self.stock, data, i):
                    return False
            for i in range(-201, -30):
                range10 = data[i:i + 10]
                if range10[-1].close / range10[0].close > 1.8:
                    return True
        except:
            return False

    def rule23(self):
        data = self.data
        stock = self.stock
        if data[-1].turnover <= 0.5 * data[-2].turnover:
            return False
        matchTime = joinTimeToStamp(data[-1].date, '09:45:00')
        if data[-1].lastLimitTime <= matchTime:
            return False
        count = 0
        for i in range(5):
            if t_high_pct(data, i) <= limit(stock) / 100:
                continue
            if t_open_pct(data, i) - t_low_pct(data, i) > 0.04:
                count += 1
        if count >= 3:
            return True

    def rule24(self):
        data = self.data
        stock = self.stock
        for i in range(2):
            if not (data[-i - 1].limitOpenTime > 1 and t_open_pct(data, i) > limit(stock) / 100):
                return False
        return True

    def rule25(self):
        data = self.data
        stock = self.stock
        if data[-1].turnover <= 0.5 * data[-2].turnover:
            return False
        matchTime = joinTimeToStamp(data[-1].date, '09:45:00')
        if data[-1].lastLimitTime <= matchTime:
            return False
        flag: bool = False
        for i in range(5):
            if t_open_pct(data, i) - t_low_pct(data, i) > 0.05:
                if t_high_pct(data, i) > limit(stock) / 100:
                    matchTime = joinTimeToStamp(data[-i - 1].date, '10:30:00')
                    if data[-i - 1].lastLimitTime > matchTime:
                        if flag:
                            return True
                        else:
                            flag = True
                            continue

    def rule26(self):
        data = self.data
        stock = self.stock
        for i in range(2):
            if not t_limit(stock, data, i + 1):
                return False
        if data[-2].limitOpenTime <= 2:
            return False
        if data[-3].turnover <= data[-4].turnover:
            return False
        if getMinute(stamp=data[-2].lastLimitTime) <= '11:00':
            return False
        if t_low_pct(self.gemIndex, 1) > -0.01:
            return True

    def rule27(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data):
                return False
            d = data[-1]
            if d.buy_elg_vol / d.volume >= 0.45:
                return False
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol >= 0.6:
                return False
            flag = False
            for i in range(30):
                j = i + 1
                ma30 = [data[-_] for _ in range(j, j + 30)]
                ma60 = [data[-_] for _ in range(j, j + 60)]
                avg30 = sum(_.close for _ in ma30) / len(ma30)
                avg60 = sum(_.close for _ in ma60) / len(ma60)
                if avg30 < avg60:
                    flag = True
                    break
            if not flag:
                return False
            for i in range(10, 51):
                if limit_height(stock, data, i) >= 3:
                    return False
            count = 0
            range90 = data[-90:]
            highPrice = max([_.high for _ in range90])
            if data[-1].close >= highPrice:
                return False
            for i in range(3, 93):
                if not t_limit(stock, data, i):
                    continue
                if t_limit(stock, data, i + 1):
                    continue
                if t_limit(stock, data, i - 1):
                    continue
                if t_limit(stock, data, i - 2):
                    continue
                if t_open_pct(data, i - 1) < 0.045:
                    count += 1
                if count >= 2:
                    return True
        except:
            return False

    def rule28(self):
        data = self.data
        count = 0
        for i in range(5):
            if t_open_pct(data, i) <= 0.09:
                continue
            if t_low_pct(data, i) >= 0.05:
                continue
            if t_low_pct(self.gemIndex, i) > -0.01:
                count += 1
            if count >= 2:
                return True

    def rule29(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            d = data[-1]
            if d.buy_elg_vol / d.volume < 0.3:
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol < 0.45:
                    return True
        except:
            pass

    def rule30(self):
        data = self.data
        stock = self.stock
        if not data[-1].pctChange < 16:
            return False
        if t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if data[-1].concentration - data[-2].concentration > 2:
            return data[-1].TP / weakenedIndex(self.shIndex) < 38 and data[-1].TF < 60

    def rule31(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if data[-1].concentration - data[-2].concentration > 3.5:
            return getMinute(stamp=data[-1].firstLimitTime) > '0945' and getMinute(stamp=data[-2].firstLimitTime) < '0945'

    def rule32(self):
        data = self.data
        stock = self.stock
        try:
            if data[-1].turnover <= 0.8 * data[-2].turnover:
                return False
            count = 0
            for i in range(3):
                if not t_limit(stock, data, i):
                    return False
                matchTime = joinTimeToStamp(data[-i - 1].date, '09:45:00')
                if data[-i - 1].firstLimitTime >= matchTime:
                    return False
                if t_open_pct(data, i) < limit(stock) / 100:
                    count += 1
            return count >= 2
        except:
            pass

    def rule33(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if data[-1].limitOpenTime <= 1:
            return False
        if t_down_limit(stock, data):
            if data[-1].buy_elg_vol / data[-1].volume < 0.4:
                return True

    def rule34(self):
        data = self.data
        stock = self.stock
        for i in range(3):
            if not t_limit(stock, data, i):
                return False
            if t_open_pct(data, i) >= 0.05:
                return False
        return True

    def rule35(self):
        data = self.data
        stock = self.stock
        try:
            d = data[-1]
            if d.CP / weakenedIndex(self.shIndex, weak_degree=5) >= 60:
                return False
            if d.TF >= 70:
                return False
            if t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            for i in range(10, 91):
                if limit_height(stock, data, i) >= 3:
                    return False
            plus = 0
            minus = 0
            for i in range(50):
                if t_low_pct(self.gemIndex, i) < -0.02:
                    continue
                d = data[-i - 1]
                if d.close > d.open:
                    plus += 1
                else:
                    minus += 1
            return plus < minus
        except:
            pass

    def rule36(self):
        data = self.data
        stock = self.stock
        try:
            d = data[-1]
            if not d.CP / weakenedIndex(self.shIndex, weak_degree=5) < 55:
                return False
            if not getMinute(stamp=data[-1].lastLimitTime) > '0950':
                return False
            if not day2elg(data) < 60:
                return False
            if t_limit(stock, data, 2):
                return False
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
            for i in range(10, 61):
                if limit_height(stock, data, i) >= 3:
                    return False
            plus = 0
            minus = 0
            for i in range(30):
                if t_low_pct(self.gemIndex, i) < -0.02:
                    continue
                d = data[-i - 1]
                if d.close > d.open:
                    plus += 1
                else:
                    minus += 1
            return plus < minus
        except:
            pass

    def rule37(self):
        data = self.data
        stock = self.stock
        index = self.gemIndex
        try:
            d = data[-1]
            if d.buy_elg_vol / d.volume / (1 + t_close_pct(self.shIndex) * 10) >= 0.4:
                return False
            if data[-1].TF >= 80:
                return False
            limitCount = 0
            plus = 1
            minus = 1
            plusVol = 0
            minusVol = 0
            for i in range(20):
                if limit_height(stock, data, i) >= 3:
                    return False
                if t_limit(stock, data, i):
                    limitCount += 1
                if t_low_pct(index, i) <= -0.02:
                    continue
                d = data[-i - 1]
                if d.close > d.open:
                    plusVol += data[-i - 1].volume
                    plus += 1
                else:
                    minusVol += data[-i - 1].volume
                    minus += 1
            if limitCount >= 2:
                return False
            return plusVol / plus < minusVol / minus
        except:
            pass

    def rule38(self):
        data = self.data
        stock = self.stock
        index = self.gemIndex
        try:
            d = data[-1]
            if d.buy_elg_vol / d.volume / (1 + t_close_pct(self.shIndex) * 10) >= 0.4:
                return False
            if data[-1].TF >= 80:
                return False
            limitCount = 0
            plus = 0
            minus = 0
            for i in range(30):
                if t_limit(stock, data, i):
                    limitCount += 1
                    if limitCount >= 2:
                        return False
                if i in range(20):
                    if t_low_pct(index, i) <= -0.02:
                        continue
                    d = data[-i - 1]
                    if d.close > d.open:
                        plus += 1
                    else:
                        minus += 1
            return plus < minus
        except:
            pass

    def rule39(self):
        data = self.data
        stock = self.stock
        try:
            if (data[-1].close - data[-101].close) / data[-101].close <= 0.7:
                return False
            count = 0
            for i in range(100):
                if t_limit(stock, data, i):
                    count += 1
                    if count >= 3:
                        return False
            return True
        except:
            pass

    def rule40(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data):
                return False
            if t_open_pct(data) >= 0.05:
                return False
            if data[-1].turnover <= data[-2].turnover / 4:
                return False
            d = data[-1]
            if d.lastLimitTime < joinTimeToStamp(d.date, '09:40:00'):
                return d.CP / weakenedIndex(self.shIndex, weak_degree=5) < 65
        except:
            pass

    def rule41(self):
        data = self.data
        stock = self.stock
        try:
            if data[-1].TF > 50 and data[-1].TP > 50:
                return False
            if (data[-11].close - data[-101].close) / data[-101].close <= 0.5:
                return False
            for i in range(10, 101):
                if limit_height(stock, data, i) >= 2:
                    return False
            return True
        except:
            pass

    def rule42(self):
        data = self.data
        stock = self.stock
        if data[-1].TP >= 90:
            return False
        for i in range(2):
            if not model_1(stock, data, i):
                return False
        if data[-1].turnover <= 1.5 * data[-2].turnover:
            return False
        return data[-1].turnover > sum([data[-i - 1].turnover for i in range(3, 23)]) / 20 / 3

    def rule43(self):
        data = self.data
        stock = self.stock
        if data[-1].turnover <= data[-2].turnover / 4:
            return False
        if data[-2].TP >= 60:
            return False
        if data[-1].TP >= 90:
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if model_1(stock, data, 1):
            return False
        if not model_1(stock, data):
            return False
        return getMinute(stamp=data[-2].firstLimitTime) < '0945'

    def rule44(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        for i in range(2):
            if not model_1(stock, data, i):
                return False
        if data[-1].turnover <= data[-1].turnover:
            return False
        return data[-2].turnover > data[-3].turnover / 3

    def rule45(self):
        data = self.data
        try:
            if not data[-1].TF < 75:
                return False
            if data[-1].CP / weakenedIndex(self.shIndex, weak_degree=5) >= 70:
                return False
            if data[-1].TF >= 75:
                return False
            count = 0
            for i in range(2, 42):
                if data[-i - 1].close < move_avg(data, 30, i):
                    count += 1
                    if count >= 35:
                        return True
        except:
            ...

    def rule47(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data, 1):
            return False
        if (data[-1].TF > 0 and data[-1].TP > 40 and data[-1].CP > 60) is True:
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            if getMinute(stamp=data[-i - 1].firstLimitTime) >= '0940':
                return False
        return data[-1].limitOpenTime > 2

    def rule48(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            if getMinute(stamp=data[-i - 1].firstLimitTime) >= '0940':
                return False
        return data[-1].turnover > data[-2].turnover * 0.7 and data[-1].turnover > data[-3].turnover * 0.7

    def rule49(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        close = 1000000
        turnover = 1000000
        for i in range(1, 5):
            d = data[-i - 1]
            if t_limit(stock, data, i):
                return False
            if d.close >= close:
                return False
            if d.turnover >= turnover:
                return False
            close = d.close
            turnover = d.turnover
        return data[-1].CP < 55 and data[-1].close > data[-1].his_high / 2

    def rule50(self):
        data = self.data
        count = 0
        try:
            d = data[-1]
            if d.TF > 75 and d.CP > 65 and d.TP > 35 and d.CP / d.TP > 1.37:
                return False
            for i in range(1, 51):
                if t_high_pct(data, i) > 0.055:
                    return False
                if i in range(2, 42):
                    if data[-i - 1].close < move_avg(data, 20, i):
                        count += 1
            return count >= 15 and data[-1].CP < 70 and data[-1].TF < 90
        except:
            ...

    def rule51(self):
        data = self.data
        try:
            for i in range(15, 75):
                d = data[-i - 1]
                if (d.high - d.low) / d.high > 0.3:
                    return True
        except:
            ...

    def rule52(self):
        data = self.data
        stock = self.stock
        try:
            down_limit_flag = False
            for i in range(1, 151):
                if i in range(2, 31):
                    if t_high_pct(data, i) > limit(stock) / 100:
                        return False
                if i in range(30, 151):
                    if limit_height(stock, data, i) >= 4:
                        return False
                if i in range(1, 61):
                    if not down_limit_flag and t_down_limit(stock, data, i) is True:
                        down_limit_flag = True
            return down_limit_flag
        except:
            pass

    @skip
    def rule53(self):
        data = self.data
        stock = self.stock
        for i in range(1, 5):
            if t_limit(stock, data, i):
                return False
        return data[-2].high > data[-3].high > data[-4].high > data[-5].high and data[-1].TP < 35

    def rule54(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if t_limit(stock, data, 1):
            return False
        return t_open_pct(data) > 0.02 and data[-1].limitOpenTime > 1

    def rule55(self):
        data = self.data
        stock = self.stock
        for i in range(3):
            if not model_1(stock, data, i):
                return False
        return data[-3].turnover * 1.8 < data[-2].turnover < data[-1].turnover and data[-1].turnover > data[-3].turnover * 2

    def rule56(self):
        data = self.data
        stock = self.stock
        for i in range(4):
            if not model_1(stock, data, i):
                return False
        return data[-3].turnover > data[-4].turnover * 1.8 and data[-2].turnover > data[-4].turnover * 2

    def rule57(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if t_limit(stock, data, 1):
            return False
        return getMinute(stamp=data[-1].firstLimitTime) < '0940' and data[-1].limitOpenTime > 0 and data[-1].CP < 60 and data[-1].TF < 75

    def rule58(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        for i in range(1, 11):
            if t_limit(stock, data, i):
                return False
        return t_low_pct(data) < -0.035

    def rule59(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if model_1(stock, data, 1):
            return False
        if not (getMinute(stamp=data[-2].firstLimitTime) < '0945'):
            return False
        if not model_1(stock, data):
            return False
        if not data[-2].TP < 60:
            return False
        for i in range(5, 16):
            if t_limit(stock, data, i):
                return True

    def rule60(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 1):
                return False
            if not getMinute(stamp=data[-1].firstLimitTime) < '0940':
                return False
            if not t_limit(stock, data):
                return False
            if not data[-1].turnover > data[-2].turnover / 4:
                return False
            for i in range(1, 61):
                if t_limit(stock, data, i):
                    return False
            count = 0
            for i in range(10):
                if data[-i - 1].close < move_avg(data, 20, i):
                    count += 1
                    if count == 7:
                        return True
        except:
            ...

    def rule61(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 1):
            return False
        if not getMinute(stamp=data[-1].firstLimitTime) < '0940':
            return False
        if data[-2].close == max([data[-i - 1].close for i in range(10)]):
            return False
        if not (data[-1].TF < 70 and data[-1].TP < 70):
            return False
        for i in range(1, 11):
            if t_high_pct(data, i) > limit(stock) / 100 and t_close_pct(data, i) < 0.055:
                return True

    def rule62(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        if not getMinute(stamp=data[-2].firstLimitTime) < '0940':
            return False
        if not model_1(stock, data):
            return False
        if data[-2].close == max([data[-i - 1].close for i in range(10)]):
            return False
        return data[-1].TP < 90

    def rule63(self):
        data = self.data
        stock = self.stock
        for i in [1, 2]:
            if t_limit(stock, data, i):
                return False
        if not t_limit(stock, data):
            return False
        d = data[-1]
        return t_close_pct(data, 1) < -0.05 and d.CP < 65 and d.TP < 45

    def rule64(self):
        data = self.data
        stock = self.stock
        flag = False
        for i in range(1, 11):
            if t_limit(stock, data, i):
                return False
            if flag:
                continue
            if t_low_pct(data, i) < -0.055 and t_close_pct(data, i) < -0.035 and t_high_pct(data, i + 1) < 0.08:
                flag = True
        return flag

    def rule65(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        return t_high_pct(data, 1) > 0.045 and t_close_pct(data, 1) < -0.02 and t_open_pct(data) > 0.01

    def rule66(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        return t_high_pct(data, 1) > 0.045 and t_close_pct(data, 1) < 0.01 and data[-1].limitOpenTime > 2

    def rule67(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if t_limit(stock, data, 1):
            return False
        try:
            for i in range(1, 41):
                if t_limit(stock, data, i):
                    return False
                d = data[-i - 1]
                if not (d.high - d.low) / d.low > 0.025:
                    return False
            return True
        except:
            ...

    def rule68(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if t_limit(stock, data, 1):
            return False
        return getMinute(stamp=data[-1].firstLimitTime) < '0950' and getMinute(stamp=data[-1].lastLimitTime) > '1040' and data[-1].TF < 50

    def rule69(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        try:
            for i in range(1, 41):
                if t_close_pct(data, i) > 0.05:
                    return False
            return data[-1].turnover > 4 * sum([data[-i - 1].turnover for i in range(1, 21)]) / 20
        except:
            ...

    def rule70(self):
        data = self.data
        stock = self.stock
        for i in range(3):
            if not t_limit(stock, data, i):
                return
        if model_1(stock, data, 2):
            return False
        for i in range(2):
            if not model_1(stock, data, i):
                return False
        return data[-1].turnover > data[-2].turnover and data[-1].TF < 90

    def rule71(self):
        data = self.data
        stock = self.stock
        if not model_1(stock, data):
            return False
        if model_1(stock, data, 1):
            return False
        return data[-1].turnover > data[-2].turnover / 2

    def rule72(self):
        data = self.data
        return sum([data[-i - 1].turnover for i in range(5)]) / 5 < 4 and max([data[-i - 1].turnover for i in range(20)]) < 3 * sum(
            [data[-i - 1].turnover for i in range(61, 121)]) / 60

    def rule73(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data, 1):
            return False
        if not model_1(stock, data):
            return False
        return data[-2].turnover < 2 * sum([data[-_ - 1].turnover for _ in range(10, 71)]) / 60 and data[-2].turnover < data[-1].turnover * 3
