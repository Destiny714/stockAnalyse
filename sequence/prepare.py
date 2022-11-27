# -*- coding: utf-8 -*-
# @Time    : 2022/10/11 23:49
# @Author  : Destiny_
# @File    : prepare.py
# @Software: PyCharm
import tushare
from api import config
from prefs.params import Params
from utils import concurrent_util
from utils.stockdata_util import RankLimitStock
from utils.date_util import prevTradeDay, nextTradeDay


class Prepare(object):
    def __init__(self, stocks: list[str] = None, aimDates: list[str] = None):
        self.stocks = stocks
        self.aimDates = aimDates

    def preTushare(self):
        token = config['tushareKey']
        tushare.set_token(token)
        print('tushare registered')

    def preIndustryLimitDict(self):
        lastDay = self.aimDates[-1]
        dates = set()
        for aimDate in self.aimDates:
            prevDate = prevTradeDay(aimDate)
            dates.add(prevDate)
            dates.add(aimDate)
        for date in dates:
            limitData = concurrent_util.getStockLimitDataByDate(date=date)
            Params.dailyLimitData[date] = limitData
            Params.dailyIndustryLimitDict[date] = RankLimitStock(limitData).by('limitTime-industry', date)
        Params.dailyIndustryLimitDict[nextTradeDay(lastDay)] = Params.dailyIndustryLimitDict[lastDay]

    def do(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'pre' in _]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                return True
