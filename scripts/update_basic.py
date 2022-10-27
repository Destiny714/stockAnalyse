# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 23:23
# @Author  : Destiny_
# @File    : update_basic.py
# @Software: PyCharm

from utils import concurrent_util
from sequence.prepare import Prepare

Prepare().do()
concurrent_util.initStock(needReload=True, extra=True)
