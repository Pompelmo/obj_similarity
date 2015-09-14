import json
from elasticsearch import Elasticsearch, helpers
import csv
import certifi
import globalvariable as gv
from urlparse import urlparse


http = gv.http
index = gv.index
password = gv.password
es = Elasticsearch([http], http_auth=password, use_ssl=True, verify_certs=True,
                   ca_certs=certifi.where())


def scan_index_out(field):
    """scan the index"""
    query = json.dumps({
        '_source': ['_id', 'description', 'keywords'],
        'query': {
            'filtered': {
                'filter': {
                    'exists': {'field': field}
                }
            }
        }
    })

    response = helpers.scan(client=es, query=query, index=index)

    return response


def write_info(path, url_set, field):
    """function that creates a csv file website url - keywords/description"""
    # should be used once to have in memory information to retrieve

    response = scan_index_out(field)  # scan the index

    i = j = 0
    with open(path, "w") as outfile:
        writer = csv.writer(outfile)
        for item in response:
            i += 1
            if i % 10000 == 0:
                print i

            if item[u'_id'] in url_set:
                lin = [item[u'_id'].encode('utf-8')]
                line = item[u'_source'][field]
                lin.append(line)
                writer.writerow(lin)

    print j
    print i

    return None


def main():
    url_list = []
    with open("source/websites.csv", "r") as asd:
        read = csv.reader(asd)
        for line in read:
            parsed = urlparse(line[1])
            url_list.append(parsed.netloc)

    url_set = set(url_list)  # retrieve url without http://

    # write all the keywords/description in a csv (modify inside the function that should be
    # used just once)
    write_info("source/websites_keywords.csv", url_set, u'keywords')
    write_info("source/websites_description.csv", url_set, u'description')


if __name__ == '__main__':
    main()
