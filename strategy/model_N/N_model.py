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
    try:
        client = db.Stock_Database()
    except Exception as e:
        print(f'{stock} db error : {e}')
        return
    try:
        data = queryData(stock, dateRange=10, aimDate=aimDate)
        if len(data) < 10:
            return
        n_res = rules.n_model_rule(stock, data)
        n_plus_res = rules.n_plus_model_rule(stock, data)
        if n_res != 0:
            print(f'N-{stock}-{aimDate}-{n_res}日')
            Ns.append({'code': stock, 'name': client.selectNameByStock(stock), 'inCycle': n_res})
        if n_plus_res != 0:
            print(f'N-PLUS-{stock}-{aimDate}-{n_plus_res}日')
            N_plus_s.append({'code': stock, 'name': client.selectNameByStock(stock), 'inCycle': n_plus_res})
    except Exception as e:
        errors.append(f'{stock} : logic error : {e}')
        pass
    finally:
        if isinstance(client, db.Stock_Database):
            client.close()


def N_plus(stock):
    try:
        client = db.Stock_Database()
    except Exception as e:
        print(f'{stock} db error : {e}')
        return
    try:
        data = queryData(stock, dateRange=10, aimDate=aimDate)
        if len(data) < 3:
            return
        res = rules.n_plus_model_rule(stock, data)
        if res == 0:
            return
        print(f'N-PLUS-{stock}-{aimDate}-{res}日')
        N_plus_s.append({'code': stock, 'name': client.selectNameByStock(stock), 'inCycle': res})
    except Exception as e:
        errors.append(f'{stock} : logic error : {e}')
        pass
    finally:
        if isinstance(client, db.Stock_Database):
            client.close()


if __name__ == '__main__':
    aimDate = lastTradeDay()
    print(aimDate)
    stocks = concurrent_util.initStock(needReload=False, extra=False)
    errors = []
    chosenStocks = [stock for stock in stocks if stock[:2] in ['00', '60', '30', '68']]
    Ns = []
    N_plus_s = []
    tool_box.thread_pool_executor(N, chosenStocks, 10)
    DingtalkPush(modes=[PushMode.Dev, PushMode.Release]).pushN(aimDate, Ns)
    DingtalkPush(mode=PushMode.Dev).pushN(aimDate, N_plus_s, model_name='N-PLUS')
