# -*- coding: utf-8 -*-
# @Time    : 2022/6/26 15:34
# @Author  : Destiny_
# @File    : excel_process.py
# @Software: PyCharm
import os
import xlwt
import xlrd

from common.toolBox import errorHandler

cols = [
    'code', 'name', 'industry',
    'ptg_industry', 'level',
    'AJ', 'CF', 'TF', 'TP', 'height', 'white', 'black',
    'b1', 'b2', 'score', 'T1S', 'T1F', 'S',
    'open_price', 'date', 'details', 'T1S_detail', 'T1F_detail'
]


def write(date: str, datas: list):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('stockAnalyse', cell_overwrite_ok=True)
    col = cols
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])
    for index, data in enumerate(datas):
        for j in range(0, len(col)):
            sheet.write(index + 1, j, data[j])
    absPath = os.getcwd().replace('/dragon_s1', '').replace('/common', '')
    savePath = f'{absPath}/dragon_s1/result/{date}.xls'
    book.save(savePath)


def readScoreFromExcel(date):
    excelDict = {}
    try:
        absPath = os.getcwd().replace('/dragon_s1', '')
        filePath = f'{absPath}/dragon_s1/result/{date}.xls'
        data = xlrd.open_workbook(filePath)
        sheet = data.sheet_by_index(0)
        header: list = sheet.row_values(0)
        for i in range(1, sheet.nrows):
            detail = sheet.row_values(i)
            excelDict[detail[0]] = {'white': detail[header.index("white")],
                                    'black': detail[header.index("black")],
                                    'score': detail[header.index("score")]}
    except Exception as e:
        errorHandler(e)
    return excelDict
