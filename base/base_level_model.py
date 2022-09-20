# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 23:08
# @Author  : Destiny_
# @File    : base_level_model.py
# @Software: PyCharm

from utils.stockdata_util import *
from models.initDataModel import dataModel
from models.limitDataModel import limitDataModel
from models.stockDetailModel import stockDetailModel


class base_level(object):
    def __init__(self, level, stockDetail: stockDetailModel, data: list[dataModel], index: list[dataModel],
                 limitData: dict[str, list[limitDataModel]]):
        self.data = data
        self.index = index
        self.level = level
        self.limitData = limitData
        self.stock = stockDetail.symbol()
        self.industry = stockDetail.industry()
        self.height: int = limit_height(stockDetail.symbol(), data)
        self.shot_rule: list = []
        self.fail_rule: list = []
        self.f_rule: bool = 'F' in self.level

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule,
                'result': self.shot_rule == [] if self.f_rule else self.shot_rule != []}

    def filter(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'rule' in _]
        for rule in rules:
            func = getattr(self, rule)
            ruleID = int(str(rule).replace('rule', ''))
            self.shot_rule.append(ruleID) if func() else self.fail_rule.append(ruleID)
        return self.result()
