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
                                  database=self.__DB, connect_timeout=5)
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
                    f"firstLimitTime BIGINT default 6666666666," \
                    f"lastLimitTime BIGINT default 6666666666," \
                    f"openTime int default 0," \
                    f"buy_sm_vol int default 0," \
                    f"buy_sm_amount double default 0," \
                    f"sell_sm_vol int default 0," \
                    f"sell_sm_amount double default 0," \
                    f"buy_md_vol int default 0," \
                    f"buy_md_amount double default 0," \
                    f"sell_md_vol int default 0," \
                    f"sell_md_amount double default 0," \
                    f"buy_lg_vol int default 0," \
                    f"buy_lg_amount double default 0," \
                    f"sell_lg_vol int default 0," \
                    f"sell_lg_amount double default 0," \
                    f"buy_elg_vol int default 0," \
                    f"buy_elg_amount double default 0," \
                    f"sell_elg_vol int default 0," \
                    f"sell_elg_amount double default 0," \
                    f"net_mf_vol int default 0," \
                    f"net_mf_amount double default 0," \
                    f"trade_count int default 0," \
                    f"his_low float default 0," \
                    f"his_high float default 0," \
                    f"cost_5pct float default 0," \
                    f"cost_15pct float default 0," \
                    f"cost_50pct float default 0," \
                    f"cost_85pct float default 0," \
                    f"cost_95pct float default 0," \
                    f"weight_avg float default 0," \
                    f"winner_rate float default 0," \
                    f"time json NULL)"
        self.action(output=False)

    def selectExistTable(self):
        self.word = 'show tables'
        data = self.action(output=True)
        dontDelete = ['stockList', 'tradeCalender', 'version', 'stockIndexList', 'NoShIndex']
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

    def selectLastTradeDate(self, date):
        self.word = f"SELECT lastDate FROM tradeCalender where date='{date}'"
        data = self.action(output=True)
        return data[0][0]

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

    def insertShIndex(self, data):
        self.word = f"INSERT ignore INTO NoShIndex " \
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

    def selectShIndexUpdateDate(self):
        self.word = f"SELECT date FROM NoshIndex ORDER BY id DESC LIMIT 1"
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

    def stockDetailUpdateDate(self, date):
        self.word = f"UPDATE version SET stockDetailUpdateDate='{date}'"
        self.action(output=False)

    def stockListUpdateDate(self, date):
        self.word = f"UPDATE version SET stockListUpdateDate='{date}'"
        self.action(output=False)

    def updateLimitDetailData(self, data):
        self.word = f"UPDATE No{str(data['ts_code']).split('.')[0]} SET " \
                    f"firstLimitTime={dateHandler.joinTimeToStamp(data['trade_date'], data['first_time'] if data['first_time'] != '' else '09:30:00')}," \
                    f"lastLimitTime={dateHandler.joinTimeToStamp(data['trade_date'], data['last_time'] if data['last_time'] != '' else '09:30:00')}," \
                    f"openTime={data['open_times']} " \
                    f"WHERE date = '{data['trade_date']}'"
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

    def updateMoneyFlow(self, data):
        self.word = f"UPDATE No{str(data['ts_code']).split('.')[0]} SET " \
                    f"buy_sm_vol={data['buy_sm_vol']}," \
                    f"buy_sm_amount={data['buy_sm_amount']}," \
                    f"sell_sm_vol={data['sell_sm_vol']}," \
                    f"sell_sm_amount={data['sell_sm_amount']}," \
                    f"buy_md_vol={data['buy_md_vol']}," \
                    f"buy_md_amount={data['buy_md_amount']}," \
                    f"sell_md_vol={data['sell_md_vol']}," \
                    f"sell_md_amount={data['sell_md_amount']}," \
                    f"buy_lg_vol={data['buy_lg_vol']}," \
                    f"buy_lg_amount={data['buy_lg_amount']}," \
                    f"sell_lg_vol={data['sell_lg_vol']}," \
                    f"sell_lg_amount={data['sell_lg_amount']}," \
                    f"buy_elg_vol={data['buy_elg_vol']}," \
                    f"buy_elg_amount={data['buy_elg_amount']}," \
                    f"sell_elg_vol={data['sell_elg_vol']}," \
                    f"sell_elg_amount={data['sell_elg_amount']}," \
                    f"net_mf_vol={data['net_mf_vol']}," \
                    f"net_mf_amount={data['net_mf_amount']}," \
                    f"trade_count={data['trade_count']} " \
                    f"WHERE date = {data['trade_date']}"
        self.action(output=False)

    def updateChipDetail(self, data):
        self.word = f"UPDATE No{str(data['ts_code']).split('.')[0]} SET " \
                    f"his_low={data['his_low']}," \
                    f"his_high={data['his_high']}," \
                    f"cost_5pct={data['cost_5pct']}," \
                    f"cost_15pct={data['cost_15pct']}," \
                    f"cost_50pct={data['cost_50pct']}," \
                    f"cost_85pct={data['cost_85pct']}," \
                    f"cost_95pct={data['cost_95pct']}," \
                    f"weight_avg={data['weight_avg']}," \
                    f"winner_rate={data['winner_rate']} " \
                    f"WHERE date = {data['trade_date']}"
        self.action(output=False)

    def updateTimeData(self, json: dict):
        self.word = f"UPDATE No{json['symbol']} SET time='{json['data']}' WHERE date='{json['date']}'"
        self.action(output=False)

    def changeColumn(self, table):
        print(table)
        self.word = f"ALTER TABLE {table} change COLUMN firstLimitTime firstLimitTime BIGINT default 6666666666,change COLUMN lastLimitTime lastLimitTime BIGINT default 6666666666"
        self.action(output=False)

    def updateTMP(self, table):
        print(table)
        self.word = f"UPDATE {table} SET firstLimitTime=6666666666 WHERE firstLimitTime=4090665600"
        self.action(output=False)
        self.word = f"UPDATE {table} SET lastLimitTime=6666666666 WHERE lastLimitTime=4090665600"
        self.action(output=False)
