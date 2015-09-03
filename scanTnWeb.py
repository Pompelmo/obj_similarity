import json
import certifi
import csv
from elasticsearch import Elasticsearch, helpers
import globalvariable as gv

gv.init()
http = gv.http
index = gv.index_atk

es = Elasticsearch([http], use_ssl=True, verify_certs=True, ca_certs=certifi.where())


def entities_scan():
    keywords_list = {}
    query = json.dumps({
        'query': {
            'filtered': {
                'filter': {
                    'bool': {
                        'must': [{
                            'exists': {'field': 'websites'}
                        },
                            {
                            'exists': {'field': 'entities'}
                        },
                            {
                            'term': {'isActive': 'true'}
                        },
                            {
                            'term': {'headquarters.address.municipality': 'Trento'}
                        }
                        ]
                    }
                }
            }
        }
    })

    # scan companies with headquarter in Trento with at least a website
    response = helpers.scan(client=es, query=query, index=index)

    for item in response:
        keywords = item[u'_source'][u'entities']
        keywords_list[item[u'_id']] = [keywords[0][u'url']]
        for keyword in keywords[1:]:
            keywords_list[item[u'_id']].append(keyword[u'url'])

    return keywords_list


def main(path):
    keyword_url = entities_scan()

    with open(path, "wb") as boh:
        writer = csv.writer(boh)
        for key in keyword_url:
            line = [key]
            for i in range(0, len(keyword_url[key])):
                line.append(keyword_url[key][i])

            writer.writerow(line)


if __name__ == '__main__':
    main('source/tnweb_entities.csv')
