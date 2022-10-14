# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 23:23
# @Author  : Destiny_
# @File    : params.py
# @Software: PyCharm

from enum import Enum


class Params(object):
    levelRuleDict = {}
    scoreRuleDict = {}
    stockDataModelDict = {}  # 所有指定日期的股票详情dict


class RunMode(Enum):
    TEST = -1
    DEBUG = 0
    RELEASE = 1


runMode = 0
