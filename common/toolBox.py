# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 20:48
# @Author  : Destiny_
# @File    : toolBox.py
# @Software: PyCharm

# import os
# import xlrd
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
