# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
import json

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pylab import *
import pandas as pd

font_size =15 # 字体大小

def run_(li):
    sum_zhihu = []
    sum_bilibili = []
    sum_weibo = []
    for each in li:
        pos = 0
        neg = 0
        neu = 0
        with open(f'./metadata/result/result_{each}.json', 'r+', encoding='utf-8') as f:
            for line in f:
                data_ = json.loads(line)
                senti = data_['sentiment']
                if senti == 'positive':
                    pos += 1
                elif senti == 'negative':
                    neg += 1
                else:
                    neu += 1
        if each == 'zhihu':
            sum_zhihu.append(pos)
            sum_zhihu.append(neg)
            sum_zhihu.append(neu)
        elif each == 'bilibili':
            sum_bilibili.append(pos)
            sum_bilibili.append(neg)
            sum_bilibili.append(neu)
        else:
            sum_weibo.append(pos)
            sum_weibo.append(neg)
            sum_weibo.append(neu)
        data = [pos, neg, neu]
        labels = ['positive', 'negative', 'neutral']
        col = ['green', 'red', 'yellow']
        plt.axis('equal')
        explode = (0, 0, 0)
        print(data)
        plt.cla()
        plt.pie(data, labels=labels, autopct='%1.1f%%', colors=col, explode=explode)
        plt.title(f'{each} pie chart')
        plt.savefig(f'./metadata/img/{each}.png')
    bar_chart(sum_zhihu, sum_bilibili, sum_weibo)

def bar_chart(zhihu, bilibili, weibo):
    num_list_1 = [zhihu[0], bilibili[0], weibo[0]]
    num_list_2 = [zhihu[1], bilibili[1], weibo[1]]
    num_list_3 = [zhihu[2], bilibili[2], weibo[2]]
    print(num_list_1)
    print(num_list_2)
    print(num_list_3)
    n_groups = 3
    plt.ylim(8000)
    plt.cla()
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 1
    error_config = {'ecolor': '0.3'}

    rects_1 = ax.bar(index, num_list_1, bar_width,
                alpha=opacity, color='green',
                error_kw=error_config,
                label='positive')

    rects_2 = ax.bar(index + bar_width, num_list_2, bar_width,
                alpha=opacity, color='red',
                error_kw=error_config,
                label='negative')

    rects_3 = ax.bar(index + bar_width, num_list_3, bar_width,
                alpha=opacity, color='yellow',
                error_kw=error_config,
                label='neutral')
    ax.set_xlabel('social media')
    ax.set_ylabel('scores')
    ax.set_title('bar chart')
    ax.set_xticks(index + bar_width/3)
    ax.set_xticklabels(('zhihu', 'bilibili', 'weibo'))
    ax.legend()
    fig.tight_layout()
    plt.savefig('./metadata/img/bar_chart.png')
    plt.cla()
