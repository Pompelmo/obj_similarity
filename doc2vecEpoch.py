# --------------------------------------------------
# script for training doc2vec using more than one
# epoch. keeps the input in memory
# --------------------------------------------------

import gensim.models.doc2vec
from gensim.models import Doc2Vec
import csv
from random import shuffle
from collections import defaultdict
import datetime
from TokenStem import TokenStem

sdf = TokenStem()
best_error = defaultdict(lambda: 1.0)  # selectively print only best error achieved


def train_model_buck(doc_list, path):
    # copied from
    # https://github.com/piskvorky/gensim/blob/develop/docs/notebooks/doc2vec-IMDB.ipynb
    # bulk training

    alpha, min_alpha, passes = 0.025, 0.001, 10
    alpha_delta = (alpha - min_alpha) / passes

    print "START %s" % datetime.datetime.now()

    train_model = Doc2Vec(size=100, min_count=20, workers=4, window=10)
    train_model.build_vocab(doc_list)

    for epoch in range(passes):
        shuffle(doc_list)  # apparently shuffle gives best results

        train_model.alpha, train_model.min_alpha = alpha, alpha

        train_model.train(doc_list)

        print "completed pass %i at alpha %f" % (epoch+1, alpha)
        alpha -= alpha_delta

    print "END %s" % datetime.datetime.now()

    train_model.save(path)


def load_description():
    all_docs = []
    path = 'source/websites_description.csv'

    with open(path, "r") as asd:
        reader = csv.reader(asd)
        for line in reader:
            tag = [line[0]]
            value = sdf.tokenize_description(line[1])
            all_docs.append(gensim.models.doc2vec.TaggedDocument(value, tag))

    return all_docs[:]


def load_keywords():
    all_docs = []
    path = 'source/websites_keywords.csv'

    with open(path, "r") as asd:
        reader = csv.reader(asd)
        for line in reader:
            tag = [line[0]]
            value = sdf.tokenize_keywords(line[1])
            all_docs.append(gensim.models.doc2vec.TaggedDocument(value, tag))

    return all_docs[:]


def main():
    doc_list = load_keywords()
    train_model_buck(doc_list, 'source/d2vkeyword')


if __name__ == '__main__':
    main()
