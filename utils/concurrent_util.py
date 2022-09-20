# -*- coding: utf-8 -*-
# @Time    : 2022/4/17 19:36
# @Author  : Destiny_
# @File    : concurrent_util.py
# @Software: PyCharm
from api import netease_api
from common import tool_box
from utils.log_util import log
from utils import stockdata_util
from utils.stockdata_util import *
from api.database_api import Mysql
from api.tushare_api import Tushare
from middleWare.stockFilter import stockFilter
from models.limitDataModel import limitDataModel

_log = log()


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


def createStockDetailMap(detail: tuple[tuple]):
    detailMap: dict[str, tuple] = {}

    def one(d: tuple):
        detailMap[d[1]] = d

    tool_box.thread_pool_executor(one, detail)
    return detailMap


def deleteEndStocks():
    """删除退市的股票"""
    endStocks = Tushare().allEndStocks()
    Mysql().deleteTable([f'No{_}' for _ in endStocks])


def updateLimitDetailData(date=lastTradeDay()):
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

    tool_box.thread_pool_executor(update, data)
    print('stock limit detail update done')


def updateStockListDailyIndex(date=lastTradeDay()):
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

    tool_box.thread_pool_executor(update, data)

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
        tool_box.thread_pool_executor(tmp, data)
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


def updateShIndex(start=lastTradeDay(), end=lastTradeDay()):
    """更新上证指数"""
    code = '000001.SH'
    data = Tushare().indexData(start=start, end=end, code=code)
    for d in data:
        Mysql().insertIndex(d, indexTable='NoShIndex')


def updateGemIndex(start=lastTradeDay(), end=lastTradeDay()):
    """更新创业板指数"""
    code = '399006.SZ'
    data = Tushare().indexData(start=start, end=end, code=code)
    for d in data:
        Mysql().insertIndex(d, indexTable='NoGemIndex')


def updateMoneyFlow(aimDate=lastTradeDay()):
    """更新资金流向"""
    print(f'updating {aimDate} money flow')
    data = Tushare().moneyFlow(aimDate)

    def updateOne(d):
        try:
            client = Mysql()
            client.updateMoneyFlow(d)
        except Exception as e:
            _log.warning(f'update money flow error - {e}')

    tool_box.thread_pool_executor(updateOne, data)
    print(f'{aimDate} money flow update done')


def updateChipDetail(aimDate=lastTradeDay()):
    """更新筹码图"""
    print(f'updating {aimDate} chip detail')
    data = Tushare().chipDetail(aimDate)

    def updateOne(d):
        if str(d['ts_code'])[0] != '8':
            try:
                client = Mysql()
                client.updateChipDetail(d)
            except Exception as e:
                _log.warning(f'update chip detail error - {e}')

    tool_box.thread_pool_executor(updateOne, data)
    print(f'{aimDate} chip detail update done')


def updateTimeDataToday():
    """更新分时数据"""
    errs = []
    stocks = Mysql().selectAllStock()

    def updateOne(stock):
        try:
            data = netease_api.getTimeDataToday(stock)
            if data is None:
                _log.warning(f'{stock} update time data error')
                errs.append(stock)
                return
            client = Mysql()
            client.updateTimeData(json=data)
        except:
            errs.append(stock)
            _log.warning(f'{stock} update time data error')

    checkDate = netease_api.getTimeDataToday('399001')['date']
    if checkDate != lastTradeDay():
        _log.error('分时数据缺失,退出')
        exit()
    print(f'updating {checkDate} time data')
    tool_box.thread_pool_executor(updateOne, stocks, 15)
    if len(errs) != 0:
        tool_box.thread_pool_executor(updateOne, errs, 15)
    print(f'update time data done')


def updateStockLimit(start=lastTradeDay(), end=lastTradeDay()):
    """每日更新 stockLimit 表"""
    data = Tushare().fullLimitDetail(start=start, end=end)

    def updateOneDay(d):
        try:
            mysql = Mysql()
            mysql.insertOneLimitStock(d)
        except Exception as e:
            _log.warning(f'update stockLimit error - {e}')

    tool_box.thread_pool_executor(updateOneDay, data, 10)


def rankingLimitTime(aimDate=lastTradeDay()) -> list:
    """涨停时间排序"""
    print('ranking limit time')
    client = Mysql()
    stocks = client.selectAllStock()
    datas = {}

    def addData(stock):
        try:
            data = collectData(stock, dateRange=5, aimDate=aimDate)
            if stockdata_util.t_open_pct(data) > limit(stock):
                return
            for i in range(3):
                if not stockdata_util.t_limit(stock, data, i):
                    return
                if model_1(stock, data):
                    return
                limitTime = data[-1].firstLimitTime()
                if limitTime in datas.keys():
                    datas[limitTime].append(stock)
                else:
                    datas[limitTime] = [stock]
        except:
            pass

    tool_box.thread_pool_executor(addData, stocks)

    rankList = [{'time': _, 'stocks': datas[_]} for _ in datas.keys()]

    def rank(d):
        return d['time']

    rankList.sort(key=rank)
    print('limit time rank done')
    return [_['stocks'] for _ in rankList]


def getStockLimitDataByDate(date: str = lastTradeDay(), lead: int = 100):
    """并发获取 stockLimit表 内容"""
    res: dict[str, list[limitDataModel]] = {}
    tradeDates = Mysql().selectTradeDate()
    index = tradeDates.index(date)
    selectDates = tradeDates[index - lead + 1:index + 1]
    stockLimitDetails: tuple[tuple] = Mysql().selectLimitStockByDateRange(selectDates)

    def one(detail: tuple):
        _date = detail[1]
        if _date not in res.keys():
            res[_date] = [limitDataModel(detail)]
        else:
            res[_date].append(limitDataModel(detail))

    tool_box.thread_pool_executor(one, stockLimitDetails)
    return res


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
        mysql.stockListUpdateDate(lastTradeDay())
        if int(stockDetailVersion) < int(lastTradeDay()):
            fullDates = mysql.selectTradeDate()
            dates = [_ for _ in fullDates if int(stockDetailVersion) < int(_) <= int(lastTradeDay())]
            updateDaily(dates)
            mysql.stockDetailUpdateDate(lastTradeDay())
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
