# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 20:48
# @Author  : Destiny_
# @File    : toolBox.py
# @Software: PyCharm

import os
import yaml
import time
import logging
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


def arg_yaml():
    """读取args.yaml"""
    yaml_path = os.path.join(projectPath(), "api/args.yaml")
    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data
    except:
        return None


def projectPath() -> str:
    """获取项目根目录"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class log:
    """自定义log类 单例"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        logger = logging.getLogger('stock-log')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(os.path.join(projectPath(), 'dragon_s1/process.log'))
        fh.setLevel(logging.WARNING)
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        self.logger = logger

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, warn: str):
        self.logger.warning(warn)

    def error(self, error: str):
        self.logger.error(error)

    def critical(self, error: str):
        self.logger.critical(error)
