# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:25
# @Author  : Destiny_
# @File    : levelF2.py
# @Software: PyCharm

from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class levelF2(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel],
                 shIndex: list[StockDataModel],
                 limitData: dict[str, list[LimitDataModel]]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex, limitData)

    def rule1(self):
        data = self.data
        stock = self.stock
        count = 0
        if not (data[-3].turnover < data[-2].turnover < data[-1].turnover):
            return False
        for i in range(3):
            if not t_limit(stock, data, i):
                return False
            if data[-i - 1].limitOpenTime > 2:
                count += 1
            if count >= 2:
                return True

    def rule2(self):
        data = self.data
        stock = self.stock
        for i in range(3):
            if not t_limit(stock, data, i):
                return False
            if model_1(stock, data, i):
                return False
        if data[-1].turnover > 1.5 * data[-2].turnover:
            if data[-2].turnover > 1.5 * data[-3].turnover:
                return True

    def rule3(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data):
                return False
            if not t_limit(stock, data, 1):
                return False
            if model_1(stock, data):
                return False
            if model_1(stock, data, 1):
                return False
            if data[-1].turnover <= 3 * data[-2].turnover:
                return False
            matchTime = joinTimeToStamp(data[-1].date, '09:45:00')
            if data[-1].firstLimitTime <= matchTime:
                return False
            if data[-1].timeVol(timeStamp=data[-1].firstLimitTime) < 100000:
                if t_low_pct(self.gemIndex) > -0.01:
                    return True
        except:
            pass

    def rule4(self):
        data = self.data
        stock = self.stock
        for i in range(4):
            if not t_limit(stock, data, i):
                return False
        if model_1(stock, data):
            return False
        if model_1(stock, data, 1):
            return False
        if data[-1].turnover < data[-2].turnover < data[-3].turnover:
            if data[-2].turnover < data[-4].turnover:
                return True

    def rule5(self):
        data = self.data
        stock = self.stock
        count1 = 0
        count2 = 0
        for i in range(1, 5):
            if t_limit(stock, data, i - 1):
                count1 += 1
            if model_1(stock, data, i - 1):
                count2 += 1
        if count2 > 1:
            return False
        if count1 < 3:
            return False
        if data[-4].turnover < data[-3].turnover < data[-2].turnover < data[-1].turnover:
            if t_open_pct(data, 1) < 0.06 and t_open_pct(data) < 0.06:
                return True

    def rule6(self):
        data = self.data
        stock = self.stock
        if not model_1(stock, data, 0):
            return False
        range10 = data[-11:-1]
        if data[-1].turnover > 1.8 * max([_.turnover for _ in range10]):
            return True

    def rule7(self):
        data = self.data
        stock = self.stock
        limitCount = 0
        if data[-1].turnover <= data[-2].turnover / 5:
            return False
        for i in range(3):
            if t_limit(stock, data, i + 1):
                limitCount += 1
        if limitCount < 2:
            return False
        range30 = data[-34:-4]
        for d in range30:
            if d.pctChange >= limit(stock):
                return False
        if not (data[-4].turnover > data[-3].turnover > data[-2].turnover):
            return False
        if model_1(stock, data, 1):
            return False
        if model_1(stock, data, 3):
            return False
        return True

    def rule8(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(1, 5):
            if data[-i].pctChange < limit(stock):
                return False
            if t_open_pct(data, i - 1) < 0.03:
                count += 1
        if count >= 3:
            return True

    def rule9(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 4):
                if not t_limit(stock, data, i - 1):
                    return False
            for i in range(2):
                d = data[- i - 1]
                if data[-i - 1].limitOpenTime <= 1:
                    continue
                if t_close_pct(data, i) <= limit(stock) / 100:
                    continue
                if t_open_pct(data, i) < -0.025 or t_low_pct(data, i) < -0.045:
                    if (d.buy_elg_vol + d.buy_lg_vol) < (d.sell_elg_vol + d.sell_lg_vol):
                        if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol < 0.3:
                            return True
        except:
            pass

    def rule10(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(1, 4):
            if data[-i].pctChange < limit(stock):
                return False
            if t_low_pct(data, i - 1) < -0.06:
                matchTime = joinTimeToStamp(data[-i].date, '10:30:00')
                if data[-i].firstLimitTime != 0 and data[-i].firstLimitTime > matchTime:
                    if data[-i].limitOpenTime > 0:
                        count += 1
        return count >= 1

    def rule11(self):
        data = self.data
        stock = self.stock
        flag = False
        for i in range(4):
            if not t_limit(stock, data, i):
                return False
            if flag:
                continue
            if not t_limit(stock, data, i + 1):
                return False
            if t_open_pct(data, i) < -0.04:
                matchTime = joinTimeToStamp(data[-i - 1].date, '10:20:00')
                if data[-i - 1].lastLimitTime > matchTime:
                    flag = True
        return flag

    def rule12(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data, 3):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if t_limit(stock, data, 2):
            return False
        if data[-3].turnover * 0.7 > data[-2].turnover:
            if data[-3].turnover * 0.7 > data[-1].turnover:
                return data[-2].turnover > data[-3].turnover / 4

    def rule13(self):
        data = self.data
        stock = self.stock
        flag = False
        model1Count = 0
        for i in range(30):
            if model_1(stock, data, i):
                flag = True
                model1Count += 1
        if flag and model1Count <= 4:
            allVol = [_.turnover for _ in data[-30:]]
            if min(allVol) > (1 / 3) * max(allVol):
                return True

    def rule14(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 3):
            return False
        if t_limit(stock, data, 2):
            return False
        if not model_1(stock, data, 1):
            return False
        if not model_1(stock, data):
            return t_low_pct(data) < 0.055 and data[-1].TP < 35

    def rule15(self):
        try:
            data = self.data
            stock = self.stock
            d = data[-1]
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol / weakenedIndex(self.shIndex) >= 0.6:
                return False
            if d.CP / weakenedIndex(self.shIndex) >= 60:
                return False
            plus = []
            minus = []
            for i in range(3, 43):
                if t_low_pct(self.gemIndex, i) < -0.02:
                    continue
                if t_limit(stock, data, i):
                    return False
                d = data[-i - 1]
                if d.close > d.open:
                    plus.append(data[-i - 1].volume)
                else:
                    minus.append(data[-i - 1].volume)
            if sum(plus) / (len(plus) + 1) < sum(minus) / (len(minus) + 1):
                return True
        except:
            pass

    def rule16(self):
        data = self.data
        try:
            d = data[-1]
            for i in range(10):
                if t_close_pct(data, i) > 0.06:
                    return False
            if d.TF / weakenedIndex(self.shIndex) < 80:
                if d.CP / weakenedIndex(self.shIndex) < 60:
                    plus = 0
                    minus = 0
                    for i in range(30):
                        if t_low_pct(self.gemIndex, i) < -0.01:
                            continue
                        if data[-i - 1].close > data[-i - 1].open:
                            plus += 1
                        else:
                            minus += 1
                    return plus < minus
        except:
            pass

    def rule17(self):
        data = self.data
        stock = self.stock
        flag = False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            if t_low_pct(data, i) >= -0.05:
                continue
            matchTime = joinTimeToStamp(data[-i - 1].date, '13:00:00')
            if data[-i - 1].lastLimitTime > matchTime:
                flag = True
        return flag

    def rule18(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data):
                return False
            matchTime = joinTimeToStamp(data[-1].date, '10:00:00')
            if data[-1].lastLimitTime <= matchTime:
                return False
            count = 0
            for i in range(5):
                d = data[-i - 1]
                if t_open_pct(data, i) - t_low_pct(data, i) > 0.07 and t_high_pct(data, i) > 0.06:
                    if (d.buy_elg_vol + d.buy_lg_vol - d.sell_elg_vol - d.sell_lg_vol) / (
                            d.buy_elg_vol + d.buy_lg_vol) < 0.2:
                        count += 1
                if count >= 2:
                    return True
        except:
            pass

    def rule19(self):
        data = self.data
        stock = self.stock
        try:
            count = 0
            for i in range(3):
                if not t_limit(stock, data, i):
                    return False
                if model_1(stock, data, i):
                    return False
                if t_open_pct(data, i) >= limit(stock) / 100:
                    return False
                matchTime = joinTimeToStamp(data[-i - 1].date, '09:47:00')
                if data[-i - 1].firstLimitTime >= matchTime:
                    return False
                d = data[-i - 1]
                if d.CP / weakenedIndex(self.shIndex, i, weak_degree=5) < 65:
                    count += 1
            return count >= 2
        except:
            pass

    def rule20(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if t_open_pct(data) >= 0.04:
            return False
        matchTime = joinTimeToStamp(data[-1].date, '10:30:00')
        if data[-1].firstLimitTime > matchTime:
            return True

    def rule21(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(4):
            if t_open_pct(data, i) - t_low_pct(data, i) > 0.07:
                if t_high_pct(data, i) > limit(stock) / 100:
                    count += 1
            if count >= 3:
                return True

    def rule22(self):
        data = self.data
        stock = self.stock
        for i in range(3):
            if not t_limit(stock, data, i):
                return False
            matchTime = joinTimeToStamp(data[-i - 1].date, '10:00:00')
            if data[-i - 1].firstLimitTime <= matchTime:
                return False
            if data[-i - 1].lastLimitTime <= matchTime:
                return False
        return True

    def rule23(self):
        data = self.data
        stock = self.stock
        if t_low_pct(data) >= 0.075:
            return False
        if model_1(stock, data):
            return False
        if getMinute(stamp=data[-1].firstLimitTime) <= '0950':
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if t_limit(stock, data, 2):
            return False
        if (data[-1].concentration - data[-2].concentration) / data[-2].concentration > 0.2:
            return data[-1].CP < 70

    def rule24(self):
        data = self.data
        stock = self.stock
        try:
            rank = RankLimitStock(self.limitData).by('open-industry', data[-1].date)
            if stock in rank[self.industry][:2]:
                return False
            for i in range(3):
                if t_limit(stock, data, i + 1):
                    return False
            if not t_limit(stock, data):
                return False
            if model_1(stock, data):
                return False
            d = data[-1]
            if d.buy_elg_vol / d.volume >= 0.35:
                return False
            matchTime = date_util.joinTimeToStamp(data[-1].date, '09:40:00')
            if data[-1].firstLimitTime < matchTime:
                if data[-1].timeVol(timeStamp=data[-1].firstLimitTime) < data[-1].volume * 0.1:
                    return True
        except:
            pass

    def rule25(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if model_1(stock, data):
            return False
        for i in range(2, 4):
            if t_limit(stock, data, i):
                return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if data[-4].turnover > data[-3].turnover > data[-2].turnover > data[-1].turnover:
            return True

    def rule26(self):
        data = self.data
        stock = self.stock
        try:
            d = data[-1]
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol / weakenedIndex(self.shIndex) >= 0.6:
                return False
            if d.buy_elg_vol / d.volume / weakenedIndex(self.shIndex) >= 0.6:
                return False
            if t_open_pct(data) >= 0.07:
                return False
            if model_1(stock, data):
                return False
            if not t_limit(stock, data, 1):
                if t_limit(stock, data):
                    matchTime = joinTimeToStamp(data[-1].date, '09:45:00')
                    if data[-1].lastLimitTime < matchTime:
                        return True
        except:
            pass

    def rule27(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            if not t_limit(stock, data, 1):
                return False
            if model_1(stock, data, 1):
                return False
            for i in range(2):
                d = data[-i - 1]
                if d.TP / weakenedIndex(self.shIndex) >= 60:
                    return False
            if t_open_pct(data, 1) >= 0.07:
                return False
            return getMinute(stamp=data[-2].firstLimitTime) < '0945'
        except:
            pass

    def rule28(self):
        data = self.data
        stock = self.stock
        try:
            flag = False
            for i in range(4, 13):
                if t_limit(stock, data, i):
                    if t_limit(stock, data, i + 1):
                        if t_limit(stock, data, i + 2):
                            flag = True
                            break
            if not flag:
                return False
            if t_limit(stock, data, 3):
                return False
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
            if data[-2].turnover >= sum(_.turnover for _ in data[-6:-3]) / 3:
                return False
            if data[-1].turnover > data[-2].turnover:
                matchTime = joinTimeToStamp(data[-1].date, '10:00:00')
                if data[-1].firstLimitTime > matchTime:
                    return True
        except:
            pass

    def rule29(self):
        data = self.data
        stock = self.stock
        flag = False
        for i in range(4, 13):
            if t_limit(stock, data, i):
                if t_limit(stock, data, i + 1):
                    if t_limit(stock, data, i + 2):
                        flag = True
                        break
        if not flag:
            return False
        if t_limit(stock, data, 3):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            matchTime = joinTimeToStamp(data[-i - 1].date, '09:40:00')
            if data[-i - 1].firstLimitTime >= matchTime:
                return False
        if data[-2].turnover >= 0.6 * sum(_.turnover for _ in data[-6:-3]) / 3:
            return False
        if data[-1].turnover < 0.6 * sum(_.turnover for _ in data[-6:-3]) / 3:
            return True

    def rule30(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if t_low_pct(data) < -0.045:
            return True

    def rule31(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data, 2):
            return False
        if model_1(stock, data, 2):
            return False
        for i in range(2):
            if not model_1(stock, data, i):
                return False
        if data[-1].turnover > 1.5 * data[-2].turnover and data[-1].turnover > max([data[-i - 1].turnover for i in range(1, 11)]) / 5:
            return True

    def rule32(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            if (data[-1].concentration - data[-2].concentration) / data[-2].concentration <= 0.15:
                return False
            d = data[-1]
            if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol < 0.8:
                if d.buy_elg_vol / d.volume < 0.5:
                    return True
        except:
            pass

    def rule33(self):
        data = self.data
        stock = self.stock
        if t_high_pct(data) > limit(stock):
            if t_close_pct(data) < 0.065:
                return True

    def rule34(self):
        data = self.data
        stock = self.stock
        for i in [0, 1, 3, 4]:
            if not t_limit(stock, data, i):
                return False
        if t_limit(stock, data, 2):
            return False
        return data[-1].TP < 40

    def rule35(self):
        data = self.data
        stock = self.stock
        for i in [0, 1, 3]:
            if not t_limit(stock, data, i):
                return False
        if t_limit(stock, data, 2):
            return False
        return t_open_pct(data) < 0.05

    def rule36(self):
        pass
        # TODO

    def rule37(self):
        for i in range(1, 11):
            if not t_down_limit(self.stock, self.data, i):
                continue
            if t_limit(self.stock, self.data, i - 1):
                continue
            if self.data[-i - 1].CF / weakenedIndex(self.shIndex, i) < -40:
                return True

    def rule38(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if model_1(stock, data):
            return False
        if data[-1].turnover >= 1 / 3 * max([_.turnover for _ in data[-50:]]):
            return False
        if data[-1].close < move_avg(data, 10) and data[-1].close < move_avg(data, 20):
            return True

    def rule39(self):
        data = self.data
        stock = self.stock
        if data[-1].turnover >= data[-2].turnover * 3:
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            if model_1(stock, data, i):
                return False
            if data[-i - 1].turnover >= 2:
                return False
        return True

    def rule40(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 1):
            return False
        d = data[-1]
        if getMinute(stamp=d.lastLimitTime) < '0940':
            return d.CP / weakenedIndex(self.shIndex) < 60

    def rule41(self):
        data = self.data
        try:
            if t_limit(self.stock, data, 1):
                return False
            if data[-1].TP / weakenedIndex(self.shIndex, weak_degree=5) >= 50:
                return False
            if data[-1].CP >= 70:
                return False
            if model_1(self.stock, self.data):
                return False
            sumTurnover = 0
            for i in range(2, 22):
                if t_limit(self.stock, self.data, i):
                    return False
                sumTurnover += self.data[-i - 1].turnover
            return (sumTurnover / 20) < 2 and (data[-1].amount * 1000) < 1e8
        except:
            pass

    def rule42(self):
        data = self.data
        if data[-1].CP >= 55:
            return False
        if t_open_pct(data) - t_low_pct(data) > 0.03:
            return data[-1].limitOpenTime > 1

    def rule43(self):
        data = self.data
        if data[-1].TP >= 40:
            return False
        if t_open_pct(data, 1) - t_low_pct(data, 1) > 0.02:
            return data[-2].limitOpenTime > 0

    def rule44(self):
        data = self.data
        stock = self.stock
        for i in [1, 2]:
            if t_limit(stock, data, i):
                return False
        if not t_limit(stock, data):
            return False
        return data[-1].turnover > 15 and data[-2].limitOpenTime > 0

    def rule45(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data, 1):
            return False
        if data[-1].limitOpenTime > 1:
            return getMinute(stamp=data[-1].firstLimitTime) > '1310'

    def rule46(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(5):
            d = data[-i - 1]
            if t_limit(stock, data, i):
                return False
            if d.close > d.open:
                count += 1
        return count >= 4

    def rule47(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data):
                return False
            limitList = RankLimitStock(self.limitData).by('limitTime-industry', self.data[-1].date)[self.industry]
            return len(limitList) >= 3
        except:
            ...

    def rule48(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            if not data[-1].CP < 60:
                return False
            if not data[-1].TF < 70:
                return False
            posDay = 1
            negDay = 1
            posTurnover = 0
            negTurnover = 0
            for i in range(1, 41):
                d = data[-i - 1]
                if d.close > d.open:
                    posDay += 1
                    posTurnover += d.turnover
                else:
                    negDay += 1
                    negTurnover += d.turnover
            return posDay < negDay and posTurnover / posDay < negTurnover / negDay
        except:
            ...

    def rule49(self):
        data = self.data
        stock = self.stock
        try:
            if data[-1].limitOpenTime == 0:
                return False
            if data[-1].CP >= 55:
                return False
            if data[-1].TF >= 60:
                return False
            return len([1 for i in range(1, 61) if t_limit(stock, data, i)]) == 0
        except:
            ...

    def rule50(self):
        data = self.data
        stock = self.stock
        try:
            count = 0
            for i in range(1, 61):
                if not t_limit(stock, data, i):
                    continue
                if t_limit(stock, data, i + 1):
                    continue
                if t_close_pct(data, i - 1) < -0.07:
                    count += 1
                    if count >= 2:
                        return True
        except:
            ...

    def rule51(self):
        data = self.data
        stock = self.stock
        try:
            if data[-1].limitOpenTime == 0:
                return False
            count = 0
            for i in range(1, 61):
                if not t_limit(stock, data, i):
                    continue
                if data[-i].turnover <= data[-1].turnover * 1.7:
                    continue
                if data[-i].high > data[-1].close:
                    count += 1
                    if count >= 2:
                        return True
        except:
            ...

    def rule52(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(2):
                if t_limit(stock, data, i):
                    return False
            if getMinute(stamp=data[-1].firstLimitTime) >= '0940':
                return False
            for i in range(1, 61):
                if not t_limit(stock, data, i):
                    continue
                if t_limit(stock, data, i + 1):
                    continue
                if data[-i].high * 1.03 > data[-1].close:
                    return True
        except:
            ...

    def rule53(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data):
                return False
            if (data[-1].TF > 55 and data[-1].TP > 35) is True:
                return False
            if data[-1].close > max([data[-i - 1].high for i in range(1, 101)]):
                for j in range(1, 101):
                    if not t_limit(stock, data, j):
                        continue
                    if data[-j - 1].close > max([data[-k - 1].high for k in range(j + 1, 101)]):
                        return False
                return True
        except:
            ...

    def rule54(self):
        ...
        # TODO

    def rule55(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if t_limit(stock, data, 1):
            return False
        return data[-1].concentration > 15 and data[-1].limitOpenTime > 0 and data[-1].CP < 65

    def rule56(self):
        data = self.data
        stock = self.stock
        for i in range(2):
            if not model_1(stock, data, i):
                return False
        return data[-1].turnover > data[-2].turnover * 1.5 and data[-1].TF < 80

    def rule57(self):
        data = self.data
        stock = self.stock
        for i in [1, 2]:
            if not model_1(stock, data, i):
                return False
        return data[-2].TF < 80 and data[-1].TF < -10

    def rule58(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 4):
            return False
        if not t_limit(stock, data, 3):
            return False
        if model_1(stock, data, 3):
            return False
        for i in range(3):
            if not model_1(stock, data, i):
                return False
        return data[-1].turnover > data[-2].turnover * 1.7

    def rule59(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 5):
            return False
        if not t_limit(stock, data, 4):
            return False
        if model_1(stock, data, 4):
            return False
        for i in range(4):
            if not model_1(stock, data, i):
                return False
        return data[-1].turnover > data[-2].turnover * 1.7

    def rule60(self):
        data = self.data
        stock = self.stock
        sumTurnover = 0
        for i in range(2, 82):
            sumTurnover += data[-i - 1].turnover
            if t_limit(stock, data, i):
                return False
        if sumTurnover / 20 < 2:
            return data[-1].turnover > 3 * sumTurnover / 20 and data[-1].amount * 1000 < 5e8

    def rule61(self):
        data = self.data
        stock = self.stock
        for i in [1, 2]:
            if t_limit(stock, data, i):
                return False
        if not t_limit(stock, data):
            return False
        for i in range(1, 21):
            d = data[-i - 1]
            if (d.high - d.low) / d.low <= 0.3:
                return False
        return True

    def rule62(self):
        data = self.data
        d = data[-1]
        return getMinute(stamp=d.firstLimitTime) > '1330' and d.limitOpenTime > 0 and d.CP < 60

    def rule63(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 1):
            return False
        if model_1(stock, data, 1):
            return False
        if not model_1(stock, data):
            return False
        return data[-1].turnover > data[-2].turnover / 4 and data[-1].TP < 80

    def rule64(self):
        data = self.data
        stock = self.stock
        if getMinute(stamp=data[-2].firstLimitTime) <= '0940':
            return False
        if data[-2].CP / weakenedIndex(self.shIndex, weak_degree=5) >= 50:
            return False
        return getMinute(stamp=data[-1].firstLimitTime) < '0940' and data[-1].CP / weakenedIndex(self.shIndex, weak_degree=5) < 65

    def rule65(self):
        data = self.data
        stock = self.stock
        for i in [1, 2]:
            if t_limit(stock, data, i):
                return False
        if not model_1(stock, data):
            return False
        return data[-1].TP / weakenedIndex(self.shIndex, weak_degree=5) < 90

    def rule66(self):
        data = self.data
        stock = self.stock
        if not model_1(stock, data):
            return False
        try:
            for i in range(1, 21):
                if t_close_pct(data, i) > 0.05:
                    return False
        except:
            ...
        return data[-1].TP / weakenedIndex(self.shIndex, weak_degree=5) < 90
