# -*- coding: utf-8 -*-
# @Time    : 2022/9/18 00:07
# @Author  : Destiny_
# @File    : stock_data_model.py
# @Software: PyCharm

import json
from utils import date_util


class StockDataModel:
    """单支股票单日数据模型"""

    def __str__(self):
        return str(self.data)

    def __init__(self, data):
        self.data = data

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]

    @property
    def date(self):
        return self.data[1]

    @property
    def open(self):
        return self.data[2]

    @property
    def close(self):
        return self.data[3]

    @property
    def preClose(self):
        return self.data[4]

    @property
    def high(self):
        return self.data[5]

    @property
    def low(self):
        return self.data[6]

    @property
    def pctChange(self):
        return self.data[7]

    @property
    def volume(self):
        return self.data[8]

    @property
    def amount(self):
        """
        单位 k
        :return:
        """
        return self.data[9]

    @property
    def turnover(self):
        return self.data[10]

    @property
    def firstLimitTime(self) -> int:
        return self.data[11]

    @property
    def lastLimitTime(self):
        return self.data[12]

    @property
    def limitOpenTime(self):
        return self.data[13]

    @property
    def buy_sm_vol(self):
        return self.data[14]

    @property
    def buy_sm_amount(self):
        return self.data[15]

    @property
    def sell_sm_vol(self):
        return self.data[16]

    @property
    def sell_sm_amount(self):
        return self.data[17]

    @property
    def buy_md_vol(self):
        return self.data[18]

    @property
    def buy_md_amount(self):
        return self.data[19]

    @property
    def sell_md_vol(self):
        return self.data[20]

    @property
    def sell_md_amount(self):
        return self.data[21]

    @property
    def buy_lg_vol(self):
        return self.data[22]

    @property
    def buy_lg_amount(self):
        return self.data[23]

    @property
    def sell_lg_vol(self):
        return self.data[24]

    @property
    def sell_lg_amount(self):
        return self.data[25]

    @property
    def buy_elg_vol(self):
        return self.data[26]

    @property
    def buy_elg_amount(self):
        return self.data[27]

    @property
    def sell_elg_vol(self):
        return self.data[28]

    @property
    def sell_elg_amount(self):
        return self.data[29]

    @property
    def net_mf_vol(self):
        return self.data[30]

    @property
    def net_mf_amount(self):
        return self.data[31]

    @property
    def trade_count(self):
        return self.data[32]

    @property
    def his_low(self):
        return self.data[33]

    @property
    def his_high(self):
        return self.data[34]

    @property
    def cost_5pct(self):
        return self.data[35]

    @property
    def cost_15pct(self):
        return self.data[36]

    @property
    def cost_50pct(self):
        return self.data[37]

    @property
    def cost_85pct(self):
        return self.data[38]

    @property
    def cost_95pct(self):
        return self.data[39]

    @property
    def weight_avg(self):
        return self.data[40]

    @property
    def winner_rate(self):
        return self.data[41]

    @property
    def time(self) -> dict:
        return json.loads(self.data[42])

    @property
    def concentration(self) -> float:
        """
        集中度
        0.xx
        未*100
        :return:
        """
        _sum = self.cost_95pct + self.cost_5pct
        if _sum == 0:
            return 100
        return ((self.cost_95pct - self.cost_5pct) / _sum) * 100

    @property
    def CF(self) -> float:
        """
        (buy_elg_vol + buy_lg_vol - sell_elg_vol - sell_lg_vol) / (buy_elg_vol + buy_lg_vol)
        """
        if (self.buy_elg_vol + self.buy_lg_vol) == 0:
            return 0
        return round(((self.buy_elg_vol + self.buy_lg_vol - self.sell_elg_vol - self.sell_lg_vol) / (self.buy_elg_vol + self.buy_lg_vol)) * 100, 1)

    @property
    def TF(self) -> float:
        """
        (buy_elg_vol - sell_elg_vol) / buy_elg_vol
        """
        if self.buy_elg_vol == 0:
            return 0
        return round(((self.buy_elg_vol - self.sell_elg_vol) / self.buy_elg_vol) * 100, 1)

    @property
    def CP(self) -> float:
        """
        (buy_elg_vol + buy_lg_vol) / volume
        """
        if self.volume == 0:
            return 0
        return round(((self.buy_elg_vol + self.buy_lg_vol) / self.volume) * 100, 1)

    @property
    def TP(self) -> float:
        """
        buy_elg_vol / volume
        """
        res = 0.1 if self.volume == 0 else round((self.buy_elg_vol / self.volume) * 100, 1)
        return res if res != 0 else 0.1

    def timeVol(self, timeStamp: int = None, minute: str = None):
        assert (timeStamp is None or minute is None)
        time = self.time
        if minute is None:
            limitMinute = date_util.getMinute(stamp=timeStamp)
        else:
            limitMinute = minute
        return time[limitMinute]
