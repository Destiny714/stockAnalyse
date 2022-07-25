# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 19:20
# @Author  : Destiny_
# @File    : databaseApi.py
# @Software: PyCharm

import pymysql
from common import dateHandler


class Mysql:
    def __init__(self):
        self.__account = 'root'
        self.__pswd = 'destinyroot'
        self.__DB = 'stock'
        self.host = 'localhost'
        self.word = ''
        self.db = pymysql.connect(host=self.host, port=3306, user=self.__account, password=self.__pswd,
                                  database=self.__DB,connect_timeout=60)
        self.cursor = self.db.cursor()

    def action(self, output: bool):
        self.cursor.execute(self.word)
        if output:
            callback = self.cursor.fetchall()
            return callback
        else:
            self.db.commit()

    def suffix(self, stock: str) -> str:
        self.word = f"SELECT exchange FROM stockList WHERE symbol={stock}"
        market = self.action(output=True)[0][0]
        return f"{stock}.{'SZ' if market == 'SZSE' else 'SH'}"

    def insertTradeCalender(self, data):
        self.word = f"INSERT ignore INTO tradeCalender (date, lastDate) VALUES ('{data['date']}','{data['lastDate']}')"
        self.action(output=False)

    def insertStockDetail(self, data):
        self.word = f"INSERT ignore INTO stockList " \
                    f"(symbol, name, industry, market, exchange) " \
                    f"VALUES ('{data['symbol']}','{data['name']}','{data['industry']}','{data['market']}','{data['exchange']}')"
        self.action(output=False)

    def createTableForStock(self, stock):
        self.word = f"CREATE TABLE IF NOT EXISTS No{stock} " \
                    f"(id INT NOT NULL primary key AUTO_INCREMENT," \
                    f"date varchar(50)not null unique ," \
                    f"open double not null," \
                    f"close double not null, " \
                    f"preClose double not null," \
                    f"high double not null," \
                    f"low double not null, " \
                    f"pctChange double not null," \
                    f"volume double not null," \
                    f"amount double not null," \
                    f"turnover double default 0," \
                    f"firstLimitTime BIGINT default 0," \
                    f"lastLimitTime BIGINT default 0," \
                    f"openTime int default 0)"
        self.action(output=False)

    def selectExistTable(self):
        self.word = 'show tables'
        data = self.action(output=True)
        dontDelete = ['stockList', 'tradeCalender', 'version', 'No399006', 'stockIndexList']
        return [_[0] for _ in data if _[0] not in dontDelete]

    def selectAllStock(self):
        self.word = "SELECT symbol FROM stockList"
        data = self.action(output=True)
        return [_[0] for _ in data]

    def selectAllIndex(self):
        self.word = 'SELECT symbol FROM stockIndexList'
        data = self.action(output=True)
        return [_[0] for _ in data]

    def selectTradeDate(self):
        self.word = 'SELECT date FROM tradeCalender'
        data = self.action(output=True)
        return [_[0] for _ in data]

    def selectNextTradeDay(self, date):
        self.word = f"SELECT date FROM tradeCalender WHERE id > (SELECT id FROM tradeCalender WHERE date='{date}') LIMIT 1"
        data = self.action(output=True)
        return data[0][0]

    def deleteTable(self, tableList: list):
        tables = ''
        for table in tableList:
            if table[0:2] == 'No':
                if not tables:
                    tables += table
                else:
                    tables += f",{table}"
        self.word = f"DROP TABLE IF EXISTS {tables}"
        print(self.word)
        self.action(output=False)

    def insertOneRecord(self, data):
        self.word = f"INSERT ignore INTO No{str(data['ts_code']).split('.')[0]} " \
                    f"(date,open,close,preClose,high,low,pctChange,volume,amount) VALUES " \
                    f"('{data['trade_date']}',{data['open']},{data['close']},{data['pre_close']}," \
                    f"{data['high']},{data['low']},{data['pct_chg']},{data['vol']},{data['amount']})"
        self.action(output=False)

    def selectStockAmount(self, stock) -> float:
        self.word = f"SELECT amount FROM stockList WHERE symbol='{stock}'"
        volume = self.action(output=True)
        return volume[0][0]

    def selectIndustryByStock(self, stock: str):
        self.word = f"SELECT industry FROM stockList WHERE symbol='{stock}'"
        industry = self.action(output=True)
        return industry[0][0]

    def selectAllIndustry(self):
        self.word = f"SELECT industry FROM stockList"
        industries = self.action(output=True)
        return list(set([_[0] for _ in industries]))

    def selectStockByIndustry(self, industry: str):
        self.word = f"SELECT symbol FROM stockList WHERE industry='{industry}'"
        stocks = self.action(output=True)
        return [_[0] for _ in stocks]

    def selectStockDetail(self, stock: str):
        self.word = f"SELECT * FROM stockList WHERE symbol='{stock}'"
        detail = self.action(output=True)
        return detail[0]

    def selectOneAllData(self, stock, dateRange, aimDate=''):
        if aimDate == '':
            self.word = f"SELECT * FROM No{stock}"
        else:
            self.word = f"(SELECT * FROM No{stock} WHERE id <= (SELECT id FROM No{stock} WHERE date={aimDate}) " \
                        f"ORDER BY id DESC LIMIT {dateRange}) " \
                        f"ORDER BY id"
        data = self.action(output=True)
        return data

    def selectLastDate(self, date):
        self.word = f"SELECT lastDate FROM tradeCalender WHERE date='{date}'"
        data = self.action(output=True)
        return data[0][0]

    def selectVerifyData(self, stock, startDate, dateRange=2):
        self.word = f"SELECT * FROM No{stock} " \
                    f"WHERE (id > " \
                    f"(SELECT id FROM No{stock} WHERE date = '{startDate}') AND " \
                    f"id <= " \
                    f"((SELECT id FROM No{stock} WHERE date = '{startDate}') + {dateRange}))"
        data = self.action(output=True)
        return data

    def selectGemUpdateDate(self):
        self.word = f"SELECT date FROM No399006 ORDER BY id DESC LIMIT 1"
        data = self.action(output=True)
        return data[0][0]

    def selectDetailUpdateDate(self):
        self.word = 'SELECT stockDetailUpdateDate FROM version'
        date = self.action(output=True)
        return date[0][0]

    def selectListUpdateDate(self):
        self.word = 'SELECT stockListUpdateDate FROM version'
        date = self.action(output=True)
        return date[0][0]

    def selectIndexUpdateDate(self):
        self.word = 'SELECT stockIndexUpdateDate FROM version'
        date = self.action(output=True)
        return date[0][0]

    def stockDetailUpdateDate(self, date):
        self.word = f"UPDATE version SET stockDetailUpdateDate='{date}'"
        self.action(output=False)

    def stockListUpdateDate(self, date):
        self.word = f"UPDATE version SET stockListUpdateDate='{date}'"
        self.action(output=False)

    def stockIndexUpdateDate(self, date):
        self.word = f"UPDATE version SET stockIndexUpdateDate='{date}'"
        self.action(output=False)

    def addLimitDetail(self, table):
        self.word = f"ALTER TABLE {table} ADD COLUMN firstLimitTime BIGINT default 0"
        self.action(output=False)
        self.word = f"ALTER TABLE {table} ADD COLUMN lastLimitTime BIGINT default 0"
        self.action(output=False)
        self.word = f"ALTER TABLE {table} ADD COLUMN openTime INT default 0"
        self.action(output=False)

    def updateLimitDetailData(self, data):
        self.word = f"UPDATE No{str(data['ts_code']).split('.')[0]} SET " \
                    f"firstLimitTime={dateHandler.joinTimeToStamp(data['trade_date'], data['first_time'] if data['first_time'] != '' else '09:30:00')}," \
                    f"lastLimitTime={dateHandler.joinTimeToStamp(data['trade_date'], data['last_time'] if data['last_time'] != '' else '09:30:00')}," \
                    f"openTime={data['open_times']} WHERE date = '{data['trade_date']}'"
        self.action(output=False)

    def updateStockListDailyIndex(self, data):
        if data['circ_mv'] is None or '':
            return
        if data['turnover_rate'] is None or '':
            return
        self.word = f"UPDATE stockList SET amount={data['circ_mv']} WHERE symbol={str(data['ts_code']).split('.')[0]}"
        self.action(output=False)
        self.word = f'UPDATE No{str(data["ts_code"]).split(".")[0]} SET turnover={data["turnover_rate"]} WHERE date={data["trade_date"]}'
        self.action(output=False)
