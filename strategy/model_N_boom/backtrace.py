# -*- coding: utf-8 -*-
# @Time    : 2023/1/22 21:50
# @Author  : Destiny_
# @File    : backtrace_old.py
# @Software: PyCharm

import rules
import warnings
from database import db
from common import tool_box
from utils import concurrent_util
from utils.file_util import projectPath
from utils.stockdata_util import queryData
from models.stock_detail_model import StockDetailModel

warnings.filterwarnings('ignore')


def boom(stock, date):
    client = db.Stock_Database()
    try:
        data = queryData(stock, dateRange=3, aimDate=date)
        detail = StockDetailModel(client.selectStockDetail(stock))
        if not detail.amount > 150e5:
            return
        if len(data) < 3:
            return
        res = rules.boom_model_rule(stock, data)
        if res == 0:
            return
        result = {'code': stock, 'name': detail.name, 'date': date}
        profit = backtrace(stock,date)
        print(result)
        print(f'{date}-{stock}-{detail.name}-{profit}%')
    except Exception as e:
        pass
    finally:
        client.close()


def backtrace(stock, date) -> float:
    try:
        data = queryData(stock, dateRange=6, aimDate=date, after=True)
        baseline = data[0].close
        low = data[1].low
        high = max([data[i].high for i in range(2, 6)])
        swing = round((high / baseline - low / baseline) * 100, 1)
        return swing
    except Exception:
        return 0


if __name__ == '__main__':
    stocks = concurrent_util.initStock(needReload=False, extra=False)
    chosenStocks = [stock for stock in stocks if stock[:2] in ['00', '60']]
    singleton = db.Stock_Database()
    dates = singleton.selectTradeDateRange(20230101, 20230329)
    singleton.close()
    for _date in dates:
        print(_date)
        ans = tool_box.thread_pool_executor(boom, chosenStocks, 20, _date)

