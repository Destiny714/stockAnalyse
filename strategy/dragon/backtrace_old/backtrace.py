# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 01:51
# @Author  : Destiny_
# @File    : backtrace_old.py
# @Software: PyCharm

import os
import xlwt
from typing import Union
from matplotlib import pyplot as plt

import excel_model
from database.db import Stock_Database
from utils.stockdata_util import *
from column_model import ColumnModel
from utils.file_util import projectPath
from common.tool_box import process_pool_executor


def incrData(file: str):
    _date = file.replace('.xls', '')
    data = excel_model.ExcelModel.load(_date)
    return data


def makeModel(_):
    date = _['date']
    code = _['code']
    columnMap = {
        'backTraceDate': date,
        'level': _['level'],
        'height': _['height'],
        'name': _['name'],
    }
    if int(nextXTradeDay(date, 3)) <= int(lastTradeDay()):
        aimDate = nextXTradeDay(date, 3)
        backTraceData = queryData(code, 30, aimDate=aimDate)
        shIndexData = queryIndexData('ShIndex', 30, aimDate)
        columnMap['shIndexClosePCT_0'] = toPercent(t_close_pct(shIndexData, 3))
        for i in range(1, 4):
            try:
                columnMap[f'lowPCT_{i}'] = toPercent(t_low_pct(backTraceData, 3 - i))
                columnMap[f'openPCT_{i}'] = toPercent(t_open_pct(backTraceData, 3 - i))
                columnMap[f'highPCT_{i}'] = toPercent(t_high_pct(backTraceData, 3 - i))
                columnMap[f'closePCT_{i}'] = toPercent(t_close_pct(backTraceData, 3 - i))
                columnMap[f'isLimit_{i}'] = 1 if t_limit(code, backTraceData, 3 - i) else 0
                columnMap[f'shIndexClosePCT_{i}'] = toPercent(t_close_pct(shIndexData, 3 - i))
            except:
                pass
        columnModel = ColumnModel(columnMap)
        return columnModel


def toPercent(n: Union[int, float]):
    return f'{round(n * 100, 2)}%'


def toNum(pct: str):
    if pct == 'N/A':
        return 0
    return round(float(pct.replace('%', '')) / 100, 2)


def write():
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('backtrace_old', cell_overwrite_ok=True)
    col = ColumnModel.__cols__
    for o in range(0, len(col)):
        sheet.write(0, o, col[o])
    for index, model in enumerate(columnModels):
        models = [_ for _ in model.__dict__.values()]
        for j in range(0, len(col)):
            sheet.write(index + 1, j, models[j])
    savePath = f'{projectPath()}/strategy/dragon/backtrace_old/backtrace_old.xls'
    book.save(savePath)


if __name__ == '__main__':
    excelPath = f'{projectPath()}/strategy/dragon/result'
    files = os.listdir(excelPath)
    client = Stock_Database()
    datas = []

    res = process_pool_executor(incrData, files, 20)
    for _ in res:
        datas.extend(_)


    def rank(d: ColumnModel):
        return int(d.backTraceDate)


    columnModels = []
    res = process_pool_executor(makeModel, datas, 20)
    columnModels.extend([_ for _ in res if _ is not None])
    columnModels.sort(key=rank)
    hashmap = {}
    standardRate = 0.02
    for bc in columnModels:
        if bc.backTraceDate in hashmap.keys():
            hashmap[bc.backTraceDate].append(bc)
        else:
            hashmap[bc.backTraceDate] = [bc]
    winRateMap = {}
    winDay = 0
    for backTraceDate in hashmap.keys():
        bcs: list[ColumnModel] = hashmap[backTraceDate]
        win = 0
        len_ = len(bcs)
        profitSum = 0
        for bc in bcs:
            try:
                base = 1 * (1 + toNum(bc.lowPCT_1))
                columnDict = bc.__dict__
                v = 2
                sellPoint = max(
                    [
                        toNum(_) for _ in
                        [columnDict[f'lowPCT_{v}'], columnDict[f'openPCT_{v}'], columnDict[f'highPCT_{v}'], columnDict[f'closePCT_{v}']]
                    ]
                )
                cursor = 1 * (1 + toNum(bc.closePCT_1)) * (1 + sellPoint)
                if cursor / base < 1 + standardRate:
                    cursor = 1 * (1 + toNum(bc.closePCT_1)) * (1 + toNum(bc.closePCT_2))
                    v = 3
                    sellPoint = max(
                        [
                            toNum(_) for _ in
                            [columnDict[f'lowPCT_{v}'], columnDict[f'openPCT_{v}'], columnDict[f'highPCT_{v}'], columnDict[f'closePCT_{v}']]
                        ]
                    )
                    cursor *= (1 + sellPoint)
                if cursor / base >= 1 + standardRate:
                    win += 1
                profitSum += cursor / base
            except:
                len_ -= 1
        winRate = win / len_ * 100
        winRateMap[backTraceDate] = winRate
        if profitSum / len_ > 1 + standardRate:
            winDay += 1
    print(winRateMap)
    print(f'{winDay}/{len(hashmap.keys())}')
    plt.figure(figsize=(100, 20))
    x = [_ for _ in hashmap.keys()]
    y = [winRateMap[_] for _ in x]
    plt.title = "winrate backtrace_old"
    plt.xlabel = 'date'
    plt.ylabel = 'rate/%'
    plt.plot(x, y, label=f"winrate for profit > {standardRate * 100}%", color="red")
    plt.xticks(x[::1])
    plt.xticks(list(x)[::1], x[::1], rotation=90)
    plt.grid(alpha=0.4)
    plt.legend(loc=2)
    plt.show()
