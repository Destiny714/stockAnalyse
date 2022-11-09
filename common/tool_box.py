# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 20:48
# @Author  : Destiny_
# @File    : tool_box.py
# @Software: PyCharm

import os
import time
from typing import Iterable, Callable
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


def timeCount(func: Callable):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f'use {(time.time() - start) * 1000}ms')
        return res

    return wrapper


def thread_pool_executor(func: Callable, iterable: Iterable, thread_num=20, *args, **kwargs):
    """
    多线程入口函数
    :param func: 多线程运行的函数
    :param iterable: 线程启动器，可迭代对象
    :param thread_num: 同时运行最大线程数
    :return: list -> 每个线程的返回值
    """
    executor = ThreadPoolExecutor(max_workers=thread_num)
    tasks = [executor.submit(func, _, *args, **kwargs) for _ in iterable]
    return [task.result() for task in as_completed(tasks)]


def process_pool_executor(func: Callable, iterable: Iterable, process_num=10, *args, **kwargs):
    """
    多进程入口函数
    :param func: 多进程运行的函数
    :param iterable: 进程启动器，可迭代对象
    :param process_num: 同时运行最大进程数，不超过核心数量两倍
    :return: list -> 每个进程的返回值
    """
    assert process_num <= os.cpu_count() * 2, '进程数超出'
    executor = ProcessPoolExecutor(max_workers=process_num)
    tasks = [executor.submit(func, _, *args, **kwargs) for _ in iterable]
    return [task.result() for task in as_completed(tasks)]


def errorHandler(e: Exception) -> str:
    """
    Exception格式转换 --> 控制台输出
    :param e: Exception
    :return: errors str
    """
    errMsg = ''
    tb = e.__traceback__
    while tb is not None:
        errMsg += f' <line {tb.tb_lineno} , in {tb.tb_frame.f_code.co_filename}> '
        tb = tb.tb_next
    return errMsg


def cutList(full_list: list, piece_len: int) -> list[list]:
    """
    切割大列表 --> list[小列表]
    :param full_list: 大列表
    :param piece_len: 切割后每个小列表的长度
    :return: list[小列表]
    """
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
