# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
import re, sys, csv, time, json
from multiprocessing.dummy import Pool
sys.path.append('..')

import requests
import pandas as pd

from src.database import db
from src.crawler import config

# 设置User-Agent请求头
HEADERS = config.head('bilibili')
url_head = config.URL('bilibili')

def crawler_bilibili():
    thread_pool()

def thread_pool():
    url_li = []
    num_pages = req_pre()
    url_list(num_pages, url_li)
    pool = Pool(16)
    pool.map(req_html, url_li)
    print('「B站数据已爬取并入库」')

def req_pre():
    contents = json.loads(requests.get(url_head+'&pn=0').content.decode())
    data_ = contents['data']['page']
    count = data_['count']
    size = data_['size']
    num_pages = count//size
    return num_pages

def url_list(num_pages, url_li):
    for i in range(num_pages):
        url = url_head + '&pn={}'.format(i)
        url_li.append(url)
    return url_li

def req_html(each_url):
    content_ =  requests.get(each_url, headers=HEADERS)
    data_handle(content_)

def data_handle(content):
    obj = content.json()
    # print(len(obj['data']['replies']))
    for each in range(len(obj['data']['replies'])):
        data_1 = [(obj['data']['replies'][each]['member']['uname'],
            obj['data']['replies'][each]['content']['message'])]
        data_2 = []
        if obj['data']['replies'][each]['replies'] != None:
            for every in range(len(obj['data']['replies'][each]['replies'])):
                data_2.append((obj['data']['replies'][each]['replies'][every]['content']['message']))
        else:
            data_2 = []
        data = data_1 + data_2
        data_store(data)
        store_csv(data)

def data_store(data):
    try:
        client = db.client()
        database_ = client['data_experiment']
        col = database_['bilibili']
    except:
        print('MongoDB未启动！')
    for each in data:
        if(each and len(each)>1):
            content = re.findall('[\u4e00-\u9fa5]+', each[1])
            content = ''.join(content)
            dic = {
                    'user': each[0],
                    'content': content
                    }
        else:
            dic = {
                    'user': 'At_Last',
                    'content': None
                    }
        col.insert_one(dic, col)
        store_txt(dic['content'])

def store_csv(data):
    datas = pd.DataFrame(data)
    datas.to_csv('./metadata/B站评论.csv', header=False, index=False, mode='w+')

# 将数据写入到.txt文件中
def store_txt(data):
    with open('./metadata/raw_txt/bilibili.txt', mode='w+', encoding='utf-8') as f:
        f.write(f'{data}\n')


if __name__ == '__main__':
    crawler_bilibili()
