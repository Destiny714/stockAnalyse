# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 18:39
# @Author  : Destiny_
# @File    : tushareApi.py
# @Software: PyCharm

import tushare
from common import dateHandler


class Tushare:
    def __init__(self):
        self._token = '389034377016716d6513ce5c1f5fc4adfef93112af12b786b29d639c'
        tushare.set_token(self._token)
        self._tushare = tushare
        self._instance = tushare.pro_api()

    def tradeCalender(self):
        data = self._instance.query('trade_cal', start_date='20190101')
        dayList = []
        for i in range(len(data)):
            day = data.iloc[i]
            if day['is_open'] == 1:
                dayList.append({'date': day['cal_date'], 'lastDate': day['pretrade_date']})
        return dayList

    def allStocks(self):
        stockList = []
        data = self._instance.query('stock_basic', exchange='', list_status='L',
                                    fields='exchange,symbol,name,industry,market')
        for i in range(len(data)):
            stock = data.iloc[i]
            stockList.append(stock)
        return stockList

    def oneDayDetail(self, date):
        details = []
        data = self._instance.query('daily', trade_date=date)
        for i in range(len(data)):
            details.append(data.iloc[i])
        return details

    def indexData(self, start: str, end: str, code: str = '399006.SZ'):
        details = []
        data = self._instance.index_daily(ts_code=code, start_date=start, end_date=end)
        for i in range(len(data)):
            details.append(data.iloc[-i - 1])
        return details

    def stockDailyIndex(self, date: str):
        details = []
        data = self._instance.daily_basic(ts_code='', trade_date=date,
                                          fields='ts_code,trade_date,circ_mv,turnover_rate')
        for i in range(len(data)):
            details.append(data.iloc[i])
        return details

    def limitTimeDetail(self, date: str = dateHandler.lastTradeDay()):
        details = []
        data = self._instance.limit_list(**{
            "trade_date": "",
            "ts_code": "",
            "limit_type": "U",
            "start_date": date,
            "end_date": date,
            "limit": "",
            "offset": ""
        }, fields=[
            "trade_date",
            "ts_code",
            "name",
            "first_time",
            "last_time",
            "open_times",
        ])
        for i in range(len(data)):
            d = data.iloc[-i - 1]
            details.append(d)
        return details

    def allLimitUpDetail(self, date=dateHandler.lastTradeDay()) -> list:
        details = []
        data = self._instance.limit_list(**{
            "trade_date": date,
            "ts_code": "",
            "limit_type": "U",
            "start_date": "",
            "end_date": "",
            "limit": "",
            "offset": ""
        }, fields=[
            "trade_date",
            "ts_code",
            "name",
        ])
        for i in range(len(data)):
            details.append(data.iloc[i])
        return details
