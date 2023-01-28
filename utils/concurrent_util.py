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
from api.tushare_api import Tushare
from utils.excel_util import readExcel2DF
from middleWare.stock_filter import stockFilter
from models.limit_data_model import LimitDataModel
from database.db import Stock_Database, Server_Database

_log = log()


def updateRankDetail(date: str):
    print(f'update {date}')
    df = readExcel2DF(date)

    def update(data):
        client = Server_Database()
        client.insertDailyRankDetail(data)
        client.close()

    tool_box.thread_pool_executor(update, [i[1] for i in df.iterrows()])


def updateTradeCalender():
    """更新交易日历"""
    data = Tushare().tradeCalender()
    mysql = Stock_Database()
    for d in data:
        mysql.insertTradeCalender(d)
    mysql.close()


def updateStockList():
    """更新股票资料列表"""
    print('start update stock list...')
    data = Tushare().allStocks()
    mysql = Stock_Database()
    existStocks = mysql.selectAllStock()
    for d in data:
        if d['symbol'] not in existStocks:
            mysql.insertStockDetail(d)
        else:
            mysql.updateStockDetail(d)
    mysql.close()
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
    Stock_Database().deleteTable([f'No{_}' for _ in endStocks])


def updateLimitDetailData(date=lastTradeDay()):
    """更新股票涨停详情"""
    print(f'start update {date} stock limit detail...')
    errors = []
    data = Tushare().limitTimeDetail(date)

    def update(d):
        try:
            mysql = Stock_Database()
            mysql.updateLimitDetailData(d)
            mysql.close()
        except Exception as e:
            errors.append(e)
            pass

    tool_box.thread_pool_executor(update, data)
    print('stock limit detail update done')


def updateTurnover(date=lastTradeDay()):
    """更新换手率数据"""
    print(f'start update {date} stock index...')
    errors = []
    data = Tushare().stockDailyIndex(date)

    def update(d):
        try:
            mysql = Stock_Database()
            mysql.updateTurnover(d)
            mysql.close()
        except Exception as e:
            errors.append(e)
            pass

    tool_box.thread_pool_executor(update, data)

    print('stock index update done')


def updateDaily(dateList):
    """更新每日股票基础数据"""
    print(f'start update stock data for {dateList[0]} to {dateList[-1]}')
    count = []

    def tmp(d):
        if d['ts_code'][0] in ['4', '8']:
            return
        mysql = Stock_Database()
        try:
            mysql.insertOneDailyBasicRecord(d)
            count.append(d["ts_code"])
        except Exception as e:
            print(f'{d["ts_code"]} update daily error : {e}')
            pass
        finally:
            mysql.close()

    for date in dateList:
        print(f'updating {date} stock data')
        data = Tushare().qfqDailyData(date)
        if data[0]['trade_date'] != date or data is None:
            print('数据未更新')
            exit()
        tool_box.thread_pool_executor(tmp, data)
    print(f'update {len(count)} stock basic data %%%%%%%%%%%%')
    print('stock data update done')


def createTableIfNotExist(stockList):
    """检查并创建新stock table"""
    print('start update stock table...')
    mysql = Stock_Database()
    tables = mysql.selectExistTable()
    for stock in stockList:
        if f'No{stock}' not in tables:
            mysql.createTableForStock(stock)
    mysql.close()
    print('stock table update done')


def updateShIndex(date=None):
    """更新上证指数"""
    if not date:
        date = lastTradeDay()
    client = Stock_Database()
    code = '000001.SH'
    data = Tushare().indexData(date=date, code=code)
    for d in data:
        client.insertIndex(d, indexTable='NoShIndex')
    client.close()


def updateGemIndex(date=None):
    """更新创业板指数"""
    if not date:
        date = lastTradeDay()
    client = Stock_Database()
    code = '399006.SZ'
    data = Tushare().indexData(date=date, code=code)
    for d in data:
        client.insertIndex(d, indexTable='NoGemIndex')
    client.close()


def updateMoneyFlow(aimDate=lastTradeDay()):
    """更新资金流向"""
    print(f'updating {aimDate} money flow')
    data = Tushare().moneyFlow(aimDate)

    def updateOne(d):
        try:
            client = Stock_Database()
            client.updateMoneyFlow(d)
            client.close()
        except Exception as e:
            _log.warning(f'update money flow error - {e}')

    tool_box.thread_pool_executor(updateOne, data)
    print(f'{aimDate} money flow update done')


def updateChipDetail(aimDate=lastTradeDay()):
    """更新筹码图"""
    print(f'updating {aimDate} chip detail')

    def updateOne(d):
        if str(d['ts_code'])[0] not in ['4', '8']:
            try:
                client = Stock_Database()
                client.updateChipDetail(d)
                client.close()
            except Exception as e:
                _log.warning(f'update chip detail error - {e}')

    mysql = Stock_Database()
    stocks = mysql.selectAllStockWithSuffix()
    mysql.close()
    for one_part in tool_box.cutList(stocks, 1000):
        stockJoin = ','.join(one_part)
        data = Tushare().chipDetail(stockJoin, aimDate)
        tool_box.thread_pool_executor(updateOne, data)
    print(f'{aimDate} chip detail update done')


def updateTimeDataToday():
    """更新分时数据"""
    errs = []
    stocks = Stock_Database().selectAllStock()

    def updateOne(stock):
        try:
            data = netease_api.getTimeDataToday(stock)
            if data is None:
                _log.warning(f'{stock} update time data error')
                errs.append(stock)
                return
            client = Stock_Database()
            client.updateTimeData(json=data)
            client.close()
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
            mysql = Stock_Database()
            mysql.insertOneLimitStock(d)
            mysql.close()
        except Exception as e:
            _log.warning(f'update stockLimit error - {e}')

    tool_box.thread_pool_executor(updateOneDay, data, 10)


def rankingLimitTime(aimDate=lastTradeDay()) -> list:
    """涨停时间排序"""
    print('ranking limit time')
    client = Stock_Database()
    stocks = client.selectAllStock()
    client.close()
    datas = {}

    def addData(stock):
        try:
            data = queryData(stock, dateRange=5, aimDate=aimDate)
            if stockdata_util.t_open_pct(data) > limit(stock):
                return
            for i in range(3):
                if not stockdata_util.t_limit(stock, data, i):
                    return
                if model_1(stock, data):
                    return
                limitTime = data[-1].firstLimitTime
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


def getStockLimitDataByDate(date: str = lastTradeDay(), lead: int = 100) -> dict[str, list[LimitDataModel]]:
    """并发获取 stockLimit表 内容"""
    res: dict[str, list[LimitDataModel]] = {}
    client = Stock_Database()
    tradeDates = client.selectTradeDate()
    index = tradeDates.index(date)
    selectDates = tradeDates[index - lead + 1:index + 1]
    stockLimitDetails: tuple[tuple] = client.selectLimitStockByDateRange(selectDates)
    client.close()

    def one(detail: tuple):
        _date = detail[1]
        if _date not in res.keys():
            res[_date] = [LimitDataModel(detail)]
        else:
            res[_date].append(LimitDataModel(detail))

    tool_box.thread_pool_executor(one, stockLimitDetails)
    return res


def initStock(needReload=True, extra=False):
    """每日数据更新汇总脚本"""
    mysql = Stock_Database()
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
        updateTurnover()
        updateMoneyFlow()
        updateChipDetail()
        # updateTimeDataToday() #TODO:fix minuteData update method
        updateStockLimit()
    mysql.close()
    return stocks
