# -*- coding: utf-8 -*-
# @Time    : 2023/2/18 22:48
# @Author  : Destiny_
# @File    : backtrace.py
# @Software: PyCharm
from utils.excel_util import readExcel_AS
from utils.stockdata_util import queryData, limit
from models.stock_data_model import StockDataModel
from utils.date_util import allTradeDay, nextXTradeDay


def percent(res: float):
    return int(res * 100)


if __name__ == '__main__':
    tradeDays = [day for day in allTradeDay() if '20221101' <= day <= '20221231']

    # with open('./limit_rate.csv', 'w') as f:
    #     f.write('日期,T日A票个数,T+1日涨停率,T+2日涨停率,T+3日涨停率,T+4日涨停率\n')
    #     for date in tradeDays:
    #         AS = readExcel_AS(date)
    #         A = [d for d in AS if d['level'] == 'A']
    #         count = len(A)
    #         if count == 0:
    #             continue
    #         t1l, t2l, t3l, t4l = 0, 0, 0, 0
    #         for a in A:
    #             code = a['code']
    #             limit_rate = limit(code)
    #             day2calculate = nextXTradeDay(date, 4)
    #             data = queryData(code, 10, day2calculate)
    #             t1 = data[-4]
    #             if t1.pctChange >= limit_rate:
    #                 t1l += 1
    #             t2 = data[-3]
    #             if t2.pctChange >= limit_rate:
    #                 t2l += 1
    #             t3 = data[-2]
    #             if t3.pctChange >= limit_rate:
    #                 t3l += 1
    #             t4 = data[-1]
    #             if t4.pctChange >= limit_rate:
    #                 t4l += 1
    #         f.write(f'{date},{count},{percent(t1l / count)},{percent(t2l / count)},{percent(t3l / count)},{percent(t4l / count)}\n')

    def rule1(t_1: StockDataModel, t_2: StockDataModel):
        return percent((t_2.open / t_1.open) - 1)


    def rule2(t_1: StockDataModel, t_2: StockDataModel):
        return percent((t_2.high / t_1.open) - 1)


    def rule3(t_1: StockDataModel, t_2: StockDataModel):
        return percent((t_2.low / t_1.open) - 1)


    def rule4(t_1: StockDataModel, t_2: StockDataModel):
        return percent((t_2.open / t_1.high) - 1)


    def rule5(t_1: StockDataModel, t_2: StockDataModel):
        return percent((t_2.high / t_1.high) - 1)


    def rule6(t_1: StockDataModel, t_2: StockDataModel):
        return percent((t_2.low / t_1.high) - 1)


    with open('./profit.csv', 'w') as f:
        f.write('日期,T日A票个数,收益率1,收益率2,收益率3,收益率4,收益率5,收益率6\n')
        for date in tradeDays:
            AS = readExcel_AS(date)
            A = [d for d in AS if d['level'] == 'A']
            count = len(A)
            if count == 0:
                continue
            r1, r2, r3, r4, r5, r6 = 0, 0, 0, 0, 0, 0,
            for a in A:
                code = a['code']
                limit_rate = limit(code)
                day2calculate = nextXTradeDay(date, 2)
                data = queryData(code, 10, day2calculate)
                t1 = data[-4]
                t2 = data[-3]
                p1 = rule1(t1, t2)
                p2 = rule2(t1, t2)
                p3 = rule3(t1, t2)
                p4 = rule4(t1, t2)
                p5 = rule5(t1, t2)
                p6 = rule6(t1, t2)
                r1 += p1
                r2 += p2
                r3 += p3
                r4 += p4
                r5 += p5
                r6 += p6
            f.write(
                f'{date},{count},{round(r1 / count, 1)}%,{round(r2 / count, 1)}%,{round(r3 / count, 1)}%,{round(r4 / count, 1)}%,{round(r5 / count, 1)}%,{round(r6 / count, 1)}%\n')
