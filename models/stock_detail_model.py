# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 23:09
# @Author  : Destiny_
# @File    : stock_detail_model.py
# @Software: PyCharm


class StockDetailModel:
    """股票详情"""

    def __init__(self, data):
        self.data = data

    def symbol(self) -> str:
        return self.data[1]

    @property
    def name(self) -> str:
        return self.data[2]

    @property
    def industry(self) -> str:
        return self.data[3]
