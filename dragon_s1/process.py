# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 19:54
# @Author  : Destiny_
# @File    : process.py
# @Software: PyCharm


import pymysql
import warnings
import excel_process
from rule_level import A, S, F
from api import databaseApi, tushareApi
from common import toolBox, concurrentActions, dateHandler, push
from rule_black import levelF1, levelF2, levelF3, levelF4, levelF5
from rule_white import level1, level2, level3, level4, level5, level6, levelA1, levelA2, levelA3, levelA4
from common.collect_data import collectData, t_open_pct, limit_height, collectIndexData, virtualIndexData

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    stocks = concurrentActions.initStock(needReload=False, extra=False)
    tradeDays = databaseApi.Mysql().selectTradeDate()
    aimDates = [dateHandler.lastTradeDay()]


    def process(aimDate):
        industryIndexDict = concurrentActions.industryIndex(aimDate=aimDate)
        limitUpCount = tushareApi.Tushare().dailyLimitCount(date=aimDate)
        limitTimeRank = concurrentActions.rankingLimitTime(aimDate)
        errors = []
        excelDatas = []
        virtualDict = {f'{stock}': {} for stock in stocks}
        indexData = collectIndexData('ShIndex')
        nextTradeDay = databaseApi.Mysql().selectNextTradeDay(aimDate)
        excelDict: dict = excel_process.readScoreFromExcel(databaseApi.Mysql().selectLastDate(aimDate))

        def processOneStock(argMap: dict):
            index = indexData
            stock = argMap['stock']
            virtual = argMap['virtual']
            stockDetail = databaseApi.Mysql().selectStockDetail(stock)
            industry = stockDetail[3]
            industryLimitRank = industryIndexDict[industry]['rank']
            if virtual is not None:
                index = virtualIndexData(indexData, nextTradeDay)
            try:
                data = collectData(stock, aimDate=aimDate, virtual=virtual)
                t0Day = data[-1]
                details = {}
                score = 0
                white_sum = 0
                black_sum = 0
                l1 = level1.level1(stock, data).filter()
                l2 = level2.level2(stock, data).filter()
                l3 = level3.level3(stock, data, index).filter()
                l4 = level4.level4(stock, data, index).filter()
                l5 = level5.level5(stock, data, index, limitTimeRank, industryLimitRank).filter()
                l6 = level6.level6(stock, data, index).filter()
                lA1 = levelA1.levelA1(stock, data).filter()
                lA2 = levelA2.levelA2(stock, data).filter()
                lA3 = levelA3.levelA3(stock, data).filter()
                lA4 = levelA4.levelA4(stock, data).filter()
                lF1 = levelF1.levelF1(stock, data, index, industryLimitRank).filter()
                lF2 = levelF2.levelF2(stock, data, index).filter()
                lF3 = levelF3.levelF3(stock, data, index).filter()
                lF4 = levelF4.levelF4(stock, data, index).filter()
                lF5 = levelF5.levelF5(stock, data, index).filter()
                for white in [l1, l2, l3, l4, l5, l6, lA1, lA2, lA3, lA4]:
                    if virtual is None:
                        white_sum += len(white['detail'])
                    if white['result']:
                        details[white['level']] = white['detail']
                for black in [lF1, lF2, lF3, lF4, lF5]:
                    if virtual is None:
                        black_sum += len(black['detail'])
                    if black['result'] is False:
                        details[black['level']] = black['detail']
                score += len(l1['detail']) * 1
                score += len(l2['detail']) * 1
                score += len(l3['detail']) * 2
                score += len(l4['detail']) * 4
                score += len(l5['detail']) * 7
                score += len(l6['detail']) * 7
                score += len(lA1['detail']) * 4
                score += len(lA2['detail']) * 3
                score += len(lA3['detail']) * 3
                score += len(lA4['detail']) * 3
                score -= len(lF1['detail']) * 5
                score -= len(lF2['detail']) * 5
                score -= len(lF3['detail']) * 7
                score -= len(lF4['detail']) * 7
                score -= len(lF5['detail']) * 8
                if virtual is None:
                    height = limit_height(stock, data)
                    T1S = virtualDict[stock]['s']
                    T1F = virtualDict[stock]['f']
                    _S = int(score - excelDict[stock]['score'] if excelDict != {} else -8888)
                    AJ = round(data[-1].concentration() * 100, 1)
                    CF = -8888 if (t0Day.buy_elg_vol() + t0Day.buy_lg_vol()) == 0 else round(
                        ((t0Day.buy_elg_vol() + t0Day.buy_lg_vol() - t0Day.sell_elg_vol() - t0Day.sell_lg_vol()) / (
                                t0Day.buy_elg_vol() + t0Day.buy_lg_vol())) * 100, 1)
                    TF = -8888 if t0Day.buy_elg_vol() == 0 else round(
                        ((t0Day.buy_elg_vol() - t0Day.sell_elg_vol()) / t0Day.buy_elg_vol()) * 100, 1)
                    TP = -8888 if t0Day.volume() == 0 else round((t0Day.buy_elg_vol() / t0Day.volume()) * 100, 1)
                    hitPlus = (len(lA1['detail']) + len(lA2['detail']) + len(lA3['detail'])) > 0
                    level = 'B'
                    if A.ruleA(score=score, height=height, T1S=T1S, T1F=T1F, black=black_sum, white=white_sum, S=_S,
                               data=data, aj=AJ, stock=stock).filter():
                        level = 'A'
                    if S.ruleS(score=score, height=height, T1S=T1S, T1F=T1F, black=black_sum, white=white_sum, S=_S,
                               data=data, aj=AJ, stock=stock).filter():
                        level = 'S'
                    if F.ruleF(score=score, height=height, T1S=T1S, T1F=T1F, black=black_sum, white=white_sum,
                               S=_S, F5=len(lF5['detail']), hitPlus=hitPlus).filter():
                        level = 'F'
                    result = {
                        'code': stock,
                        'name': stockDetail[2],
                        'industry': stockDetail[3],
                        'ptg_industry': f'{industryIndexDict[industry]["limit"]}/{limitUpCount}',
                        'AJ': AJ,
                        'CF': CF,
                        'TF': TF,
                        'TP': TP,
                        'level': level,
                        'height': height,
                        'white': white_sum,
                        'black': black_sum,
                        'b1': virtualDict[stock]['b1'],
                        'b2': virtualDict[stock]['b2'],
                        'score': score,
                        'T1S': T1S,
                        'T1F': T1F,
                        'S': _S,
                        'open_price': f'{round(t_open_pct(data) * 100, 2)}%',
                        'date': aimDate,
                        'details': str(details),
                        'T1S_detail': str(virtualDict[stock]['s_detail']),
                        'T1F_detail': str(virtualDict[stock]['f_detail']),
                    }
                    excelData = [result[_] for _ in excel_process.cols]
                    print(result)
                    excelDatas.append(excelData)
                else:
                    matchDict = {'s': 'b1', 'f': 'b2'}
                    virtualDict[stock][virtual] = score
                    virtualDict[stock][matchDict[virtual]] = black_sum
                    virtualDict[stock][f'{virtual}_detail'] = details
                    print(f'virtual {str(virtual).upper()} {stock}')
            except (IndexError, ValueError, KeyError, TypeError, pymysql.Error) as e:
                errors.append([stock, e])

        toolBox.thread_pool_executor(processOneStock, [{'stock': stock, 'virtual': 's'} for stock in stocks], 10)
        toolBox.thread_pool_executor(processOneStock, [{'stock': stock, 'virtual': 'f'} for stock in stocks], 10)
        toolBox.thread_pool_executor(processOneStock, [{'stock': stock, 'virtual': None} for stock in stocks], 10)

        def rankExcelData(d):
            _white = d[excel_process.cols.index('white')]
            _height = d[excel_process.cols.index('height')]
            _score = d[excel_process.cols.index('score')]
            return _height * 1000000 + _score * 1000 + _white * 1

        excelDatas.sort(key=rankExcelData, reverse=True)
        errStocks = list(set([_[0] for _ in errors]))
        for error in errors:
            toolBox.errorHandler(error[1], arg=error[0])
        for errStock in errStocks:
            errStockDetail = databaseApi.Mysql().selectStockDetail(errStock)
            excelDatas.append([
                errStock, errStockDetail[2], errStockDetail[3],
                f'{industryIndexDict[errStockDetail[3]]["limit"]}/{limitUpCount}',
                'N/A', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0%', aimDate, '', '', ''
            ])

        excel_process.write(aimDate, excelDatas)


    for date in aimDates:
        process(date)
        push.bark_pusher(f'{date}的Excel生成完毕', '请查看', _url='https://file.geekshop.space')
