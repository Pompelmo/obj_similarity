from elasticsearch import Elasticsearch, helpers
import globalvariable as gv
from TokenStem import TokenStem
from urlparse import urlparse
import csv

gv.init()
http = gv.http
index_idg = gv.index
password = gv.password
esc = Elasticsearch(['http://es-idg:9200'])
ts = TokenStem()


def scan_index_out():
    """scan the index"""
    query = {
        'size': 100,
        'query': {
            'match_all': {}}
    }

    response = helpers.scan(client=esc, query=query, index=index_idg, scroll='15m')

    return response


def get_urls():                                             # retrieve all url of companies
    url_list = []
    with open("source/websites.csv", "r") as asd:               # they are in a csv file
        read = csv.reader(asd)
        for line in read:
            parsed = urlparse(line[1])                          # parse in order to eliminate http:// or https://
            url_list.append(parsed.netloc)

    url_set = set(url_list)                                     # set so easier to see if something is in the set

    return url_set


def find_max():
    dis_keys = list()
    dis_des = list()
    dis_text = list()
    i = 0

    urls = get_urls()

    response = scan_index_out()

    for item in response:
        if item[u'_id'] in urls:
            used = item[u'_source']
            i += 1
            if u'keywords' in used.keys():
                n_key = len(ts.tokenize_keywords(used[u'keywords']))
                dis_keys.append(n_key)

            if u'description' in used.keys():
                n_des = len(ts.tokenize_description(used[u'description']))
                dis_des.append(n_des)

            if u'text' in used.keys():
                n_text = len(ts.tokenize_description(used[u'text']))
                dis_text.append(n_text)

            if i % 10000 == 0:
                print max(dis_keys), max(dis_des), max(dis_text)
                break

    return dis_keys, dis_des, dis_text


if __name__ == '__main__':
    dk, dd, dt = find_max()

    with open('source/dis_key_10000.csv', 'wb') as fil:
        write = csv.writer(fil)
        for ite in dk:
            write.writerow(str(ite))

    with open('source/dis_des_10000.csv', 'wb') as fil:
        write = csv.writer(fil)
        for ite in dd:
            write.writerow(str(ite))

    with open('source/dis_text_10000.csv', 'wb') as fil:
        write = csv.writer(fil)
        for ite in dt:
            write.writerow(str(ite))
