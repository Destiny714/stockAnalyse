# -*- coding: utf-8 -*-
# @Time    : 2022/11/30 22:25
# @Author  : Destiny_
# @File    : crud.py
# @Software: PyCharm

import models
from sqlalchemy.orm import Session


def get_rank_details(db: Session, date: str, page: int = 0):
    limit = 20
    return db.query(models.RankDetail).where(models.RankDetail.date == date).offset(page * limit).limit(limit).all()
