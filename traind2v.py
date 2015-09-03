# -------------------------------------------------------
# script to train doc2vec model from
# keywords or descriptions of all companies' websites
# -------------------------------------------------------

from trainw2v import MySentences
import gensim
import logging
import csv


class LabeledLineSentence(MySentences):
    """subclass that are used to have an iterator for the doc2vec to save memory"""
    def __init__(self, path, inp_type):
        super(LabeledLineSentence, self).__init__(path, inp_type)

    def __iter__(self):
        if self.inp_type == 'description':
            i = 0
            with open(self.path, "r") as asd:
                read = csv.reader(asd)
                for line in read:
                    i += 1
                    tok_stem_des = self.tokstem.tokenize_description(line[1])
                    tags = [line[0]]
                    yield gensim.models.doc2vec.TaggedDocument(tok_stem_des, tags)

        elif self.inp_type == 'keywords':
            with open(self.path, "r") as asd:
                read = csv.reader(asd)
                for line in read:
                    keywords = self.tokstem.tokenize_keywords(line[1])
                    tags = [line[0]]
                    if len(keywords) <= 30:
                        yield gensim.models.doc2vec.TaggedDocument(keywords, tags)


def idg_doc2vec(path, inp_type, save_model_path,
                num_features=100, min_word_count=20, num_workers=4,
                context=10, downsampling=0):
    """function to train doc2vec model. parameters have been chosen following the tutorial,
    see https://github.com/piskvorky/gensim/blob/develop/docs/notebooks/doc2vec-IMDB.ipynb,
    but for min_count due to my pc small memory"""

    # logging to see the progression of the model
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)

    # class to create the iterator to save memory
    label_sentences = LabeledLineSentence(path, inp_type)

    # train the model
    model = gensim.models.Doc2Vec(label_sentences, size=num_features, min_count=min_word_count,
                                  workers=num_workers, window=context, sample=downsampling)
    # save it
    model.save(save_model_path)


def main(read_path, method, write_path):

    idg_doc2vec(read_path, method, write_path)


if __name__ == '__main__':
    main(read_path='source/websites_keywords.csv',
         method='keywords',
         write_path='source/d2vmodel_keywords_stemmed_20')

