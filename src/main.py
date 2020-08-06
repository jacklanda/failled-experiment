# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
from time import time
from random import randint

from src.crawler import zhihu, weibo, bilibili, config
from src.dataAnal import data_exec, data_anal, data_visual, data_cleanse, wd

class experiment(object):

    def __init__(self):
        self.welcome()
        self.crawl()
        self.analyse()
        self.visual()

    def welcome(self):
        Reset = "\033[0m"
        cor = ["\033[1;33m", "\033[1;34m", "\033[1;30m", "\033[1;36m", "\033[1;31m", "\033[35m", "\033[95m", "\033[96m", "\033[39m",                                                "\033[38;5;82m", "\033[38;5;198m", "\033[38;5;208m", "\033[38;5;167m","\033[38;5;91m", "\033[38;5;210m", "\033[38;5;165m", "\033[38;5;49m", "\033[38;5;160m", "\033[38;5;51m", "\033[38;5;13m", "\033[38;5;162m", "\033[38;5;203m", "\033[38;5;113m", "\033[38;5;14m"]
        colors = cor[randint(0, 15)]
        print(colors + '''
                        _
          __      _____| | ___ ___  _ __ ___   ___
          \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ |
           \ V  V /  __/ | (_| (_) | | | | | |  __/
            \_/\_/ \___|_|\___\___/|_| |_| |_|\___|

              __  __          _____     _                _
             |  \/  |_   _   |  ___| __(_) ___ _ __   __| |
             | |\/| | | | |  | |_ | '__| |/ _ \ '_ \ / _` |
             | |  | | |_| |  |  _|| |  | |  __/ | | | (_| |
             |_|  |_|\__, |  |_|  |_|  |_|\___|_| |_|\__,_|
                     |___/
        ''')

    def crawl(self):
        print('****************************数据爬取中，请稍后****************************')
        # 暂未设置可传入存储参数选项
        zhihu.crawler_zhihu()
        print('###############知乎数据爬取完毕###############')
        bilibili.crawler_bilibili()
        print('###############B站数据爬取完毕###############')
        username = input('请输入你的微博用户名：')
        password = input('请输入你的微博密码：')
        cookie_path = config.addr('weibo_cookie')
        weibo.Weibo(username, password, cookie_path).run_()
        print('###############微博数据爬取完毕###############')

    def analyse(self):
        start_time = time()
        print('\n***************************数据预处理中，请稍后***************************')
        data_exec.make_stopwd(['zhihu', 'bilibili' ,'weibo'])
        data_cleanse.make_corpus()
        #mes = data_exec.make_vector()
        #if mes == True:
            #print('词向量生成完毕')
            #end_time = time()
            #print(f'构建词向量耗时：{end_time-start_time}秒')
        #else:
            #print('词向量文件已存在，直接采用之')
        data_anal.main(['zhihu', 'weibo', 'bilibili'])
        print('###############数据预处理完毕###############\n')

    def visual(self):
        data_visual.run_(['zhihu', 'bilibili', 'weibo'])
        wd.generate_cloud(['zhihu', 'bilibili', 'weibo'])

