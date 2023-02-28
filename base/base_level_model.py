# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 23:08
# @Author  : Destiny_
# @File    : base_level_model.py
# @Software: PyCharm

from prefs.params import *
from utils.stockdata_util import *
from models.stock_data_model import StockDataModel
from models.stock_detail_model import StockDetailModel


class base_level(object):
    def __init__(self, level, stockDetail: StockDetailModel, data: list[StockDataModel], gemIndex: list[StockDataModel],
                 shIndex: list[StockDataModel]):
        self.data: list[StockDataModel] = data
        self.level = level
        self.shIndex = shIndex
        self.gemIndex = gemIndex
        self.stock = stockDetail.symbol()
        self.industry = stockDetail.industry
        self.height: int = limit_height(stockDetail.symbol(), data)
        self.shot_rule: list = []
        self.fail_rule: list = []
        self.f_rule: bool = 'F' in self.level
        self.errors = []
        if level not in Params.levelRuleDict.keys():
            Params.levelRuleDict[level] = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule,
                'result': self.shot_rule == [] if self.f_rule else self.shot_rule != []}

    def filter(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            ruleID = int(str(rule).replace('rule', ''))
            try:
                res = func()
            except Exception as e:
                res = False
                self.errors.append(e)
            self.shot_rule.append(ruleID) if res else self.fail_rule.append(ruleID)
        for error in self.errors:
            raise error
        return self.result()
