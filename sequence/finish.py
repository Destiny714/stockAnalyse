# -*- coding: utf-8 -*-
# @Time    : 2022/10/27 02:01
# @Author  : Destiny_
# @File    : finish.py
# @Software: PyCharm
from utils.file_util import projectPath
from utils.oss_util import oss_push_object
from utils.push_util import DingtalkPush, WechatPush


class Finish(object):
    def __init__(self, date):
        self.date = date

    def finPush(self):
        url = oss_push_object(f'{projectPath()}/strategy/dragon/result/{self.date}.xls')
        WechatPush().pushDragon(self.date, url=url)
        DingtalkPush().pushDragon(self.date, url=url)

    def all(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'fin' in _]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                return True
