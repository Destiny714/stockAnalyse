# -*- coding: utf-8 -*-
# @Time    : 2023/3/26 13:14
# @Author  : Destiny_
# @File    : rules.py
# @Software: PyCharm

from database import db
from typing import Optional
from models.stock_data_model import StockDataModel
from models.stock_detail_model import StockDetailModel
from utils.stockdata_util import queryData, move_avg, t_close_pct, t_limit, limit_height, t_low_pct, getMinute, t_high_pct, t_down_limit


def boom_rule(stock: str, date=''):
    client = db.Stock_Database()
    try:
        detail = StockDetailModel(client.selectStockDetail(stock))
        if not detail.amount > 150e5:
            return
        data = queryData(stock, 300, date)
        if sum([data[-i - 1].amount for i in range(3)]) / 3 < 8e5:
            return
        if not 25e4 < data[-1].amount < 35e5:
            return
        count1 = 0
        for i in range(5):
            d = data[-i - 1]
            if d.close > move_avg(data, 5, i):
                count1 += 1
        if count1 < 4:
            count2 = 0
            for i in range(10):
                if data[-i - 1].close > move_avg(data, 5, i):
                    count2 += 1
            if count2 < 8:
                return
        if not (max([data[-i - 1].high for i in range(1, 10)]) - min([data[-i - 1].low for i in range(1, 10)])) / min(
                [data[-i - 1].low for i in range(1, 10)]) < 0.45:
            return
        limitCount = 0
        for i in range(10):
            if t_limit(stock, data, i):
                limitCount += 1
            if limitCount > 1:
                return
        for i in range(1, 8):
            d = data[-i - 1]
            max8to200 = max([data[-j - 1].high for j in range(8, 201)])
            if d.open > d.close:
                continue
            if not t_close_pct(data, i) > 0.06:
                continue
            boomDay = d.date
            if not d.close > max8to200:
                continue
            if not d.turnover > data[-1].turnover * 1.48:
                continue
            if d.limitOpenTime >= 3 and t_limit(stock, data, i):
                continue
            shrinkDay = data[-1].date
            if d.open < data[-1].close:
                name = client.selectNameByStock(stock)
                res = {"stock": stock, "name": name, "boomDay": boomDay, "shrinkDay": shrinkDay}
                return res
        return None
    except:
        return None
    finally:
        client.close()


class BoomRule(object):

    def __init__(self, stock: str, date=''):
        self.stock = stock
        self.boomDay = None
        self.boomData: Optional[StockDataModel] = None
        self.client = db.Stock_Database()
        self.data = queryData(stock, 300, date)
        self.detail = StockDetailModel(self.client.selectStockDetail(stock))
        self.dates = [_.date for _ in self.data]

    # def rule1(self):
    #     if self.detail.amount > 150e5:
    #         return True

    def rule2(self):
        if 25e4 < self.data[-1].amount:
            return True

    def rule3(self):
        data = self.data
        a = len([i for i in range(5) if data[-i - 1].close > move_avg(data, 5, i)]) >= 4
        b = len([i for i in range(10) if data[-i - 1].close > move_avg(data, 5, i)]) >= 8
        c = len([i for i in range(10) if data[-i - 1].close > move_avg(data, 10, i)]) >= 8 and len(
            [i for i in range(10) if data[-i - 1].close > move_avg(data, 5, i)]) >= 7
        d = len([i for i in range(20) if data[-i - 1].close > move_avg(data, 20, i)]) >= 19
        return a or b or c or d

    def rule4(self):
        data = self.data
        limit = 0.6 if self.stock[:2] in ['30', '68'] else 0.4
        if (max([data[-i - 1].high for i in range(1, 10)]) - min([data[-i - 1].low for i in range(1, 10)])) / min(
                [data[-i - 1].low for i in range(1, 10)]) < limit:
            return True

    def rule5(self):
        limitCount = 0
        for i in range(5):
            if t_limit(self.stock, self.data, i):
                limitCount += 1
            if limitCount > 1:
                return False
        return True

    def rule6(self):
        data = self.data
        limit = 0.09 if self.stock[:2] in ['30', '68'] else 0.065
        for i in range(1, 6):
            d = data[-i - 1]
            nxt = data[-i]
            max8to200 = max([data[-j - 1].close for j in range(5, 201)])
            if not t_close_pct(data, i) > limit:
                continue
            if not d.close > max8to200:
                continue
            if not d.turnover > data[-1].turnover * 1.29:
                continue
            if not d.turnover < nxt.turnover * 1.75:
                continue
            if not (d.high - d.close) / (d.close - d.open) < 3 / 5:
                continue
            if not t_low_pct(data, i) > -0.025:
                continue
            if t_limit(self.stock, data, i):
                if not (d.limitOpenTime < 3 or getMinute(stamp=d.firstLimitTime) < '1400'):
                    continue
            else:
                limitPercent = 0.198 if self.stock[:2] in ['30', '68'] else 0.098
                if t_high_pct(data, i) >= limitPercent:
                    continue
            self.boomDay = d.date
            self.boomData = d
            return True

    def rule7(self):
        return True
        # data = self.data
        # count1 = 0
        # count2 = 0
        # for i in range(1, 31):
        #     ma30 = move_avg(data, 30, i)
        #     if i in range(10):
        #         if data[-i - 1].close > ma30:
        #             count1 += 1
        #     if ma30 > move_avg(data, 60, i):
        #         count2 += 1
        # if count1 >= 9 and count2 >= 27:
        #     return True

    def rule8(self):
        data = self.data
        count = 0
        for i in range(1, 61):
            if move_avg(data, 30, i) > move_avg(data, 60, i):
                count += 1
            if count >= 45:
                return True

    def rule9(self):
        for i in range(1, 221):
            if limit_height(self.stock, self.data, i) >= 4:
                return False
        return True

    def fail1(self):
        limit = -0.05 if self.stock[:2] in ['30', '68'] else -0.03
        return t_low_pct(self.data) < limit and self.boomData.turnover < self.data[-1].turnover * 1.6

    def fail2(self):
        limit = -0.05 if self.stock[:2] in ['30', '68'] else -0.03
        return t_low_pct(self.data, 1) < limit and self.boomData.turnover < self.data[-1].turnover * 1.8

    def fail3(self):
        count = 0
        limit = -0.055 if self.stock[:2] in ['30', '68'] else -0.025
        for i in range(3):
            if t_low_pct(self.data, i) < limit:
                count += 1
        return count >= 2 and self.boomData.turnover < self.data[-1].turnover * 1.8

    def fail4(self):
        limit = 0.06 if self.stock[:2] in ['30', '68'] else 0.04
        for i in range(2):
            if not self.data[-i - 1].close < self.data[-3].high:
                return
        d0 = self.data[-1]
        return (d0.open - d0.low) / d0.low > limit

    def fail5(self):
        if sum([self.data[-i - 1].turnover for i in range(5)]) / 5 < 4:
            if sum([self.data[-i - 1].turnover for i in range(20)]) / 20 < 3 * sum([self.data[-i - 1].turnover for i in range(61, 121)]) / 20:
                return True

    def fail6(self):
        if t_down_limit(self.stock, self.data):
            return True

    def fail7(self):
        if t_close_pct(self.data) < -0.05 and self.data[-1].close < move_avg(self.data, 5):
            return True

    def fail8(self):
        if self.boomDay:
            boomIndex = self.dates.index(self.boomDay)
            if boomIndex:
                for i in range(boomIndex + 1, len(self.dates)):
                    d = self.data[i]
                    if (d.high - d.close) / d.preClose > 0.04 and d.pctChange < 2 and ((d.high / d.preClose) - 1) > 0.05:
                        if d.turnover > self.boomData.turnover * 0.8:
                            return True

    def fail9(self):
        data = self.data
        if t_high_pct(data) - t_close_pct(data) > 0.05:
            return data[-1].close < move_avg(data, 10)

    def fail10(self):
        for i in range(3):
            if not self.data[-i - 1].open < move_avg(self.data, 5, i):
                return False
        return True

    def fail11(self):
        if self.boomData:
            return self.boomData.turnover > self.data[-2].turnover * 1.3

    def fail12(self):
        if self.boomData:
            boomIndex = self.dates.index(self.boomDay)
            if boomIndex:
                for i in range(boomIndex + 1, len(self.dates)):
                    if not self.boomData.high > self.data[i].high:
                        return False
                return True

    def run(self):
        passCount = 0
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        fails = [_ for _ in self.__class__.__dict__.keys() if 'fail' in _]
        for rule in rules:
            func = getattr(self, rule)
            try:
                res = func()
            except Exception:
                res = False
            if not res:
                break
            passCount += 1
        if passCount != len(rules):
            return
        for fail in fails:
            func = getattr(self, fail)
            try:
                res = func()
            except Exception:
                res = True
            if res:
                return
        self.client.close()
        if passCount == len(rules):
            return {"stock": self.stock, "name": self.detail.name, "boomDay": self.boomDay, "shrinkDay": self.data[-1].date}
