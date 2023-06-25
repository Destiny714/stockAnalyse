# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 19:54
# @Author  : Destiny_
# @File    : process.py
# @Software: PyCharm

# import sys
# from utils.file_util import projectPath
# sys.path.append(projectPath())

import warnings
from prefs.params import *
from common import tool_box
from level_rule import LevelRule
from sequence.finish import Finish
from utils.stockdata_util import *
from sequence.prepare import Prepare
from utils.excel_util import ColumnModel
from utils.concurrent_util import initStock
from models.stock_detail_model import StockDetailModel
from utils import concurrent_util, excel_util, log_util
from rule_black import levelF1, levelF2, levelF3, levelF4, levelF5
from rule_white import level1, level2, level3, level4, level5, level6, levelA1, levelA2, levelA3, levelA4, levelA5, levelA6

if __name__ == '__main__':
    RunMode.Status = RunMode.DEBUG
    log = log_util.log()
    sqlClient = db.Stock_Database()  # 数据库查询client
    warnings.filterwarnings('ignore')
    stocks = initStock(False, False)  # 经过筛选的所有股票

    tradeDays = sqlClient.selectTradeDate()  # 所有交易日
    stockDetails = sqlClient.selectAllStockDetail()  # 所有股票的detail 从stockList表查到
    lead = 1
    _aimDate = lastTradeDay()
    aimDates = sqlClient.selectTradeDateByDuration(_aimDate, lead)  # 要计算的日期范围
    limitDatas = concurrent_util.getStockLimitDataByDate(_aimDate, lead)
    Prepare(None, aimDates).do()


    def process(aimDate):
        stockDetailDict = concurrent_util.createStockDetailMap(stockDetails)  # 利用stockDetails生成stock为key的dict
        limitColumnModels: list[ColumnModel] = []
        shIndex = queryIndexData('ShIndex', aimDate=aimDate)
        gemIndex = queryIndexData('GemIndex', aimDate=aimDate)

        def processModel(stock):
            stockDetail = StockDetailModel(stockDetailDict[stock])
            score = 0
            details = {}
            white_sum = 0
            black_sum = 0
            data = queryData(stock, aimDate=aimDate)
            if not t_limit(stock, data):
                return {
                    'score': score,
                    'black': black_sum,
                    'white': white_sum,
                    'details': details,
                    'stockDetail': stockDetail,
                    'data': data,
                }
            lA1 = levelA1.levelA1(stockDetail, data, gemIndex, shIndex).filter()
            lA2 = levelA2.levelA2(stockDetail, data, gemIndex, shIndex).filter()
            lA3 = levelA3.levelA3(stockDetail, data, gemIndex, shIndex).filter()
            lA4 = levelA4.levelA4(stockDetail, data, gemIndex, shIndex).filter()
            lA5 = levelA5.levelA5(stockDetail, data, gemIndex, shIndex).filter()
            lA6 = levelA6.levelA6(stockDetail, data, gemIndex, shIndex).filter()
            lF1 = levelF1.levelF1(stockDetail, data, gemIndex, shIndex).filter()
            lF2 = levelF2.levelF2(stockDetail, data, gemIndex, shIndex).filter()
            lF3 = levelF3.levelF3(stockDetail, data, gemIndex, shIndex).filter()
            lF4 = levelF4.levelF4(stockDetail, data, gemIndex, shIndex).filter()
            lF5 = levelF5.levelF5(stockDetail, data, gemIndex, shIndex).filter()
            l1 = level1.level1(stockDetail, data, gemIndex, shIndex).filter()
            l2 = level2.level2(stockDetail, data, gemIndex, shIndex).filter()
            l3 = level3.level3(stockDetail, data, gemIndex, shIndex).filter()
            l4 = level4.level4(stockDetail, data, gemIndex, shIndex).filter()
            l5 = level5.level5(stockDetail, data, gemIndex, shIndex).filter()
            l6 = level6.level6(stockDetail, data, gemIndex, shIndex).filter()
            for white in [lA1, lA2, lA3, lA4, lA5, lA6]:
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
            score += len(l4['detail']) * 3
            score += len(l5['detail']) * 5
            score += len(l6['detail']) * 7
            score += len(lA1['detail']) * 4
            score += len(lA2['detail']) * 3
            score += len(lA3['detail']) * 3
            score += len(lA4['detail']) * 2
            score += len(lA5['detail']) * 2
            score += len(lA6['detail']) * 2
            score -= len(lF1['detail']) * 5
            score -= len(lF2['detail']) * 5
            score -= len(lF3['detail']) * 5
            score -= len(lF4['detail']) * 5
            score -= len(lF5['detail']) * 7
            return {
                'score': score,
                'black': black_sum,
                'white': white_sum,
                'details': details,
                'stockDetail': stockDetail,
                'data': data,
            }

        def processModelResult(stock):
            try:
                modelResult = processModel(stock)
                data = modelResult['data']
                score = modelResult['score']
                black_sum = modelResult['black']
                white_sum = modelResult['white']
                details = modelResult['details']
                stockDetail = modelResult['stockDetail']
                height = limit_height(stock, data)
                isLimit = t_limit(stock, data)
                t0Day = data[-1]
                AJ = t0Day.concentration
                CF = t0Day.CF
                TF = t0Day.TF
                TP = t0Day.TP
                CP = t0Day.CP
                limitOpenTime = t0Day.limitOpenTime
                buy_elg_2 = day2elg(data)
                buy_elg_3 = day3elg(data)
                if isLimit:
                    scoreLevelData = {
                        'score': score,
                        'height': height,
                        'black': black_sum,
                        'white': white_sum,
                        'data': data,
                        'AJ': AJ,
                        'CF': CF,
                        'TF': TF,
                        'TP': TP,
                        'CP': CP,
                        'stock': stock,
                        'details': details,
                        'day2elg': buy_elg_2,
                        'day3elg': buy_elg_3,
                        'is1': model_1(stock, data),
                    }
                    levelModel = LevelRule(scoreLevelData)
                    levelModel.filter()
                    level = levelModel.limitRank
                else:
                    level = 'O'
                result = {
                    'code': stock,
                    'name': stockDetail.name,
                    'industry': stockDetail.industry,
                    'AJ': AJ,
                    'CF': CF,
                    'TF': TF,
                    'TP': TP,
                    'CP': CP,
                    'limitOpenTime': limitOpenTime,
                    'level': level,
                    'height': height,
                    'white': white_sum,
                    'black': black_sum,
                    'score': score,
                    'open_price': f'{round(t_open_pct(data) * 100, 2)}%',
                    'date': aimDate,
                    'details': str(details),
                    'day2elg': buy_elg_2,
                    'day3elg': buy_elg_3,
                }
                log.info(f'{aimDate}-{stock} - NOW')
                limitColumnModels.append(ColumnModel(result))
            except (IndexError, ValueError, KeyError, TypeError) as er:
                log.warning(f'{aimDate} - {stock} - NOW - {er} - {tool_box.errorHandler(er)}')

        tool_box.thread_pool_executor(processModelResult, stocks, 20)
        log.info('模型运行完毕')

        def rankExcelData(d: ColumnModel):
            d = d.dict()
            _height = d['height']
            _TP = d['TP']
            return _height * 1000000 + _TP * 100

        limitColumnModels.sort(key=rankExcelData, reverse=True)
        columnModels = limitColumnModels
        try:
            excel_util.write(aimDate, columnModels)
        except Exception as e:
            log.error('模型数据写入excel出错')
            log.error_quick(e)


    for date in aimDates:
        process(date)
        Finish(date).all()
