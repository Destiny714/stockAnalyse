# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:25
# @Author  : Destiny_
# @File    : levelF4.py
# @Software: PyCharm
from utils.stockdata_util import *
from base.base_level_model import base_level
from models.stockDetailModel import stockDetailModel


class levelF4(base_level):
    def __init__(self, stockDetail: stockDetailModel, data: list[dataModel], index: list[dataModel], limitData: dict[str, list[limitDataModel]]):
        self.level = 'F4'
        super().__init__(self.level, stockDetail, data, index, limitData)

    def rule1(self):
        data = self.data
        stock = self.stock
        if data[-1].limitOpenTime() <= 1:
            return False
        count = 0
        limitCount = 0
        for i in range(1, 6):
            if t_limit(stock, data, i - 1):
                limitCount += 1
            if t_open_pct(data, i - 1) >= -0.01:
                continue
            if t_close_pct(data, i - 1) > limit(stock) / 100:
                count += 1
        if count >= 2 and limitCount >= 3:
            return True

    def rule2(self):
        data = self.data
        stock = self.stock
        if data[-1].limitOpenTime() <= 1:
            return False
        limitCount = 0
        for i in range(5):
            if t_limit(stock, data, i):
                limitCount += 1
        if limitCount < 3:
            return False
        for i in range(3):
            if t_low_pct(data, i) < -0.06 and t_close_pct(data, i) > limit(stock) / 100:
                return True

    def rule3(self):
        data = self.data
        count = 0
        for i in range(1, 6):
            if t_open_pct(data, i - 1) <= 0.08:
                continue
            matchTime = joinTimeToStamp(data[-i].date(), '10:00:00')
            if data[-i].lastLimitTime() > matchTime:
                count += 1
            if count >= 2:
                return True

    def rule4(self):
        data = self.data
        stock = self.stock
        if model_1(stock, data, 1):
            return False
        if not model_1(stock, data):
            return False
        if data[-1].turnover() > data[-2].turnover() / 3:
            if data[-1].buy_elg_vol() < data[-1].sell_elg_vol():
                return True

    def rule5(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(3):
                if not t_limit(stock, data, i):
                    return False
            if sum([data[-1].turnover(), data[-2].turnover(), data[-3].turnover()]) <= 40:
                return False
            matchTime = date_util.joinTimeToStamp(data[-1].date(), '10:00:00')
            if data[-1].firstLimitTime() > matchTime and data[-1].lastLimitTime() > matchTime:
                d = data[-1]
                if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                        d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
                    return True
        except:
            pass

    def rule6(self):
        data = self.data
        stock = self.stock
        if data[-5].pctChange() > limit(stock):
            return False
        if data[-4].pctChange() > limit(stock):
            return False
        if model_1(stock, data, 2):
            return False
        if data[-3].pctChange() <= limit(stock):
            return False
        if not model_1(stock, data, 1):
            return False
        if t_open_pct(data) < limit(stock) / 100:
            return False
        if t_low_pct(data) >= limit(stock) / 100:
            return False
        if not model_t(stock, data):
            return False
        if data[-1].turnover() > 1.8 * max([_.turnover() for _ in data[-6:-1]]):
            return True

    def rule7(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        if data[-1].turnover() <= 1.8 * data[-2].turnover():
            return False
        standard = (sum([data[-_].turnover() for _ in range(3, 8)]) / 5) * 3
        if data[-1].turnover() > standard and data[-2].turnover() > standard:
            return True

    def rule8(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data):
                return False
            if not t_limit(stock, data, 1):
                return False
            if data[-1].turnover() > 3 * data[-2].turnover():
                matchTime = joinTimeToStamp(data[-1].date(), '11:00:00')
                if data[-1].firstLimitTime() > matchTime and data[-1].lastLimitTime() > matchTime:
                    d = data[-1]
                    if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                            d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
                        return True
        except:
            pass

    def rule9(self):
        data = self.data
        stock = self.stock
        for i in range(20):
            if not model_1(stock, data, i):
                continue
            if model_1(stock, data, i + 1):
                continue
            if data[-i - 1].turnover() > 1:
                if data[-i - 1].turnover() > max([_.turnover() for _ in data[-i - 6:-i - 1]]) / 2:
                    return True

    def rule10(self):
        data = self.data
        if data[-1].turnover() <= 10:
            return False
        try:
            range60 = data[-61:-1]
            if data[-1].turnover() > 2.5 * max([_.turnover() for _ in range60]):
                return True
        except:
            return False

    def rule11(self):
        data = self.data
        stock = self.stock
        if not model_1(stock, data):
            return False
        if not model_1(stock, data, 1):
            return False
        if (data[-1].turnover() + data[-2].turnover()) / 2 > 0.25 * max([_.turnover() for _ in data[-20:]]):
            return True

    def rule12(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        matchTime = joinTimeToStamp(data[-1].date(), '14:30:00')
        if data[-1].lastLimitTime() <= matchTime:
            return False
        if data[-1].limitOpenTime() > 3:
            if t_low_pct(self.index) > -0.01:
                return True

    def rule13(self):
        data = self.data
        stock = self.stock
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
            matchTime = date_util.joinTimeToStamp(data[-i - 1].date(), '09:40:00')
            if data[-i - 1].firstLimitTime() >= matchTime:
                return False
            if data[-i - 1].limitOpenTime() <= 2:
                return False
            if data[-i - 1].turnover() <= data[-3].turnover():
                return False
        return True

    def rule14(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(1, 5):
            if not t_limit(stock, data, i - 1):
                return False
            matchTime = joinTimeToStamp(data[-i].date(), '10:15:00')
            if data[-i].lastLimitTime() > matchTime and data[-i].firstLimitTime() > matchTime:
                count += 1
        return count >= 3

    def rule15(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            range5 = data[-6:-1]
            range10 = data[-11:-1]
            if data[-1].turnover() > 2 * (sum([_.turnover() for _ in range5]) / 5):
                if data[-1].turnover() > 3 * (sum([_.turnover() for _ in range10]) / 10):
                    return True
        except:
            pass

    def rule16(self):
        data = self.data
        stock = self.stock
        for i in range(5):
            if t_open_pct(data, i) <= limit(stock) / 100:
                continue
            if t_low_pct(data, i) >= 0.06:
                continue
            if not t_limit(stock, data, i):
                continue
            if data[-i - 1].limitOpenTime() > 3:
                d = data[-i - 1]
                if (d.buy_elg_vol() + d.buy_lg_vol()) < (d.sell_elg_vol() + d.sell_lg_vol()):
                    if t_low_pct(self.index, i) > -0.01:
                        return True

    def rule17(self):
        data = self.data
        stock = self.stock
        for i in range(1, 4):
            if not t_limit(stock, data, i - 1):
                return False
        if t_open_pct(data, 1) >= 0.03:
            return False
        if t_open_pct(data) >= 0.03:
            return False
        return True

    def rule18(self):
        data = self.data
        stock = self.stock
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        matchTime0 = joinTimeToStamp(data[-1].date(), '10:15:00')
        matchTime1 = joinTimeToStamp(data[-2].date(), '10:15:00')
        if data[-1].firstLimitTime() > matchTime0 and data[-2].firstLimitTime() > matchTime1:
            return True

    def rule19(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if not t_limit(stock, data, 1):
            return False
        for i in range(2):
            matchTime = joinTimeToStamp(data[-i - 1].date(), '13:00:00')
            if data[-i - 1].lastLimitTime() <= matchTime:
                return False
        if data[-1].turnover() > data[-3].turnover() * 5:
            if data[-2].turnover() > data[-3].turnover() * 5:
                return True

    def rule20(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        if t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if model_1(stock, data):
            return False
        if data[-1].turnover() < 0.5 * data[-2].turnover():
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.5:
                return True

    def rule21(self):
        data = self.data
        stock = self.stock
        try:
            if data[-1].limitOpenTime() == 0:
                return False
            if t_limit(stock, data, 2):
                return False
            if not t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            if data[-1].firstLimitTime() <= data[-2].firstLimitTime() + timeDelta(data[-2].date(), data[-1].date()):
                return False
            if data[-1].lastLimitTime() <= data[-2].lastLimitTime() + timeDelta(data[-2].date(), data[-1].date()):
                return False
            if t_low_pct(self.index) > -0.01:
                if data[-1].timeVol(timeStamp=data[-1].firstLimitTime()) < 100000:
                    return True
        except:
            pass

    def rule22(self):
        data = self.data
        stock = self.stock
        try:
            if data[-1].limitOpenTime() == 0:
                return False
            if t_limit(stock, data, 2):
                return False
            if not t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            matchTime = joinTimeToStamp(data[-1].date(), '10:30:00')
            if data[-1].firstLimitTime() > matchTime and data[-1].lastLimitTime() > matchTime:
                if data[-1].timeVol(timeStamp=data[-1].firstLimitTime()) < 100000:
                    return True
        except:
            pass

    def rule23(self):
        data = self.data
        stock = self.stock
        for i in range(1, 4):
            if not t_limit(stock, data, i - 1):
                return False
        if data[-2].turnover() >= data[-3].turnover():
            return False
        if data[-1].turnover() <= data[-2].turnover():
            return False
        if t_low_pct(data) >= 0.03:
            return False
        if data[-1].limitOpenTime() <= 2:
            return False
        if t_open_pct(data, 2) < t_open_pct(data, 1) < t_open_pct(data, 0):
            if t_low_pct(self.index) > -0.01:
                return True

    def rule24(self):
        data = self.data
        stock = self.stock
        try:
            if not t_limit(stock, data):
                return False
            if not t_limit(stock, data, 1):
                return False
            if data[-2].limitOpenTime() <= 1:
                return False
            matchTime = joinTimeToStamp(data[-1].date(), '09:45:00')
            if data[-1].firstLimitTime() <= matchTime:
                return False
            if data[-1].timeVol(timeStamp=data[-1].firstLimitTime()) >= 100000:
                return False
            if data[-1].lastLimitTime() > data[-2].lastLimitTime() + timeDelta(data[-2].date(),
                                                                               data[-1].date()):
                if t_low_pct(self.index) > -0.01:
                    return True
        except:
            pass

    def rule25(self):
        data = self.data
        stock = self.stock
        try:
            count = 0
            for i in range(1, 6):
                if not t_limit(stock, data, i - 1):
                    continue
                if data[-i].limitOpenTime() > 5:
                    d = data[-i]
                    if (d.buy_elg_vol() + d.buy_lg_vol() - d.sell_elg_vol() - d.sell_lg_vol()) / (
                            d.buy_elg_vol() + d.buy_lg_vol()) < 0.2:
                        count += 1
                if count >= 2:
                    return True
        except:
            pass

    def rule26(self):
        data = self.data
        stock = self.stock
        if t_limit(stock, data, 2):
            return False
        if not t_limit(stock, data, 1):
            return False
        if not t_limit(stock, data):
            return False
        if data[-1].turnover() <= data[-2].turnover():
            return False
        range10 = data[-12:-2]
        if data[-2].turnover() > 3 * (sum([_.turnover() for _ in range10]) / 10):
            if t_open_pct(data) < 0.03:
                return True

    def rule27(self):
        data = self.data
        stock = self.stock
        for i in range(3, 153):
            if not t_limit(stock, data, i):
                continue
            if not t_limit(stock, data, i + 1):
                continue
            if t_limit(stock, data, i - 1):
                continue
            nxt = data[-i]
            if nxt.turnover() <= 1.5 * data[-1].turnover():
                continue
            if nxt.high() * 1.03 <= data[-1].close():
                continue
            matchTime = joinTimeToStamp(data[-i - 1].date(), '10:00:00')
            if data[-i - 1].firstLimitTime() > matchTime:
                return True

    def rule28(self):
        data = self.data
        stock = self.stock
        for i in range(3):
            if not t_limit(stock, data, i):
                return False
        if data[-1].turnover() > data[-2].turnover() > data[-3].turnover() > 15:
            return True

    def rule29(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            if not t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            if data[-1].turnover() <= data[-2].turnover():
                return False
            matchTime = joinTimeToStamp(data[-1].date(), '09:45:00')
            if data[-1].firstLimitTime() <= matchTime:
                return False
            if data[-1].timeVol(timeStamp=data[-1].firstLimitTime()) >= 100000:
                return False
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / (d.buy_elg_vol()) < 0.3:
                if t_low_pct(data) < t_open_pct(data):
                    return True
        except:
            pass

    def rule30(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            if not t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            if data[-1].turnover() <= data[-2].turnover() * 0.8:
                return False
            if t_open_pct(data) >= 0.035:
                return False
            matchTime = joinTimeToStamp(data[-1].date(), '09:50:00')
            if data[-1].firstLimitTime() > matchTime:
                if data[-1].timeVol(timeStamp=data[-1].firstLimitTime()) < 100000:
                    if t_low_pct(data) < t_open_pct(data):
                        return True
        except:
            pass

    def rule31(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            if not t_limit(stock, data, 1):
                return False
            if not t_limit(stock, data):
                return False
            if data[-1].turnover() <= data[-2].turnover():
                return False
            range5 = data[-7:-2]
            if data[-2].turnover() > 3 * (sum([_.turnover() for _ in range5]) / 5):
                if data[-1].timeVol(timeStamp=data[-1].firstLimitTime()) < 100000:
                    return True
        except:
            pass

    def rule32(self):
        data = self.data
        stock = self.stock
        try:
            d = data[-1]
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() >= 0.7:
                return False
            for i in range(10, 51):
                if limit_height(stock, data, i) >= 3:
                    return False
            for i in range(3, 153):
                if not t_limit(stock, data, i):
                    continue
                if t_limit(stock, data, i - 1):
                    continue
                if t_limit(stock, data, i + 1):
                    continue
                if data[-i].turnover() > 1.5 * data[-1].turnover():
                    if data[-i].high() * 1.03 > data[-1].close():
                        if t_limit(stock, data):
                            return True
        except:
            return False

    def rule33(self):
        data = self.data
        stock = self.stock
        try:
            if t_limit(stock, data, 2):
                return False
            for i in range(2):
                if not t_limit(stock, data, i):
                    return False
                if t_open_pct(data, i) >= 0.03:
                    return False
            matchTime = date_util.joinTimeToStamp(data[-1].date(), '09:45:00')
            if data[-1].firstLimitTime() <= matchTime:
                return False
            if data[-1].timeVol(timeStamp=data[-1].firstLimitTime()) >= 100000:
                return False
            if data[-1].turnover() > data[-2].turnover():
                return True
        except:
            pass

    def rule34(self):
        data = self.data
        stock = self.stock
        if t_low_pct(data) >= 0.035:
            return False
        if t_limit(stock, data, 2):
            return False
        for i in range(2):
            if not t_limit(stock, data, i):
                return False
        matchTime = joinTimeToStamp(data[-1].date(), '09:50:00')
        if data[-1].firstLimitTime() <= matchTime:
            return False
        if data[-1].turnover() > data[-2].turnover():
            matchTime = joinTimeToStamp(data[-2].date(), '09:40:00')
            if data[-2].firstLimitTime() < matchTime:
                if t_low_pct(data) < t_open_pct(data):
                    return True

    def rule35(self):
        data = self.data
        stock = self.stock
        try:
            range4MaxClose = max([_.close() for _ in data[-5:-1]])
            if not t_limit(stock, data):
                return False
            if t_limit(stock, data, 1):
                return False
            for i in range(3, 153):
                if not t_limit(stock, data, i):
                    continue
                if t_limit(stock, data, i - 1):
                    continue
                flag = False
                for j in range(2):
                    if t_limit(stock, data, i + j):
                        flag = True
                        break
                if flag:
                    continue
                if data[-i].turnover() > 1.3 * data[-1].turnover():
                    if data[-i].high() * 1.03 > data[-1].close():
                        if data[-i].open() > range4MaxClose:
                            return True
        except:
            return False

    def rule36(self):
        data = self.data
        stock = self.stock
        try:
            if t_open_pct(data) >= t_open_pct(data, 1):
                return False
            if t_low_pct(data) >= 0.05:
                return False
            flag = False
            for i in range(3, 153):
                if not t_limit(stock, data, i):
                    continue
                if t_limit(stock, data, i - 1):
                    continue
                if data[-i].turnover() > 1.5 * data[-1].turnover():
                    if data[-i].high() * 1.03 > data[-2].close():
                        flag = True
                        break
            if not flag:
                return False
            if not t_limit(stock, data, 1):
                return False
            if t_limit(stock, data, 2):
                return False
            matchTime = joinTimeToStamp(data[-2].date(), '09:50:00')
            if data[-2].firstLimitTime() < matchTime:
                return True
        except:
            return False

    def rule37(self):
        data = self.data
        try:
            d = data[-1]
            if d.buy_elg_vol() / d.volume() >= 0.35:
                return False
            if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() >= 0.6:
                return False
            badCount = 0
            for i in range(50):
                j = i + 1
                ma30 = [data[-_] for _ in range(j, j + 30)]
                ma60 = [data[-_] for _ in range(j, j + 60)]
                avg30 = sum(_.close() for _ in ma30) / len(ma30)
                avg60 = sum(_.close() for _ in ma60) / len(ma60)
                if avg30 < avg60:
                    badCount += 1
                if badCount >= 15:
                    return True
        except:
            return False

    def rule38(self):
        data = self.data
        stock = self.stock
        try:
            if model_1(stock, data):
                return False
            if not t_limit(stock, data):
                return False
            limitTime = data[-1].firstLimitTime()
            limitMinute = getMinute(limitTime)
            limitMinuteLast = lastMinute(limitMinute)
            if data[-1].timeVol(minute=limitMinute) < data[-1].timeVol(minute=limitMinuteLast) * 3:
                d = data[-1]
                if (d.buy_elg_vol() - d.sell_elg_vol()) / d.buy_elg_vol() < 0.4:
                    if t_low_pct(data) < t_open_pct(data):
                        return True
        except:
            return False

    def rule39(self):
        data = self.data
        flag = False
        for i in range(20):
            if t_low_pct(self.index, i) < -0.02:
                continue
            if move_avg(data, 30, i) < move_avg(data, 60, i):
                flag = True
                break
        if not flag:
            return False
        count = 0
        for i in range(10):
            if data[-i - 1].close() < move_avg(data, 30, i):
                count += 1
            if count >= 3:
                return True

    def rule40(self):
        data = self.data
        try:
            badCount10 = 0
            for i in range(10):
                if t_low_pct(self.index, i) < -0.02:
                    continue
                if data[-i - 1].close() < move_avg(data, 20, i):
                    badCount10 += 1
                    if badCount10 >= 2:
                        return True
        except:
            return False

    def rule41(self):
        data = self.data
        count1 = 0
        count2 = 0
        for i in range(30):
            ma60 = move_avg(data, 60, i)
            if i in range(20) and count1 == 0:
                ma30 = move_avg(data, 30, i)
                if ma30 < ma60:
                    count1 += 1
            if data[-i - 1].close() < move_avg(data, 60, i):
                count2 += 1
            if count1 >= 1 and count2 >= 3:
                return True

    def rule42(self):
        data = self.data
        try:
            badCount1 = 0
            badCount2 = 0
            for i in range(40):
                j = i + 1
                ma60 = [data[-_] for _ in range(j, j + 60)]
                avg60 = sum(_.close() for _ in ma60) / len(ma60)
                if data[-i - 1].close() < avg60:
                    if t_low_pct(self.index, i) > -0.01:
                        badCount1 += 1
                if i in range(10) and badCount2 == 0:
                    ma10 = [data[-_] for _ in range(j, j + 10)]
                    ma30 = [data[-_] for _ in range(j, j + 30)]
                    avg10 = sum(_.close() for _ in ma10) / len(ma10)
                    avg30 = sum(_.close() for _ in ma30) / len(ma30)
                    if avg10 < avg30 < avg60:
                        badCount2 += 1
                if badCount1 >= 3 and badCount2 > 0:
                    return True
        except:
            return False

    def rule43(self):
        data = self.data
        stock = self.stock
        try:
            for i in range(10, 51):
                if limit_height(stock, data, i) >= 3:
                    return False
            badCount = 0
            for i in range(10):
                if t_low_pct(self.index, i) <= -0.02:
                    continue
                if data[-i - 1].close() < move_avg(data, 60, i):
                    badCount += 1
                if badCount >= 2:
                    return True
        except:
            return False

    def rule44(self):
        data = self.data
        try:
            badCount10 = 0
            badCount40 = 0
            for i in range(40):
                j = i + 1
                if t_low_pct(self.index, i) <= -0.02:
                    continue
                if i in range(10):
                    ma20 = [data[-_] for _ in range(j, j + 20)]
                    avg20 = sum(_.close() for _ in ma20) / len(ma20)
                    if data[-i - 1].close() < avg20:
                        badCount10 += 1
                ma60 = [data[-_] for _ in range(j, j + 60)]
                avg60 = sum(_.close() for _ in ma60) / len(ma60)
                if data[-i - 1].close() < avg60:
                    badCount40 += 1
                if badCount10 >= 2 and badCount40 >= 3:
                    return True
        except:
            return False

    def rule45(self):
        data = self.data
        stock = self.stock
        for i in range(3, 153):
            if not t_limit(stock, data, i):
                continue
            if t_limit(stock, data, i - 1):
                continue
            if t_high_pct(data, i - 1) > max([_.high() for _ in data[-5:]]):
                return True

    def rule46(self):
        data = self.data
        stock = self.stock
        try:
            d = data[-1]
            if d.buy_elg_vol() / d.volume() >= 0.45:
                return False
            for i in range(3, 153):
                if not t_limit(stock, data, i):
                    continue
                if t_limit(stock, data, i - 1):
                    continue
                flag = False
                for j in range(2):
                    if t_limit(stock, data, i + j):
                        flag = True
                        break
                if flag:
                    continue
                nxt = data[-i]
                if nxt.turnover() > 1.3 * data[-1].turnover():
                    if nxt.high() * 1.03 > data[-1].close():
                        if nxt.high() > max([_.close() for _ in data[-5:]]):
                            return True
        except:
            pass

    def rule47(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        if data[-1].turnover() <= 3 * sum([_.turnover() for _ in data[-11:-1]]) / 10:
            return False
        if data[-1].turnover() <= 2 * sum([_.turnover() for _ in data[-6:-1]]) / 5:
            return False
        for i in range(3, 153):
            if not t_limit(stock, data, i):
                continue
            if t_limit(stock, data, i - 1):
                continue
            if data[-i].high() * 1.03 > data[-1].close():
                return True

    def rule48(self):
        data = self.data
        stock = self.stock
        if not t_limit(stock, data):
            return False
        for i in range(3, 153):
            if not t_limit(stock, data, i):
                continue
            if t_limit(stock, data, i - 1):
                continue
            if data[-i].high() * 1.03 > data[-1].close():
                if t_down_limit(stock, data, i):
                    return True

    def rule49(self):
        data = self.data
        stock = self.stock
        count = 0
        for i in range(3, 153):
            if not t_limit(stock, data, i):
                continue
            if not t_limit(stock, data, i + 1):
                continue
            if t_limit(stock, data, i - 1):
                continue
            if data[-i].high() * 1.03 > data[-1].close():
                if data[-i].turnover() > data[-1].turnover() * 1.5:
                    count += 1
            if count >= 2:
                return True
