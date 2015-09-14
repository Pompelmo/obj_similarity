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


def get_urls():                                             # retrieve all url of companies
    url_list = []
    with open("source/websites.csv", "r") as asd:               # they are in a csv file
        read = csv.reader(asd)
        for line in read:
            parsed = urlparse(line[1])                          # parse in order to eliminate http:// or https://
            url_list.append(parsed.netloc)

    url_set = set(url_list)                                     # set so easier to see if something is in the set

    return url_set


def iter_docs(response, url_set, tokstem_izer):
    i = 0
    for item in response:
        i += 1
        if item[u'_id'] in url_set and i % 10 == 0:
            sentence = tokstem_izer.tokenize_description(item[u'_source'][u'text'])
            yield sentence


class MyCorpus(object):

    def __init__(self):
        gv.init()
        self.http = gv.http
        self.index = gv.index                                           # websites index
        self.es = Elasticsearch(['http://elasticsearch:9200'])
        self.response = scan_index_out('text', self.es, self.index)     # scan the entire index
        self.url_set = get_urls()                                       # get urls connected to a company
        self.ts = TokenStem()                                           # class for tokenize and stemming
        self.dictionary = gensim.corpora.Dictionary.load('source/web_text_dict.dict')  # corpus dictionary
        # should eliminate only once words but since we are already eliminating a lot of doc to
        # train the model, for the moment I leave it
        # once_ids = [tokenid for tokenid, docfreq in self.dictionary.dfs.iteritems() if docfreq == 1]
        # self.dictionary.filter_tokens(once_ids)
        self.dictionary.compactify()                                    # remove gaps in id sequence

    def __iter__(self):                                                             # define the iterator
        for item in self.response:                                                  # for every retrieved url
            if item[u'_id'] in self.url_set:                                        # if it belongs to a company
                sentence = self.ts.tokenize_description(item[u'_source'][u'text'])  # tokenize the text
                yield self.dictionary.doc2bow(sentence)                             # transform in doc2bow


def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    corpus = MyCorpus()

    corpus.dictionary.save('source/web_text_dict_2.dict')

    gensim.corpora.MmCorpus.serialize('source/web_text_mm_2.mm', corpus)


if __name__ == '__main__':
    main()
