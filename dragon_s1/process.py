# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 19:54
# @Author  : Destiny_
# @File    : process.py
# @Software: PyCharm

import write_excel
from rule_level import A, S, F
from api import databaseApi, tushareApi
from rule_black import level6, level7, level8, level9
from common import toolBox, concurrentActions, dateHandler
from rule_white import level1, level2, level3, level4, level5
from common.collect_data import collectData, t_open_pct, limit_height

if __name__ == '__main__':
    stocks = concurrentActions.initStock(needReload=False, extra=True)
    tradeDays = databaseApi.Mysql().selectTradeDate()
    aimDates = [dateHandler.lastTradeDay()]


    def process(aimDate):
        industryLimitDict = concurrentActions.industryLimit(aimDate=aimDate)
        limitUpCount = len(tushareApi.Tushare().allLimitUpDetail(date=aimDate))
        errors = []
        excelDatas = []
        virtualDict = {f'{stock}': {} for stock in stocks}
        excelDict: dict = toolBox.readScoreFromExcel(databaseApi.Mysql().selectLastDate(aimDate))

        def processVirtualS(stock):
            details = {}
            try:
                data = collectData(stock, aimDate=aimDate, virtual='s')
                score = 0
                l1 = level1.level1(stock, data).filter()
                l2 = level2.level2(stock, data).filter()
                l3 = level3.level3(stock, data).filter()
                l4 = level4.level4(stock, data).filter()
                l5 = level5.level5(stock, data, virtual='s').filter()
                l6 = level6.level6(stock, data).filter()
                l7 = level7.level7(stock, data).filter()
                l8 = level8.level8(stock, data, virtual='s').filter()
                l9 = level9.level9(stock, data).filter()
                for white in [l1, l2, l3, l4, l5]:
                    if white['result']:
                        details[white['level']] = white['detail']
                for black in [l6, l7, l8, l9]:
                    if black['result'] is False:
                        details[black['level']] = black['detail']
                for white in [l1, l2]:
                    score += len(white['detail'])
                score += len(l3['detail']) * 2
                score += len(l4['detail']) * 4
                score += len(l5['detail']) * 8
                for black in [l6, l7]:
                    score -= len(black['detail']) * 2
                for black in [l8, l9]:
                    score -= len(black['detail']) * 4
                virtualDict[stock]['s'] = score
                virtualDict[stock]['s_detail'] = details
                print(f'virtual S {stock}')
            except Exception as e:
                errors.append([stock, e])

        def processVirtualF(stock):
            details = {}
            try:
                data = collectData(stock, aimDate=aimDate, virtual='f')
                score = 0
                l1 = level1.level1(stock, data).filter()
                l2 = level2.level2(stock, data).filter()
                l3 = level3.level3(stock, data).filter()
                l4 = level4.level4(stock, data).filter()
                l5 = level5.level5(stock, data, virtual='f').filter()
                l6 = level6.level6(stock, data).filter()
                l7 = level7.level7(stock, data).filter()
                l8 = level8.level8(stock, data, virtual='f').filter()
                l9 = level9.level9(stock, data).filter()
                for white in [l1, l2, l3, l4, l5]:
                    if white['result']:
                        details[white['level']] = white['detail']
                for black in [l6, l7, l8, l9]:
                    if black['result'] is False:
                        details[black['level']] = black['detail']
                for white in [l1, l2]:
                    score += len(white['detail'])
                score += len(l3['detail']) * 2
                score += len(l4['detail']) * 4
                score += len(l5['detail']) * 8
                for black in [l6, l7]:
                    score -= len(black['detail']) * 2
                for black in [l8, l9]:
                    score -= len(black['detail']) * 4
                virtualDict[stock]['f'] = score
                virtualDict[stock]['f_detail'] = details
                print(f'virtual F {stock}')
            except Exception as e:
                errors.append([stock, e])

        def processOne(stock):
            try:
                data = collectData(stock, aimDate=aimDate)
                details = {}
                score = 0
                white_sum = 0
                black_sum = 0
                l1 = level1.level1(stock, data).filter()
                l2 = level2.level2(stock, data).filter()
                l3 = level3.level3(stock, data).filter()
                l4 = level4.level4(stock, data).filter()
                l5 = level5.level5(stock, data).filter()
                l6 = level6.level6(stock, data).filter()
                l7 = level7.level7(stock, data).filter()
                l8 = level8.level8(stock, data).filter()
                l9 = level9.level9(stock, data).filter()
                for white in [l1, l2, l3, l4, l5]:
                    white_sum += len(white['detail'])
                    if white['result']:
                        details[white['level']] = white['detail']
                for black in [l6, l7, l8, l9]:
                    black_sum += len(black['detail'])
                    if black['result'] is False:
                        details[black['level']] = black['detail']
                for white in [l1, l2]:
                    score += len(white['detail'])
                score += len(l3['detail']) * 2
                score += len(l4['detail']) * 4
                score += len(l5['detail']) * 8
                for black in [l6, l7]:
                    score -= len(black['detail']) * 2
                for black in [l8, l9]:
                    score -= len(black['detail']) * 4
                stockDetail = databaseApi.Mysql().selectStockDetail(stock)
                industry = databaseApi.Mysql().selectIndustryByStock(stock)
                height = limit_height(stock, data)
                T1S = virtualDict[stock]['s']
                T1F = virtualDict[stock]['f']
                level = 'B'
                if A.ruleA(score=score, height=height, T1S=T1S, T1F=T1F, black=black_sum).filter():
                    level = 'A'
                if F.ruleF(score=score, height=height, T1S=T1S, T1F=T1F, black=black_sum).filter():
                    level = 'F'
                if S.ruleS(score=score, height=height, T1S=T1S, T1F=T1F, black=black_sum).filter():
                    level = 'S'
                result = {
                    'code': stock,
                    'name': stockDetail[2],
                    'industry': stockDetail[3],
                    'ptg_industry': f'{industryLimitDict[industry]}/{limitUpCount}',
                    'level': level,
                    'height': height,
                    'white': white_sum,
                    'black': black_sum,
                    'score': score,
                    'T1S': T1S,
                    'T1F': T1F,
                    'S': int(score - excelDict[stock]['score'] if excelDict != {} else -8888),
                    'W': int(white_sum - excelDict[stock]['white'] if excelDict != {} else -8888),
                    'B': int(black_sum - excelDict[stock]['black'] if excelDict != {} else -8888),
                    'open_price': f'{round(t_open_pct(data) * 100, 2)}%',
                    'date': aimDate,
                    'details': str(details),
                    'T1S_detail': str(virtualDict[stock]['s_detail']),
                    'T1F_detail': str(virtualDict[stock]['f_detail']),
                }
                excelData = [
                    result['code'], result['name'], result['industry'],
                    result['ptg_industry'], result['level'], result['height'],
                    result['white'], result['black'], result['score'],
                    result['T1S'], result['T1F'],
                    result['S'], result['W'], result['B'],
                    result['open_price'], result['date'], result['details'],
                    result['T1S_detail'], result['T1F_detail'],
                ]
                print(result)
                excelDatas.append(excelData)
            except Exception as e:
                errors.append([stock, e])

        toolBox.thread_pool_executor(processVirtualS, stocks, 10)
        toolBox.thread_pool_executor(processVirtualF, stocks, 10)
        toolBox.thread_pool_executor(processOne, stocks, 10)

        for error in errors:
            toolBox.errorHandler(error[1], arg=error[0])

        def rankExcelData(d):
            _height = d[5]
            _score = d[8]
            _white = d[6]
            return _height * 10000 + _score * 100 + _white * 1

        excelDatas.sort(key=rankExcelData, reverse=True)

        write_excel.write(aimDate, excelDatas)


    for date in aimDates:
        process(date)
