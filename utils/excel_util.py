# -*- coding: utf-8 -*-
# @Time    : 2022/6/26 15:34
# @Author  : Destiny_
# @File    : excel_util.py
# @Software: PyCharm

import xlwt
import xlrd
import pandas
from utils.file_util import *
from utils.log_util import log
from common.tool_box import errorHandler


class ColumnModel(object):
    placeholder = 0
    columns = [
        'code', 'name', 'level',
        'AJ', 'CF', 'TF', 'CP', 'TP', 'limitOpenTime', 'height', 'white', 'black',
        'score', 'day2elg', 'day3elg',
        'open_price', 'date', 'details'
    ]

    translate = {
        'code': '代码',
        'name': '名称',
        'level': '评级',
        'AJ': '集中度',
        'CF': '主力净流入',
        'TF': '特大单净流入',
        'CP': '主力买入权重',
        'TP': '特大单买入权重',
        'limitOpenTime': '涨停打开次数',
        'height': '连板高度',
        'white': '白名单',
        'black': '黑名单',
        'score': '得分',
        'open_price': '开盘涨幅',
        'date': '日期',
        'details': '今日明细',
        'day2elg': '2日特单净流入',
        'day3elg': '3日特单净流入',
    }

    tranReverse = {}

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

    @classmethod
    def getEn(cls, ch) -> str:
        if not cls.tranReverse:
            cls.tranReverse = {cls.translate[key]: key for key in cls.translate.keys()}
        tran = cls.tranReverse.get(ch)
        return ch if not tran else tran

    @classmethod
    def getCh(cls, en) -> str:
        tran = cls.translate.get(en)
        return en if not tran else tran

    @classmethod
    def is_not_en_word(cls, word: str) -> bool:
        """
        判断一个词是否是非英文词
        :param word:
        :return: bool
        """
        count = 0
        for s in word.encode('utf-8').decode('utf-8'):
            if u'\u4e00' <= s <= u'\u9fff':
                count += 1
                break
        if count > 0:
            return True
        else:
            return False


def write(date: str, datas: list[ColumnModel]):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('stockAnalyse', cell_overwrite_ok=True)
    col = ColumnModel.columns
    for i in range(0, len(col)):
        enColumnName = col[i]
        translation = ColumnModel.translate.get(enColumnName)
        sheet.write(0, i, enColumnName if not translation else translation)
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
            excelDict[detail[0]] = {_: detail[header.index(_)] if _ in header else detail[header.index(ColumnModel.getCh(_))] for _ in
                                    ['black', 'white', 'score']}
    except Exception as e:
        log().error(errorHandler(e))
    return excelDict


def readExcel_AS(date: str, hide: bool = True) -> list[dict]:
    AS = []
    try:
        filePath = f'{projectPath()}/strategy/dragon/result/{date}.xls'
        data = xlrd.open_workbook(filePath)
        sheet = data.sheet_by_index(0)
        header: list = sheet.row_values(0)
        header = [ColumnModel.getEn(_) for _ in header]
        for i in range(1, sheet.nrows):
            detail = sheet.row_values(i)
            if detail[header.index('level')] in ['S', 'A']:
                columnDict = {_: (detail[header.index(_)] if _ in header else detail[header.index(ColumnModel.getCh(_))]) for _ in
                              ['code', 'name', 'height', 'level']}
                if hide:
                    if int(columnDict['height']) > 0:
                        AS.append(columnDict)
                else:
                    AS.append(columnDict)
    except Exception as e:
        log().error(errorHandler(e))
    return AS


def readExcel_white(date: str) -> dict:
    details_dict = {}
    try:
        filePath = f'{projectPath()}/strategy/dragon/result/{date}.xls'
        data = xlrd.open_workbook(filePath)
        sheet = data.sheet_by_index(0)
        header: list = sheet.row_values(0)
        header = [ColumnModel.getEn(_) for _ in header]
        code_index = header.index('code') if 'code' in header else header.index(ColumnModel.getCh('code'))
        details_index = header.index('details') if 'details' in header else header.index(ColumnModel.getCh('details'))
        for i in range(1, sheet.nrows):
            detail = sheet.row_values(i)
            details_dict[detail[code_index]] = detail[details_index]
    except Exception as e:
        log().error(errorHandler(e))
    return details_dict


def readExcel2DF(date: str) -> pandas.DataFrame:
    filePath = f'{projectPath()}/strategy/dragon/result/{date}.xls'
    if not os.path.exists(filePath):
        raise Exception(f'{date} 结果 EXCEL 不存在')
    df = pandas.read_excel(filePath, converters={'代码': str, 'code': str})
    df.columns = [ColumnModel.getEn(_) for _ in df.columns]
    df = df.dropna()
    return df
