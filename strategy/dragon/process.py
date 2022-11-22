# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 19:54
# @Author  : Destiny_
# @File    : process.py
# @Software: PyCharm


import warnings
from prefs.params import *
from api import tushare_api
from common import tool_box
from rule_level import A, B, S, F
from sequence.finish import Finish
from utils.stockdata_util import *
from sequence.prepare import Prepare
from utils.excel_util import ColumnModel
from utils.concurrent_util import initStock
from models.stock_detail_model import StockDetailModel
from utils import concurrent_util, excel_util, log_util
from rule_black import levelF1, levelF2, levelF3, levelF4, levelF5
from rule_white import level1, level2, level3, level4, level5, level6, levelA1, levelA2, levelA3, levelA4, levelA5

if __name__ == '__main__':
    RunMode.Status = RunMode.DEBUG
    log = log_util.log()
    sqlClient = db.Mysql()  # 数据库查询client
    warnings.filterwarnings('ignore')
    stocks = initStock(False, False)  # 经过筛选的所有股票
    tradeDays = sqlClient.selectTradeDate()  # 所有交易日
    stockDetails = sqlClient.selectAllStockDetail()  # 所有股票的detail 从stockList表查到
    aimDates = sqlClient.selectTradeDateByDuration(lastTradeDay(), 2)  # 要计算的日期范围
    Prepare(stocks, aimDates).do()
    sqlClient.close()


    def process(aimDate):
        stockDetailDict = concurrent_util.createStockDetailMap(stockDetails)  # 利用stockDetails生成stock为key的dict
        _limitData = Params.dailyLimitData[aimDate]  # 从stockLimit表读取当日所有涨停票详情 返回 dict[str, list[limitDataModel]]
        limitData_virtualDict = {  # 生成下一天虚拟数据的涨停票详情
            's': virtualLimitData(_limitData, 's'),
            'f': virtualLimitData(_limitData, 'f'),
        }
        industryLimitDict = Params.dailyIndustryLimitDict[aimDate]  # 通过行业分类生成行业涨停票列表 返回dict[行业，股票列表]
        limitUpCount = tushare_api.Tushare().dailyLimitCount(date=aimDate)
        errors = []
        columnModels = []
        virtualDict = {f'{stock}': {} for stock in stocks}
        shIndexData = queryIndexData('ShIndex', aimDate=aimDate)
        gemIndexData = queryIndexData('GemIndex', aimDate=aimDate)
        shIndexData_virtual = virtualIndexData(shIndexData)
        gemIndexData_virtual = virtualIndexData(gemIndexData)
        excelDict: dict = excel_util.readScoreFromExcel(db.Mysql().selectPrevTradeDate(aimDate))

        def processOneStock(argMap: dict):
            stock = argMap['stock']
            virtual = argMap['virtual']
            g.save(virtual, 'virtual')
            stockDetail = StockDetailModel(stockDetailDict[stock])
            industryLimitCount = 0 if stockDetail.industry not in industryLimitDict.keys() else len(industryLimitDict[stockDetail.industry])
            if virtual is not None:
                shIndex = shIndexData_virtual
                gemIndex = gemIndexData_virtual
                limitData = limitData_virtualDict[virtual]
            else:
                shIndex = shIndexData
                gemIndex = gemIndexData
                limitData = _limitData
            try:
                data = queryData(stock, aimDate=aimDate, virtual=virtual)
                height = limit_height(stock, data)
                t0Day = data[-1]
                details = {}
                score = 0
                white_sum = 0
                black_sum = 0
                lA1 = levelA1.levelA1(stockDetail, data, gemIndex, shIndex, limitData).filter()
                lA2 = levelA2.levelA2(stockDetail, data, gemIndex, shIndex, limitData).filter()
                lA3 = levelA3.levelA3(stockDetail, data, gemIndex, shIndex, limitData).filter()
                lA4 = levelA4.levelA4(stockDetail, data, gemIndex, shIndex, limitData).filter()
                lA5 = levelA5.levelA5(stockDetail, data, gemIndex, shIndex, limitData).filter()
                lF1 = levelF1.levelF1(stockDetail, data, gemIndex, shIndex, limitData).filter()
                lF2 = levelF2.levelF2(stockDetail, data, gemIndex, shIndex, limitData).filter()
                lF3 = levelF3.levelF3(stockDetail, data, gemIndex, shIndex, limitData).filter()
                lF4 = levelF4.levelF4(stockDetail, data, gemIndex, shIndex, limitData).filter()
                lF5 = levelF5.levelF5(stockDetail, data, gemIndex, shIndex, limitData).filter()
                l1 = level1.level1(stockDetail, data, gemIndex, shIndex, limitData).filter()
                l2 = level2.level2(stockDetail, data, gemIndex, shIndex, limitData).filter()
                l3 = level3.level3(stockDetail, data, gemIndex, shIndex, limitData).filter()
                l4 = level4.level4(stockDetail, data, gemIndex, shIndex, limitData).filter()
                l5 = level5.level5(stockDetail, data, gemIndex, shIndex, limitData).filter()
                l6 = level6.level6(stockDetail, data, gemIndex, shIndex, limitData).filter()
                for white in [lA1, lA2, lA3, lA4, lA5]:
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
                score -= len(lF1['detail']) * 5
                score -= len(lF2['detail']) * 5
                score -= len(lF3['detail']) * 5
                score -= len(lF4['detail']) * 5
                score -= len(lF5['detail']) * 7
                if virtual is None:
                    T1S = virtualDict[stock]['s']
                    T1F = virtualDict[stock]['f']
                    _S = int(score - excelDict[stock]['score'] if excelDict != {} else -8888)
                    AJ = round(data[-1].concentration * 100, 1)
                    CF = t0Day.CF
                    TF = t0Day.TF
                    TP = t0Day.TP
                    CP = t0Day.CP
                    limitOpenTime = t0Day.limitOpenTime
                    b1 = virtualDict[stock]['b1']
                    b2 = virtualDict[stock]['b2']
                    scoreLevelData = {
                        'b1': b1,
                        'b2': b2,
                        'score': score,
                        'height': height,
                        'T1S': T1S,
                        'T1F': T1F,
                        'black': black_sum,
                        'white': white_sum,
                        'S': _S,
                        'data': data,
                        'AJ': AJ,
                        'CF': CF,
                        'TF': TF,
                        'TP': TP,
                        'stock': stock,
                        'details': details,
                    }
                    level = 'F'
                    if F.ruleF(scoreLevelData).filter():
                        level = 'F'
                    if B.ruleB(scoreLevelData).filter():
                        level = 'B'
                    if A.ruleA(scoreLevelData).filter():
                        level = 'A'
                    if S.ruleS(scoreLevelData).filter():
                        level = 'S'
                    result = {
                        'code': stock,
                        'name': stockDetail.name,
                        'industry': stockDetail.industry,
                        'ptg_industry': f'{industryLimitCount}/{limitUpCount}',
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
                        'b1': b1,
                        'b2': b2,
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
                    log.info(f'{aimDate}-{stock} - {"NOW" if not virtual else virtual}')
                    columnModels.append(ColumnModel(result))
                else:
                    matchDict = {'s': 'b1', 'f': 'b2'}
                    virtualDict[stock][virtual] = score
                    virtualDict[stock][matchDict[virtual]] = black_sum
                    virtualDict[stock][f'{virtual}_detail'] = details
                    log.info(f'{aimDate} - {stock} - T1{str(virtual).upper()}')
            except (IndexError, ValueError, KeyError, TypeError) as e:
                errors.append([stock, e])
                log.warning(
                    f'{aimDate} - {stock} - {"NOW" if not virtual else "".join(["T1", str(virtual).upper()])} - {e} - {tool_box.errorHandler(e)}')

        tool_box.thread_pool_executor(processOneStock, [{'stock': stock, 'virtual': 's'} for stock in stocks], 10)
        tool_box.thread_pool_executor(processOneStock, [{'stock': stock, 'virtual': 'f'} for stock in stocks], 10)
        tool_box.thread_pool_executor(processOneStock, [{'stock': stock, 'virtual': None} for stock in stocks], 10)

        def rankExcelData(d: ColumnModel):
            d = d.dict()
            _white = d['white']
            _height = d['height']
            _score = d['score']
            return _height * 1000000 + _score * 1000 + _white * 1

        columnModels.sort(key=rankExcelData, reverse=True)
        errStocks = list(set([_[0] for _ in errors]))
        for errStock in errStocks:
            errStockDetail = db.Mysql().selectStockDetail(errStock)
            _stockName = errStockDetail[2]
            res = {'code': errStock, 'name': _stockName, 'level': 'N/A'}
            columnModels.append(ColumnModel(res))

        excel_util.write(aimDate, columnModels)


    for date in aimDates:
        process(date)
        Finish(date).all()
