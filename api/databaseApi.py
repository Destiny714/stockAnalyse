# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 19:20
# @Author  : Destiny_
# @File    : databaseApi.py
# @Software: PyCharm

import pymysql
from api import args
from common import dateHandler


class Mysql:
    def __init__(self):
        self.__account = args['mysqlAccount']
        self.__pswd = args['mysqlPassword']
        self.__DB = args['mysqlDatabase']
        self.host = args['mysqlHost']
        self.word = ''
        self.db = pymysql.connect(host=self.host, port=3306, user=self.__account, password=self.__pswd,
                                  database=self.__DB, connect_timeout=5)
        self.cursor = self.db.cursor()

    def action(self, output: bool):
        """mysql语句执行基础单元"""
        self.cursor.execute(self.word)
        if output:
            callback = self.cursor.fetchall()
            return callback
        else:
            self.db.commit()

    def suffix(self, stock: str) -> str:
        """获取带后缀的stock"""
        self.word = f"SELECT exchange FROM stockList WHERE symbol={stock}"
        market = self.action(output=True)[0][0]
        return f"{stock}.{'SZ' if market == 'SZSE' else 'SH'}"

    def insertTradeCalender(self, data):
        """交易日历插入新数据"""
        self.word = f"INSERT ignore INTO tradeCalender (date, lastDate) VALUES ('{data['date']}','{data['lastDate']}')"
        self.action(output=False)

    def insertStockDetail(self, data):
        """股票资料列表插入新数据"""
        self.word = f"INSERT ignore INTO stockList " \
                    f"(symbol, name, industry, market, exchange) " \
                    f"VALUES ('{data['symbol']}','{data['name']}','{data['industry']}','{data['market']}','{data['exchange']}')"
        self.action(output=False)

    def updateStockDetail(self, data):
        """股票资料列更新数据"""
        self.word = f"UPDATE stockList SET name='{data['name']}',industry='{data['industry']}' WHERE symbol={data['symbol']}"
        self.action(output=False)

    def createTableForStock(self, stock):
        """创建新stock table"""
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
        """查找现存的stock table"""
        self.word = 'show tables'
        data = self.action(output=True)
        dontDelete = ['stockList', 'tradeCalender', 'version', 'stockIndexList', 'NoShIndex']
        return [_[0] for _ in data if _[0] not in dontDelete and _[0][:2] == 'No' and 'Index' not in _[0]]

    def selectAllStock(self):
        """从股票资料列表中查找所有股票"""
        self.word = "SELECT symbol FROM stockList"
        data = self.action(output=True)
        return [_[0] for _ in data]

    def selectAllIndex(self):
        """查找所有股票指数列表"""
        self.word = 'SELECT symbol FROM stockIndexList'
        data = self.action(output=True)
        return [_[0] for _ in data]

    def selectTradeDate(self):
        """查找所有交易日"""
        self.word = 'SELECT date FROM tradeCalender'
        data = self.action(output=True)
        return [_[0] for _ in data]

    def selectTradeDateByDuration(self, date, duration: int):
        """选取指定date往前推『duration』日的日期范围"""
        self.word = f"(SELECT id,date FROM tradeCalender WHERE id <= (SELECT id FROM tradeCalender WHERE date={date}) " \
                    f"ORDER BY id DESC LIMIT {duration}) " \
                    f"ORDER BY id"
        result = self.action(output=True)
        return [_[1] for _ in result]

    def selectLastTradeDate(self, date):
        """选取上一个交易日"""
        self.word = f"SELECT lastDate FROM tradeCalender where date='{date}'"
        data = self.action(output=True)
        return data[0][0]

    def selectNextTradeDay(self, date):
        """选取下一个交易日"""
        self.word = f"SELECT date FROM tradeCalender WHERE id > (SELECT id FROM tradeCalender WHERE date='{date}') LIMIT 1"
        data = self.action(output=True)
        return data[0][0]

    def deleteTable(self, tableList: list):
        """删除给定的table列表"""
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

    def deleteStockFromList(self, stock):
        self.word = f"DELETE FROM stockList WHERE symbol='{stock}'"
        self.action(output=False)

    def insertOneRecord(self, data):
        """新增股票每日基础数据"""
        self.word = f"INSERT ignore INTO No{str(data['ts_code']).split('.')[0]} " \
                    f"(date,open,close,preClose,high,low,pctChange,volume,amount) VALUES " \
                    f"('{data['trade_date']}',{data['open']},{data['close']},{data['pre_close']}," \
                    f"{data['high']},{data['low']},{data['pct_chg']},{data['vol']},{data['amount']})"
        self.action(output=False)

    def insertIndex(self, data, indexTable='NoShIndex'):
        """新增指数每日基础数据"""
        self.word = f"INSERT ignore INTO {indexTable} " \
                    f"(date,open,close,preClose,high,low,pctChange,volume,amount) VALUES " \
                    f"('{data['trade_date']}',{data['open']},{data['close']},{data['pre_close']}," \
                    f"{data['high']},{data['low']},{data['pct_chg']},{data['vol']},{data['amount']})"
        self.action(output=False)

    def selectIndustryByStock(self, stock: str):
        """获取某股票对应的行业"""
        self.word = f"SELECT industry FROM stockList WHERE symbol='{stock}'"
        industry = self.action(output=True)
        return industry[0][0]

    def selectAllIndustry(self):
        """选取所有行业分类"""
        self.word = f"SELECT industry FROM stockList"
        industries = self.action(output=True)
        return list(set([_[0] for _ in industries]))

    def selectStockByIndustry(self, industry: str):
        """选取同一行业的所有股票"""
        self.word = f"SELECT symbol FROM stockList WHERE industry='{industry}'"
        stocks = self.action(output=True)
        return [_[0] for _ in stocks]

    def selectStockDetail(self, stock: str):
        """获取股票资料"""
        self.word = f"SELECT * FROM stockList WHERE symbol={stock}"
        detail = self.action(output=True)
        return detail[0]

    def selectOneAllData(self, stock, dateRange=None, aimDate=''):
        """获取给定时间范围内的股票每日所有数据"""
        if aimDate == '':
            self.word = f"SELECT * FROM No{stock}"
        else:
            if dateRange is None:
                self.word = f"(SELECT * FROM No{stock} WHERE id <= (SELECT id FROM No{stock} WHERE date={aimDate}) " \
                            f"ORDER BY id DESC) " \
                            f"ORDER BY id"
            else:
                self.word = f"(SELECT * FROM No{stock} WHERE id <= (SELECT id FROM No{stock} WHERE date={aimDate}) " \
                            f"ORDER BY id DESC LIMIT {dateRange}) " \
                            f"ORDER BY id"
        data = self.action(output=True)
        return data

    def selectShIndexUpdateDate(self):
        """获取指数更新日期"""
        self.word = f"SELECT date FROM NoshIndex ORDER BY id DESC LIMIT 1"
        data = self.action(output=True)
        return data[0][0]

    def selectDetailUpdateDate(self):
        """获取股票详情更新日期"""
        self.word = 'SELECT stockDetailUpdateDate FROM version'
        date = self.action(output=True)
        return date[0][0]

    def selectListUpdateDate(self):
        """获取股票列表更新日期"""
        self.word = 'SELECT stockListUpdateDate FROM version'
        date = self.action(output=True)
        return date[0][0]

    def stockDetailUpdateDate(self, date):
        """更新股票详情更新日期"""
        self.word = f"UPDATE version SET stockDetailUpdateDate='{date}'"
        self.action(output=False)

    def stockListUpdateDate(self, date):
        """更新股票列表更新日期"""
        self.word = f"UPDATE version SET stockListUpdateDate='{date}'"
        self.action(output=False)

    def updateLimitDetailData(self, data):
        """单独更新股票涨停详情"""
        firstTime = data['first_time']
        lastTime = data['last_time']
        new_firstTime = f'{0 if len(firstTime[:-4]) == 1 else ""}{firstTime[:-4]}:{firstTime[-4:-2]}:{firstTime[-2:]}' if firstTime != '' else '09:25:00'
        new_lastTime = f'{0 if len(lastTime[:-4]) == 1 else ""}{lastTime[:-4]}:{lastTime[-4:-2]}:{lastTime[-2:]}' if lastTime != '' else None
        self.word = f"UPDATE No{str(data['ts_code']).split('.')[0]} SET " \
                    f"firstLimitTime = {dateHandler.joinTimeToStamp(data['trade_date'], new_firstTime)}," \
                    f"lastLimitTime = {6666666666 if new_lastTime is None else dateHandler.joinTimeToStamp(data['trade_date'], new_lastTime)}," \
                    f"openTime = {data['open_times']} " \
                    f"WHERE date = '{data['trade_date']}'"
        self.action(output=False)

    def updateStockListDailyIndex(self, data):
        """单独更新换手率"""
        if data['circ_mv'] is None or '':
            return
        if data['turnover_rate'] is None or '':
            return
        self.word = f"UPDATE stockList SET amount={data['circ_mv']} WHERE symbol={str(data['ts_code']).split('.')[0]}"
        self.action(output=False)
        self.word = f'UPDATE No{str(data["ts_code"]).split(".")[0]} SET turnover={data["turnover_rate"]} WHERE date={data["trade_date"]}'
        self.action(output=False)

    def updateMoneyFlow(self, data):
        """单独更新资金流向"""
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
        """单独更新筹码图"""
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
        """更新分时交易数据"""
        self.word = f"UPDATE No{json['symbol']} SET time='{json['data']}' WHERE date='{json['date']}'"
        self.action(output=False)
