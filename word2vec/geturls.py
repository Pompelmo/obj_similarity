# --------------------------------------------------
# script to write a csv with all websites from
# companies with headquarter in Trento
# --------------------------------------------------

from elasticsearch import Elasticsearch, helpers
import certifi
import csv
import json
import globalvariable as gv

gv.init()
http = gv.http
index = gv.index_atk
path = 'source/websites_trento.csv'

# create the elasticsearch client
es = Elasticsearch([http], use_ssl=True, verify_certs=True, ca_certs=certifi.where())


def url_scan():
    """find all the websites of companies located (headquarters) in Trento"""
    url_list = []
    query = json.dumps({
        '_source': ['_id', 'websites.website', 'websites.confidence'],
        'query': {
            'filtered': {
                'filter': {
                    'bool': {
                        'must': [{
                            'exists': {
                                'field': 'websites'
                            }},
                            {'term': {
                                'headquarters.address.municipality': 'Trento'
                            }}
                        ]
                    }
                }
            }
        }
    })

    # scan companies with headquarter in Trento with at least a website
    response = helpers.scan(client=es, query=query, index=index)

    for item in response:
        websites = item[u'_source'][u'websites']

        for website in websites:  # companies may have more than one website

            # eliminate website with confidence = 0
            if u'confidence' in website.keys():
                if website[u'confidence'] > 0:
                    line = [item[u'_id'], website[u'website']]
                    url_list.append(line)
            else:
                # sometimes confidence is not present
                line = [item[u'_id'], website[u'website']]
                url_list.append(line)

    return url_list


def main():

    urls = url_scan()

    with open(path, "wb") as asd:
        writer = csv.writer(asd)
        for line in urls:
            writer.writerow(line)


if __name__ == '__main__':
    main()
