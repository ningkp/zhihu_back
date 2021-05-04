'''
Availabel Methods:
Tfidf (bag of word): sklearn
Doc2Vec: gensim
'''

import random
import os
import sys

import numpy as np
from gensim.models import doc2vec
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import normalize, robust_scale, minmax_scale, maxabs_scale

METHODS = ['Tfidf', 'CountVectorizer', 'Doc2Vec']

__all__ = ['extract_bow',
           'extract_cv',
           'extract_doc2vec',
           ]

file_dir = os.path.join(os.path.dirname(__file__), 'txt_model')


def extract_bow(data, preprocess=None):
    """

    :param data: list
        A list of documents. Each element is a document.
        E.g.,
        data = [
         'This is the first document.',
         'This is the second second document.',
         'And the third one.',
         'Is this the first document?',
         ]
    :param method:
    :param preprocess:
    :return:
    """
    vec = TfidfVectorizer()
    if preprocess:
        assert preprocess in ['normalize', 'robust_scale', 'minmax_scale', 'maxabs_scale'], "preprocess must be one of ['normalize', 'robust_scale', 'minmax_scale', 'maxabs_scale']"
        vec = eval(preprocess + '(vec)')
    else:
        return vec.fit_transform(data).toarray()


def extract_cv(data, preprocess=None):
    """

    :param data: list
        A list of documents. Each element is a document.
        E.g.,
        data = [
         'This is the first document.',
         'This is the second second document.',
         'And the third one.',
         'Is this the first document?',
         ]
    :param method:
    :param preprocess:
    :return:
    """
    vec = CountVectorizer()
    if preprocess:
        assert preprocess in ['normalize', 'robust_scale', 'minmax_scale',
                              'maxabs_scale'], "preprocess must be one of ['normalize', 'robust_scale', 'minmax_scale', 'maxabs_scale']"
        vec = eval(preprocess + '(vec)')
    else:
        return vec.fit_transform(data).toarray()


def train_doc2vec(data):
    d2v = doc2vec.Doc2Vec(min_count=1,  # Ignores all words with total frequency lower than this
                          window=10,  # The maximum distance between the current and predicted word within a sentence
                          vector_size=300,  # Dimensionality of the generated feature vectors
                          workers=5,  # Number of worker threads to train the model
                          alpha=0.025,  # The initial learning rate
                          min_alpha=0.00025,  # Learning rate will linearly drop to min_alpha as training progresses
                          dm=1)  # dm defines the training algorithm. If dm=1 means 'distributed memory' (PV-DM)
    # and dm =0 means 'distributed bag of words' (PV-DBOW)
    d2v.build_vocab(data)

    # 10 epochs take around 10 minutes on my machine (i7), if you have more time/computational power make it 20
    for epoch in range(10):
        d2v.train(data, total_examples=d2v.corpus_count, epochs=d2v.epochs)
        # shuffle the corpus
        random.shuffle(data)
        # decrease the learning rate
        d2v.alpha -= 0.0002
        # fix the learning rate, no decay
        d2v.min_alpha = d2v.alpha

    d2v.save(os.path.join(file_dir, "d2v.model"))
    return d2v


def label_sentences(corpus, label_type):
    """
    Gensim's Doc2Vec implementation requires each document/paragraph to have a label associated with it.
    We do this by using the LabeledSentence method. The format will be "TRAIN_i" or "TEST_i" where "i" is
    a dummy index of the review.
    """
    labeled = []
    for i, v in enumerate(corpus):
        label = label_type + '_' + str(i)
        labeled.append(doc2vec.LabeledSentence(v.split(), [label]))
    return labeled


def get_vectors(doc2vec_model, corpus_size, vectors_type, vectors_size=300):
    """
    Get vectors from trained doc2vec model
    :param doc2vec_model: Trained Doc2Vec model
    :param corpus_size: Size of the data
    :param vectors_size: Size of the embedding vectors
    :param vectors_type: Training or Testing vectors
    :return: list of vectors
    """
    vectors = np.zeros((corpus_size, vectors_size))
    for i in range(0, corpus_size):
        prefix = vectors_type + '_' + str(i)
        vectors[i] = doc2vec_model.docvecs[prefix]
    return vectors


def extract_doc2vec(dataSet, preprocess=None):
    #从dataset中读取data
    with open()

    data = label_sentences(data, 'Train')
    d2vModel = train_doc2vec(data)
    vec = get_vectors(d2vModel, len(data), 'Train')
    if preprocess:
        assert preprocess in ['normalize', 'robust_scale', 'minmax_scale',
                              'maxabs_scale'], "preprocess must be one of ['normalize', 'robust_scale', 'minmax_scale', 'maxabs_scale']"
        vec = eval(preprocess + '(vec)')
    return vec


###########################  test doc2vec  ##########################
'''
data = [
         'This is the first document.',
         'This is the second second document.',
         'And the third one.',
         'Is this the first document?',
         ]

print(extract_doc2vec(data).shape)
'''
###########################  test doc2vec  ##########################
if __name__ == '__main__':
    dataSet = sys.argv[1]
    modelName = sys.argv[2]
    modelName = 'VGG'
    feature2d, _ = extract_doc2vec(dataSet, modelName)
    print(feature2d)