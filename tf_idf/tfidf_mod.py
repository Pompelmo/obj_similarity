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
import sparmap

ts = TokenStem()
dictionary = gensim.corpora.Dictionary.load('source/web_text_dict_last.dict')


def _ts_and_bow(sentence):
    ts_sentence = ts.tokenize_description(sentence)
    return dictionary.doc2bow(ts_sentence)


def get_urls():                                             # retrieve all url of companies
    url_list = []
    with open("source/websites.csv", "r") as asd:               # they are in a csv file
        read = csv.reader(asd)
        for line in read:
            parsed = urlparse(line[1])                          # parse in order to eliminate http:// or https://
            url_list.append(parsed.netloc)

    url_set = set(url_list)                                     # set so easier to see if something is in the set

    return url_set


def _process_input_queue(input_list):
        output_generator = sparmap.parmap(input_list, fun=_ts_and_bow, workers=6, max_queue_size=-1)
        for item in output_generator:
            yield item


class MyCorpus(object):

    def __init__(self):
        gv.init()
        self.index = gv.index                                           # websites index
        self.es = Elasticsearch(['http://es-idg:9200'], max_retries=100,
                                retry_on_status=True, retry_on_timeout=True)
        self.response = scan_index_out('text', self.es, self.index)     # scan the entire index
        self.url_set = get_urls()                                       # get urls connected to a company
        self.ts = TokenStem()                                           # class for tokenize and stemming
        self.dictionary = dictionary
        self.enum_doc = dict()

    def __iter__(self):                                                             # define the iterator
        i = j = 0                                                                    # recover doc order
        input_list = []
        for item in self.response:                                                  # for every retrieved url
            if item[u'_id'] in self.url_set:                                        # if it belongs to a company
                i += 1
                self.enum_doc[i] = item[u'_id']                                  # create n doc dict
                input_list.append(item[u'_source'][u'text'])
                if len(input_list) > 1000:
                    j += 1
                    print "iterations: ", j, " of 444"
                    for item_2 in _process_input_queue(input_list):
                        yield item_2
                    input_list = []


def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    corpus = MyCorpus()

    gensim.corpora.MmCorpus.serialize('source/web_text_mm_last.mm', corpus)

    doc_order = corpus.enum_doc
    output = open('source/web_text_doc_last.pkl', 'wb')
    pickle.dump(doc_order, output)
    output.close()


if __name__ == '__main__':
    main()
