# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 19:55
# @Author  : Destiny_
# @File    : collect_data.py
# @Software: PyCharm
import json
from typing import List
from api import databaseApi
from common import dateHandler


class dataModel:
    def __init__(self, data):
        self.data = data

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]

    def date(self):
        return self.data[1]

    def open(self):
        return self.data[2]

    def close(self):
        return self.data[3]

    def preClose(self):
        return self.data[4]

    def high(self):
        return self.data[5]

    def low(self):
        return self.data[6]

    def pctChange(self):
        return self.data[7]

    def volume(self):
        return self.data[8]

    def amount(self):
        return self.data[9]

    def turnover(self):
        return self.data[10]

    def firstLimitTime(self):
        return self.data[11]

    def lastLimitTime(self):
        return self.data[12]

    def limitOpenTime(self):
        return self.data[13]

    def buy_sm_vol(self):
        return self.data[14]

    def buy_sm_amount(self):
        return self.data[15]

    def sell_sm_vol(self):
        return self.data[16]

    def sell_sm_amount(self):
        return self.data[17]

    def buy_md_vol(self):
        return self.data[18]

    def buy_md_amount(self):
        return self.data[19]

    def sell_md_vol(self):
        return self.data[20]

    def sell_md_amount(self):
        return self.data[21]

    def buy_lg_vol(self):
        return self.data[22]

    def buy_lg_amount(self):
        return self.data[23]

    def sell_lg_vol(self):
        return self.data[24]

    def sell_lg_amount(self):
        return self.data[25]

    def buy_elg_vol(self):
        return self.data[26]

    def buy_elg_amount(self):
        return self.data[27]

    def sell_elg_vol(self):
        return self.data[28]

    def sell_elg_amount(self):
        return self.data[29]

    def net_mf_vol(self):
        return self.data[30]

    def net_mf_amount(self):
        return self.data[31]

    def trade_count(self):
        return self.data[32]

    def his_low(self):
        return self.data[33]

    def his_high(self):
        return self.data[34]

    def cost_5pct(self):
        return self.data[35]

    def cost_15pct(self):
        return self.data[36]

    def cost_50pct(self):
        return self.data[37]

    def cost_85pct(self):
        return self.data[38]

    def cost_95pct(self):
        return self.data[39]

    def weight_avg(self):
        return self.data[40]

    def winner_rate(self):
        return self.data[41]

    def time(self) -> dict:
        return json.loads(self.data[42])

    def concentration(self):
        cost5pct = self.data[35]
        cost95pct = self.data[39]
        if cost95pct + cost5pct == 0:
            return 100
        return (cost95pct - cost5pct) / (cost95pct + cost5pct)

    def timeVol(self, timeStamp: int):
        time = json.loads(self.data[42])
        limitMinute = dateHandler.getMinute(timeStamp)
        return time[limitMinute]


def collectIndexData(index, dateRange: int = 500, aimDate=dateHandler.lastTradeDay()) -> List[dataModel]:
    mysql = databaseApi.Mysql()
    allData = mysql.selectOneAllData(stock=index, dateRange=dateRange, aimDate=aimDate)
    res = [dataModel(_) for _ in allData]
    return res


def virtualIndexData(data: List[dataModel], nextTradeDay) -> List[dataModel]:
    res = data
    modifyData = list(res[-1])
    modifyData[0] = 8888
    modifyData[1] = nextTradeDay
    res.append(dataModel(modifyData))
    return res


def collectData(stock, dateRange: int = 800, aimDate=dateHandler.lastTradeDay(), virtual=None) -> List[dataModel]:
    mysql = databaseApi.Mysql()
    allData = mysql.selectOneAllData(stock=stock, dateRange=dateRange, aimDate=aimDate)
    res = [dataModel(_) for _ in allData]
    if virtual is None:
        pass
    elif virtual == 's':
        modifyData = res[-1]
        nextDate = mysql.selectNextTradeDay(modifyData.date())
        largePct = 1.05
        smallPct = 0.95
        virtualData = [8888,
                       nextDate,
                       modifyData.close() * 1.07,
                       modifyData.close() * (1 + (limit(stock) / 100)),
                       modifyData.close(),
                       modifyData.close() * (1 + (limit(stock) / 100)),
                       modifyData.close() * 1.06,
                       limit(stock),
                       modifyData.volume() * 0.6,
                       modifyData.amount() * 0.6,
                       modifyData.turnover() * 0.6,
                       dateHandler.joinTimeToStamp(nextDate, '09:36:00'),
                       dateHandler.joinTimeToStamp(nextDate, '09:36:00'),
                       0,
                       modifyData.buy_sm_vol() * smallPct,
                       modifyData.buy_sm_amount() * smallPct,
                       modifyData.sell_sm_vol() * smallPct,
                       modifyData.sell_sm_amount() * smallPct,
                       modifyData.buy_md_vol() * smallPct,
                       modifyData.buy_md_amount() * smallPct,
                       modifyData.sell_md_vol() * smallPct,
                       modifyData.sell_md_amount() * smallPct,
                       modifyData.buy_lg_vol() * largePct,
                       modifyData.buy_lg_amount() * largePct,
                       modifyData.sell_lg_vol() * largePct,
                       modifyData.sell_lg_amount() * largePct,
                       modifyData.buy_elg_vol() * largePct,
                       modifyData.buy_elg_amount() * largePct,
                       modifyData.sell_elg_vol() * largePct,
                       modifyData.sell_elg_amount() * largePct,
                       sum([modifyData.buy_sm_vol() * smallPct, modifyData.buy_md_vol() * smallPct,
                            modifyData.buy_lg_vol() * largePct, modifyData.buy_elg_vol() * largePct]),
                       sum([modifyData.buy_sm_amount() * smallPct, modifyData.buy_md_amount() * smallPct,
                            modifyData.buy_lg_amount() * largePct, modifyData.buy_elg_amount() * largePct]),
                       modifyData.trade_count() * smallPct,
                       modifyData.his_low(),
                       modifyData.his_high(),
                       modifyData.cost_5pct(),
                       modifyData.cost_15pct(),
                       modifyData.cost_50pct(),
                       modifyData.cost_85pct(),
                       modifyData.cost_95pct(),
                       modifyData.weight_avg(),
                       modifyData.winner_rate(),
                       modifyData.time()]
        res.append(dataModel(virtualData))
    elif virtual == 'f':
        modifyData = res[-1]
        nextDate = mysql.selectNextTradeDay(modifyData.date())
        largePct = 0.95
        smallPct = 1.05
        virtualData = [8888,
                       nextDate,
                       modifyData.close() * 1.03,
                       modifyData.close() * (1 + (limit(stock) / 100)),
                       modifyData.close(),
                       modifyData.close() * (1 + (limit(stock) / 100)),
                       modifyData.close(),
                       limit(stock),
                       modifyData.volume() * 1.4,
                       modifyData.amount() * 1.4,
                       modifyData.turnover() * 1.4,
                       dateHandler.joinTimeToStamp(nextDate, '09:50:00'),
                       dateHandler.joinTimeToStamp(nextDate, '14:00:00'),
                       1,
                       modifyData.buy_sm_vol() * smallPct,
                       modifyData.buy_sm_amount() * smallPct,
                       modifyData.sell_sm_vol() * smallPct,
                       modifyData.sell_sm_amount() * smallPct,
                       modifyData.buy_md_vol() * smallPct,
                       modifyData.buy_md_amount() * smallPct,
                       modifyData.sell_md_vol() * smallPct,
                       modifyData.sell_md_amount() * smallPct,
                       modifyData.buy_lg_vol() * largePct,
                       modifyData.buy_lg_amount() * largePct,
                       modifyData.sell_lg_vol() * largePct,
                       modifyData.sell_lg_amount() * largePct,
                       modifyData.buy_elg_vol() * largePct,
                       modifyData.buy_elg_amount() * largePct,
                       modifyData.sell_elg_vol() * largePct,
                       modifyData.sell_elg_amount() * largePct,
                       sum([modifyData.buy_sm_vol() * smallPct, modifyData.buy_md_vol() * smallPct,
                            modifyData.buy_lg_vol() * largePct, modifyData.buy_elg_vol() * largePct]),
                       sum([modifyData.buy_sm_amount() * smallPct, modifyData.buy_md_amount() * smallPct,
                            modifyData.buy_lg_amount() * largePct, modifyData.buy_elg_amount() * largePct]),
                       modifyData.trade_count() * smallPct,
                       modifyData.his_low(),
                       modifyData.his_high(),
                       modifyData.cost_5pct(),
                       modifyData.cost_15pct(),
                       modifyData.cost_50pct(),
                       modifyData.cost_85pct(),
                       modifyData.cost_95pct(),
                       modifyData.weight_avg(),
                       modifyData.winner_rate(),
                       modifyData.time()]
        res.append(dataModel(virtualData))
    return res


def t_low_pct(data: List[dataModel], plus: int = 0):
    return (data[-plus - 1].low() / data[-plus - 2].close()) - 1


def t_high_pct(data: List[dataModel], plus: int = 0):
    return (data[-plus - 1].high() / data[-plus - 2].close()) - 1


def t_close_pct(data: List[dataModel], plus: int = 0):
    return (data[-plus - 1].close() / data[-plus - 2].close()) - 1


def t_open_pct(data: List[dataModel], plus: int = 0):
    return (data[-plus - 1].open() / data[-plus - 2].close()) - 1


def limit(stock: str) -> float:
    return 19.6 if stock[0:2] in ['30', '68'] else 9.8


def model_1(stock: str, data: List[dataModel], plus: int = 0):
    if (data[-plus - 1].close() == data[-plus - 1].low()) and (data[-plus - 1].open() == data[-plus - 1].high()) and (
            data[-plus - 1].open() == data[-plus - 1].close()):
        if data[-plus - 1].pctChange() > limit(stock):
            return True


def model_t(stock: str, data: List[dataModel], plus: int = 0):
    open_p = t_open_pct(data, plus)
    close_p = t_close_pct(data, plus)
    if open_p != close_p:
        return False
    if close_p <= limit(stock) / 100:
        return False
    if t_low_pct(data, plus) < limit(stock) / 100:
        return True


def t_limit(stock: str, data: List[dataModel], plus: int = 0):
    return data[-plus - 1].pctChange() > limit(stock)


def limit_height(stock: str, data: List[dataModel]):
    height = 0
    for i in range(20):
        if t_limit(stock, data, i):
            height += 1
        else:
            return height
    return height
