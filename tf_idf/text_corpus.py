#!/usr/bin/python
# -*- coding: utf-8 -*-

# the first two line of comment are needed to encode the text in websites.
# texts are usually in italian, so it's easy to get encoding errors

import gensim
from elasticsearch import Elasticsearch
import logging
from TokenStem import TokenStem
import globalvariable as gv
from write_metadata import scan_index_out
from urlparse import urlparse
import csv
import pickle


def get_urls():                                             # retrieve all url of companies
    url_list = []
    with open("source/websites.csv", "r") as asd:               # they are in a csv file
        read = csv.reader(asd)
        for line in read:
            parsed = urlparse(line[1])                          # parse in order to eliminate http:// or https://
            url_list.append(parsed.netloc)

    url_set = set(url_list)                                     # set so easier to see if something is in the set

    return url_set


def iter_docs(url_set, tokstem_izer):

    es = Elasticsearch(['http://es-idg:9200'])
    gv.init()
    index = gv.index
    response = scan_index_out('text', es, index)

    for item in response:
        if item[u'_id'] in url_set:
            sentence = tokstem_izer.tokenize_description(item[u'_source'][u'text'])
            yield sentence


class MyCorpus(object):

    def __init__(self, dictionary):
        gv.init()
        self.index = gv.index                                           # websites index
        self.es = Elasticsearch(['http://es-idg:9200'])
        self.response = scan_index_out('text', self.es, self.index)     # scan the entire index
        self.url_set = get_urls()                                       # get urls connected to a company
        self.ts = TokenStem()                                           # class for tokenize and stemming
        self.dictionary = dictionary  # corpus dictionary
        # should eliminate only once words but since we are already eliminating a lot of doc to
        # train the model, for the moment I leave it
        # once_ids = [tokenid for tokenid, docfreq in self.dictionary.dfs.iteritems() if docfreq == 1]
        # self.dictionary.filter_tokens(once_ids)
        self.dictionary.compactify()                                    # remove gaps in id sequence
        self.enum_doc = dict()

    def __iter__(self):                                                             # define the iterator
        i = 0                                                                    # recover doc order
        for item in self.response:                                                  # for every retrieved url
            if item[u'_id'] in self.url_set:                                        # if it belongs to a company
                i += 1
                self.enum_doc[i] = item[u'_id']                                  # create n doc dict
                sentence = self.ts.tokenize_description(item[u'_source'][u'text'])  # tokenize the text
                yield self.dictionary.doc2bow(sentence)                             # transform in doc2bow


def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    url_set = get_urls()
    ts = TokenStem()

    dictionary = gensim.corpora.Dictionary(iter_docs(url_set, ts))

    corpus = MyCorpus(dictionary)

    corpus.dictionary.save('source/web_text_dict_last.dict')

    gensim.corpora.MmCorpus.serialize('source/web_text_mm_last.mm', corpus)

    doc_order = corpus.enum_doc
    output = open('source/web_text_doc_last.pkl', 'wb')
    pickle.dump(doc_order, output)
    output.close()


if __name__ == '__main__':
    main()
