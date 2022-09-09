# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 18:39
# @Author  : Destiny_
# @File    : tushareApi.py
# @Software: PyCharm

import tushare
from api import args
from common import dateHandler


class Tushare:
    def __init__(self):
        self._token = args['tushareKey']
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
        SSEdata = self._instance.query('stock_basic', exchange='SSE', list_status='L', fields='exchange,symbol,name,industry,market')
        SZSEdata = self._instance.query('stock_basic', exchange='SZSE', list_status='L', fields='exchange,symbol,name,industry,market')
        for i in range(len(SSEdata)):
            stock = SSEdata.iloc[i]
            stockList.append(stock)
        for i in range(len(SZSEdata)):
            stock = SZSEdata.iloc[i]
            stockList.append(stock)
        return stockList

    def oneDayDetail(self, date):
        details = []
        data = self._instance.query('daily', trade_date=date)
        for i in range(len(data)):
            details.append(data.iloc[i])
        return details

    def indexData(self, start: str, end: str, code: str = '000001.SH'):
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
        data = self._instance.limit_list_d(**{
            "trade_date": date,
            "ts_code": "",
            "limit_type": "U",
            "exchange": "",
            "start_date": "",
            "end_date": "",
            "limit": "",
            "offset": ""
        }, fields=[
            "trade_date",
            "ts_code",
            "name",
            "first_time",
            "last_time",
            "open_times"
        ])
        for i in range(len(data)):
            d = data.iloc[-i - 1]
            details.append(d)
        return details

    def dailyLimitCount(self, date=dateHandler.lastTradeDay()) -> int:
        details = []
        data = self._instance.daily_basic(**{
            "ts_code": "",
            "trade_date": date,
            "start_date": "",
            "end_date": "",
            "limit": "",
            "offset": ""
        }, fields=[
            "limit_status",
            "ts_code"
        ])
        for i in range(len(data)):
            details.append(data.iloc[i])
        return len([_ for _ in details if _['limit_status'] != 0])

    def moneyFlow(self, date=dateHandler.lastTradeDay()):
        details = []
        data = self._instance.moneyflow(**{
            "ts_code": "",
            "trade_date": date,
            "start_date": "",
            "end_date": "",
            "limit": "",
            "offset": ""
        }, fields=[
            "ts_code",
            "trade_date",
            "buy_sm_vol",
            "buy_sm_amount",
            "sell_sm_vol",
            "sell_sm_amount",
            "buy_md_vol",
            "buy_md_amount",
            "sell_md_vol",
            "sell_md_amount",
            "buy_lg_vol",
            "buy_lg_amount",
            "sell_lg_vol",
            "sell_lg_amount",
            "buy_elg_vol",
            "buy_elg_amount",
            "sell_elg_vol",
            "sell_elg_amount",
            "net_mf_vol",
            "net_mf_amount",
            "trade_count"
        ])
        for i in range(len(data)):
            details.append(data.iloc[i])
        return details

    def chipDetail(self, date=dateHandler.lastTradeDay()):
        details = []
        data = self._instance.cyq_perf(**{
            "ts_code": "",
            "trade_date": date,
            "start_date": "",
            "end_date": "",
            "limit": "",
            "offset": ""
        }, fields=[
            "ts_code",
            "trade_date",
            "his_low",
            "his_high",
            "cost_5pct",
            "cost_15pct",
            "cost_50pct",
            "cost_85pct",
            "cost_95pct",
            "weight_avg",
            "winner_rate"
        ])
        for i in range(len(data)):
            details.append(data.iloc[i])
        return details

    def fullLimitDetail(self, start, end=dateHandler.lastTradeDay()):
        df = self._instance.limit_list_d(**{
            "trade_date": "",
            "ts_code": "",
            "limit_type": "U",
            "exchange": "",
            "start_date": start,
            "end_date": end,
            "limit": "",
            "offset": ""
        }, fields=[
            "trade_date",
            "ts_code",
            "industry",
            "name",
            "close",
            "pct_chg",
            "amount",
            "limit_amount",
            "float_mv",
            "total_mv",
            "turnover_ratio",
            "fd_amount",
            "first_time",
            "last_time",
            "open_times",
            "limit_times",
            "limit",
            "up_stat",
            "swing"
        ])
        return df
