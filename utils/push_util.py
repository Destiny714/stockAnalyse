# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 20:57
# @Author  : Destiny_
# @File    : push_util.py
# @Software: PyCharm

import json
import requests
from enum import Enum
from typing import Optional
from utils.log_util import log
from utils.excel_util import readExcel_AS
from utils.oss_util import oss_push_object
from utils.file_util import config_yaml, projectPath

logCli = log()


def bark_pusher(title, content, _url=None):
    try:
        url = f'https://api.day.app/{config_yaml()["webhook"]["bark"]}/{title}/{content}'
        if _url is not None:
            url += f'?url={_url}'
        requests.get(url, verify=False)
    except:
        pass


class PushMode(Enum):
    Dev = 'dev'
    Release = 'release'


class BasePushTemplate(object):
    def toJson(self, *args, **kwargs) -> dict:
        ...


class BaseDingtalkTemplate(BasePushTemplate):
    def toJson(self) -> dict:
        ...


class BaseWechatTemplate(BasePushTemplate):

    def toJson(self) -> dict:
        ...


class MarkDownTemplate(object):
    def template(self, *args, **kwargs) -> str:
        ...


class WechatTemplates(object):
    class MarkDown(BaseWechatTemplate):
        def __init__(self, title: str = '默认标题', markdown: MarkDownTemplate = None, url: str = None):
            self.title = title
            self.text = '' if not markdown else markdown.template(title=self.title, url=url)

        def toJson(self, *args, **kwargs) -> dict:
            return {
                "msgtype": "markdown",
                "markdown": {
                    "content": self.text
                }
            }


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

    def template(self, title: str = '', url=None) -> str:
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


class BoomModelMarkDownTemplate(MarkDownTemplate):
    def __init__(self, stock_details: list[dict]):
        self.stock_details = stock_details

    def template(self, title: str = '', url=None) -> str:
        insert = ''
        for _ in self.stock_details:
            space = ''
            name = _['name']
            if len(name) < 5:
                space += ' ' * 4 * (5 - len(name))
            insert += f"> **{_['stock']}**  **{name}**{space} **{_['boomDay'][-4:]}**         **{_['shrinkDay'][-4:]}**"
            insert += '\n\n'
        markdown = f"""# **{title}**

>    代码         名称         爆量日         缩量日

{insert}"""
        return markdown


class N_Boom_ModelMarkDownTemplate(MarkDownTemplate):
    def __init__(self, stock_details: list[dict]):
        self.stock_details = stock_details

    def template(self, title: str = '', url=None) -> str:
        insert = ''
        for _ in self.stock_details:
            space = ''
            name = _['name']
            if len(name) < 5:
                space += ' ' * 4 * (5 - len(name))
            insert += f"> **{_['code']}**   **{name}**{space}"
            insert += '\n\n'
        markdown = f"""# **{title}**

>    代码             名称

{insert}"""
        return markdown


class DragonModelMarkDownTemplate(MarkDownTemplate):
    def __init__(self, stock_details: list[dict]):
        self.stock_details = stock_details

    def template(self, title: str = '', url=None, wechat=False):
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
        if wechat and (url is not None):
            markdown += '\n'
            markdown += f'[点击打开]({url})'
        return markdown


class BasePush(object):
    scope: str
    headers = {'content-type': 'application/json'}

    def __init__(self, mode: PushMode = PushMode.Dev, modes=Optional[list[PushMode]]):
        self.config = config_yaml()['webhook'][self.scope]
        self.pushModes = []
        if mode:
            self.pushModes.append(mode)
        if modes:
            self.pushModes.extend(modes)
            self.pushModes = list(set(self.pushModes))

    def pushDragon(self, *args, **kwargs):
        ...

    def pushN(self, *args, **kwargs):
        ...

    def request(self, template: BasePushTemplate):
        body = json.dumps(template.toJson())
        for pushMode in self.pushModes:
            res = requests.post(url=self.config[pushMode.value], headers=self.headers, data=body)
            if res.status_code == 200:
                logCli.info(f'{pushMode.name} channel push done')
            else:
                logCli.error(f'{pushMode.name} channel ' + res.json())


class DingtalkPush(BasePush):
    scope = 'Dingtalk'

    def __init__(self, mode: PushMode = PushMode.Release, modes=None):
        super().__init__(mode=mode, modes=modes)

    def pushDragon(self, date: str, url: str = None):
        if not url:
            url = oss_push_object(f'{projectPath()}/strategy/dragon/result/{date}.xls')
        title = f'{date} 涨停模型'
        excelName = url.split('/')[-1]
        if '_' in excelName:
            level = int(excelName.replace('.xls', '').split('_')[-1]) + 1
            title = title + f' 更新版本{level}'
        template = DingtalkTemplates.ActionCard(
            markdown=DragonModelMarkDownTemplate(readExcel_AS(date)),
            url=url,
            title=title,
            singleTitle='点击查看')
        self.request(template)
        return url

    def pushN(self, date: str, stock_details: list[dict], model_name='N'):
        logCli.info('push start')
        template = DingtalkTemplates.BarelyMarkDown(
            title=f'{date} {model_name} 模型',
            markdown=N_ModelMarkDownTemplate(stock_details)
        )
        self.request(template)

    def pushBoom(self, date: str, stock_details: list[dict], model_name='爆量'):
        logCli.info('push start')
        template = DingtalkTemplates.BarelyMarkDown(
            title=f'{date} {model_name} 模型',
            markdown=BoomModelMarkDownTemplate(stock_details)
        )
        self.request(template)

    def pushN_boom(self, date: str, stock_details: list[dict], model_name='N-BOOM'):
        logCli.info('push start')
        template = DingtalkTemplates.BarelyMarkDown(
            title=f'{date} {model_name} 模型',
            markdown=N_Boom_ModelMarkDownTemplate(stock_details)
        )
        self.request(template)


class WechatPush(BasePush):
    scope = 'Wechat'

    def __init__(self, mode: PushMode = PushMode.Release, modes=None):
        super().__init__(mode=mode, modes=modes)

    def pushDragon(self, date: str, url: str = None):
        if not url:
            url = oss_push_object(f'{projectPath()}/strategy/dragon/result/{date}.xls')
        template = WechatTemplates.MarkDown(
            markdown=DragonModelMarkDownTemplate(readExcel_AS(date)),
            title=f'{date} 涨停模型', url=url)
        self.request(template)
        return url

    def pushN(self, date: str, stock_details: list[dict]):
        template = WechatTemplates.MarkDown(
            title=f'{date} N字模型',
            markdown=N_ModelMarkDownTemplate(stock_details)
        )
        self.request(template)
