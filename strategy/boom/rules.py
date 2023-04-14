# -*- coding: utf-8 -*-
# @Time    : 2023/3/26 13:14
# @Author  : Destiny_
# @File    : rules.py
# @Software: PyCharm

from database import db
from models.stock_detail_model import StockDetailModel
from utils.stockdata_util import queryData, move_avg, t_close_pct, t_limit, limit_height


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
        self.client = db.Stock_Database()
        self.data = queryData(stock, 300, date)
        self.detail = StockDetailModel(self.client.selectStockDetail(stock))

    def rule1(self):
        if self.detail.amount > 150e5:
            return True

    def rule2(self):
        if 25e4 < self.data[-1].amount < 35e5:
            return True

    def rule3(self):
        count1 = 0
        for i in range(5):
            d = self.data[-i - 1]
            if d.close > move_avg(self.data, 5, i):
                count1 += 1
        if count1 >= 4:
            return True
        else:
            count2 = 0
            for i in range(10):
                if self.data[-i - 1].close > move_avg(self.data, 5, i):
                    count2 += 1
            if count2 >= 8:
                return True

    def rule4(self):
        data = self.data
        if (max([data[-i - 1].high for i in range(1, 10)]) - min([data[-i - 1].low for i in range(1, 10)])) / min(
                [data[-i - 1].low for i in range(1, 10)]) < 0.40:
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
        for i in range(1, 8):
            d = data[-i - 1]
            max8to200 = max([data[-j - 1].high for j in range(8, 201)])
            if not t_close_pct(data, i) > 0.06:
                continue
            if not d.close > max8to200:
                continue
            if not d.turnover > data[-1].turnover * 1.29:
                continue
            if not d.open < data[-1].close:
                continue
            if t_limit(self.stock, data, i) and d.limitOpenTime >= 3:
                continue
            self.boomDay = d.date
            return True

    def rule7(self):
        data = self.data
        count1 = 0
        count2 = 0
        for i in range(1, 31):
            ma30 = move_avg(data, 30, i)
            if i in range(10):
                if data[-i - 1].close > ma30:
                    count1 += 1
            if ma30 > move_avg(data, 60, i):
                count2 += 1
        if count1 >= 9 and count2 >= 27:
            return True

    def rule8(self):
        for i in range(1, 221):
            if limit_height(self.stock, self.data, i) >= 4:
                return False
        return True

    def run(self):
        passCount = 0
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            try:
                res = func()
            except Exception:
                res = False
            if not res:
                break
            passCount += 1
        self.client.close()
        if passCount == len(rules):
            return {"stock": self.stock, "name": self.detail.name, "boomDay": self.boomDay, "shrinkDay": self.data[-1].date}
