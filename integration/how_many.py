# -------------------------------------------------------------
# script used to count number of keywords or tokens used
# by the model for a given website
# -------------------------------------------------------------


from elasticsearch import Elasticsearch
import json
import globalvariable as gv
from TokenStem import TokenStem
import url_id_to_text as uitt

es = Elasticsearch(['http://es-idg:9200'])  # client for the elasticsearh index

gv.init()
index = gv.index

ts = TokenStem()        # class for tokenizing and stemming


class Counter(object):                                           # class with all the methods for counting

    def __init__(self, w2v_model, d2v_model, tfidf_dict, tfidf):
        self.w2v_model = w2v_model      # keywords word2vector model
        self.d2v_model = d2v_model      # description doc2vector model
        self.tfidf_dict = tfidf_dict    # tfidf text model dictionary
        self.tfidf = tfidf              # tfidf text model

    def q_tokenize(self, url_id, field):
        """query + function to retrieve keywords or tokens in description"""
        url_id = [url_id]
        query = json.dumps({
            '_source': ['_id', field],
            'query': {
                'filtered': {
                    'filter': {
                        'terms': {'_id': url_id}
                    }
                }
            }
        })

        response = es.search(index=index, body=query)[u'hits'][u'hits'][0]

        if field == "keywords":
            if u'keywords' in response[u'_source'].keys():
                return ts.tokenize_keywords(response[u'_source'][u'keywords'])

        elif field == "description":
            if u'description' in response[u'_source'].keys():
                return ts.tokenize_description(response[u'_source'][u'description'])

        else:
            return []

    def count_keywords(self, url):
        """function to count keywords present in the model keywords word2vec"""
        keywords = self.q_tokenize(url, "keywords")  # retrieve keywords
        i = 0
        for item in keywords:
            try:
                a = self.w2v_model[item]            # this a is useless, but PyCharm complain that self.w2v[item]
                i += 1                              # has no effect
            except KeyError:
                a = 0

        return i                        # return how many keywords are present in the model

    def count_description(self, url):
        """function to count description tokens present in the model description doc2vec"""
        description = self.q_tokenize(url, "description")
        i = 0
        for item in description:
            try:
                a = self.d2v_model[item]            # this a is useless, but PyCharm complain that self.w2v[item]
                i += 1                              # has no effect
            except KeyError:
                a = 0

        return i                        # return how many keywords are present in the model

    def count_text(self, url):
        """function to count text tokens present in tfidf model"""
        i = 0
        text = uitt.transform(url)                          # retrieve text
        txtbow = self.tfidf_dict.doc2bow(text)              # transform in bag of word vector
        vector = self.tfidf[txtbow]                         # transform in tfidf vector (maybe not necessary)

        return len([x for x in vector if x != 0])           # count non zero entries
