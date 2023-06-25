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
from utils.push_util import PushMode, DingtalkPush
from models.stock_detail_model import StockDetailModel

warnings.filterwarnings('ignore')


def boom(stock):
    client = db.Stock_Database()
    try:
        data = queryData(stock, dateRange=3, aimDate=aimDate)
        detail = StockDetailModel(client.selectStockDetail(stock))
        if not detail.amount > 150e5:
            return
        if len(data) < 3:
            return
        res = rules.boom_model_rule(stock, data)
        if res == 0:
            return
        res = {'code': stock, 'name': client.selectNameByStock(stock)}
        print(res)
        booms.append(res)
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
    chosenStocks = stocks
    booms = []
    tool_box.thread_pool_executor(boom, chosenStocks, 20)
    DingtalkPush(modes=[PushMode.Release, PushMode.Dev]).pushN_boom(aimDate, booms, model_name='N-BOOM')
