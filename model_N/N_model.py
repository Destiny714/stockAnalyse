# -*- coding: utf-8 -*-
# @Time    : 2022/4/17 19:39
# @Author  : Destiny_
# @File    : N_model.py
# @Software: PyCharm
import rules
from common import toolBox, dateHandler, concurrentActions

if __name__ == '__main__':
    stocks = concurrentActions.initStock(needReload=True, extra=False)
    errors = []
    chosenStocks = [stock for stock in stocks if stock[:2] in ['00', '60']]


    def N(stock):
        try:
            day2 = rules.twoDaySlideWindow(stock, aimDate=dateHandler.lastTradeDay())
            if day2:
                print(f'{stock}-{day2}-二日')
            day3 = rules.threeDaySlideWindow(stock, aimDate=dateHandler.lastTradeDay())
            if day3:
                print(f'{stock}-{day3}-三日')
        except Exception as e:
            errors.append(f'{stock} : logic error : {e}')
            pass


    toolBox.thread_pool_executor(N, chosenStocks, 20)
