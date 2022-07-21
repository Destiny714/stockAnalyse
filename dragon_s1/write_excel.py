# -*- coding: utf-8 -*-
# @Time    : 2022/6/26 15:34
# @Author  : Destiny_
# @File    : write_excel.py
# @Software: PyCharm

import xlwt


def write(date: str, datas: list):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('stockAnalyse', cell_overwrite_ok=True)
    col = [
        'code', 'name', 'industry',
        'ptg_industry', 'level', 'height',
        'white', 'black', 'score',
        'T1S', 'T1F', 'S', 'W', 'B',
        'open_price', 'date', 'details', 'T1S_detail', 'T1F_detail'
    ]
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])
    for index, data in enumerate(datas):
        for j in range(0, len(col)):
            sheet.write(index + 1, j, data[j])
    savePath = f'/Users/destiny/code/dev/python/stock/stockAnalyse/dragon_s1/result/{date}.xls'
    book.save(savePath)
