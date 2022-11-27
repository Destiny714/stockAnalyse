# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:25
# @Author  : Destiny_
# @File    : levelF1.py
# @Software: PyCharm

from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stock_detail_model import StockDetailModel


class levelF1(base_level):
    def __init__(self, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel], shIndex: list[StockDataModel],
                 limitData: dict[str, list[LimitDataModel]]):
        self.level = self.__class__.__name__.replace('level', '')
        super().__init__(self.level, stockDetail, data, gemIndex, shIndex, limitData)

    def rule1(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
                if t_low_pct(data, i) >= -0.01:
                    return False
                d = data[-i - 1]
                if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol >= 0.6:
                    return False
            return True
        except:
            pass

    def rule2(self):
        data = self.data
        stock = self.stock
        if not model_1(stock, data):
            return False
        if not model_1(stock, data, 1):
            return False
        if data[-1].turnover > 1.8 * data[-2].turnover:
            if data[-1].turnover > 1:
                return True

    def rule3(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(1, 4):
            if not t_limit(stock, data, i - 1):
                return False
            if t_open_pct(data, i - 1) >= -0.01:
                continue
            if t_close_pct(data, i - 1) > limit(stock) / 100:
                count += 1
        return count >= 2

    def rule4(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data, 2):
            return False
        if model_1(stock, data, 2):
            return False
        if t_low_pct(data, 1) > 0.07:
            if data[-2].turnover > data[-3].turnover:
                if data[-2].firstLimitTime > data[-3].firstLimitTime + timeDelta(data[-3].date, data[-2].date):
                    return True

    def rule5(self):
        data = self.data
        stock = self.stock
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if model_1(stock, data, 1):
            return False
        if not model_1(stock, data):
            return False
        return data[-1].turnover > data[-2].turnover * 2

    def rule6(self):
        data = self.data
        stock = self.stock
        try:
            count = 0
            for i in range(30, 121):
                if t_limit(stock, data, i):
                    count += 1
                if count >= 5:
                    return False
            if data[-31].close / data[-121].close > 2.2:
                return True
        except:
            pass

    def rule7(self):
        data = self.data
        stock = self.stock
        if data[-1].TP / weakenedIndex(self.shIndex, weak_degree=5) >= 50:
            return False
        if t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if model_1(stock, data):
            return False
        matchTime = joinTimeToStamp(data[-1].date, '09:37:00')
        if data[-1].lastLimitTime < matchTime:
            return True

    def rule8(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data, 2):
            return False
        if data[-2].turnover > 2 * data[-3].turnover:
            if data[-1].turnover > 2 * data[-2].turnover:
                if not model_1(stock, data, 1):
                    return True

    def rule9(self):
        data = self.data
        stock = self.stock
        for i in range(1, 3):
            if not t_limit(stock, data, i):
                return False
        for i in range(2):
            if model_1(stock, data, i):
                return False
        for i in range(1, 3):
            if t_open_pct(data, i) < -0.04:
                if t_low_pct(self.gemIndex, i) > -0.01:
                    return True

    def rule10(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(1, 6):
            if not t_limit(stock, data, i - 1):
                continue
            if t_low_pct(data, i - 1) < -0.055 and t_high_pct(data, i - 1) > limit(stock) / 100:
                count += 1
            if count >= 2:
                return True

    def rule11(self):
        data = self.data
        stock = self.stock
        for i in range(1, 4):
            if not t_limit(stock, data, i - 1):
                return False
            if t_open_pct(data, i - 1) >= 0.035:
                return False
        return True

    def rule12(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        if t_limit(stock, data, 3):
            return False
        if not t_limit(stock, data, 1):
            return False
        if model_1(stock, data, 1):
            return False
        if not model_1(stock, data):
            return False
        if data[-1].turnover > 0.5 * data[-2].turnover:
            if data[-1].buy_elg_vol < data[-1].sell_elg_vol:
                return True

    def rule13(self):
        data = self.data
        try:
            flag = True
            for i in range(1, 61):
                t1 = data[-i]
                t2 = data[-i - 1]
                t3 = data[-i - 2]
                if t3.turnover < t2.turnover < t1.turnover:
                    if t3.close < t2.close < t1.close:
                        flag = False
                        break
            return flag
        except:
            pass

    def rule14(self):
        data = self.data
        try:
            for i in range(2, 32):
                if t_high_pct(data, i) > 0.049:
                    return False
            return data[-1].CP < 55
        except:
            return False

    def rule15(self):
        data = self.data
        stock = self.stock
        for i in range(2, 5):
            if t_limit(stock, data, i):
                return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if data[-2].turnover > 3 * sum([_.turnover for _ in data[-12:-2]]) / 3:
            if data[-1].turnover > 3 * sum([_.turnover for _ in data[-12:-2]]) / 3:
                return True

    def rule16(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            if not t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            matchTime = date_util.joinTimeToStamp(data[-1].date, '10:00:00')
            if data[-1].firstLimitTime > matchTime:
                d = data[-1]
                if (d.buy_elg_vol + d.buy_lg_vol) < (d.sell_elg_vol + d.sell_lg_vol):
                    if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol < 0.3:
                        return True
        except:
            pass

    def rule17(self):
        data = self.data
        stock = self.stock
        turnover = -1
        if (model_1(stock, data) and model_1(stock, data, 1)) is True:
            return False
        for i in range(4):
            if not t_limit(stock, data, i):
                return False
            if turnover < data[-i - 1].turnover:
                turnover = data[-i - 1].turnover
            else:
                return False
        return True

    def rule18(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data, 3):
            return False
        if model_1(stock, data, 2):
            return False
        if not t_limit(stock, data, 3):
            return False
        if not t_limit(stock, data, 2):
            return False
        if not model_1(stock, data, 1):
            return False
        if not model_1(stock, data):
            return False
        if data[-2].turnover > (1 / 3) * data[-3].turnover:
            return True

    def rule19(self):
        data = self.data
        stock = self.stock
        if t_low_pct(self.shIndex) <= -0.015:
            return False
        for i in range(1, 3):
            if not t_limit(stock, data, i):
                return False
            if model_1(stock, data, i):
                return False
        if not model_1(stock, data):
            return False
        if data[-1].turnover > (1 / 3) * data[-2].turnover:
            return True

    def rule20(self):
        data = self.data
        stock = self.stock
        if data[-1].turnover <= data[-2].turnover * 0.8:
            return False
        if not (t_open_pct(data) > t_open_pct(data, 1) > 0.05):
            return False
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if data[-1].lastLimitTime > data[-2].lastLimitTime + timeDelta(data[-2].date, data[-1].date):
            if t_low_pct(self.gemIndex) > -0.01:
                return True

    def rule21(self):
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
        for i in range(2):
            if getMinute(stamp=data[-i - 1].lastLimitTime) >= '0945':
                return False
        return data[-1].turnover > data[-2].turnover * 2

    def rule22(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(1, 3):
                if t_open_pct(data, i) <= limit(stock) / 100:
                    continue
                if t_low_pct(data, i) >= 0.05:
                    continue
                if t_close_pct(data, i) <= limit(stock) / 100:
                    continue
                matchTime = date_util.joinTimeToStamp(data[-i - 1].date, '10:30:00')
                if data[-i - 1].lastLimitTime > matchTime:
                    d = data[-i]
                    if (d.buy_elg_vol + d.buy_lg_vol) / d.volume < 0.5 and d.buy_elg_vol < d.sell_elg_vol:
                        if (d.buy_elg_vol - d.sell_elg_vol) / d.buy_elg_vol < 0.3:
                            return True
        except:
            pass

    def rule23(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 3):
            return False
        if not t_limit(stock, data, 2):
            return False
        if model_1(stock, data, 2):
            return False
        for i in range(2):
            if not model_1(stock, data, i):
                return False
        if data[-3].firstLimitTime < joinTimeToStamp(data[-3].date, '09:40:00'):
            if data[-1].turnover > 1 / 3 * data[-3].turnover:
                return data[-2].turnover > 1 / 3 * data[-3].turnover

    def rule24(self):
        data = self.data
        if t_open_pct(self.data) >= 0.03:
            return False
        matchTime = joinTimeToStamp(data[-1].date, '09:40:00')
        if data[-1].firstLimitTime < matchTime:
            if data[-1].limitOpenTime > 2:
                return True

    def rule25(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        return data[-1].turnover > data[-2].turnover * 2 and getMinute(stamp=data[-1].lastLimitTime) < '0937'

    def rule26(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if t_limit(stock, data, 1):
            return False
        if data[-1].turnover > 16:
            matchTime = joinTimeToStamp(data[-1].date, '13:30:00')
            if data[-1].firstLimitTime > matchTime:
                return True

    def rule27(self):
        data = self.data
        stock = self.stock
        for i in range(3):
            if t_limit(stock, data, i + 2):
                return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        if (data[-3].close - data[-6].close) / data[-6].close > 0.1:
            return True

    def rule28(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data, 1):
                return False
            flag = False
            for i in range(20):
                if t_limit(self.stock, self.data, i):
                    if limit_height(self.stock, self.data, i) <= 1:
                        continue
                    if t_open_pct(self.data, i) > limit(self.stock) / 100:
                        return False
                    flag = True
                    date = self.data[-i - 1].date
                    rank: list = RankLimitStock(self.limitData).by('limitTime-industry+height>1', str(date), eliminateModel1=True)[self.industry]
                    if self.stock in rank[:2]:
                        return False
            return flag
        except:
            pass

    def rule29(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        range30 = data[-37:-7]
        count = 0
        for i in range30:
            if i.close > data[-1].close:
                count += 1
            if count >= 3:
                return True

    def rule30(self):
        data = self.data
        stock = self.stock
        if data[-1].CP / weakenedIndex(self.shIndex) >= 75:
            return False
        if not t_limit(stock, data, 3):
            return False
        if not t_limit(stock, data):
            return False
        if t_limit(stock, data, 2):
            return False
        if t_limit(stock, data, 1):
            return False
        if data[-1].turnover < data[-4].turnover * 0.8:
            return True

    def rule31(self):
        d = self.data[-1]
        if d.turnover > 18:
            if d.limitOpenTime > 3:
                return d.CP / weakenedIndex(self.shIndex) < 60

    def rule32(self):
        data = self.data
        stock = self.stock
        if data[-1].TF >= 60:
            return False
        if t_limit(stock, data, 2):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            if model_1(stock, data, i):
                return False
            d = data[-i - 1]
            matchTime = joinTimeToStamp(d.date, '09:45:00')
            if d.firstLimitTime >= matchTime:
                return False
        for i in range(3, 11):
            if not t_limit(stock, data, i):
                continue
            if not t_limit(stock, data, i - 1):
                return True

    def rule33(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data):
            return False
        if not t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 3):
            return False
        matchTime = joinTimeToStamp(data[-3].date, '10:30:00')
        if data[-3].firstLimitTime <= matchTime:
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            matchTime = joinTimeToStamp(data[-i - 1].date, '09:50:00')
            if data[-i - 1].firstLimitTime >= matchTime:
                return False
        return True

    def rule34(self):
        data = self.data
        stock = self.stock
        try:
            if data[-1].CP / weakenedIndex(self.shIndex, weak_degree=5) >= 65:
                return False
            limitDates = []
            for i in range(90):
                if t_limit(stock, data, i):
                    if t_open_pct(data, i) > limit(stock) / 100:
                        continue
                    limitDates.append(data[-i - 1].date)
                    if len(limitDates) >= 2:
                        break
            if len(limitDates) < 2:
                return False
            for date in limitDates:
                rank = RankLimitStock(self.limitData).by('limitTime-industry', str(date), eliminateModel1=True)[self.industry]
                if stock in rank[:3]:
                    return False
            return True
        except:
            pass

    def rule35(self):
        data = self.data
        stock = self.stock
        try:
            if t_open_pct(data) > limit(stock) / 100:
                return False
            for i in range(3):
                if not t_limit(stock, data, i):
                    return False
            rank: list = RankLimitStock(self.limitData).by('open-industry', self.data[-1].date)[self.industry]
            if self.stock in rank[:2]:
                return False
            return True
        except:
            pass

    def rule37(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data, 2):
                return False
            for i in range(2):
                if t_open_pct(data, i) > limit(stock) / 100:
                    return False
                if not t_limit(stock, data, i):
                    return False
                rank: list = RankLimitStock(self.limitData).by('open-industry', data[-i - 1].date)[self.industry]
                if stock in rank[:2]:
                    return False
            return True
        except:
            pass

    def rule38(self):
        data = self.data
        stock = self.stock
        try:
            if model_1(stock, data):
                return False
            if not t_limit(stock, data, 2):
                return False
            for i in range(2):
                if t_open_pct(data, i) > limit(stock) / 100:
                    return False
                if not t_limit(stock, data, i):
                    return False
                rank: list = RankLimitStock(self.limitData).by('open-height', data[-i - 1].date, eliminateModel1=True)[self.height]
                if stock in rank[:2]:
                    return False
            return True
        except:
            pass

    def rule39(self):
        try:
            if self.data[-1].TF > 70 and self.data[-1].TP > 35:
                return False
            for i in range(3, 43):
                if t_close_pct(self.data, i) > 0.04:
                    return False
            return True
        except:
            pass

    def rule40(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if t_limit(stock, data, 1):
            return False
        return t_low_pct(data) < -0.02 and data[-1].limitOpenTime > 3

    def rule41(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if data[-1].high == max([_.high for _ in data[-20:]]):
            return False
        return data[-1].turnover > 15

    def rule42(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 3):
            return False
        for i in range(3):
            if not model_1(stock, data, i):
                return False
        return data[-1].turnover > 1.8 * data[-2].turnover

    def rule43(self):
        data = self.data
        stock = self.stock
        if data[-1].turnover <= data[-1].turnover * 1.1:
            return False
        for i in [3, 4]:
            if t_limit(stock, data, i):
                return False
        for i in [0, 1]:
            if not model_1(stock, data, i):
                return False
        for i in range(5, 16):
            if t_limit(stock, data, i):
                return True

    def rule44(self):
        try:
            data = self.data
            stock = self.stock
            if t_limit(stock, data, 3):
                return False
            for i in range(3):
                if not t_limit(stock, data, i):
                    return False
            if not model_t(stock, data, 1):
                return False
            if not model_1(stock, data):
                return False
            return sum([data[-i - 1].turnover for i in range(4, 21)]) / 17 < 3
        except:
            ...

    def rule45(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        flag = 10000
        for i in range(1, 5):
            if not data[-i - 1].close < flag:
                return False
            flag = data[-i - 1].close
        return getMinute(stamp=data[-1].firstLimitTime) < '0937'

    def rule46(self):
        data = self.data
        stock = self.stock
        if t_high_pct(data, 1) <= 0.075:
            return False
        if t_close_pct(data, 1) >= 0.025:
            return False
        flag = 10000
        for i in range(1, 4):
            if not data[-i - 1].close < flag:
                return False
            flag = data[-i - 1].close
        return getMinute(stamp=data[-1].firstLimitTime) < '0937'

    def rule47(self):
        data = self.data
        stock = self.stock
        if t_high_pct(data, 2) <= 0.075:
            return False
        if t_close_pct(data, 1) >= -0.075:
            return False
        return getMinute(stamp=data[-1].firstLimitTime) < '0937'

    def rule48(self):
        data = self.data
        stock = self.stock
        if t_close_pct(data, 1) >= -0.075:
            return False
        flag = 10000
        for i in range(2, 6):
            if not data[-i - 1].close < flag:
                return False
            flag = data[-i - 1].close
        return getMinute(stamp=data[-1].firstLimitTime) < '0937'

    def rule49(self):
        data = self.data
        stock = self.stock
        if t_high_pct(data, 1) <= 0.08:
            return False
        if t_close_pct(data, 1) >= 0.04:
            return False
        return getMinute(stamp=data[-1].firstLimitTime) < '0940'

    def rule50(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 1):
                return False
            return sum([data[-_ - 1].turnover for _ in range(1, 26)]) < sum([data[-_ - 1].turnover for _ in range(26, 51)]) and getMinute(
                stamp=data[-1].firstLimitTime) < '0940'
        except:
            ...

    def rule51(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 1):
                return False
            return data[-1].turnover > max([data[-i - 1].turnover for i in range(1, 11)]) / 2 and getMinute(stamp=data[-1].firstLimitTime) < '0940'
        except:
            ...

    def rule52(self):
        data = self.data
        stock = self.stock
        if t_high_pct(data, 2) <= 0.08:
            return False
        if t_close_pct(data, 2) >= 0.04:
            return False
        if t_limit(stock, data, 2):
            return False
        for i in range(2):
            if getMinute(stamp=data[-i - 1].firstLimitTime) >= '0940':
                return False
        return True
