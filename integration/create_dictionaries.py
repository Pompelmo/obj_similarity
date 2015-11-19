from elasticsearch import Elasticsearch, helpers
import json
import globalvariable as gv
from TokenStem import TokenStem
import csv
from urlparse import urlparse
import pickle
import gensim

es = Elasticsearch(['***'])  # client for the elasticsearch index

gv.init()
index = gv.index

ts = TokenStem()        # class for tokenizing and stemming


def q_tokenize(method):
    if method == "keywords":
        field = "keywords"
        tokenizer = ts.tokenize_keywords
        model = gensim.models.Word2Vec.load('source/w2vmodel_keywords_scan')

    elif method == "description":
        field = "description"
        tokenizer = ts.tokenize_description
        model = gensim.models.Doc2Vec.load('source/d2vdescription')
    else:
        raise TypeError("wrong input")

    dictionary = dict()
    query = json.dumps({
        'size': 100,
        '_source': ['_id', field],
        'query': {
            'filtered': {
                'filter': {
                    'exists': {'field': field}
                }
            }
        }
    })

    response = helpers.scan(client=es, query=query, index=index, scroll='15m')

    url_list = []
    with open("source/websites.csv", "r") as asd:
        read = csv.reader(asd)
        for line in read:
            parsed = urlparse(line[1])
            url_list.append(parsed.netloc)

    url_set = set(url_list)

    i = 0
    for item in response:
        if item[u'_id'] in url_set:
            i += 1
            tokens = []
            value = tokenizer(item[u'_source'][field])
            for token in value:
                if token in model.vocab:
                    tokens.append(token)
            dictionary[item[u'_id']] = tokens
        if i % 1000 == 0:
            print i

    return dictionary


def main():
    dictionary = q_tokenize('description')

    output = open("source/des_dict", "wb")
    pickle.dump(dictionary, output)
    output.close()

if __name__ == '__main__':
    main()



