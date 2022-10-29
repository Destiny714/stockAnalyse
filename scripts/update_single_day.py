# -*- coding: utf-8 -*-
# @Time    : 2022/9/23 04:14
# @Author  : Destiny_
# @File    : update_single_day.py
# @Software: PyCharm
import time
import numpy
import tushare

from database import db
from sequence.prepare import Prepare
from utils.concurrent_util import initStock
from utils.date_util import getMinute, lastTradeDay
from common.tool_box import timeCount, cutList, thread_pool_executor, process_pool_executor
from utils.push_util import bark_pusher


def minuteData(stockWithSuffix: str, start: str, end: str):
    details = []
    data = None
    err = None
    _end = f'{end[:4]}-{end[4:6]}-{end[6:]}'
    _start = f'{start[:4]}-{start[4:6]}-{start[6:]}'
    retryTime = 0
    while data is None and retryTime <= 3:
        try:
            if retryTime != 0:
                time.sleep(20)
            data = tushare.pro_bar(ts_code=stockWithSuffix, freq='1min', start_date=f'{_start} 09:30:00', end_date=f'{_end} 15:00:00', asset='E')
            retryTime += 1
        except Exception as e:
            err = e
            time.sleep(60)
    else:
        if data is None:
            bark_pusher(f'{stockWithSuffix} {start} to {end} 发生错误', err.args[0])
    for i in range(len(data)):
        details.append(data.iloc[i])
    return details


def getData(stockNo: str, dateList: list[list]):
    print(f'{stockNo} {dateList[0][0]} to {dateList[-1][-1]} start')
    allData = []
    for d_range in dateList:
        data = minuteData(stockNo, d_range[0], d_range[-1])
        sqlWriteData = []
        dateSortMap = {}
        for value in numpy.array(data):  # 生成日期为键值为[]的dict
            date = value[8]
            if date not in dateSortMap.keys():
                dateSortMap[date] = [value]
            else:
                dateSortMap[date].append(value)
        for day in numpy.array([_ for _ in dateSortMap.keys()]):
            timeData = {}
            oneDayData: list[numpy.ndarray] = dateSortMap[day]
            for oneMinData in numpy.array(oneDayData):
                trade_time = oneMinData[1]
                minute = getMinute(timeStr=trade_time)
                vol = int(oneMinData[6] / 100)  # 转换为手
                timeData[minute] = vol
            resDict = {'symbol': stockNo.split('.')[0], 'date': day, 'data': timeData}
            sqlWriteData.append(resDict)
        allData.extend(sqlWriteData)
    print(f'{stockNo} {dateList[0][0]} to {dateList[-1][-1]} done')
    return allData


if __name__ == '__main__':
    Prepare().do()
    initStock(needReload=True, extra=True)
    sql = db.Mysql()
    dateSize = 30
    dateRange = 1
    dates = sql.selectTradeDateByDuration(lastTradeDay(), dateRange)
    datesList = cutList(dates, dateSize)
    stocks = sql.selectAllStockWithSuffix()
    cut_stocks = cutList(stocks, 500)


    @timeCount
    def multiProcess(stock_list):
        return process_pool_executor(getData, stock_list, 20, datesList)


    def writeSQL(_):
        db.Mysql().updateTimeData(_)


    def writeData(r: list):
        datas = []
        for _ in numpy.array(r, dtype=object):
            datas.extend(_)
        thread_pool_executor(writeSQL, datas, 25)


    startTime = time.time()
    for _stocks in cut_stocks:
        res = multiProcess(_stocks)
        writeData(res)
        surplus = 60 - (time.time() - startTime)
        if surplus >= 0 and _stocks != cut_stocks[-1]:
            print(f'等待 {surplus + 5}秒')
            time.sleep(surplus + 5)
            startTime = time.time()
