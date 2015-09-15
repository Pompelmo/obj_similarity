# ---------------------------------------------------
# script that compute a weighted query using
# w2v-enriched information from a given website, in
# order to find similar websites
# ---------------------------------------------------

# at the moment this doesn't work, due to the fact that elasticsearch
# index doesn't use stemmed words, but this script does.

import gensim
from elasticsearch import Elasticsearch
from collections import OrderedDict
import certifi
import json
from TokenStem import TokenStem
import globalvariable as gv


class Suggest(object):
    def __init__(self, model):
        # load the two models
        self.model = model
        gv.init()
        # create elasticsearch client for the queries
        self.http = gv.http
        self.index = gv.index
        self.es = Elasticsearch([self.http], use_ssl=True, verify_certs=True, ca_certs=certifi.where())

        self.tokstem = TokenStem()

    def most_similar(self, words):
        """having a list of words, creates a dictionary word-score from the w2v model"""

        model = self.model
        similar_words = dict()

        for word in words:
            # keep all original word with score 1
            similar_words[word] = 1

            # if the word is in the vocabulary ->
            if word in model.vocab:
                # -> take the (10 by default) most similar word in word2vec model
                simlist = model.most_similar(word)

                for item in simlist:
                    # check that we don't have duplicates
                    # if we have them, keep the one with higher score
                    if item[0] not in similar_words.keys():
                        similar_words[item[0]] = item[1]
                    else:
                        # u is the index of the word that already appears in the similar words set
                        if similar_words[item[0]] < item[1]:
                            # if the score is higher, substitute
                            similar_words[item[0]] = item[1]

        return similar_words

    def construct_query(self, stem_dict, field):
        functions = []
        for key in stem_dict:
            itemd = OrderedDict()
            itemd['filter'] = {'term': {field: key}}
            itemd['weight'] = stem_dict[key]
            functions.append(itemd)

        return functions

    def get_info(self, id_website, field):
        """retrieve information from a website and then use it to make a weighted query"""

        # query to retrieve the needed information
        query = json.dumps({
            '_source': ['_id', 'description', 'keywords'],
            'query': {
                'filtered': {
                    'filter': {
                        'bool': {
                            'must': [
                                {
                                    'term': {'_id': id_website}
                                },
                                {
                                    'exists': {'field': field}
                                }
                            ]
                        }
                    }
                }
            }
        })

        response = self.es.search(index=self.index, body=query)[u'hits'][u'hits'][0]

        if field == 'keywords':  # search for keywords
            keywords = response[u'_source'][u'keywords']
            keywords = self.tokstem.tokenize_keywords(keywords)  # tokenize and stem them
            info_list = self.most_similar(keywords)  # enrich the set using w2v model

        elif field == 'description':  # search for description
            description = response[u'_source'][u'description']
            description = self.tokstem.tokenize_description(description)  # tokenize and stem description
            info_list = self.most_similar(description)  # enrich the set using w2v model

        else:
            print "wrong field"
            info_list = []

        return info_list

    def similar_web(self, id_website, field):
        info_list = self.get_info(id_website, field)

        if info_list:  # if info is non empty
            functions = self.construct_query(info_list, field)  # construct the weighted part of the query

            query2 = json.dumps({
                '_source': ['_id'],  # , 'description', 'keywords'],
                'query': {
                    'function_score': {
                        'query': {
                            'match_all': {}     # change here to Trento if needed
                        },
                        'functions': functions,
                        'score_mode': 'avg'
                    }
                }
            })
            response2 = self.es.search(index=self.index, body=query2)

            return response2

        else:
            print 'No ' + field + ' found'
            return None

    def pretty_print_response(self, id_website, field):
        """print the ten most similar websites"""
        response = self.similar_web(id_website, field)
        for item in response[u'hits'][u'hits']:
            print item[u'_id']


def main():

    model = gensim.models.Word2Vec.load('source/w2vmodel_description_stemmed')

    prova = Suggest(model)
    prova.pretty_print_response(["www.auto-futura.it"], 'keywords')


if __name__ == '__main__':
    main()

