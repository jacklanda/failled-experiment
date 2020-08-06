# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
import re, json

def make_corpus():
    with open('./metadata/corpus/corpus_execed.txt', mode='w+', encoding='utf-8') as write_f:
        with open('./metadata/corpus/corpus_news.json', mode='r', encoding='utf-8') as read_f:
            i = 0
            for line in read_f:
                if i < 3000:
                    line = json.loads(line)
                    content = re.findall('[\u4e00-\u9fa5]+', line['content'])
                    content = ''.join(content)
                    write_f.write(f'{content}\n')
                    i += 1


