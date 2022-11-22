# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 22:50
# @Author  : Destiny_
# @File    : log_util.py
# @Software: PyCharm
import os
import logging
from prefs.params import *
from utils.file_util import projectPath


class log:
    """自定义log类 单例"""
    firstStart = True
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self.firstStart:
            logger = logging.getLogger('stock-log')
            logger.setLevel(logging.INFO)
            fh = logging.FileHandler(os.path.join(projectPath(), '.logs/dragon.log'))
            ch = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            fh.setLevel(logging.WARNING)
            ch.setFormatter(formatter)
            ch.setLevel(logging.WARNING)
            if RunMode.Status == RunMode.TEST:
                logger.setLevel(logging.FATAL)
                ch.setLevel(logging.FATAL)
                fh.setLevel(logging.FATAL)
            if RunMode.Status != RunMode.TEST and not logger.handlers:
                logger.addHandler(fh)
                logger.addHandler(ch)
            self.logger = logger
            self.firstStart = False

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, warn: str):
        self.logger.warning(warn)

    def error(self, error: str):
        self.logger.error(error)

    def critical(self, error: str):
        self.logger.critical(error)
