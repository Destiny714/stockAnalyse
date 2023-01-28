# -*- coding: utf-8 -*-
# @Time    : 2023/1/23 14:26
# @Author  : Destiny_
# @File    : plot.py
# @Software: PyCharm

from matplotlib import pyplot as plt

from utils.file_util import projectPath

if __name__ == '__main__':
    swing_limit = 6
    with open(f'{projectPath()}/strategy/model_N/n_backtrace_swing{swing_limit}.txt', 'r') as f:
        lines = f.readlines()
        hashMap = {}
        for line in [_ for _ in lines if (_ != '\n' and '--' not in _)]:
            res = line
            details = res.split('-')
            date = details[0]
            code = details[1]
            profit = float(details[2].replace('%', ''))
            if date not in hashMap:
                hashMap[date] = [profit]
            else:
                hashMap[date].append(profit)
        all_profits = []
        for key in hashMap:
            all_profits.extend(hashMap[key])
        avg_profit = round(sum(all_profits)/len(all_profits),2)
        plt.figure(figsize=(100, 20))
        x = [_ for _ in hashMap]
        y = [round(sum(hashMap[_]) / len(hashMap[_]), 2) for _ in x]
        plt.title = "profit backtrace"
        plt.xlabel = 'date'
        plt.ylabel = 'avg profit/%'
        plt.plot(x, y, label=f"swing limit {swing_limit}%", color="red")
        plt.xticks(list(x)[::1], x[::1], rotation=45)
        ax = plt.gca()
        ax.set_title(f'avg daily profit {avg_profit}%')
        ax.set_xticks(ax.get_xticks()[::9])
        plt.grid(alpha=0.4)
        plt.legend(loc=2)
        plt.show()
