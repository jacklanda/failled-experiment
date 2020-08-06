# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
import io, os, re

import jieba
from gensim.models import word2vec

def make_stopwd(typ_li):
    tip_1 = os.path.exists('./metadata/execed_txt/zhihu_execed.txt')
    tip_2 = os.path.exists('./metadata/execed_txt/bilibili_execed.txt')
    tip_3 = os.path.exists('./metadata/execed_txt/weibo_execed.txt')
    if tip_1 and tip_2 and tip_3:
        print('测试集的分词文件已存在，默认使用之')
        pass
    elif typ_li[0] == 'corpus':
        jieba.load_userdict('./metadata/stopword.txt')
        typ = 'corpus'
        with io.open(f'./metadata/corpus/corpus_exe.txt', 'r', encoding='utf-8') as f:
            for line in f:
                seg_list = jieba.cut(line)
                with io.open(f'./metadata/corpus/{typ}_execed.txt', 'w+', encoding='utf-8') as output:
                    line_word = ' '.join(seg_list)                        #print(line_word)
                    output.write(line_word)
    else:
        jieba.load_userdict('./metadata/stopword.txt')
        for typ in typ_li:
            with io.open(f'./metadata/raw_txt/{typ}.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    seg_list = jieba.cut(line)
                    with io.open(f'./metadata/execed_txt/{typ}_execed.txt', 'w+', encoding='utf-8') as output:
                        line_word = ' '.join(seg_list)
                        #print(line_word)
                        output.write(line_word)

def make_vector():
    judge_file = os.path.exists('./metadata/model/model_news.model')
    if judge_file == False:
        num_features = 100    # 每个词的向量维度
        min_word_count = 10   # 文本中一个词出现的最低频率，若小于5，则会被丢弃
        num_workers = 4       # 启动训练的进程个数，通常为机器的核心数
        context = 10          # 训练词向量时，上下文扫描窗口的大小
        downsampling = 1e-3   # 为高频词设置
        sentences = word2vec.Text8Corpus('./metadata/corpus/corpus_execed.txt')  # 一句话即为文本中的一行
        model = word2vec.Word2Vec(sentences, workers=num_workers, \
                size=num_features, min_count = min_word_count, \
                window = context, sg = 1, sample = downsampling)
        model.init_sims(replace=True)
        # 保存模型
        model.save('./metadata/model/model_news.model')
        # model = gensim.models.Word2Vec.load('/tmp/mymodel')
        # model.train(more_sentences)
        return True
    else:
        return False


if __name__ == '__main__':
    typ = input('请输入待测试的源数据文件名：')
    make_stopwd(typ)
    print('分词成功')
