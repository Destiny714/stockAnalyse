# -*- coding: utf-8 -*-
# @Time    : 2022/4/17 19:36
# @Author  : Destiny_
# @File    : concurrentActions.py
# @Software: PyCharm
from api import extApi
from api import databaseApi
from api.databaseApi import Mysql
from api.tushareApi import Tushare
from common import toolBox, dateHandler, collect_data

log = toolBox.log()


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
        if d['symbol'][0] not in ['4', '8']:
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


def updateShIndex(start=dateHandler.lastTradeDay(), end=dateHandler.lastTradeDay()):
    code = '000001.SH'
    data = Tushare().indexData(start=start, end=end, code=code)
    for d in data:
        databaseApi.Mysql().insertIndex(d, indexTable='NoShIndex')


def updateGemIndex(start=dateHandler.lastTradeDay(), end=dateHandler.lastTradeDay()):
    code = '399006.SZ'
    data = Tushare().indexData(start=start, end=end, code=code)
    for d in data:
        print(d['trade_date'])
        databaseApi.Mysql().insertIndex(d, indexTable='NoGemIndex')


def updateMoneyFlow(aimDate=dateHandler.lastTradeDay()):
    print(f'updating {aimDate} money flow')
    data = Tushare().moneyFlow(aimDate)

    def updateOne(d):
        try:
            client = Mysql()
            client.updateMoneyFlow(d)
        except Exception as e:
            log.warning(f'update money flow error - {e}')

    toolBox.thread_pool_executor(updateOne, data)
    print(f'{aimDate} money flow update done')


def updateChipDetail(aimDate=dateHandler.lastTradeDay()):
    print(f'updating {aimDate} chip detail')
    data = Tushare().chipDetail(aimDate)

    def updateOne(d):
        if str(d['ts_code'])[0] != '8':
            try:
                client = Mysql()
                client.updateChipDetail(d)
            except Exception as e:
                log.warning(f'update chip detail error - {e}')

    toolBox.thread_pool_executor(updateOne, data)
    print(f'{aimDate} chip detail update done')


def updateTimeDataToday():
    errs = []
    stocks = Mysql().selectAllStock()

    def updateOne(stock):
        try:
            data = extApi.getTimeDataToday(stock)
            if data is None:
                log.warning(f'{stock} update time data error')
                errs.append(stock)
                return
            client = Mysql()
            client.updateTimeData(json=data)
        except:
            errs.append(stock)
            log.warning(f'{stock} update time data error')

    checkDate = extApi.getTimeDataToday('399001')['date']
    if checkDate != dateHandler.lastTradeDay():
        log.error('分时数据缺失,退出')
        exit()
    print(f'updating {checkDate} time data')
    toolBox.thread_pool_executor(updateOne, stocks, 15)
    if len(errs) != 0:
        toolBox.thread_pool_executor(updateOne, errs, 15)
    print(f'update time data done')


def rankingLimitTime(aimDate=dateHandler.lastTradeDay()) -> list:
    print('ranking limit time')
    client = Mysql()
    stocks = client.selectAllStock()
    datas = {}

    def addData(stock):
        try:
            data = collect_data.collectData(stock, dateRange=5, aimDate=aimDate)
            if collect_data.t_open_pct(data) > collect_data.limit(stock):
                return
            for i in range(3):
                if not collect_data.t_limit(stock, data, i):
                    return
                if collect_data.model_1(stock, data):
                    return
                limitTime = data[-1].firstLimitTime()
                if limitTime in datas.keys():
                    datas[limitTime].append(stock)
                else:
                    datas[limitTime] = [stock]
        except:
            pass

    toolBox.thread_pool_executor(addData, stocks)

    rankList = [{'time': _, 'stocks': datas[_]} for _ in datas.keys()]

    def rank(d):
        return d['time']

    rankList.sort(key=rank)
    print('limit time rank done')
    return [_['stocks'] for _ in rankList]


def industryIndex(aimDate=dateHandler.lastTradeDay()):
    limitRankDict = {}
    industries = databaseApi.Mysql().selectAllIndustry()
    for i in industries:
        limitRankDict[i] = {}
    errors = []
    industryLimitDict = {}

    def processOne(industry):
        limit = 0
        mysql = databaseApi.Mysql()
        industryStocks = mysql.selectStockByIndustry(industry)
        for industryStock in industryStocks:
            try:
                stockData = collect_data.collectData(industryStock, 5, aimDate=aimDate)
                if collect_data.t_limit(industryStock, stockData):
                    limit += 1
                    if collect_data.t_open_pct(stockData) <= collect_data.limit(industryStock):
                        if stockData[-1].firstLimitTime() not in limitRankDict[industry].keys():
                            limitRankDict[industry][stockData[-1].firstLimitTime()] = [industryStock]
                        else:
                            limitRankDict[industry][stockData[-1].firstLimitTime()].append(industryStock)
            except Exception as e:
                errors.append(e)
        if len(limitRankDict[industry].keys()) == 0:
            limitRankList = []
        else:
            limitRankList = [{'time': _, 'stocks': limitRankDict[industry][_]} for _ in limitRankDict[industry].keys()]

            def rank(d):
                return d['time']

            limitRankList.sort(key=rank)
        industryLimitDict[industry] = {'limit': limit, 'rank': [] if not limitRankList else [_['stocks'] for _ in limitRankList]}

    print('processing industry index...')
    toolBox.thread_pool_executor(processOne, industries, 10)
    print('processing industry index done')
    return industryLimitDict


def initStock(needReload: bool = True, extra: bool = False):
    mysql = databaseApi.Mysql()
    stocks = mysql.selectAllStock()
    if needReload:
        updateShIndex()
        updateGemIndex()
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
        updateChipDetail()
        updateTimeDataToday()
    return stocks
