# -*- coding: utf-8 -*-
# @Time    : 2022/4/17 19:39
# @Author  : Destiny_
# @File    : N_model.py
# @Software: PyCharm
# import os
# import sys
# import warnings
#
# warnings.filterwarnings('ignore')
#
# sys.path.append(os.getcwd().replace('/model_N', ''))

import rules
import warnings
from database import db
from common import tool_box
from utils import concurrent_util
from utils.date_util import lastTradeDay
from utils.stockdata_util import queryData
from utils.push_util import DingtalkPush, PushMode

warnings.filterwarnings('ignore')


def N(stock):
    client = db.Stock_Database()
    try:
        data = queryData(stock, dateRange=3, aimDate=aimDate)
        if len(data) < 3:
            return
        res = rules.n_model_rule(stock, data)
        if res == 0:
            return
        print(f'{stock}-{aimDate}-{res}日')
        Ns.append({'code': stock, 'name': client.selectNameByStock(stock), 'inCycle': res})
    except Exception as e:
        errors.append(f'{stock} : logic error : {e}')
        pass
    finally:
        client.close()


if __name__ == '__main__':
    aimDate = lastTradeDay()
    print(aimDate)
    stocks = concurrent_util.initStock(needReload=False, extra=False)
    errors = []
    chosenStocks = [stock for stock in stocks if stock[:2] in ['00', '60']]
    Ns = []

    tool_box.thread_pool_executor(N, chosenStocks, 20)
    DingtalkPush(mode=PushMode.Release).pushN(aimDate, Ns)
