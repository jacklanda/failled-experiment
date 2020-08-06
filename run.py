# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
'''
程序入口
'''
import sys, os
from src import main

if __name__ == '__main__':
    try:
        os.mkdir('./metadata')
    except:
        print('@该目录已存在，将默认使用之')
    main.experiment()
    sys.exit(0)
