from elasticsearch import Elasticsearch
import json
import globalvariable as gv
from TokenStem import TokenStem
import url_id_to_text as uitt

es = Elasticsearch([''])

gv.init()
index = gv.index

ts = TokenStem()


class Counter(object):

    def __init__(self, w2v_model, d2v_model, tfidf_dict, tfidf):
        self.w2v_model = w2v_model
        self.d2v_model = d2v_model
        self.tfidf_dict = tfidf_dict
        self.tfidf = tfidf

    def q_tokenize(self, url_id, field):
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
        keywords = self.q_tokenize(url, "keywords")
        i = 0
        for item in keywords:
            try:
                a = self.w2v_model[item]
                i += 1
            except KeyError:
                a = 0

        return i

    def count_description(self, url):
        description = self.q_tokenize(url, "description")
        i = 0
        for item in description:
            try:
                a = self.d2v_model[item]
                i += 1
            except KeyError:
                a = 0

        return i

    def count_text(self, url):
        i = 0
        text = uitt.transform(url)
        txtbow = self.tfidf_dict.doc2bow(text)
        vector = self.tfidf[txtbow]

        return len([x for x in vector if x != 0])


