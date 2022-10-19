# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 01:29
# @Author  : Destiny_
# @File    : excel_model.py
# @Software: PyCharm


import xlrd

from utils.file_util import projectPath


class ExcelModel:

    @classmethod
    def load(cls, date: str):
        filePath = f'{projectPath()}/strategy/dragon/result/{date}.xls'
        data = xlrd.open_workbook(filePath)
        sheet = data.sheet_by_index(0)
        header: list = sheet.row_values(0)
        dateInd = header.index('date')
        codeInd = header.index('code')
        nameInd = header.index('name')
        levelInd = header.index('level')
        heightInd = header.index('height')
        results = []
        for i in range(1, sheet.nrows):
            result = sheet.row_values(i)
            if result[levelInd] in ['S', 'A']:
                dataDict = {'date': result[dateInd], 'code': result[codeInd], 'name': result[nameInd], 'level': result[levelInd],
                            'height': int(result[heightInd])}
                results.append(dataDict)
        return results
