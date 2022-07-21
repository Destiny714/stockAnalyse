# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 19:19
# @Author  : Destiny_
# @File    : test.py
# @Software: PyCharm
from common.concurrentActions import updateLimitDetailData, updateStockListDailyIndex

for i in [20220711,
          20220712,
          20220713,
          20220714,
          20220715,
          20220718,
          20220719]:
    updateLimitDetailData(i)
    updateStockListDailyIndex(i)
