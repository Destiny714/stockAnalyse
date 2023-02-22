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

warnings.filterwarnings('ignore')


def N(stock, date):
    try:
        data = queryData(stock, dateRange=10, aimDate=date)
        if len(data) < 3:
            return
        res = rules.n_plus_model_rule(stock, data)
        if res == 0:
            return
        return {'code': stock, 'inCycle': res, 'date': date}
    except Exception:
        ...


def backtrace(stock, date) -> float:
    try:
        data = queryData(stock, dateRange=4, aimDate=date, after=True)
        day3 = data[1]
        day4 = data[2]
        day5 = data[3]
        buyPoint = sum([day3.open, day3.close]) / 2
        sellPoint = max([day4.high, day5.high])
        return round((sellPoint / buyPoint - 1) * 100, 1)
    except Exception:
        return 0


if __name__ == '__main__':
    stocks = concurrent_util.initStock(needReload=False, extra=False)
    chosenStocks = [stock for stock in stocks if stock[:2] in ['00', '60']]
    singleton = db.Stock_Database()
    dates = singleton.selectTradeDateRange(20230101, 20230213)
    singleton.close()
    with open(f'{projectPath()}/strategy/model_N/n_backtrace_swing6.txt','w') as f:
        for _date in dates:
            ans = tool_box.thread_pool_executor(N, chosenStocks, 20, _date)
            _ans = [_ for _ in ans if _ is not None]
            f.write(f'----------{_date}----------\n')
            for _detail in _ans:
                code = _detail['code']
                __date = _detail['date']
                profit = backtrace(code, __date)
                _res = f'{__date}-{code}-{profit}%'
                f.write(_res)
                f.write('\n')
                print(_res)
            f.write('\n')
