import json
from elasticsearch import Elasticsearch, helpers
import certifi
import globalvariable as gv
import csv
from urlparse import urlparse


def scan_tn_web_idg():
    """get the dictionary[id website] = source from the url lists that come from the
    companies with headquarter in Trento. since not all id are found in websites index,
    a new list without them is created"""

    # create client to query the index
    http = gv.http
    index = gv.index
    password = gv.password
    es = Elasticsearch([http], http_auth=password, use_ssl=True, verify_certs=True,
                       ca_certs=certifi.where())

    url_list = []
    websites_source = dict()

    with open("source/websites_trento.csv", "r") as asd1:
        reader = csv.reader(asd1)
        for line1 in reader:
            parsed = urlparse(line1[1])
            url_list.append(parsed.netloc)

    query = json.dumps({
        'query': {
            'filtered': {
                'filter': {
                    'terms': {
                        '_id': url_list
                    }
                }
            }
        }
    })

    response = helpers.scan(client=es, query=query, index=index)

    for item in response:
        if u'_source' in item.keys():
            websites_source[item[u'_id']] = item[u'_source']

    return websites_source  # dictionary[website] = source from idg
