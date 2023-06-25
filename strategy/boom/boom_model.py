# -*- coding: utf-8 -*-
# @Time    : 2023/3/26 13:23
# @Author  : Destiny_
# @File    : boom_model.py
# @Software: PyCharm

from utils.date_util import lastTradeDay
from strategy.boom.rules import BoomRule
from utils.concurrent_util import initStock
from common.tool_box import thread_pool_executor
from utils.push_util import DingtalkPush, PushMode


def run_model(stock: str):
    instance = BoomRule(stock, aimDate)
    res = instance.run()
    if res is not None:
        print(res)
        booms.append(res)


if __name__ == '__main__':
    aimDate = lastTradeDay()
    print(aimDate)
    stocks = initStock(needReload=False, extra=False)
    booms = []
    push_mode = PushMode.Release
    thread_pool_executor(run_model, stocks, 10)
    DingtalkPush(mode=push_mode).pushBoom(aimDate, booms)
