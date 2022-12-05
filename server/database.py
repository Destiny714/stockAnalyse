# -*- coding: utf-8 -*-
# @Time    : 2022/10/25 20:53
# @Author  : Destiny_
# @File    : database.py
# @Software: PyCharm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:destinyroot@localhost/stock_server", echo=True)
SessionMaker = sessionmaker(bind=engine)
