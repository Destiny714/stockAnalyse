# -*- coding: utf-8 -*-
# @Time    : 2022/10/27 02:01
# @Author  : Destiny_
# @File    : finish.py
# @Software: PyCharm
from utils.file_util import projectPath
from utils.excel_util import readExcel_AS
from utils.oss_util import oss_push_object
from utils.push_util import DingtalkTemplates, DragonModelMarkDownTemplate, dingtalk_push


class Finish(object):
    def __init__(self, date):
        self.date = date

    def finPush(self):
        url = oss_push_object(f'{projectPath()}/strategy/dragon/result/{self.date}.xls')
        model = DingtalkTemplates.ActionCard(
            markdown=DragonModelMarkDownTemplate(readExcel_AS(self.date)),
            url=url,
            title=f'{self.date}模型结果',
            singleTitle='点击查看')
        dingtalk_push(model)

    def all(self):
        rules = [_ for _ in self.__class__.__dict__.keys() if 'fin' in _]
        for rule in rules:
            func = getattr(self, rule)
            if func():
                return True
