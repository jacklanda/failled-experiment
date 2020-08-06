# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
import json

import jieba
import joblib
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from gensim.models import word2vec
from sklearn.model_selection import train_test_split

def main(li):
    pos, neg, neu = read_file()
    pos_neg_neu, pos_, neg_, neu_ = cut_word(pos, neg, neu)
    table = make_tag(pos_, neg_, neu_)
    #切分训练数据集
    x_train, x_test, y_train, y_test = train_test_split(pos_neg_neu, table, test_size=0.2)
    #print(x_train[0])
    #训练数据集
    train_model = model(x_train,'./metadata/model/train_model.model')
    test_model = model(x_test,'./metadata/model/test_model.model')
    #计算每句话的词向量
    train_vec, test_vec = get_train_vec(x_train, x_test, train_model, test_model)
    print('\n', x_train.shape, train_vec.shape)
    #训练模型
    svm_tran(train_vec, y_train, test_vec, y_test)
    #开始情感分析
    for each in li:
        with open(f'./metadata/raw_txt/{each}.txt', mode='r+', encoding='utf-8') as f:
            for line in f:
                svm_predict(line, train_model, each)

#训练模型
def model(data, model_path):
    model = word2vec.Word2Vec(data, sg=0, hs=1, min_count=1, window=5, size=300)
    model.save(model_path)
    return model

#计算每句话的词向量
def get_train_vec(x_train, x_test, train_model, test_model):
    train_vec = np.concatenate([get_line_vec(300, sent, train_model) for sent in x_train])
    test_vec = np.concatenate([get_line_vec(300, sent, test_model) for sent in x_test])
    #保存数据
    np.save('./metadata/vec_data/train_vec.npy', train_vec)
    np.save('./metadata/vec_data/test_vec.npy', test_vec)
    return train_vec, test_vec

#计算词向量
def get_line_vec(size, sent, model):
    vec = np.zeros(size).reshape(1, size)
    count = 0
    for word in sent:
        try:
            vec += model[word].reshape(1, size)
            count += 1
        except:
            continue
    if count != 0:
        vec /= count
    return vec

#训练SVM模型
def svm_tran(train_vec, y_train, test_vec, y_test):
    clf = SVC(kernel='rbf', verbose=True)  # 创建分类器对象
    print(y_train)
    clf.fit(train_vec, y_train)  # 用训练数据拟合分类器模型
    #持久化保存模型
    joblib.dump(clf, './metadata/model/svm_model.pkl', compress=3)
    print(clf.score(test_vec, y_test))

#读入数据
def read_file():
    pos = pd.read_table('./metadata/diff_data/pos.csv', header=None, index_col=None)
    neg = pd.read_table('./metadata/diff_data/neg.csv', header=None, index_col=None)
    neu = pd.read_table('./metadata/diff_data/neu.txt', header=None, index_col=None)
    return pos, neg, neu

#构造对应的标签数组
def make_tag(pos, neg, neu):
    table = np.append((np.ones(len(pos))), (np.zeros(len(neg))), axis=0)
    table = np.append(table, np.full(len(neu), fill_value=2), axis=0)
    print(table)
    return table

#对每个句子进行情感分析
def svm_predict(line, model, typ):
    #model = word2vec.Word2Vec.load('./metadata/model/train_model.model')
    clf = joblib.load('./metadata/model/svm_model.pkl')
    line_cut = jieba.lcut(line)
    line_cut_vec = get_line_vec(300, line_cut, model)
    result = clf.predict(line_cut_vec)
    #print(result)
    sentiment = 'None'
    if int(result[0] == 1):
        sentiment = 'positive'
        print('情感分析结果：积极')
    elif int(result[0] == 0):
        sentiment = 'negative'
        print('情感分析结果：消极')
    else:
        sentiment = 'neutral'
        print('情感分析结果：中性')
    with open(f'./metadata/result/result_{typ}.json', 'a+', encoding='utf-8') as f:
        cont = json.dumps({'tag': typ, 'sentiment': sentiment})
        f.write(f'{cont}\n')

#结巴分词
def cut_word(pos, neg, neu):
    pos['cut_word'] = [jieba.lcut(sent) for sent in pos[0]]
    neg['cut_word'] = [jieba.lcut(sent) for sent in neg[0]]
    neu['cut_word'] = [jieba.lcut(sent) for sent in neu[0]]
    #print(pos['c_w'])
    #print('-----------------------------------')
    #print(neg['c_w'])
    #print('------------------------------------')
    #print(neu['c_w'])
    merge_array = numpy_merge(pos['cut_word'], neg['cut_word'], neu['cut_word'])
    return merge_array, pos['cut_word'], neg['cut_word'], neu['cut_word']

#合并neg、pos和neu
def numpy_merge(pos_, neg_, neu_):
    pos_neg = np.append(pos_, neg_, axis=0)
    pos_neg = np.append(pos_neg, neu_, axis=0)
    return pos_neg

#切分训练集合测试集
def train():
    x_train, x_test, y_train, y_test = train_test_split(pos_and_neg, table, test_size=0.2)
    return x_train, x_test, y_train, y_test

#保存数据
def save_data(doc_path, data):
    np.save(doc_path, data)
