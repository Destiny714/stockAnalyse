# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 19:20
# @Author  : Destiny_
# @File    : db.py
# @Software: PyCharm

import pymysql
from api import config
from json import dumps
from utils import date_util


class MysqlConnection:
    def __init__(self, database: str):
        self.__account__ = config['mysqlAccount']
        self.__pswd__ = config['mysqlPassword']
        self.__DB__ = database
        self.host = config['mysqlHost']
        self.word = ''
        self.conn = pymysql.connect(host=self.host, port=3306, user=self.__account__, password=self.__pswd__, database=self.__DB__,
                                    connect_timeout=30,
                                    write_timeout=30,
                                    read_timeout=30)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn.open:
            self.cursor.close()
            self.conn.close()

    def action(self, output: bool):
        """mysql语句执行基础单元"""
        self.cursor.execute(self.word)
        if output:
            callback = self.cursor.fetchall()
            return callback
        else:
            self.conn.commit()


class Server_Database(MysqlConnection):
    __DB__ = config['serverDatabase']

    def __init__(self):
        super().__init__(self.__DB__)

    def insertDailyRankDetail(self, data):
        date = data['date']
        code = data['code']
        rank = data['level']
        name = data['name']
        white = data['white']
        black = data['black']
        score = data['score']
        height = data['height']
        detail = dumps(eval(data['details']))
        fastDetail = dumps(eval(data['T1S_detail']))
        slowDetail = dumps(eval(data['T1F_detail']))
        day2elg = data['day2elg']
        day3elg = data['day3elg']
        fastBlackNum = data['b1']
        slowBlackNum = data['b2']
        comparePrevScore = data['S']
        index = f'{date}-{code}'
        self.word = f"""
                    INSERT ignore INTO rank_detail
                    (index_key,date,stock_code,stock_name,stock_rank,limitHeight,
                    whiteNum,blackNum,fastBlackNum,slowBlackNum,score,day2elg,day3elg,
                    comparePrevScore,detail,fastDetail,slowDetail) VALUES 
                    ("{index}","{date}","{code}","{name}","{rank}",{height},
                    {white},{black},{fastBlackNum},{slowBlackNum},{score},{day2elg},{day3elg},{comparePrevScore},
                    '{detail}','{fastDetail}','{slowDetail}') 
                    ON DUPLICATE KEY UPDATE 
                    stock_rank="{rank}",whiteNum={white},blackNum={black},
                    fastBlackNum={fastBlackNum},slowBlackNum={slowBlackNum},
                    score={score},day2elg={day2elg},day3elg={day3elg},
                    comparePrevScore={comparePrevScore},detail='{detail}',fastDetail='{fastDetail}',slowDetail='{slowDetail}'
                    """
        self.action(output=False)


class Stock_Database(MysqlConnection):
    __DB__ = config['stockDatabase']

    def __init__(self):

        super().__init__(self.__DB__)

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

    def selectAllStockWithSuffix(self):
        self.word = "SELECT symbol,exchange FROM stockList"
        data = self.action(output=True)
        return [f'{_[0]}.{"SZ" if _[1] == "SZSE" else "SH"}' for _ in data]

    def selectAllStockDetail(self):
        """查找所有股票详情"""
        self.word = "SELECT * FROM stockList"
        data = self.action(output=True)
        return data

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

    def selectTradeDateRange(self, start, end):
        """返回start to end 的一段日期list"""
        self.word = f'SELECT date FROM tradeCalender WHERE (date <= {end} AND date >= {start})'
        data = self.action(output=True)
        return [_[0] for _ in data]

    def selectTradeDateByDuration(self, date, duration: int):
        """选取指定date往前推『duration』日的日期范围"""
        self.word = f"(SELECT id,date FROM tradeCalender WHERE id <= (SELECT id FROM tradeCalender WHERE date={date}) " \
                    f"ORDER BY id DESC LIMIT {duration}) " \
                    f"ORDER BY id"
        result = self.action(output=True)
        return [_[1] for _ in result]

    def selectPrevTradeDate(self, date):
        """选取上一个交易日"""
        self.word = f"SELECT lastDate FROM tradeCalender where date='{date}'"
        data = self.action(output=True)
        return data[0][0]

    def selectNextTradeDay(self, date):
        """选取下一个交易日"""
        self.word = f"SELECT date FROM tradeCalender WHERE id > (SELECT id FROM tradeCalender WHERE date='{date}') LIMIT 1"
        data = self.action(output=True)
        return data[0][0]

    def selectNextXTradeDay(self, date, x: int = 1):
        """选取下X个交易日"""
        assert x >= 0, '下X个交易日 ==> X > 0'
        self.word = f"SELECT date FROM tradeCalender WHERE id >= (SELECT id FROM tradeCalender WHERE date='{date}') LIMIT {x + 1}"
        data = self.action(output=True)
        return data[-1][0]

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
        """从股票详情表中删除给定股票详情"""
        self.word = f"DELETE FROM stockList WHERE symbol='{stock}'"
        self.action(output=False)

    def insertOneDailyBasicRecord(self, data):
        """新增股票每日基础数据"""
        low_qfq = data['low_qfq']
        high_qfq = data['high_qfq']
        open_qfq = data['open_qfq']
        close_qfq = data['close_qfq']
        pct_change = data['pct_change']
        pre_close_qfq = data['pre_close_qfq']
        self.word = f"INSERT ignore INTO No{str(data['ts_code']).split('.')[0]} " \
                    f"(date,open,close,preClose,high,low,pctChange,volume,amount) VALUES " \
                    f"('{data['trade_date']}',{open_qfq},{close_qfq},{pre_close_qfq}," \
                    f"{high_qfq},{low_qfq},{pct_change},{data['vol']},{data['amount']}) " \
                    f"ON DUPLICATE KEY UPDATE " \
                    f"open={open_qfq},close={close_qfq},low={low_qfq}," \
                    f"high={high_qfq},preClose={pre_close_qfq},pctChange={pct_change}"
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

    def selectNameByStock(self, stock: str):
        """获取某股票对应的名称"""
        self.word = f"SELECT name FROM stockList WHERE symbol='{stock}'"
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

    def selectOneAllData(self, stock, dateRange=None, aimDate='', after=False):
        """获取给定时间范围内的股票每日所有数据"""
        flag = '-' if not after else ''
        symbol = '<=' if not after else '>='
        if aimDate == '':
            self.word = f"SELECT * FROM No{stock}"
        else:
            if dateRange is None:
                self.word = f"(SELECT * FROM No{stock} WHERE id <= (SELECT id FROM No{stock} WHERE date={aimDate}) " \
                            f"ORDER BY id DESC) " \
                            f"ORDER BY id"
            else:
                self.word = f"(SELECT * FROM No{stock} WHERE id {symbol} (SELECT id FROM No{stock} WHERE date={aimDate}) " \
                            f"ORDER BY {flag}id LIMIT {dateRange}) " \
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
        self.word = f"UPDATE version SET stockDetailUpdateDate='{date}' WHERE 1/1 = 1"
        self.action(output=False)

    def stockListUpdateDate(self, date):
        """更新股票列表更新日期"""
        self.word = f"UPDATE version SET stockListUpdateDate='{date}' WHERE 1/1 = 1"
        self.action(output=False)

    def updateLimitDetailData(self, data):
        """单独更新股票涨停详情"""
        firstTime = data['first_time']
        lastTime = data['last_time']
        new_firstTime = f'{0 if len(firstTime[:-4]) == 1 else ""}{firstTime[:-4]}:{firstTime[-4:-2]}:{firstTime[-2:]}' if firstTime != '' else '09:25:00'
        new_lastTime = f'{0 if len(lastTime[:-4]) == 1 else ""}{lastTime[:-4]}:{lastTime[-4:-2]}:{lastTime[-2:]}' if lastTime != '' else None
        self.word = f"UPDATE No{str(data['ts_code']).split('.')[0]} SET " \
                    f"firstLimitTime = {date_util.joinTimeToStamp(data['trade_date'], new_firstTime)}," \
                    f"lastLimitTime = {6666666666 if new_lastTime is None else date_util.joinTimeToStamp(data['trade_date'], new_lastTime)}," \
                    f"openTime = {data['open_times']} " \
                    f"WHERE date = '{data['trade_date']}'"
        self.action(output=False)

    def updateTurnover(self, data):
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
        date = json['date']
        data = json["data"]
        symbol = json['symbol']
        self.word = f"UPDATE No{symbol} SET time='{dumps(data)}' WHERE date='{date}'"
        self.action(output=False)

    def insertOneLimitStock(self, data):
        """将每日涨停股票详情插入 -stockLimit表- """
        firstTime = data['first_time']
        lastTime = data['last_time']
        new_firstTime = f'{0 if len(firstTime[:-4]) == 1 else ""}{firstTime[:-4]}:{firstTime[-4:-2]}:{firstTime[-2:]}' if firstTime != '' else '09:25:00'
        new_lastTime = f'{0 if len(lastTime[:-4]) == 1 else ""}{lastTime[:-4]}:{lastTime[-4:-2]}:{lastTime[-2:]}' if lastTime != '' else None
        date = data['trade_date']
        stockNo = str(data['ts_code']).split('.')[0]
        self.word = f"INSERT IGNORE INTO stockLimit " \
                    f"(trade_date, ts_code, industry, open, close, pre_close, pct_chg,amount, " \
                    f"turnover, fd_amount, first_time, last_time, open_times, up_stat, limit_times) VALUES " \
                    f"('{date}'," \
                    f"'{stockNo}'," \
                    f"(SELECT industry FROM stockList where symbol={stockNo})," \
                    f"(SELECT open FROM No{stockNo} WHERE date = {date})," \
                    f"{data['close']}," \
                    f"(SELECT preClose FROM No{stockNo} WHERE date = {date})," \
                    f"{data['pct_chg']}," \
                    f"{data['amount']}," \
                    f"{data['turnover_ratio']}," \
                    f"{data['fd_amount']}," \
                    f"{date_util.joinTimeToStamp(date, new_firstTime)}," \
                    f"{6666666666 if new_lastTime is None else date_util.joinTimeToStamp(date, new_lastTime)}," \
                    f"{data['open_times']}," \
                    f"'{data['up_stat']}'," \
                    f"{data['limit_times']}) ON DUPLICATE KEY UPDATE " \
                    f"open=(SELECT open FROM No{stockNo} WHERE date = {date})," \
                    f"pre_close=(SELECT preClose FROM No{stockNo} WHERE date = {date})"
        self.action(output=False)

    def selectLimitStockByDateRange(self, dates: list[str]):
        """根据日期查找 stockLimit 表"""
        self.word = f"SELECT * FROM stockLimit WHERE trade_date in ({','.join(dates)})"
        return self.action(output=True)
