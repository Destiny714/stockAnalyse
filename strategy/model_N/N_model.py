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
from common import tool_box
from utils import concurrent_util
from utils.date_util import lastTradeDay

warnings.filterwarnings('ignore')

if __name__ == '__main__':
    aimDate = lastTradeDay()
    print(aimDate)
    stocks = concurrent_util.initStock(needReload=False, extra=False)
    errors = []
    chosenStocks = [stock for stock in stocks if stock[:2] in ['00', '60']]


    def N(stock):
        try:
            day2 = rules.twoDaySlideWindow(stock, aimDate=aimDate)
            if day2:
                print(f'{stock}-{day2}-二日')
                tool_box.bark_pusher('二日', f'{stock}-{day2}')
            day3 = rules.threeDaySlideWindow(stock, aimDate=aimDate)
            if day3:
                print(f'{stock}-{day3}-三日')
                tool_box.bark_pusher('三日', f'{stock}-{day3}')
        except Exception as e:
            errors.append(f'{stock} : logic error : {e}')
            pass


    tool_box.thread_pool_executor(N, chosenStocks, 20)
