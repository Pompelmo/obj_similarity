# ---------------------------------------------------
# script that compute a weighted query using
# w2v-enriched information from a given website, in
# order to find similar websites
# ---------------------------------------------------

# at the moment this doesn't work, due to the fact that elasticsearch
# index doesn't use stemmed words, but this script does.

import gensim
from elasticsearch import Elasticsearch
from collections import OrderedDict
import certifi
import json
import re
import nltk
import globalvariable as gv

gv.init()


def main():
    prova = Suggest()
    prova.similar(["www.auto-futura.it"])


class Suggest(object):
    def __init__(self):
        # load the two models
        self.description = gensim.models.Word2Vec.load('/Users/Kate/Desktop/SpazioDati/w2vmodel_description_stemmed')
        self.keywords = gensim.models.Word2Vec.load('/Users/Kate/Desktop/SpazioDati/w2vmodel_keywords_stemmed')

        # create elasticsearch client for the queries
        self.http = gv.http
        self.index = gv.index
        self.es = Elasticsearch([self.http], use_ssl=True, verify_certs=True, ca_certs=certifi.where())

        # stop words and stemmer for italian words
        self.stemmer = nltk.stem.snowball.ItalianStemmer()  # ignore_stopwords=True)
        self.stop_words = self.get_stop_words("/Users/Kate/Desktop/SpazioDati/stopword.txt")

    def most_similar(self, words, method):
        """having a list of words, creates a dictionary word-score from the w2v model"""

        similar_words = dict()
        # keep all original word with score 1
        if method == 'keywords':
            for word in words:
                similar_words[word] = 1           # the code may have some problem, i changed from list of array to dict

            model = self.keywords

        elif method == 'description':
            for word in words:
                similar_words[word] = 1           # the code may have some problem, i changed from list of array to dict

            model = self.description
        else:
            print "Method error"
            return None

        for word in words:
            # if the word is in the vocabulary ->
            if word in model.vocab:
                # -> take the (10 by default) most similar word in word2vec model
                dlist = model.most_similar(word)

                for item in dlist:
                    # check that we don't have duplicates
                    # if we have them, keep the one with higher score
                    if item[0] not in similar_words.keys():
                        similar_words[item[0]] = item[1]
                    else:
                        # u is the index of the word that already appears in the similar words set
                        if similar_words[item[0]] < item[1]:
                            # if the score is higher, substitute
                            similar_words[item[0]] = item[1]

        return similar_words

    def similar(self, id_website):
        """retrieve information from a website and then use it to make a weighted query"""
        klist = []
        dlist = []

        # query to retrieve the needed information
        query = json.dumps({
            '_source': ['_id', 'description', 'keywords'],
            'query': {
                'filtered': {
                    'filter': {
                        'terms': {
                            '_id': id_website
                        }
                    }
                }
            }
        })

        response = self.es.search(index=self.index, body=query)[u'hits'][u'hits'][0]

        if u'keywords' in response[u'_source'].keys():  # search for keywords
            keywords = response[u'_source'][u'keywords']
            keywords = self.tokenize_keywords(keywords)  # tokenize and stem them
            klist = self.most_similar(keywords, 'keywords')  # enrich the set using w2v model

        if u'description' in response[u'_source'].keys():  # search for description
            description = response[u'_source'][u'description']
            description = self.tokenize_description(description)  # tokenize and stem description
            dlist = self.most_similar(description, 'description')  # enrich the set using w2v model

        if klist or dlist:  # if at least one info is non empty
            functions = []  # construct the weighted part of the query
            if klist:
                functions += self.construct_query(klist, 'keywords')  # weighted keywords part
            if dlist:
                functions += self.construct_query(dlist, 'description')  # weighted description part

            query2 = json.dumps({
                '_source': ['_id'],  # , 'description', 'keywords'],
                'query': {
                    'function_score': {
                        'query': {
                            'match_all': {}     # change here to Trento if needed
                        },
                        'functions': functions,
                        'score_mode': 'avg'
                    }
                }
            })
            response2 = self.es.search(index=self.index, body=query2)

            # uncomment to see the first ten results from elasticsearch

            # for item in response2[u'hits'][u'hits']:
            #     print item

            return response2

        else:
            print 'No keywords nor description found'

    def tokenize_description(self, sentence):
        """tokenize a sentence, eliminating stopwords and then stemming words. all the so found
        words are then returned in a list"""
        lower_string = sentence.lower()  # make it all lowercas
        token_list = []

        # find all the words, eliminating all punctuation marks
        tok_list = re.findall(r'[\w]+', lower_string)

        for word in tok_list:
            if word not in self.stop_words:
                # if they are not in the stop words set, stem them
                token_list.append(self.stemmer.stem(word))

        return token_list

    def tokenize_keywords(self, sentence):
        """since keywords is a list of words already, just eliminate numbers and stem it"""
        stemmed = []
        for w in sentence:
            n = re.sub(r'[0-9]+', "", w)

            # since keywords may be composed by one or more words, tokenize every one of them
            if n != "":
                s = ""
                for word in n.split(" "):
                    s += self.stemmer.stem(word) + " "
                stemmed.append(s[:len(s)-1])
        return stemmed

    def construct_query(self, stem_dict, field):
        functions = []
        for key in stem_dict:
            itemd = OrderedDict()
            itemd['filter'] = {'term': {field: key}}
            itemd['weight'] = stem_dict[key]
            functions.append(itemd)

        return functions

    def get_stop_words(self, stop_words_path):
        stop_words = []
        with open(stop_words_path, "r") as asd:
            for line in asd:
                stop_words.append(line)

        return set(stop_words)



if __name__ == '__main__':
    main()
