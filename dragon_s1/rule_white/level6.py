# -*- coding: utf-8 -*-
# @Time    : 2022/8/21 17:32
# @Author  : Destiny_
# @File    : level6.py
# @Software: PyCharm
from typing import List

from common.collect_data import dataModel


class level6:
    def __init__(self, stock: str, data: List[dataModel], index: List[dataModel]):
        self.level = 5
        self.data = data
        self.index = index
        self.stock = stock
        self.shot_rule: list = []
        self.fail_rule: list = []

    def result(self):
        return {'level': self.level, 'stock': self.stock, 'detail': self.shot_rule, 'result': self.shot_rule != []}

    def filter(self):
        return self.result()