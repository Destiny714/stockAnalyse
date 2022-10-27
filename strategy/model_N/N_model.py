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
from utils.push_util import WechatPush, DingtalkPush, Mode

warnings.filterwarnings('ignore')

if __name__ == '__main__':
    aimDate = lastTradeDay()
    print(aimDate)
    stocks = concurrent_util.initStock(needReload=False, extra=False)
    errors = []
    chosenStocks = [stock for stock in stocks if stock[:2] in ['00', '60']]
    Ns = []


    def N(stock):
        client = db.Mysql()
        try:
            day2 = rules.twoDaySlideWindow(stock, aimDate=aimDate)
            if day2:
                print(f'{stock}-{day2}-二日')
                Ns.append({'code': stock, 'name': client.selectNameByStock(stock), 'inCycle': '2'})
            day3 = rules.threeDaySlideWindow(stock, aimDate=aimDate)
            if day3:
                print(f'{stock}-{day3}-三日')
                Ns.append({'code': stock, 'name': client.selectNameByStock(stock), 'inCycle': '3'})
        except Exception as e:
            errors.append(f'{stock} : logic error : {e}')
            pass
        finally:
            client.close()


    tool_box.thread_pool_executor(N, chosenStocks, 20)
    WechatPush(Mode.Dev).pushN('20221021', Ns)
    DingtalkPush(Mode.Dev).pushN('20221021', Ns)
