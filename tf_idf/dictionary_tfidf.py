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
import sparmap

ts = TokenStem()


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
        output_generator = sparmap.parmap(input_list, fun=ts.tokenize_description, workers=5, max_queue_size=-1)
        for item in output_generator:
            yield item


def iter_docs(url_set):

    es = Elasticsearch(['http://es-idg:9200'])
    gv.init()
    index = gv.index
    input_list = []

    response = scan_index_out('text', es, index)

    i = 0
    for item in response:
        if item[u'_id'] in url_set:
            input_list.append(item[u'_source'][u'text'])
            if len(input_list) > 1000:
                i += 1
                print "iterations: ", i, " of 444"
                for item_1 in _process_input_queue(input_list):
                    yield item_1
                input_list = []


def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    url_set = get_urls()

    dictionary = gensim.corpora.Dictionary(iter_docs(url_set), prune_at=500000)
    dictionary.compactify()
    dictionary.save('source/web_text_dict_last.dict')


if __name__ == '__main__':
    main()

