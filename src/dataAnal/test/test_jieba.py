# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
import jieba

import io, re

# 加载自己的自己的词库
jieba.load_userdict("./stopword.txt")

def main():
    with io.open('./Pos-train.txt','r',encoding='utf-8') as content:
        for line in content:
            seg_list = jieba.cut(line)
            # print('/'.join(seg_list))
            with io.open('./seg2.txt', 'a+', encoding='utf-8') as output:
                line_word = ' '. join(seg_list)
                content = re.findall('[\u4e00-\u9fa5]+', line_word)
                print(content)
                output.write(' '.join(content))

if __name__ == '__main__':
    main()


