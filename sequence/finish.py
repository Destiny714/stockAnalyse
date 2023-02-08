# -*- coding: utf-8 -*-
# @Time    : 2022/10/27 02:01
# @Author  : Destiny_
# @File    : finish.py
# @Software: PyCharm
from utils.log_util import log
from prefs.params import RunMode
from utils.file_util import projectPath
from common.tool_box import errorHandler
from utils.oss_util import oss_push_object
from utils.push_util import DingtalkPush,PushMode


class Finish(object):
    def __init__(self, date, push=True):
        self.date = date
        self.push = push

    def finPush(self):
        if self.push and RunMode.Status != RunMode.TEST:
            url = oss_push_object(f'{projectPath()}/strategy/dragon/result/{self.date}.xls')
            DingtalkPush(PushMode.Release).pushDragon(self.date, url=url)

    def all(self):
        steps = [_ for _ in self.__class__.__dict__.keys() if 'fin' in _]
        for step in steps:
            func = getattr(self, step)
            try:
                func()
            except Exception as e:
                log().error(errorHandler(e))
