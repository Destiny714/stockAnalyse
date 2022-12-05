# -*- coding: utf-8 -*-
# @Time    : 2022/11/28 15:17
# @Author  : Destiny_
# @File    : schemas.py
# @Software: PyCharm

from typing import Union
from pydantic import BaseModel


class RankDetailBase(BaseModel):
    date: str
    stock_code: str
    stock_name: str
    stock_rank: str

    class Config:
        orm_mode = True


class RankDetail(RankDetailBase):
    score: int

    class Config:
        orm_mode = True
