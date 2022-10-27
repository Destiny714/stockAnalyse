# -*- coding: utf-8 -*-
# @Time    : 2022/6/26 15:34
# @Author  : Destiny_
# @File    : excel_util.py
# @Software: PyCharm

import xlwt
import xlrd
from utils.file_util import *
from utils.log_util import log
from common.tool_box import errorHandler


class ColumnModel(object):
    placeholder = 0
    columns = [
        'code', 'name', 'industry',
        'ptg_industry', 'level',
        'AJ', 'CF', 'TF', 'TP', 'height', 'white', 'black',
        'b1', 'b2', 'score', 'T1S', 'T1F', 'S',
        'open_price', 'date', 'details', 'T1S_detail', 'T1F_detail'
    ]

    def __init__(self, resultDict: dict = None):
        if not resultDict:
            resultDict = {}
        for col in self.columns:
            self.__dict__[col] = self.placeholder
        for key in resultDict.keys():
            if key in self.__dict__.keys():
                self.__dict__[key] = resultDict[key]

    def dict(self):
        return self.__dict__


def write(date: str, datas: list[ColumnModel]):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('stockAnalyse', cell_overwrite_ok=True)
    col = ColumnModel.columns
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])
    for index, data in enumerate(datas):
        args: dict = data.dict()
        for j in range(0, len(col)):
            sheet.write(index + 1, j, args[col[j]])
    savePath = f'{projectPath()}/strategy/dragon/result/{date}.xls'
    book.save(savePath)


def readScoreFromExcel(date):
    excelDict = {}
    try:
        filePath = f'{projectPath()}/strategy/dragon/result/{date}.xls'
        data = xlrd.open_workbook(filePath)
        sheet = data.sheet_by_index(0)
        header: list = sheet.row_values(0)
        for i in range(1, sheet.nrows):
            detail = sheet.row_values(i)
            excelDict[detail[0]] = {_: detail[header.index(_)] for _ in ['black', 'white', 'score']}
    except Exception as e:
        log().error(errorHandler(e))
    return excelDict


def readExcel_AS(date) -> list[dict]:
    AS = []
    try:
        filePath = f'{projectPath()}/strategy/dragon/result/{date}.xls'
        data = xlrd.open_workbook(filePath)
        sheet = data.sheet_by_index(0)
        header: list = sheet.row_values(0)
        for i in range(1, sheet.nrows):
            detail = sheet.row_values(i)
            if detail[header.index('level')] in ['S', 'A']:
                columnDict = {_: detail[header.index(_)] for _ in ['code', 'name', 'height', 'level']}
                AS.append(columnDict)
    except Exception as e:
        log().error(errorHandler(e))
    return AS
