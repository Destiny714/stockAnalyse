# -*- coding: utf-8 -*-
# @Time    : 2022/8/14 22:25
# @Author  : Destiny_
# @File    : extApi.py
# @Software: PyCharm
import json
import requests


def getTimeDataToday(stock):
    flag = 0
    if stock[0:2] in ['00', '30', '39']:
        flag = 1
    if stock[0] == '4':
        flag = 2
    url = f'https://img1.money.126.net/data/hs/time/today/{flag}{stock}.json'
    res = requests.get(url)
    try:
        jsonData = res.json()
        data: list = jsonData['data']
        dataDict = {f"{minute[0]}": int(minute[3] / 100) for minute in data}
        return {"date": jsonData['date'], "symbol": jsonData['symbol'], "data": json.dumps(dataDict)}
    except:
        return None
