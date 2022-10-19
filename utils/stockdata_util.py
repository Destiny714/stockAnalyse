# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 19:55
# @Author  : Destiny_
# @File    : stockdata_util.py
# @Software: PyCharm

from utils.date_util import *
from models.stock_data_model import *
from models.limit_data_model import *


def queryIndexData(index, dateRange: int = 500, aimDate=lastTradeDay()) -> list[StockDataModel]:
    mysql = db.Mysql()
    allData = mysql.selectOneAllData(stock=index, dateRange=dateRange, aimDate=aimDate)
    res = [StockDataModel(allData[i]) for i in range(len(allData))]
    return res


def virtualIndexData(data: list[StockDataModel]) -> list[StockDataModel]:
    res = data.copy()
    modifyData = list(res[-1])
    modifyData[0] = 8888
    modifyData[1] = db.Mysql().selectNextTradeDay(modifyData[1])
    res.append(StockDataModel(modifyData))
    return res


def virtualLimitData(data: dict[str, list[LimitDataModel]], virtual=None) -> dict[str, list[LimitDataModel]]:
    d = data.copy()
    today = str(max(int(_) for _ in data.keys()))
    nextDay = db.Mysql().selectNextTradeDay(today)
    modifyDatas = d[today].copy()

    def one(a: LimitDataModel):
        b = list(a)
        b[1] = nextDay
        b[6] = a.close
        if virtual == 's':
            b[4] = a.close * 1.07
            b[5] = a.close * (1 + (limit(a.stock) / 100)),
            b[8] = a.amount() * 0.6
            b[9] = a.turnover * 0.6
            b[11] = joinTimeToStamp(nextDay, '09:36:00')
            b[12] = joinTimeToStamp(nextDay, '09:36:00')
            b[15] = a.limitHeight + 1
        if virtual == 'f':
            b[4] = a.close * 1.03
            b[5] = a.close * (1 + (limit(a.stock) / 100)),
            b[8] = a.amount() * 1.4
            b[9] = a.turnover * 1.4
            b[11] = joinTimeToStamp(nextDay, '09:50:00')
            b[12] = joinTimeToStamp(nextDay, '14:00:00')
            b[15] = a.limitHeight + 1
        return LimitDataModel(b)

    newModifyDatas = [one(_) for _ in modifyDatas]
    d[nextDay] = newModifyDatas
    return d


def queryData(stock, dateRange: int = 800, aimDate=lastTradeDay(), virtual=None) -> list[StockDataModel]:
    mysql = db.Mysql()
    try:
        allData = mysql.selectOneAllData(stock=stock, dateRange=dateRange, aimDate=aimDate)
    except:
        allData = mysql.selectOneAllData(stock=stock, dateRange=None, aimDate=aimDate)
    res = [StockDataModel(_) for _ in allData]
    if virtual is None:
        pass
    elif virtual == 's':
        modifyData = res[-1]
        nextDate = mysql.selectNextTradeDay(modifyData.date)
        largePct = 1.3
        smallPct = 0.7
        virtualData = [8888,
                       nextDate,
                       modifyData.close * 1.07,
                       modifyData.close * (1 + (limit(stock) / 100)),
                       modifyData.close,
                       modifyData.close * (1 + (limit(stock) / 100)),
                       modifyData.close * 1.06,
                       limit(stock),
                       modifyData.volume * 0.6,
                       modifyData.amount * 0.6,
                       modifyData.turnover * 0.6,
                       joinTimeToStamp(nextDate, '09:36:00'),
                       joinTimeToStamp(nextDate, '09:36:00'),
                       0,
                       modifyData.buy_sm_vol * smallPct,
                       modifyData.buy_sm_amount * smallPct,
                       modifyData.sell_sm_vol * smallPct,
                       modifyData.sell_sm_amount * smallPct,
                       modifyData.buy_md_vol * smallPct,
                       modifyData.buy_md_amount * smallPct,
                       modifyData.sell_md_vol * smallPct,
                       modifyData.sell_md_amount * smallPct,
                       modifyData.buy_lg_vol * largePct,
                       modifyData.buy_lg_amount * largePct,
                       modifyData.sell_lg_vol * largePct,
                       modifyData.sell_lg_amount * largePct,
                       modifyData.buy_elg_vol * largePct,
                       modifyData.buy_elg_amount * largePct,
                       modifyData.sell_elg_vol * largePct,
                       modifyData.sell_elg_amount * largePct,
                       sum([modifyData.buy_sm_vol * smallPct, modifyData.buy_md_vol * smallPct,
                            modifyData.buy_lg_vol * largePct, modifyData.buy_elg_vol * largePct]),
                       sum([modifyData.buy_sm_amount * smallPct, modifyData.buy_md_amount * smallPct,
                            modifyData.buy_lg_amount * largePct, modifyData.buy_elg_amount * largePct]),
                       modifyData.trade_count * smallPct,
                       modifyData.his_low,
                       modifyData.his_high,
                       modifyData.cost_5pct,
                       modifyData.cost_15pct,
                       modifyData.cost_50pct,
                       modifyData.cost_85pct,
                       modifyData.cost_95pct,
                       modifyData.weight_avg,
                       modifyData.winner_rate,
                       modifyData.data[42]]
        res.append(StockDataModel(virtualData))
    elif virtual == 'f':
        modifyData = res[-1]
        nextDate = mysql.selectNextTradeDay(modifyData.date)
        largePct = 0.7
        smallPct = 1.3
        virtualData = [8888,
                       nextDate,
                       modifyData.close * 1.03,
                       modifyData.close * (1 + (limit(stock) / 100)),
                       modifyData.close,
                       modifyData.close * (1 + (limit(stock) / 100)),
                       modifyData.close,
                       limit(stock),
                       modifyData.volume * 1.4,
                       modifyData.amount * 1.4,
                       modifyData.turnover * 1.4,
                       joinTimeToStamp(nextDate, '09:50:00'),
                       joinTimeToStamp(nextDate, '14:00:00'),
                       1,
                       modifyData.buy_sm_vol * smallPct,
                       modifyData.buy_sm_amount * smallPct,
                       modifyData.sell_sm_vol * smallPct,
                       modifyData.sell_sm_amount * smallPct,
                       modifyData.buy_md_vol * smallPct,
                       modifyData.buy_md_amount * smallPct,
                       modifyData.sell_md_vol * smallPct,
                       modifyData.sell_md_amount * smallPct,
                       modifyData.buy_lg_vol * largePct,
                       modifyData.buy_lg_amount * largePct,
                       modifyData.sell_lg_vol * largePct,
                       modifyData.sell_lg_amount * largePct,
                       modifyData.buy_elg_vol * largePct,
                       modifyData.buy_elg_amount * largePct,
                       modifyData.sell_elg_vol * largePct,
                       modifyData.sell_elg_amount * largePct,
                       sum([modifyData.buy_sm_vol * smallPct, modifyData.buy_md_vol * smallPct,
                            modifyData.buy_lg_vol * largePct, modifyData.buy_elg_vol * largePct]),
                       sum([modifyData.buy_sm_amount * smallPct, modifyData.buy_md_amount * smallPct,
                            modifyData.buy_lg_amount * largePct, modifyData.buy_elg_amount * largePct]),
                       modifyData.trade_count * smallPct,
                       modifyData.his_low,
                       modifyData.his_high,
                       modifyData.cost_5pct,
                       modifyData.cost_15pct,
                       modifyData.cost_50pct,
                       modifyData.cost_85pct,
                       modifyData.cost_95pct,
                       modifyData.weight_avg,
                       modifyData.winner_rate,
                       modifyData.data[42]]
        res.append(StockDataModel(virtualData))
    return res


def t_low_pct(data: list[StockDataModel], plus: int = 0) -> float:
    return (data[-plus - 1].low / data[-plus - 2].close) - 1


def t_high_pct(data: list[StockDataModel], plus: int = 0) -> float:
    return (data[-plus - 1].high / data[-plus - 2].close) - 1


def t_close_pct(data: list[StockDataModel], plus: int = 0) -> float:
    return (data[-plus - 1].close / data[-plus - 2].close) - 1


def t_open_pct(data: list[StockDataModel], plus: int = 0) -> float:
    return (data[-plus - 1].open / data[-plus - 2].close) - 1


def limit(stock: str) -> float:
    return 19.6 if stock[0:2] in ['30', '68'] else 9.8


def model_1(stock: str, data: list[StockDataModel], plus: int = 0) -> bool:
    d = data[-plus - 1]
    if (d.close == d.low) and (d.open == d.high) and (d.open == d.close):
        if d.pctChange > limit(stock):
            return True


def model_t(stock: str, data: list[StockDataModel], plus: int = 0) -> bool:
    open_p = t_open_pct(data, plus)
    close_p = t_close_pct(data, plus)
    if open_p != close_p:
        return False
    if close_p <= limit(stock) / 100:
        return False
    if t_low_pct(data, plus) < limit(stock) / 100:
        return True


def t_limit(stock: str, data: list[StockDataModel], plus: int = 0) -> bool:
    return data[-plus - 1].pctChange > limit(stock)


def t_down_limit(stock: str, data: list[StockDataModel], plus: int = 0) -> bool:
    return data[-plus - 1].pctChange < - limit(stock)


def limit_height(stock: str, data: list[StockDataModel], plus: int = 0) -> int:
    height = 0
    for i in range(20):
        if t_limit(stock, data, i + plus):
            height += 1
        else:
            return height
    return height


def move_avg(data: list[StockDataModel], dateRange: int, plus: int = 0) -> float:
    """
    计算移动平均值
    :param data: list[dataModel]
    :param dateRange: ma(x)
    :param plus: 指定 t - (plus) 日
    :return:
    """
    j = plus + 1
    return sum([data[-_].close for _ in range(j, j + dateRange)]) / dateRange


class RankLimitStock(object):
    _instance = None
    resultsDict = {}

    def __init__(self, dataDict: dict[str, list[LimitDataModel]]):
        self.dataDict = dataDict.copy()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def by(self, keyword: str, date: str = lastTradeDay(), eliminateModel1=False):
        """
        根据关键词对某日涨停股票进行排序
        :param keyword: 排序方法名称
        :param date: 指定日期
        :param eliminateModel1: 是否剔除一字板
        """
        dataDict = self.dataDict
        hashKey = hash(keyword + date + ''.join(self.dataDict.keys()))
        if hashKey in self.resultsDict.keys():
            return self.resultsDict[hashKey]
        data = dataDict[date]
        res = None
        rubbish = []
        for _ in data:
            if _.open is None:
                rubbish.append(_)
                continue
            if _.preClose is None:
                rubbish.append(_)
                continue
        for rub in rubbish:
            data.remove(rub)
        if eliminateModel1:
            data = [_ for _ in data if (_.open / _.preClose) <= 1.098]
        if keyword == 'limitTime-industry':
            dictByIndustry = {}
            for _ in data:
                if _.industry not in dictByIndustry.keys():
                    dictByIndustry[_.industry] = [_]
                else:
                    dictByIndustry[_.industry].append(_)

            def rank(d: LimitDataModel):
                return d.firstLimitTime

            res = {}
            for industry in dictByIndustry.keys():
                industryStocks: list[LimitDataModel] = dictByIndustry[industry]
                industryStocks.sort(key=rank)
                res[industry] = [_.stock for _ in industryStocks]
        if keyword == 'open-industry':
            dictByIndustry = {}
            for _ in data:
                if _.industry not in dictByIndustry.keys():
                    dictByIndustry[_.industry] = [_]
                else:
                    dictByIndustry[_.industry].append(_)

            def rank(d: LimitDataModel):
                return d.open / d.preClose

            res = {}
            for industry in dictByIndustry.keys():
                industryStocks: list[LimitDataModel] = dictByIndustry[industry]
                industryStocks.sort(key=rank, reverse=True)
                res[industry] = [_.stock for _ in industryStocks]
        if keyword == 'open-height':
            dictByHeight = {}
            for _ in data:
                if _.limitHeight not in dictByHeight.keys():
                    dictByHeight[_.limitHeight] = [_]
                else:
                    dictByHeight[_.limitHeight].append(_)

            def rank(d: LimitDataModel):
                return d.open / d.preClose

            res = {}
            for height in dictByHeight.keys():
                heightStocks: list[LimitDataModel] = dictByHeight[height]
                heightStocks.sort(key=rank, reverse=True)
                res[height] = [_.stock for _ in heightStocks]
        if keyword == 'limitTime-height':
            dictByHeight = {}
            for _ in data:
                if _.limitHeight not in dictByHeight.keys():
                    dictByHeight[_.limitHeight] = [_]
                else:
                    dictByHeight[_.limitHeight].append(_)

            def rank(d: LimitDataModel):
                return d.firstLimitTime

            res = {}
            for height in dictByHeight.keys():
                heightStocks: list[LimitDataModel] = dictByHeight[height]
                heightStocks.sort(key=rank)
                res[height] = [_.stock for _ in heightStocks]
        if keyword == 'TF':
            needRankData = [{'TF': queryData(_.stock, 5, aimDate=date)[0].TF, 'stock': _.stock} for _ in data]

            def rank(d):
                return d['TF']

            needRankData.sort(key=rank, reverse=True)
            res = [_['stock'] for _ in needRankData]
        if res is None:
            raise Exception('排序出现错误')
        self.resultsDict[hashKey] = res
        return res
