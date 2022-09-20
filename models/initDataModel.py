# -*- coding: utf-8 -*-
# @Time    : 2022/9/18 00:07
# @Author  : Destiny_
# @File    : initDataModel.py
# @Software: PyCharm

import json
from utils import date_util


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
        cost5pct = self.cost_5pct()
        cost95pct = self.cost_95pct()
        if cost95pct + cost5pct == 0:
            return 100
        return (cost95pct - cost5pct) / (cost95pct + cost5pct)

    def timeVol(self, timeStamp: int = None, minute: str = None):
        assert (timeStamp is None or minute is None)
        time = self.time()
        if minute is None:
            limitMinute = date_util.getMinute(timeStamp)
        else:
            limitMinute = minute
        return time[limitMinute]
