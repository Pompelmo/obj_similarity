from elasticsearch import Elasticsearch, helpers
import json
import csv
from urlparse import urlparse


url_list = []
with open("source/websites.csv", "r") as asd:               # they are in a csv file
    read = csv.reader(asd)
    for line in read:
        parsed = urlparse(line[1])                          # parse in order to eliminate http:// or https://
        url_list.append(parsed.netloc)

    url_set = set(url_list)


query = json.dumps({
    '_source': ['_id'],
    'query': {
        'filtered': {
            'filter': {
                'bool': {
                    'must': {
                        'exists': {'field': 'description'}
                    },
                    'must_not': [{
                        'exists': {'field': 'keywords'}
                    },
                        {
                        'exists': {'field': 'text'}
                        }
                    ]
                }
            }
        }
    }
})

response = helpers.scan(client=es, query=query, index=index)

i = 0
for item in response:
    if item in url_set:
        i += 1
        print item
    if i >= 10:
        break
