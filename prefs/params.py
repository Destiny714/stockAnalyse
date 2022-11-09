# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 23:23
# @Author  : Destiny_
# @File    : params.py
# @Software: PyCharm


class Params(object):
    levelRuleDict = {}
    scoreRuleDict = {}
    stockDataModelDict = {}  # 所有指定日期的股票详情dict


class RunMode(object):
    TEST = -1
    DEBUG = 0
    RELEASE = 1


runMode = 0


class g:
    g_dict = {}

    @classmethod
    def save(cls, obj, key: str):
        cls.g_dict[key] = obj

    @classmethod
    def get(cls, key: str):
        try:
            return cls.g_dict[key]
        except:
            return None
