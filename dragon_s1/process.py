# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 19:54
# @Author  : Destiny_
# @File    : process.py
# @Software: PyCharm
import os
import sys

sys.path.append(os.getcwd().replace('/dragon_s1', ''))

import excel_process
from rule_level import A, S, F
from api import databaseApi, tushareApi
from rule_black import levelF1, levelF2, levelF3, levelF4, levelF5
from common import toolBox, concurrentActions, dateHandler, push
from rule_white import level1, level2, level3, level4, level5, levelA1, levelA2, levelS1, levelS2
from common.collect_data import collectData, t_open_pct, limit_height

if __name__ == '__main__':
    stocks = concurrentActions.initStock(needReload=False, extra=False)
    tradeDays = databaseApi.Mysql().selectTradeDate()
    aimDates = ['20220808']


    def process(aimDate):
        industryLimitDict = concurrentActions.industryIndex(aimDate=aimDate)
        limitUpCount = len(tushareApi.Tushare().allLimitUpDetail(date=aimDate))
        errors = []
        excelDatas = []
        virtualDict = {f'{stock}': {} for stock in stocks}
        excelDict: dict = excel_process.readScoreFromExcel(databaseApi.Mysql().selectLastDate(aimDate))

        def processOneStock(argMap: dict):
            stock = argMap['stock']
            virtual = argMap['virtual']
            try:
                data = collectData(stock, aimDate=aimDate, virtual=virtual)
                details = {}
                score = 0
                white_sum = 0
                black_sum = 0
                l1 = level1.level1(stock, data).filter()
                l2 = level2.level2(stock, data).filter()
                l3 = level3.level3(stock, data, virtual=virtual).filter()
                l4 = level4.level4(stock, data).filter()
                l5 = level5.level5(stock, data, virtual=virtual).filter()
                lA1 = levelA1.levelA1(stock, data).filter()
                lA2 = levelA2.levelA2(stock, data).filter()
                lS1 = levelS1.levelS1(stock, data).filter()
                lS2 = levelS2.levelS2(stock, data).filter()
                lF1 = levelF1.levelF1(stock, data, virtual=virtual).filter()
                lF2 = levelF2.levelF2(stock, data, virtual=virtual).filter()
                lF3 = levelF3.levelF3(stock, data, virtual=virtual).filter()
                lF4 = levelF4.levelF4(stock, data, virtual=virtual).filter()
                lF5 = levelF5.levelF5(stock, data).filter()
                for white in [l1, l2, l3, l4, l5, lA1, lA2, lS1, lS2]:
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
                score += len(l2['detail']) * 2
                score += len(l3['detail']) * 3
                score += len(l4['detail']) * 5
                score += len(l5['detail']) * 8
                score += len(lA1['detail']) * 8
                score += len(lA2['detail']) * 8
                score += len(lS1['detail']) * 10
                score += len(lS2['detail']) * 10
                score -= len(lF1['detail']) * 5
                score -= len(lF2['detail']) * 5
                score -= len(lF3['detail']) * 8
                score -= len(lF4['detail']) * 8
                score -= len(lF5['detail']) * 10
                if virtual is None:
                    stockDetail = databaseApi.Mysql().selectStockDetail(stock)
                    industry = databaseApi.Mysql().selectIndustryByStock(stock)
                    height = limit_height(stock, data)
                    T1S = virtualDict[stock]['s']
                    T1F = virtualDict[stock]['f']
                    level = 'B'
                    if A.ruleA(score=score, height=height, T1S=T1S, T1F=T1F, black=black_sum, white=white_sum).filter():
                        level = 'A'
                    if F.ruleF(score=score, height=height, T1S=T1S, T1F=T1F, black=black_sum, white=white_sum).filter():
                        level = 'F'
                    if S.ruleS(score=score, height=height, T1S=T1S, T1F=T1F, black=black_sum, white=white_sum).filter():
                        level = 'S'
                    result = {
                        'code': stock,
                        'name': stockDetail[2],
                        'industry': stockDetail[3],
                        'ptg_industry': f'{industryLimitDict[industry]["limit"]}/{limitUpCount}',
                        'AJ': round(data[-1].concentration() * 100, 2),
                        'INJ': round(industryLimitDict[industry]["concentration"] * 100, 2),
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
                    excelData = [result[_] for _ in excel_process.cols]
                    print(result)
                    excelDatas.append(excelData)
                else:
                    virtualDict[stock][virtual] = score
                    virtualDict[stock][f'{virtual}_detail'] = details
                    print(f'virtual {str(virtual).upper()} {stock}')
            except Exception as e:
                errors.append([stock, e])

        toolBox.thread_pool_executor(processOneStock, [{'stock': stock, 'virtual': 's'} for stock in stocks], 10)
        toolBox.thread_pool_executor(processOneStock, [{'stock': stock, 'virtual': 'f'} for stock in stocks], 10)
        toolBox.thread_pool_executor(processOneStock, [{'stock': stock, 'virtual': None} for stock in stocks], 10)

        for error in errors:
            toolBox.errorHandler(error[1], arg=error[0])

        def rankExcelData(d):
            _height = d[7]
            _score = d[10]
            _white = d[8]
            return _height * 10000 + _score * 100 + _white * 1

        excelDatas.sort(key=rankExcelData, reverse=True)

        excel_process.write(aimDate, excelDatas)


    for date in aimDates:
        process(date)
        try:
            push.bark_pusher(f'{date}的Excel生成完毕', '请查看', _url='https://file.geekshop.space')
        except:
            pass
