# -*- coding: utf-8 -*-
# @Time    : 2022/6/20 19:19
# @Author  : Destiny_
# @File    : test.py
# @Software: PyCharm
from common.collect_data import collectData
from dragon_s1.rule_black.level8 import rule22

data = collectData('000629')
res = rule22(data)
print(res)
