# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 22:43
# @Author  : Destiny_
# @File    : file_util.py
# @Software: PyCharm
import os
import yaml
from functools import lru_cache


@lru_cache()
def projectPath() -> str:
    """获取项目根目录"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@lru_cache()
def arg_yaml():
    """读取args.yaml"""
    yaml_path = os.path.join(projectPath(), "prefs/args.yaml")
    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data
    except:
        return None
