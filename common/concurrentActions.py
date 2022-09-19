# -*- coding: utf-8 -*-
# @Time    : 2022/4/17 19:36
# @Author  : Destiny_
# @File    : concurrentActions.py
# @Software: PyCharm
from api import extApi
from api.databaseApi import Mysql
from api.tushareApi import Tushare
from common.middleWare.stockFilter import stockFilter
from common import toolBox, dateHandler, dataOperation
from common.models.limitDataModel import limitDataModel

log = toolBox.log()


def updateTradeCalender():
    """更新交易日历"""
    data = Tushare().tradeCalender()
    mysql = Mysql()
    for d in data:
        mysql.insertTradeCalender(d)


def updateStockList():
    """更新股票资料列表"""
    print('start update stock list...')
    data = Tushare().allStocks()
    mysql = Mysql()
    existStocks = mysql.selectAllStock()
    for d in data:
        if d['symbol'] not in existStocks:
            mysql.insertStockDetail(d)
        else:
            mysql.updateStockDetail(d)
    print('stock list update done')


def deleteEndStocks():
    """删除退市的股票"""
    endStocks = Tushare().allEndStocks()
    Mysql().deleteTable([f'No{_}' for _ in endStocks])


def updateLimitDetailData(date=dateHandler.lastTradeDay()):
    """更新股票涨停详情"""
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
    """更新换手率数据"""
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
    """更新每日股票基础数据"""
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
    """检查并创建新stock table"""
    print('start update stock table...')
    mysql = Mysql()
    tables = mysql.selectExistTable()
    for stock in stockList:
        if f'No{stock}' not in tables:
            mysql.createTableForStock(stock)

    print('stock table update done')


def updateShIndex(start=dateHandler.lastTradeDay(), end=dateHandler.lastTradeDay()):
    """更新上证指数"""
    code = '000001.SH'
    data = Tushare().indexData(start=start, end=end, code=code)
    for d in data:
        Mysql().insertIndex(d, indexTable='NoShIndex')


def updateGemIndex(start=dateHandler.lastTradeDay(), end=dateHandler.lastTradeDay()):
    """更新创业板指数"""
    code = '399006.SZ'
    data = Tushare().indexData(start=start, end=end, code=code)
    for d in data:
        Mysql().insertIndex(d, indexTable='NoGemIndex')


def updateMoneyFlow(aimDate=dateHandler.lastTradeDay()):
    """更新资金流向"""
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
    """更新筹码图"""
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
    """更新分时数据"""
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


def updateStockLimit(start=dateHandler.lastTradeDay(), end=dateHandler.lastTradeDay()):
    """每日更新 stockLimit 表"""
    data = Tushare().fullLimitDetail(start=start, end=end)

    def updateOneDay(d):
        try:
            mysql = Mysql()
            mysql.insertOneLimitStock(d)
        except Exception as e:
            log.warning(f'update stockLimit error - {e}')

    toolBox.thread_pool_executor(updateOneDay, data, 10)


def rankingLimitTime(aimDate=dateHandler.lastTradeDay()) -> list:
    """涨停时间排序"""
    print('ranking limit time')
    client = Mysql()
    stocks = client.selectAllStock()
    datas = {}

    def addData(stock):
        try:
            data = dataOperation.collectData(stock, dateRange=5, aimDate=aimDate)
            if dataOperation.t_open_pct(data) > dataOperation.limit(stock):
                return
            for i in range(3):
                if not dataOperation.t_limit(stock, data, i):
                    return
                if dataOperation.model_1(stock, data):
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


def getStockLimitDataByDate(date: str = dateHandler.lastTradeDay(), lead: int = 100):
    """并发获取 stockLimit表 内容"""  # TODO:可以用hashmap 不用并发
    res: dict[str, list[limitDataModel]] = {}
    tradeDates = Mysql().selectTradeDate()
    index = tradeDates.index(date)

    def one(d):
        mysql = Mysql()
        data = mysql.selectLimitStockByDate(d)
        res[d] = [limitDataModel(_) for _ in data]

    toolBox.thread_pool_executor(one, tradeDates[index - lead + 1:index + 1])
    return res


def industryIndex(aimDate=dateHandler.lastTradeDay()):
    """返回同行业涨停数以及同行业涨停排序"""
    limitRankDict = {}
    industries = Mysql().selectAllIndustry()
    for i in industries:
        limitRankDict[i] = {}
    errors = []
    industryLimitDict = {}

    def processOne(industry):
        limit = 0
        mysql = Mysql()
        industryStocks = mysql.selectStockByIndustry(industry)
        for industryStock in industryStocks:
            try:
                stockData = dataOperation.collectData(industryStock, 5, aimDate=aimDate)
                if dataOperation.t_limit(industryStock, stockData):
                    limit += 1
                    if dataOperation.t_open_pct(stockData) <= dataOperation.limit(industryStock):
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


def initStock(needReload=True, extra=False):
    """每日数据更新汇总脚本"""
    mysql = Mysql()
    if needReload:
        updateShIndex()
        updateGemIndex()
        updateStockList()
        stocks = mysql.selectAllStock()
        stocks = stockFilter(stocks).result()
        stockDetailVersion = mysql.selectDetailUpdateDate()
        createTableIfNotExist(stocks)
        mysql.stockListUpdateDate(dateHandler.lastTradeDay())
        if int(stockDetailVersion) < int(dateHandler.lastTradeDay()):
            fullDates = mysql.selectTradeDate()
            dates = [_ for _ in fullDates if int(stockDetailVersion) < int(_) <= int(dateHandler.lastTradeDay())]
            updateDaily(dates)
            mysql.stockDetailUpdateDate(dateHandler.lastTradeDay())
    else:
        stocks = mysql.selectAllStock()
        stocks = stockFilter(stocks).result()
    if extra:
        updateLimitDetailData()
        updateStockListDailyIndex()
        updateMoneyFlow()
        updateChipDetail()
        updateTimeDataToday()
        updateStockLimit()
    return stocks
