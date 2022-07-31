# -*- coding: utf-8 -*-
# @Time    : 2022/4/17 19:36
# @Author  : Destiny_
# @File    : concurrentActions.py
# @Software: PyCharm
from api import databaseApi
from api.databaseApi import Mysql
from api.tushareApi import Tushare
from common import toolBox, dateHandler, collect_data


def updateTradeCalender():
    data = Tushare().tradeCalender()
    mysql = Mysql()
    for d in data:
        mysql.insertTradeCalender(d)


def updateStockList():
    print('start update stock list...')
    data = Tushare().allStocks()
    mysql = Mysql()
    for d in data:
        if d['symbol'][0] != '8':
            mysql.insertStockDetail(d)
    print('stock list update done')


def updateLimitDetailData(date=dateHandler.lastTradeDay()):
    print(f'start update {date} stock limit detail...')
    errors = []
    data = Tushare().limitTimeDetail(date)

    def update(d):
        try:
            mysql = Mysql()
            mysql.updateLimitDetailData(d)
        except Exception as e:
            errors.append(e)
            pass

    toolBox.thread_pool_executor(update, data)
    print('stock limit detail update done')


def updateStockListDailyIndex(date=dateHandler.lastTradeDay()):
    print(f'start update {date} stock index...')
    errors = []
    data = Tushare().stockDailyIndex(date)

    def update(d):
        try:
            mysql = Mysql()
            mysql.updateStockListDailyIndex(d)
        except Exception as e:
            errors.append(e)
            pass

    toolBox.thread_pool_executor(update, data)

    print('stock index update done')


def updateDaily(dateList):
    print(f'start update stock data for {dateList[0]} to {dateList[-1]}')

    def tmp(d):
        if d['ts_code'][0] == '8':
            return
        mysql = Mysql()
        try:
            mysql.insertOneRecord(d)
        except Exception as e:
            print(f'update daily error : {e}')
            pass

    for date in dateList:
        print(f'updating {date} stock data')
        data = Tushare().oneDayDetail(date)
        if data[0]['trade_date'] != date or data is None:
            print('数据未更新')
            exit()
        toolBox.thread_pool_executor(tmp, data)
    print('stock data update done')


def createTableIfNotExist(stockList):
    print('start update stock table...')

    def checkOne(stock):
        mysql = Mysql()
        mysql.createTableForStock(stock)

    toolBox.thread_pool_executor(checkOne, stockList)
    print('stock table update done')


def updateGem():
    start = Mysql().selectGemUpdateDate()
    if int(start) < int(dateHandler.lastTradeDay()):
        data = Tushare().indexData(start=str(int(start) + 1), end=dateHandler.lastTradeDay())
        for d in data:
            databaseApi.Mysql().insertOneRecord(d)


def updateMoneyFlow(aimDate=dateHandler.lastTradeDay()):
    print(f'updating {aimDate} money flow')
    data = Tushare().moneyFlow(aimDate)

    def updateOne(d):
        try:
            client = Mysql()
            client.updateMoneyFlow(d)
        except Exception as e:
            print(e)

    toolBox.thread_pool_executor(updateOne, data)
    print(f'{aimDate} money flow update done')


def industryLimit(aimDate=dateHandler.lastTradeDay()):
    industries = databaseApi.Mysql().selectAllIndustry()
    errors = []
    industryLimitDict = {}

    def processOne(industry):
        limit = 0
        mysql = databaseApi.Mysql()
        industryStocks = mysql.selectStockByIndustry(industry)
        for industryStock in industryStocks:
            try:
                stockData = collect_data.collectData(industryStock, 2, aimDate=aimDate)
                if stockData != [] and collect_data.t_limit(industryStock, stockData):
                    limit += 1
            except Exception as e:
                errors.append(e)
        industryLimitDict[industry] = limit

    print('processing industry limit...')
    toolBox.thread_pool_executor(processOne, industries, 10)
    print('processing industry done')
    return industryLimitDict


def initStock(needReload: bool = True, extra: bool = False):
    mysql = databaseApi.Mysql()
    stocks = mysql.selectAllStock()
    if needReload:
        updateGem()
        updateStockList()
        stocks = mysql.selectAllStock()
        stockDetailVersion = mysql.selectDetailUpdateDate()
        createTableIfNotExist(stocks)
        mysql.stockListUpdateDate(dateHandler.lastTradeDay())
        if int(stockDetailVersion) < int(dateHandler.lastTradeDay()):
            fullDates = mysql.selectTradeDate()
            dates = [_ for _ in fullDates if
                     int(stockDetailVersion) < int(_) <= int(dateHandler.lastTradeDay())]
            updateDaily(dates)
            mysql.stockDetailUpdateDate(dateHandler.lastTradeDay())
    if extra:
        updateLimitDetailData()
        updateStockListDailyIndex()
        updateMoneyFlow()
    return stocks
