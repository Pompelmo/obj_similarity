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

    alpha, min_alpha, passes = 0.025, 0.001, 10  # define some parameters that are used for the learning rate
    alpha_delta = (alpha - min_alpha) / passes

    print "START %s" % datetime.datetime.now()

    train_model = Doc2Vec(size=100, min_count=20, workers=4, window=10)
    # first of all we need a dictionary so all the models (from the iterations) can use it to train
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
    """load the dictionary for training the model, created from the description"""
    all_docs = []  # we need a list of TaggedDocument, that are (named)array of two lists: words + tag
    path = 'source/websites_description.csv'  # read the dictionary[website] = description

    with open(path, "r") as asd:
        reader = csv.reader(asd)
        for line in reader:
            tag = [line[0]]                             # read the tags = website id
            value = sdf.tokenize_description(line[1])   # create the list of words
            all_docs.append(gensim.models.doc2vec.TaggedDocument(value, tag))  # create TaggedDocument

    return all_docs[:]


def load_keywords():
    """load the dictionary for training the model, created from the keywords"""
    all_docs = []  # we need a list of TaggedDocument, that are (named)array of two lists: words + tag
    path = 'source/websites_keywords.csv'  # load the dictionary[website] = keywords

    with open(path, "r") as asd:
        reader = csv.reader(asd)
        for line in reader:
            tag = [line[0]]                             # load the tag = website id
            value = sdf.tokenize_keywords(line[1])      # create the list of words
            all_docs.append(gensim.models.doc2vec.TaggedDocument(value, tag)) # create TaggedDocument

    return all_docs[:]


def main():
    doc_list = load_keywords()
    train_model_buck(doc_list, 'source/d2vkeyword')


if __name__ == '__main__':
    main()
