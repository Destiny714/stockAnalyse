# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 23:23
# @Author  : Destiny_
# @File    : update_basic.py
# @Software: PyCharm

from api.tushare_api import Tushare
from utils.concurrent_util import updateChipDetail

Tushare.init()
updateChipDetail(20230112)
# concurrent_util.initStock(needReload=True, extra=True)
