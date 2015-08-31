# -------------------------------------------------------
# script to train word2vec or doc2vec models from
# keywords or descriptions of websites (all websites,
# not only Trento companies ones)
# -------------------------------------------------------

import csv
import json
from elasticsearch import Elasticsearch, helpers
import certifi
import re
import sys
import logging
import gensim
import nltk
import globalvariable as gv

gv.init()
http = gv.http
index = gv.index

es = Elasticsearch([http], use_ssl=True, verify_certs=True, ca_certs=certifi.where())
csv.field_size_limit(sys.maxsize)
stemmer = nltk.stem.snowball.ItalianStemmer()  # ignore_stopwords=True)

def main():
    url_list = []
    with open("/Users/Kate/Desktop/SpazioDati/websites.csv", "r") as asd:
        read = csv.reader(asd)
        for line in read:
            url_list.append(line[1])

    url_set = set([item[7:] for item in url_list])  # retrieve url without http://

    # write which websites has keywords and/or description
    # write_meta_info(url_set, "/Users/Kate/Desktop/SpazioDati/websitesMetaPresence.csv")

    # write all the keywords/description in a csv (modify inside the function that should be
    # used just once)
    # write_description("/Users/Kate/Desktop/SpazioDati/websites_keywords.csv", url_set)

    # train a model: (in this case doc2vec with keywords
    idg_doc2vec('/Users/Kate/Desktop/SpazioDati/websites_keywords.csv',
                'keywords',
                '/Users/Kate/Desktop/SpazioDati/d2vmodel_keywords_stemmed_20')


def write_meta_info(url_set, write_path):
    """this function is used to write, for every website, if they have keywords or description"""
    # not needed for train the models

    response = scan_index_out()

    i = 0
    with open(write_path, "wb") as asd:
        writer = csv.writer(asd)
        writer.writerow(['url', 'description', 'keywords'])
        for item in response:
            i += 1
            if i % 1000 == 0:
                print i
            if item[u'_id'] in url_set:

                linea = [item[u'_id']]
                if u'description' in item[u'_source'].keys():
                    linea.append('True')
                else:
                    linea.append('False')
                if u'keywords' in item[u'_source'].keys():
                    linea.append('True')
                else:
                    linea.append('False')

                writer.writerow(linea)

    print i

    return None


def write_description(path, url_set):
    """function that creates a csv file website url - keywords/description"""
    # should be used once to have in memory information to retrieve

    response = scan_index_out()  # scan the index

    i = j = 0
    with open(path, "w") as outfile:
        writer = csv.writer(outfile)
        for item in response:
            i += 1
            if i % 10000 == 0:
                print i

            if item[u'_id'] in url_set:
                lin = [item[u'_id'].encode('utf-8')]
                if u'keywords' in item[u'_source'].keys():
                    j += 1
                    line = item[u'_source'][u'keywords']#.encode('utf-8')
                    lin.append(line)
                    writer.writerow(lin)

    print j
    print i

    return None


def idg_word2vec(path, inp_type, save_model_path,
                        num_features=300, min_word_count=50, num_workers=4,
                        context=10, downsampling=1e-3):
    """function to train word2vec model. parameters have been chosen following the tutorial, see
    http://radimrehurek.com/2014/02/word2vec-tutorial/"""

    # logging to see the progression of the model
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)

    # create the iterator to save memory
    sentences = MySentences(path, inp_type, "/Users/Kate/Desktop/SpazioDati/stopword.txt")

    # train the model
    model = gensim.models.word2vec.Word2Vec(sentences, size=num_features, min_count=min_word_count,
                                            workers=num_workers, window=context, sample=downsampling)

    # save the model
    model.save(save_model_path)


def idg_doc2vec(path, inp_type, save_model_path,
                num_features=100, min_word_count=20, num_workers=2,
                context=10, downsampling=0):
    """function to train doc2vec model. parameters have been chosen following the tutorial,
    see https://github.com/piskvorky/gensim/blob/develop/docs/notebooks/doc2vec-IMDB.ipynb,
    but for min_count due to my pc small memory"""

    # logging to see the progression of the model
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)

    # class to create the iterator to save memory
    label_sentences = LabeledLineSentence(path, inp_type, "/Users/Kate/Desktop/SpazioDati/stopword.txt")

    # train the model
    model = gensim.models.Doc2Vec(label_sentences, size=num_features, min_count=min_word_count,
                                  workers=num_workers, window=context, sample=downsampling)
    # save it
    model.save(save_model_path)


def scan_index_out():
    """scan the index"""
    query = json.dumps({
        '_source': ['_id', 'description', 'keywords'],
        'query': {
            'match_all': {}
        }
    })

    response = helpers.scan(client=es, query=query, index=index)

    return response


class MySentences(object):
    """class that are used to have an iterator for the word2vec to save memory"""
    def __init__(self, path, inp_type, stop_words_path):
        # self.dir_name = dir_name
        self.path = path
        self.inp_type = inp_type
        # self.url_set = url_set
        self.stop_words_path = stop_words_path
        self.stop_words = self.get_stop_words()

    def __iter__(self):

        # response = self.scan_index()
        #
        # for line in response:
        #     if line[u'_id'] in self.url_set:
        #         if u'description' in line[u'_source'].keys():
        #             yield self.tokenize(line[u'source'][u'description'].encoding('utf-8'))
        if self.inp_type == 'description':
            with open(self.path, "r") as asd:
                read = csv.reader(asd)
                for line in read:
                    yield self.tokenize_description(line[1])

        elif self.inp_type == 'keywords':
            with open(self.path, "r") as asd:
                read = csv.reader(asd)
                for line in read:
                    keywords = self.tokenize_keywords(line[1])
                    if len(keywords) <= 30:
                        yield keywords

        # for fname in os.listdir(self.dir_name):
        #     for line in open(os.path.join(self.dir_name, fname)):
        #         linea = line.split(", ")[1]
        #         token_line = self.tokenize(linea)
        #         yield token_line

    def tokenize_description(self, sentence):
        """tokenizer and stemmer for the description field"""
        lower_string = sentence.lower()
        token_list = []

        tok_list = re.findall(r'[\w]+', lower_string)

        for word in tok_list:
            if word not in self.stop_words:
                token_list.append(stemmer.stem(word))

        return token_list

    def tokenize_keywords(self, sentence):
        """tokenizer and stemmer for the keywords field"""
        line = sentence[1:len(sentence)-1].lower().split(", ")
        stemmed = []
        for l in line:
            m = l[2:len(l)-1]
            n = re.sub(r'[0-9\-]+', "", m)

            if n != "":
                s = ""
                for word in n.split(" "):
                    s += stemmer.stem(word) + " "
                stemmed.append(s[:len(s)-1])

        return stemmed

    # def scan_index(self):
    # """function to retrieve information directly for the index"""
    # mai provata
    #     query = json.dumps({
    #         '_source': ['_id', 'description', 'keywords'],
    #         'query': {
    #             'match_all': {}
    #         }
    #     })
    #
    #     response = helpers.scan(client=es, query=query, index=index)
    #
    #     return response

    def get_stop_words(self):
        """retrieve italian and english stopwords from a file"""
        stop_words = []
        with open(self.stop_words_path, "r") as asd:
            for line in asd:
                # eliminate \n at the end of every word
                stop_words.append(line[:len(line)-1])

        return set(stop_words)


class LabeledLineSentence(MySentences):
    """subclass that are used to have an iterator for the doc2vec to save memory"""
    def __init__(self, path, inp_type, stop_words_path):
        super(LabeledLineSentence, self).__init__(path, inp_type, stop_words_path)

    def __iter__(self):
        if self.inp_type == 'description':
            i = 0
            with open(self.path, "r") as asd:
                read = csv.reader(asd)
                for line in read:
                    i += 1
                    tok_stem_des = self.tokenize_description(line[1])
                    tags = [line[0]]
                    yield gensim.models.doc2vec.TaggedDocument(tok_stem_des, tags)

        elif self.inp_type == 'keywords':
            with open(self.path, "r") as asd:
                read = csv.reader(asd)
                for line in read:
                    keywords = self.tokenize_keywords(line[1])
                    tags = [line[0]]
                    if len(keywords) <= 30:
                        yield gensim.models.doc2vec.TaggedDocument(keywords, tags)


if __name__ == '__main__':
    main()
