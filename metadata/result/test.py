# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
import json

with open('./result_bilibili.txt', mode='r+', encoding='utf-8') as f:
    for line in f:
        line = line.json()
        print(line['sentiment'])
