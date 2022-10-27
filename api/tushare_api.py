# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 18:39
# @Author  : Destiny_
# @File    : tushare_api.py
# @Software: PyCharm

import time
import tushare
from api import config
from utils import date_util
from utils.date_util import lastTradeDay


class Tushare:
    def __init__(self):
        self._token = config['tushareKey']
        self._instance = tushare.pro_api(token=self._token)

    def tradeCalender(self):
        """获取交易日历"""
        data = self._instance.query('trade_cal', start_date='20190101')
        dayList = []
        for i in range(len(data)):
            day = data.iloc[i]
            if day['is_open'] == 1:
                dayList.append({'date': day['cal_date'], 'lastDate': day['pretrade_date']})
        return dayList

    def allStocks(self):
        """获取所有上市状态的股票列表"""
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

    def allEndStocks(self):
        """获取所有退市状态的股票列表"""
        stockList = []
        SSEdata = self._instance.query('stock_basic', exchange='SSE', list_status='D', fields='exchange,symbol,name,industry,market')
        SZSEdata = self._instance.query('stock_basic', exchange='SZSE', list_status='D', fields='exchange,symbol,name,industry,market')
        for i in range(len(SSEdata)):
            stock = SSEdata.iloc[i]
            stockList.append(stock)
        for i in range(len(SZSEdata)):
            stock = SZSEdata.iloc[i]
            stockList.append(stock)
        return [_['symbol'] for _ in stockList]

    def dailyData(self, date):
        """获取单日所有股票基础数据"""
        details = []
        data = self._instance.query('daily', trade_date=date)
        for i in range(len(data)):
            details.append(data.iloc[i])
        return details

    def indexData(self, start: str, end: str, code: str = '000001.SH'):
        """获取指数数据"""
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

    def limitTimeDetail(self, date: str = date_util.lastTradeDay()):
        """获取部分涨停详情(时间、开板次数等)"""
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

    def dailyLimitCount(self, date=lastTradeDay()) -> int:
        """每日涨停个数"""
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

    def moneyFlow(self, date=lastTradeDay()):
        """获取股票资金流向"""
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

    def chipDetail(self, stocks:str, date=None):
        """获取股票筹码详情"""
        if not date:
            date = lastTradeDay()
        details = []
        data = self._instance.cyq_perf(**{
            "ts_code": stocks,
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

    def fullLimitDetail(self, start, end=lastTradeDay()):
        """获取股票涨停详情(全)"""
        details = []
        data = self._instance.limit_list_d(**{
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
        for i in range(len(data)):
            details.append(data.iloc[i])
        return details

    def minuteData(self, stockWithSuffix: str, start: str, end: str):
        """
        获取分时数据
        每分钟限制500次
        :param stockWithSuffix: 带后缀的股票代码
        :param start: 分时开始时间 xxxx-xx-xx xx:xx:xx
        :param end: 分时结束时间
        :return: list[pd.df]
        """
        details = []
        _end = f'{end[:4]}-{end[4:6]}-{end[6:]}'
        _start = f'{start[:4]}-{start[4:6]}-{start[6:]}'
        data = tushare.pro_bar(ts_code=stockWithSuffix, freq='1min', start_date=f'{_start} 09:30:00', end_date=f'{_end} 15:00:00', asset='E')
        for i in range(len(data)):
            details.append(data.iloc[i])
        return details

    def qfqDailyData(self, date=lastTradeDay()):
        """
        每日基础数据前复权版
        :param date: 查询日期
        :return: list[pd.df]
        """
        print(f'request {date}')
        details = []
        data = None
        retry = 0
        while data is None and retry <= 3:
            try:
                data = tushare.pro_api().stk_factor(ts_code='', trade_date=date,
                                                    fields='ts_code,trade_date,open_qfq,close_qfq,high_qfq,low_qfq,pre_close_qfq,pct_change,vol,amount')
                retry += 1
            except:
                time.sleep(20)
        if data is None:
            raise Exception(f'{date} 获取数据出错')
        for i in range(len(data)):
            details.append(data.iloc[i])
        return details
