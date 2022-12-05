# -*- coding: utf-8 -*-
# @Time    : 2022/10/25 20:53
# @Author  : Destiny_
# @File    : database.py
# @Software: PyCharm

from utils import config_yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = config_yaml()
dsn = f"mysql+pymysql://{config['mysqlAccount']}:{config['mysqlPassword']}@{config['mysqlHost']}/{config['serverDatabase']}"
engine = create_engine(dsn, echo=True)
SessionMaker = sessionmaker(bind=engine)
