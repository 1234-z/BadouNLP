#!/usr/bin/env python3  
#coding: utf-8

#基于训练好的词向量模型进行聚类
#聚类采用Kmeans算法
import math
import re
import json
import jieba
import numpy as np
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from collections import defaultdict

#输入模型文件路径
#加载训练好的模型
def load_word2vec_model(path):
    model = Word2Vec.load(path)
    return model

def load_sentence(path):
    sentences = set()
    with open(path, encoding="utf8") as f:
        for line in f:
            sentence = line.strip()
            sentences.add(" ".join(jieba.cut(sentence)))
    print("获取句子数量：", len(sentences))
    return sentences

#将文本向量化
def sentences_to_vectors(sentences, model):
    vectors = []
    for sentence in sentences:
        words = sentence.split()  #sentence是分好词的，空格分开
        vector = np.zeros(model.vector_size)
        #所有词的向量相加求平均，作为句子向量
        for word in words:
            try:
                vector += model.wv[word]
            except KeyError:
                #部分词在训练中未出现，用全0向量代替
                vector += np.zeros(model.vector_size)
        vectors.append(vector / len(words))
    return np.array(vectors)


def main():
    model = load_word2vec_model(r"E:\AI\第五周 词向量\week5 词向量及文本向量\model.w2v") #加载词向量模型
    sentences = load_sentence("titles.txt")  #加载所有标题
    vectors = sentences_to_vectors(sentences, model)   #将所有标题向量化

    n_clusters = int(math.sqrt(len(sentences)))  #指定聚类数量
    print("指定聚类数量：", n_clusters)
    kmeans = KMeans(n_clusters)  #定义一个kmeans计算类
    kmeans.fit(vectors)          #进行聚类计算
    # print(kmeans.cluster_centers_)  #每个聚类中心位置 (n_clusters, n_features)
    # print(kmeans.labels_)
    # print(vectors)
    centers = kmeans.cluster_centers_  #聚类中心
    labels = kmeans.labels_            #聚类样本
    intro_distance = []                #类内平均距离
    for i in range(len(centers)):
        point = vectors[labels == i]   #取出每个聚类对应的句子向量
        print(f"第{i+1}类句子向量", point)
        distance = np.linalg.norm(point - centers[i], axis=1) #计算欧氏距离
        intro_distance.append(distance.mean())  #求平均
    print(intro_distance)
    print(f"最小距离：{np.min(intro_distance)}, 所属类：{np.argmax(intro_distance)}")
    print("从小到大排序",sorted(intro_distance))


    sentence_label_dict = defaultdict(list)
    for sentence, label in zip(sentences, kmeans.labels_):  #取出句子和标签
        sentence_label_dict[label].append(sentence)         #同标签的放到一起
    print("最相关类：", sentence_label_dict[np.argmax(intro_distance)])   #最相关句子
    # for label, sentences in sentence_label_dict.items():
    #     print("cluster %s :" % label)
    #     for i in range(min(10, len(sentences))):  #随便打印几个，太多了看不过来
    #         print(sentences[i].replace(" ", ""))
    #     print("---------")

if __name__ == "__main__":
    main()

