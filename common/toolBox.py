# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 20:48
# @Author  : Destiny_
# @File    : toolBox.py
# @Software: PyCharm

import os
import xlrd
from concurrent.futures import ThreadPoolExecutor, as_completed


def thread_pool_executor(func, iterable, thread_num=20):
    executor = ThreadPoolExecutor(max_workers=thread_num)
    tasks = [executor.submit(func, _) for _ in iterable]
    for task in as_completed(tasks):
        task.result()


def errorHandler(e: Exception, arg=None):
    tb = e.__traceback__
    while tb:
        print(f'{arg} : <{tb.tb_frame.f_code.co_filename} line:{tb.tb_lineno} detail:{e.args[0]}>')
        tb = tb.tb_next


def readScoreFromExcel(date):
    excelDict = {}
    try:
        absPath = os.getcwd().replace('/common','')
        filePath = f'{absPath}/dragon_s1/result/{date}.xls'
        data = xlrd.open_workbook(filePath)
        sheet = data.sheet_by_index(0)
        for i in range(1, sheet.nrows):
            detail = sheet.row_values(i)
            excelDict[detail[0]] = {'score': detail[8], 'white': detail[6], 'black': detail[7]}
    except Exception as e:
        errorHandler(e)
    return excelDict