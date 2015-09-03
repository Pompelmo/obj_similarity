# -------------------------------------------------------
# script to train word2vec model from
# keywords or descriptions of all companies' websites
# -------------------------------------------------------

import csv
import sys
import logging
import gensim
from TokenStem import TokenStem

csv.field_size_limit(sys.maxsize)


def idg_word2vec(path, inp_type, save_model_path,
                 num_features=300, min_word_count=50, num_workers=4,
                 context=10, downsampling=1e-3):
    """function to train word2vec model. parameters have been chosen following the tutorial, see
    http://radimrehurek.com/2014/02/word2vec-tutorial/"""

    # logging to see the progression of the model
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)

    # create the iterator to save memory
    sentences = MySentences(path, inp_type)

    # train the model
    model = gensim.models.word2vec.Word2Vec(sentences, size=num_features, min_count=min_word_count,
                                            workers=num_workers, window=context, sample=downsampling)

    # save the model
    model.save(save_model_path)


class MySentences(object):
    """class that are used to have an iterator for the word2vec to save memory"""
    def __init__(self, path, inp_type):
        self.path = path
        self.inp_type = inp_type
        self.tokstem = TokenStem()

    def __iter__(self):

        if self.inp_type == 'description':
            with open(self.path, "r") as asd:
                read = csv.reader(asd)
                for line in read:
                    yield self.tokstem.tokenize_description(line[1])

        elif self.inp_type == 'keywords':
            with open(self.path, "r") as asd:
                read = csv.reader(asd)
                for line in read:
                    keywords = self.tokstem.tokenize_keywords(line[1])
                    if len(keywords) <= 30:
                        yield keywords


def main(read_path, method, write_path):

    idg_word2vec(read_path, method, write_path)


if __name__ == '__main__':
    main(read_path='source/websites_keywords.csv',
         method='keywords',
         write_path='source/w2vmodel_keywords_stemmed_20')
