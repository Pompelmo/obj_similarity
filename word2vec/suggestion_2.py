# ----------------------------------------------------
# script that compute similarity between all possible
# websites of companies in Trento city
# ----------------------------------------------------

# sarebeb da cambiar il modo in cui si prendono le informazioni
# poiche' ho un dizionario id-source

import certifi
import gensim
import pickle
import json
from elasticsearch import Elasticsearch
import suggestion_1
from TokenStem import TokenStem
import globalvariable as gv
import scan_tn_web_idg as stwi

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

# class for eliminate stopwords, tokenize and stem words
stem = TokenStem()

# object to use the enrich function (for the similarity between sets)
similar_key = suggestion_1.Suggest(model_2)
similar_des = suggestion_1.Suggest(model_1)


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


def get_info(website_id, field):
    # query to retrieve the needed information
    query = json.dumps({
        '_source': ['_id', field],
        'query': {
            'filtered': {
                'filter': {
                    'bool': {
                        'must': [
                            {
                                'term': {'_id': website_id}
                            },
                            {
                                'exists': {'field': field}
                            }
                        ]
                    }
                }
            }
        }
    })

    response = es.search(index=index, body=query)[u'hits'][u'hits']

    if response:                                                # if the website has the field
        if field == 'keywords':                                 # search for keywords
            keywords = response[0][u'_source'][u'keywords']
            info_list = stem.tokenize_keywords(keywords)        # tokenize and stem them

        elif field == 'description':                            # search for description
            description = response[0][u'_source'][u'description']
            info_list = stem.tokenize_description(description)  # tokenize and stem description

        else:
            print "wrong field"
            info_list = []

    else:
        info_list = []

    return set(info_list)


def get_dictionaries_intersect(new_url_list):
    """having a list of url, creates a dictionary that has as keys the urls and as value
    a dictionary[word] = score"""
    most_similar_key = dict()
    most_similar_des = dict()

    for item in new_url_list:
        keywords, description = get_info(item, 'keywords'), get_info(item, 'description')
        if keywords:
            most_similar_key[item] = similar_key.most_similar(keywords)
        else:
            most_similar_key[item] = dict()

        if description:
            most_similar_des[item] = similar_des.most_similar(description)
        else:
            most_similar_des[item] = dict()

    return most_similar_key, most_similar_des


def get_dictionaries_mean(new_url_list):
    """having a list of url, it creates two dictionary[website id] = set of keywords or
    set of words from tokenized/stemmed description"""
    keywords = dict()
    description = dict()

    for website in new_url_list:
        keywords[website] = get_info(website, 'keywords')
        description[website] = get_info(website, 'description')  # two set of words

    return keywords, description


def construct_dict(url_list, save_path, similarity):
    """create and save as a pickle object dictionary with key couple of websites and value
    their similarity computed as some strange measure derived from jaccard similarity"""
    sim_dict = dict()
    new_ul = stwi.scan_tn_web_idg()

    if similarity == 'mean':
        most_similar_key, most_similar_des = get_dictionaries_mean(url_list)

    elif similarity == 'intersection':
        most_similar_key, most_similar_des = get_dictionaries_intersect(url_list)

    else:
        print 'wrong similarity input'
        return None

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


def main():

    # load all the Trento city companies websites
    url_list = stwi.scan_tn_web_idg().keys()

    # create dictionary[website1-website2] = similarity

    # construct_dict_intersection(url_list, 'source/TnWsSimInt.pkl')

    construct_dict(url_list, 'source/TnWsSimMean.pkl', 'mean')


if __name__ == '__main__':
    main()

