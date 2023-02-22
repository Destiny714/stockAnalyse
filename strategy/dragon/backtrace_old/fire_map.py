# -*- coding: utf-8 -*-
# @Time    : 2023/2/13 22:33
# @Author  : Destiny_
# @File    : fire_map.py
# @Software: PyCharm

from matplotlib import pyplot as plt
from utils.date_util import allTradeDay, prevTradeDay, lastTradeDay
from utils.excel_util import readExcel_white, readExcel_AS

if __name__ == '__main__':
    rule_map = {}
    tradeDays: list[str] = allTradeDay()
    for today in tradeDays:
        if today.startswith('2023') and today <= lastTradeDay():
            prev_day = prevTradeDay(today)
            now_data = readExcel_AS(today, hide=False)
            prev_data = readExcel_white(prev_day)
            for d in now_data:
                if int(d['height']) == 1:
                    rule_data = prev_data[d['code']]
                    if type(rule_data) is not str:
                        continue
                    details: dict = eval(rule_data)
                    for level in details:
                        if 'F' in level:
                            continue
                        level_rule: list = details[level]
                        for rule in level_rule:
                            key = f'{level}-{rule}'
                            if key in rule_map:
                                rule_map[key] += 1
                            else:
                                rule_map[key] = 1

    plt.figure(figsize=(100, 20))
    for _ in rule_map:
        plt.bar(_,rule_map[_])
    plt.title = "fire map"
    plt.xlabel = 'rule'
    plt.ylabel = 'time'
    plt.xticks([_ for _ in rule_map], [_ for _ in rule_map], rotation=45)
    ax = plt.gca()
    ax.set_title(f'fire map')
    plt.grid(alpha=0.4)
    plt.legend(loc=2)
    plt.show()