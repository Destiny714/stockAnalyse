# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 20:57
# @Author  : Destiny_
# @File    : push_util.py
# @Software: PyCharm

import json
import requests
from utils.file_util import arg_yaml


def bark_pusher(title, content, _url=None):
    try:
        url = f'https://api.day.app/y67CydURc8wR9CVemagkYL/{title}/{content}'
        if _url is not None:
            url += f'?url={_url}'
        requests.get(url, verify=False)
    except:
        pass


class BaseDingtalkTemplate(object):
    def toJson(self, *args, **kwargs) -> dict:
        ...


class MarkDownTemplate(object):
    def template(self, *args, **kwargs) -> str:
        ...


class DingtalkTemplates(object):
    class BarelyMarkDown(BaseDingtalkTemplate):
        def __init__(self, title: str = 'stock默认标题', markdown: MarkDownTemplate = None):
            self.title = title
            self.text = '' if not markdown else markdown.template(title=self.title)

        def toJson(self, *args, **kwargs) -> dict:
            return {
                "msgtype": "markdown",
                "markdown": {
                    "title": self.title,
                    "text": self.text
                }
            }

    class ActionCard(BaseDingtalkTemplate):
        def __init__(self, title: str = 'stock默认标题',
                     singleTitle: str = '点击打开',
                     markdown: MarkDownTemplate = None,
                     url: str = 'https://www.dingtalk.com/'):
            self.title: str = title
            self.text = "" if not markdown else markdown.template(title=title)
            self.singleTitle: str = singleTitle
            self.url: str = url

        def toJson(self):
            return {
                "actionCard": {
                    "title": self.title,
                    "text": self.text,
                    "btnOrientation": "0",
                    "singleTitle": self.singleTitle,
                    "singleURL": self.url
                },
                "msgtype": "actionCard"
            }


class N_ModelMarkDownTemplate(MarkDownTemplate):
    def __init__(self, stock_details: list[dict]):
        self.stock_details = stock_details

    def template(self, title: str = '') -> str:
        insert = ''
        for _ in self.stock_details:
            space = ''
            name = _['name']
            if len(name) < 5:
                space += ' ' * 4 * (5 - len(name))
            insert += f"> **{_['code']}**   **{name}**{space}        **第{int(_['inCycle'])}天**"
            insert += '\n\n'
        markdown = f"""# **{title}**

>    代码             名称   	            周期

{insert}"""
        return markdown


class DragonModelMarkDownTemplate(MarkDownTemplate):
    def __init__(self, stock_details: list[dict]):
        self.stock_details = stock_details

    def template(self, title: str = ''):
        insert = ''
        for _ in self.stock_details:
            space = ''
            name = _['name']
            if len(name) < 5:
                space += ' ' * 4 * (5 - len(name))
            insert += f"> **{_['code']}**   **{name}**{space}        **{int(_['height'])}**               **{_['level']}**"
            insert += '\n\n'
        markdown = f"""# **{title}**
        

##### *S and A*
>    代码         名称   	         连板高度       等级
{insert}
"""
        return markdown


def dingtalk_push(model: BaseDingtalkTemplate, public=True):
    config = arg_yaml()
    webhook_url = config['productWebHook']
    if not public:
        webhook_url = config['devWebHook']
    body = model.toJson()
    body = json.dumps(body)
    headers = {'content-type': 'application/json'}
    requests.post(url=webhook_url, data=body, headers=headers)
