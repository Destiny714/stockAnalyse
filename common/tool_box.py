# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 20:48
# @Author  : Destiny_
# @File    : tool_box.py
# @Software: PyCharm

import time
import requests
from typing import List
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


def timeCount(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f'use {int((time.time() - start) * 1000)}ms')
        return res

    return wrapper


def thread_pool_executor(func, iterable, thread_num=20):
    """多线程"""
    executor = ThreadPoolExecutor(max_workers=thread_num)
    tasks = [executor.submit(func, _) for _ in iterable]
    for task in as_completed(tasks):
        task.result()


def process_pool_executor(func, iterable, process_num=10):
    """多进程"""
    assert process_num <= 10
    executor = ProcessPoolExecutor(max_workers=process_num)
    tasks = [executor.submit(func, _) for _ in iterable]
    for task in as_completed(tasks):
        task.result()


def errorHandler(e: Exception) -> str:
    errFile = None
    errLine = None
    tb = e.__traceback__
    while tb:
        errLine = tb.tb_lineno
        errFile = tb.tb_frame.f_code.co_filename
        tb = tb.tb_next
    return f'< line {errLine} , in {errFile} >'


def cutList(full_list: list, piece: int) -> List[list]:
    """切割大列表 --> list[小列表]"""
    cut_list = []
    extra_num = len(full_list) % piece
    if extra_num != 0:
        extra = full_list[-extra_num:]
        full = full_list[:-extra_num]
    else:
        extra = []
        full = full_list
    for i in range(len(full) // piece):
        small_piece = full[piece * i:piece * (i + 1)]
        cut_list.append(small_piece)
    if extra:
        cut_list.append(extra)
    return cut_list


def bark_pusher(title, content, _url=None):
    url = f'https://api.day.app/y67CydURc8wR9CVemagkYL/{title}/{content}'
    if _url is not None:
        url += f'?url={_url}'
    requests.get(url, verify=False)
