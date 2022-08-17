# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 04:58
# @Author  : Destiny_
# @File    : push.py
# @Software: PyCharm
import requests


def bark_pusher(title, content, _url=None):
    url = f'https://api.day.app/y67CydURc8wR9CVemagkYL/{title}/{content}'
    if _url is not None:
        url += f'?url={_url}'
    requests.get(url, verify=False)


def dingTalkPush():
    url = 'https://oapi.dingtalk.com/robot/send?access_token=263bc79960be1a8f0081532cc6fa47c1d36970a50e75e7b813f789872210f828'

