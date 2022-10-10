# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 20:48
# @Author  : Destiny_
# @File    : tool_box.py
# @Software: PyCharm

import os
import time
import requests
from typing import List
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


def timeCount(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f'use {(time.time() - start) * 1000}ms')
        return res

    return wrapper


def thread_pool_executor(func, iterable, thread_num=20, *args, **kwargs):
    """多线程"""
    executor = ThreadPoolExecutor(max_workers=thread_num)
    tasks = [executor.submit(func, _, *args, **kwargs) for _ in iterable]
    return [task.result() for task in as_completed(tasks)]


def process_pool_executor(func, iterable, process_num=10, *args, **kwargs):
    """多进程"""
    assert process_num <= os.cpu_count() * 2, '进程数超出'
    executor = ProcessPoolExecutor(max_workers=process_num)
    tasks = [executor.submit(func, _, *args, **kwargs) for _ in iterable]
    return [task.result() for task in as_completed(tasks)]


def errorHandler(e: Exception) -> str:
    errMsg = ''
    tb = e.__traceback__
    while tb is not None:
        errMsg += f' <line {tb.tb_lineno} , in {tb.tb_frame.f_code.co_filename}> '
        tb = tb.tb_next
    return errMsg


def cutList(full_list: list, piece_len: int) -> List[list]:
    """切割大列表 --> list[小列表]"""
    cut_list = []
    extra_num = len(full_list) % piece_len
    extra = []
    full = full_list
    if extra_num != 0:
        extra = full_list[-extra_num:]
        full = full_list[:-extra_num]
    for i in range(len(full) // piece_len):
        small_piece = full[piece_len * i:piece_len * (i + 1)]
        cut_list.append(small_piece)
    if extra:
        cut_list.append(extra)
    return cut_list


def bark_pusher(title, content, _url=None):
    url = f'https://api.day.app/y67CydURc8wR9CVemagkYL/{title}/{content}'
    if _url is not None:
        url += f'?url={_url}'
    requests.get(url, verify=False)
