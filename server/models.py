# coding: utf-8

from sqlalchemy.orm import declarative_base
from sqlalchemy import BigInteger, Column, Float, Integer, JSON, VARCHAR, Enum

Base = declarative_base()
metadata = Base.metadata


class RankDetail(Base):
    __tablename__ = 'rank_detail'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    index_key = Column(VARCHAR(50), unique=True, index=True, nullable=False)
    date = Column(VARCHAR(50), nullable=False)
    stock_code = Column(VARCHAR(50), nullable=False)
    stock_name = Column(VARCHAR(50), nullable=False)
    stock_rank = Column(Enum('A', 'B', 'S', 'F', 'N/A'), default='N/A')
    limitHeight = Column(Integer, default=0)
    whiteNum = Column(Integer, default=0)
    blackNum = Column(Integer, default=0)
    fastBlackNum = Column(Integer, default=0)
    slowBlackNum = Column(Integer, default=0)
    score = Column(Integer, default=0)
    fastScore = Column(Integer, default=0)
    slowScore = Column(Integer, default=0)
    comparePrevScore = Column(Integer, default=0)
    detail = Column(JSON)
    fastDetail = Column(JSON)
    slowDetail = Column(JSON)
