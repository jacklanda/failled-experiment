# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
import re, sys, csv, time, json
from multiprocessing.dummy import Pool

import requests

from src.database import db
from src.crawler import config

# 知乎采用最简单的反爬形式：限定User-Agent请求头
HEADERS = config.head('zhihu')
url_zhihu = config.URL('zhihu')

def crawler_zhihu():
    create_csv()
    try:
        res_pre = requests.get(url_zhihu+'&offset=0', headers=HEADERS)
        if res_pre.status_code == 200:
            content_pre = json.loads(res_pre.content.decode())
            total_pages = content_pre['paging']['totals']
            #print(total_pages)
            symbol = int(content_pre['paging']['is_end'])
            num = 0
            summary = 0
            url_li = url_list(num, total_pages)
            thread_pool(url_li)
    except requests.exceptions.RequestException as e:
        print(e)

def thread_pool(url_list):
    pool=Pool(16)
    pool.map(get_html, url_list)

def get_html(each_url):
    res = requests.get(each_url, headers=HEADERS)
    if res.status_code == 200:
        content = json.loads(res.content.decode())['data']
        col = create_col()
        extract_info(content, col)

def extract_info(array, col__):
    for li in array:
        voteup = li['voteup_count']
        content = re.findall('[\u4e00-\u9fa5]+', li['content'])
        content = ''.join(content)
        dic = {
                '获赞数': voteup,
                '回答内容': content
                }
        try:
            db.insert(dic, col__)
        except:
            print('MongoDB客户端未启动！')
        store_csv(dic)
        store_txt(dic['回答内容'])

def create_col():
    client = db.client()
    database_ = client['data_experiment']
    col = database_['zhihu']
    return col

def url_list(num, total_pages):
    url_li = []
    while(num < total_pages):
        url = url_zhihu+'&offset={}'.format(num)
        url_li.append(url)
        num = num + 20
    return url_li

# 创建.csv文件
def create_csv():
    with open('./metadata/知乎回答.csv', mode='w+', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['获赞数', '回答内容'])

# 将数据写入到.csv文件中
def store_csv(data):
    with open('./metadata/知乎回答.csv', mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([data['获赞数'], data['回答内容']])

# 将数据写入到.txt文件中
def store_txt(data):
    with open('./metadata/raw_txt/zhihu.txt', mode='w+', encoding='utf-8') as f:
        f.write(f'{data}\n')

if __name__ == '__main__':
    start_time = time.time()
    crawler_zhihu()
    end_time = time.time()
    print(f'多线程爬取脚本耗时：{end_time-start_time}秒')
