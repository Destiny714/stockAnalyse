# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 19:54
# @Author  : Destiny_
# @File    : process.py
# @Software: PyCharm


import pymysql
import warnings
from common import tool_box
from rule_level import A, B, S, F
from utils.stockdata_util import *
from api import database_api, tushare_api
from models.stockDetailModel import stockDetailModel
from utils import concurrent_util, excel_util, log_util
from rule_black import levelF1, levelF2, levelF3, levelF4, levelF5
from rule_white import level1, level2, level3, level4, level5, level6, levelA1, levelA2, levelA3, levelA4

if __name__ == '__main__':
    log = log_util.log()
    sqlClient = database_api.Mysql()
    warnings.filterwarnings('ignore')
    stocks = concurrent_util.initStock(needReload=False, extra=False)
    tradeDays = sqlClient.selectTradeDate()
    stockDetails = sqlClient.selectAllStockDetail()
    aimDates = ['20220919', '20220920']


    def process(aimDate):
        stockDetailDict = concurrent_util.createStockDetailMap(stockDetails)
        _limitData = concurrent_util.getStockLimitDataByDate(date=aimDate)
        limitData_virtualDict = {
            's': virtualLimitData(_limitData, 's'),
            'f': virtualLimitData(_limitData, 'f'),
        }
        industryLimitDict = rankLimitTimeByX('limitTime-industry', aimDate, _limitData)
        limitUpCount = tushare_api.Tushare().dailyLimitCount(date=aimDate)
        errors = []
        excelDatas = []
        virtualDict = {f'{stock}': {} for stock in stocks}
        indexData = collectIndexData('GemIndex', aimDate=aimDate)
        indexData_virtual = virtualIndexData(indexData)
        excelDict: dict = excel_util.readScoreFromExcel(database_api.Mysql().selectLastTradeDate(aimDate))

        def processOneStock(argMap: dict):
            stock = argMap['stock']
            virtual = argMap['virtual']
            stockDetail = stockDetailModel(stockDetailDict[stock])
            industryLimitCount = 0 if stockDetail.industry() not in industryLimitDict.keys() else len(industryLimitDict[stockDetail.industry()])
            if virtual is not None:
                index = indexData_virtual.copy()
                limitData = limitData_virtualDict[virtual].copy()
            else:
                index = indexData.copy()
                limitData = _limitData.copy()
            try:
                data = collectData(stock, aimDate=aimDate, virtual=virtual)
                height = limit_height(stock, data)
                t0Day = data[-1]
                details = {}
                score = 0
                white_sum = 0
                black_sum = 0
                lA1 = levelA1.levelA1(stockDetail, data, index, limitData).filter()
                lA2 = levelA2.levelA2(stockDetail, data, index, limitData).filter()
                lA3 = levelA3.levelA3(stockDetail, data, index, limitData).filter()
                lA4 = levelA4.levelA4(stockDetail, data, index, limitData).filter()
                lF1 = levelF1.levelF1(stockDetail, data, index, limitData).filter()
                lF2 = levelF2.levelF2(stockDetail, data, index, limitData).filter()
                lF3 = levelF3.levelF3(stockDetail, data, index, limitData).filter()
                lF4 = levelF4.levelF4(stockDetail, data, index, limitData).filter()
                lF5 = levelF5.levelF5(stockDetail, data, index, limitData).filter()
                l1 = level1.level1(stockDetail, data, index, limitData).filter()
                l2 = level2.level2(stockDetail, data, index, limitData).filter()
                l3 = level3.level3(stockDetail, data, index, limitData).filter()
                l4 = level4.level4(stockDetail, data, index, limitData).filter()
                l5 = level5.level5(stockDetail, data, index, limitData).filter()
                l6 = level6.level6(stockDetail, data, index, limitData).filter()
                for white in [lA1, lA2, lA3, lA4]:
                    white_sum += len(white['detail'])
                    if white['result']:
                        details[white['level']] = white['detail']
                for black in [lF1, lF2, lF3, lF4, lF5]:
                    black_sum += len(black['detail'])
                    if black['result'] is False:
                        details[black['level']] = black['detail']
                for white in [l1, l2, l3, l4, l5, l6]:
                    white_sum += len(white['detail'])
                    if white['result']:
                        details[white['level']] = white['detail']
                score += len(l1['detail']) * 1
                score += len(l2['detail']) * 1
                score += len(l3['detail']) * 2
                score += len(l4['detail']) * 4
                score += len(l5['detail']) * 5
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
                    level = 'B'
                    if A.ruleA(score=score, height=height, T1S=T1S, T1F=T1F, black=black_sum, white=white_sum, S=_S,
                               data=data, aj=AJ, stock=stock, details=details).filter():
                        level = 'A'
                    if S.ruleS(score=score, height=height, T1S=T1S, T1F=T1F, black=black_sum, white=white_sum, S=_S,
                               data=data, aj=AJ, stock=stock, details=details).filter():
                        level = 'S'
                    if F.ruleF(score=score, height=height, T1S=T1S, T1F=T1F, black=black_sum, white=white_sum,
                               S=_S, details=details).filter():
                        level = 'F'
                    # if B.ruleB(height=height, black=black, b1=virtualDict[stock]['b1'], b2=virtualDict[stock]['b2']):
                    #     level = 'B'
                    result = {
                        'code': stock,
                        'name': stockDetail.name(),
                        'industry': stockDetail.industry(),
                        'ptg_industry': f'{industryLimitCount}/{limitUpCount}',
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
                    excelData = [result[_] for _ in excel_util.cols]
                    log.info(f'{aimDate}-{stock} - {"NOW" if not virtual else virtual}')
                    excelDatas.append(excelData)
                else:
                    matchDict = {'s': 'b1', 'f': 'b2'}
                    virtualDict[stock][virtual] = score
                    virtualDict[stock][matchDict[virtual]] = black_sum
                    virtualDict[stock][f'{virtual}_detail'] = details
                    log.info(f'{aimDate} - {stock} - T1{str(virtual).upper()}')
            except (IndexError, ValueError, KeyError, TypeError, pymysql.Error) as e:
                errors.append([stock, e])
                log.warning(
                    f'{aimDate} - {stock} - {"NOW" if not virtual else "".join(["T1", str(virtual).upper()])} - {e} - {tool_box.errorHandler(e)}')

        tool_box.thread_pool_executor(processOneStock, [{'stock': stock, 'virtual': 's'} for stock in stocks], 10)
        tool_box.thread_pool_executor(processOneStock, [{'stock': stock, 'virtual': 'f'} for stock in stocks], 10)
        tool_box.thread_pool_executor(processOneStock, [{'stock': stock, 'virtual': None} for stock in stocks], 10)

        def rankExcelData(d):
            _white = d[excel_util.cols.index('white')]
            _height = d[excel_util.cols.index('height')]
            _score = d[excel_util.cols.index('score')]
            return _height * 1000000 + _score * 1000 + _white * 1

        excelDatas.sort(key=rankExcelData, reverse=True)
        errStocks = list(set([_[0] for _ in errors]))
        for errStock in errStocks:
            errStockDetail = database_api.Mysql().selectStockDetail(errStock)
            _industry = errStockDetail[3]
            _stockName = errStockDetail[2]
            _industryLimitCount = 0 if _industry not in industryLimitDict.keys() else len(industryLimitDict[_industry])
            excelDatas.append([
                errStock, _stockName, _industry,
                f'{_industryLimitCount}/{limitUpCount}',
                'N/A', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0%', aimDate, '', '', ''
            ])

        excel_util.write(aimDate, excelDatas)


    for date in aimDates:
        process(date)
        tool_box.bark_pusher(f'{date}的Excel生成完毕', '请查看', _url='https://file.geekshop.space')
