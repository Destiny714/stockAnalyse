# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 19:19
# @Author  : Destiny_
# @File    : test.py
# @Software: PyCharm

from common.collect_data import collectData
from dragon_s1.rule_black.level8 import rule21
d = collectData(stock='002395',aimDate='20220727')
res = rule21('002395',d)
print(res)
