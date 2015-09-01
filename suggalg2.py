# ----------------------------------------------------
# script that compute similarity between all possible
# websites of companies in Trento city
# ----------------------------------------------------

import csv
import certifi
import gensim
import pickle
import nltk
import json
from elasticsearch import Elasticsearch, helpers
import suggalg1
import globalvariable as gv

gv.init()

# load word2vec models
model_1 = gensim.models.Word2Vec.load('source/w2vmodel_description_stemmed')
model_2 = gensim.models.Word2Vec.load('source/w2vmodel_keywords_stemmed')

# create client to query the index
http = gv.http
index = gv.index
password = gv.password
es = Elasticsearch([http], http_auth=password, use_ssl=True, verify_certs=True,
                   ca_certs=certifi.where())

# stemmer for italian word (it doesn't eliminate stop word)
stemmer = nltk.stem.snowball.ItalianStemmer()  # ignore_stopwords=True)

# object to use the enrich function (for the similarity between sets)
similar = suggalg1.Suggest()

# compute stop words from a file
stop_words = []
with open("source/stopword.txt", "r") as asd:
    for line in asd:
        # eliminate character \n at the end of each line
        stop_words.append(line[:len(line)-1])

stop_words = set(stop_words)


def construct_dict_mean(url_list, save_path):
    """create and save as a pickle object dictionary with key couple of websites and value
    their similarity computed as n_similarity from gensim.word2vec"""
    sim_dict = dict()
    tnweb, new_ul = get_tnweb_dict(url_list)

    # construct the two dictionary with key = website id and value = list of words
    most_similar_key, most_similar_des = get_dictionaries_mean(tnweb, new_ul)

    k = len(new_ul)
    print k

    for i in range(0, k):
        u_i = most_similar_key[new_ul[i]], most_similar_des[new_ul[i]]  # array of two sets
        for j in range(i+1, k):
            u_j = most_similar_key[new_ul[j]], most_similar_des[new_ul[j]]  # array of two sets
            # compute the similarity for every couple of websites
            sim_dict[new_ul[i], new_ul[j]] = similarity_mean(u_i, u_j)

        print i

    output = open(save_path, 'wb')

    # save the similarity dictionary constructed as pickle obj
    pickle.dump(sim_dict, output)

    output.close()

    return None


def construct_dict_intersection(url_list, save_path):
    """create and save as a pickle object dictionary with key couple of websites and value
    their similarity computed as some strange measure derived from jaccard similarity"""
    sim_dict = dict()
    tnweb, new_ul = get_tnweb_dict(url_list)
    most_similar_key, most_similar_des = get_dictionaries_intersect(tnweb, new_ul)

    k = len(new_ul)
    print k

    for i in range(0, k):
        u_i = most_similar_key[new_ul[i]], most_similar_des[new_ul[i]]  # array of two dictionaries
        for j in range(i+1, k):
            u_j = most_similar_key[new_ul[j]], most_similar_des[new_ul[j]]  # array of two dictionaries
            # compute the similarity for every couple of websites
            sim_dict[new_ul[i], new_ul[j]] = similarity_set(u_i, u_j)

        print i

    output = open(save_path, 'wb')

    # save the similarity dictionary constructed as pickle obj
    pickle.dump(sim_dict, output)

    output.close()

    return None


def similarity_mean(u_couple, v_couple):
    """this function computes the similarity between two website using the n_similarity of the
    gensim.word2vec using the websites set of keywords, or set of word from description field,
    compute the set vector mean, then compute cosine similarity between the two mean"""

    k1, d1 = u_couple
    k2, d2 = v_couple

    # if one of them is empty, similarity is 0, otherwise compute it through n_similarity
    if k1 and k2:
        sk = model_2.n_similarity(k1, k2)
    else:
        sk = 0

    if d1 and d2:
        sd = model_1.n_similarity(d1, d2)
    else:
        sd = 0

    return sk, sd


def similarity_set_partial(enrich_1, enrich_2):
    """compute the similarity in this way: having two dictionary word-score,
    confront the two set: every intersection is weighted by its similarity weight (one for original
    word) and the final result is the sum of those divided by their union (set union, so minus the
    intersection)"""

    # return 0 if one of the two dictionary is empty
    if not enrich_1 or not enrich_2:
        return 0

    # use partial_score to compute the weighted intersection
    partial_score = 0

    # use set to make it faster (I hope)
    en_key = set(enrich_2.keys()).intersection(set(enrich_1.keys()))

    # weight sum of scores for item that intersect
    for item in en_key:
        partial_score += enrich_1[item] * enrich_2[item]   # multiplication between scores

    return partial_score / (len(enrich_1) + len(enrich_2) - len(en_key))


def weighted_jaccard(enrich_1, enrich_2):
    """weighted Jaccard similarity """
    # not yet tested

    if not enrich_1 or not enrich_2:
        return 0

    sum_min = 0
    sum_max = 0

    en_key = set(enrich_2.keys()).intersection(set(enrich_1.keys()))

    if len(en_key) == 0:
        return 0

    for item in en_key:
        sum_min += min(enrich_1[item], enrich_2[item])
        sum_max += max(enrich_1[item], enrich_2[item])

    return sum_min / sum_max


def similarity_set(u_couple, v_couple):
    """compute the set similarity for both keywords and description words"""
    k1, d1 = u_couple
    k2, d2 = v_couple

    a = similarity_set_partial(k1, k2)
    b = similarity_set_partial(d1, d2)

    return a, b


def get_info(website, tnweb):
    """retrieve information about keywords and description of a website, using the precomputed
    dictionary that have dict[id website] = _source"""
    klist = set()
    dlist = set()

    item = tnweb[website]

    # if the keywords field exists, retrieve it
    if u'keywords' in item.keys():
        keywords = item[u'keywords']
        keywords = similar.tokenize_keywords(keywords)
        for keyword in keywords:
            if keyword in model_2.vocab:
                klist |= {keyword}

    # if the description field exists, retrieve it
    if u'description' in item.keys():
        description = item[u'description']
        description = similar.tokenize_description(description)
        for word in description:
            if word in model_1.vocab:
                dlist |= {word}

    return klist, dlist


def get_tnweb_dict(url_list):
    """get the dictionary[id website] = source from the url lists that come from the
    companies with headquarter in Trento. since not all id are found in websites index,
    a new list without them is created"""
    new_url_list = []

    query = json.dumps({
        '_source': ['_id', 'description', 'keywords'],
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

    tnweb = dict()

    for item in response:
        tnweb[item[u'_id']] = item[u'_source']
        new_url_list.append(item[u'_id'])

    return tnweb, new_url_list


def get_dictionaries_intersect(tnweb, new_url_list):
    """having a list of url, creates a dictionary that has as keys the urls and as value
    a dictionary[word] = score"""
    most_similar_key = dict()
    most_similar_des = dict()

    for item in new_url_list:
        keywords, description = get_info(item, tnweb)
        if keywords:
            most_similar_key[item] = similar.most_similar(keywords, 'keywords')
        else:
            most_similar_key[item] = dict()

        if description:
            most_similar_des[item] = similar.most_similar(description, 'description')
        else:
            most_similar_des[item] = dict()

    return most_similar_key, most_similar_des


def get_dictionaries_mean(tnweb, new_url_list):
    """having a list of url, it creates two dictionary[website id] = set of keywords or
    set of words from tokenized/stemmed description"""
    keywords = dict()
    description = dict()

    for item in new_url_list:
        keywords[item], description[item] = get_info(item, tnweb)  # two set of words

    return keywords, description


def main():

    # load all the Trento city companies websites
    url_list = []

    with open("source/websites_trento.csv", "r") as asd1:
        reader = csv.reader(asd1)
        for line1 in reader:
            url_list.append(line1[1][7:])

    # create dictionary[website1-website2] = similarity

    # construct_dict_intersection(url_list, 'source/TnWsSimInt.pkl')

    construct_dict_mean(url_list, 'source/TnWsSimMean.pkl')


if __name__ == '__main__':
    main()
