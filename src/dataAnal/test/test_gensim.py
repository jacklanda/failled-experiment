# -*- coding: UTF-8 -*-
# -*- Author: Jacklanda
from gensim.models import word2vec

def main():
    num_features = 100    # Word vector dimensionality
    min_word_count = 10   # Minimum word count
    num_workers = 16       # Number of threads to run in parallel
    context = 10          # Context window size
    downsampling = 1e-3   # Downsample setting for frequent words
    sentences = word2vec.Text8Corpus("./seg2.txt")
    model = word2vec.Word2Vec(sentences, workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sg = 1, sample = downsampling)
    model.init_sims(replace=True)
    # 保存模型，供日後使用
    model.save("model_test.model")
    # model = gensim.models.Word2Vec.load('/tmp/mymodel')
    # model.train(more_sentences)

if __name__ == "__main__":
    main()

