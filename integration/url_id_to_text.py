from elasticsearch import Elasticsearch
import json
import globalvariable as gv
from TokenStem import TokenStem

gv.init()
index = gv.index

ts = TokenStem()


def transform(url_id):
    ts_text = []
    url_id = [url_id]
    query = json.dumps({
        '_source': ['_id', 'text'],
        'query': {
            'filtered': {
                'filter': {
                    'terms': {'_id': url_id}
                }
            }
        }
    })

    response = es.search(index=index, body=query)[u'hits'][u'hits'][0]
    if u'text' in response[u'_source'].keys():
        testo = response[u'_source'][u'text']
        ts_text = ts.tokenize_description(testo)

    return ts_text

