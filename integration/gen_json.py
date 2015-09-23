# ------------------------------------------------------------
# script to generate the json object with websites similar
# to inout website and their scores
# ------------------------------------------------------------

from how_many import Counter
from pairwise_distance import *
import json
from integration import Integration
from loading import loading
from create_function import create_function


class CreateJson(object):
    def __init__(self, tfidf, index, tfidf_dict, tfidf_web, mean_dict, ball_tree, w2v_model, d2v_model):
        self.tfidf = tfidf                      # tfidf model
        self.index = index                      # tfidf similarity matrix
        self.tfidf_dict = tfidf_dict            # dictionary for word <-> id
        self.tfidf_web = tfidf_web              # dictionary for doc n <-> website
        self.ball_tree = ball_tree              # nearest neighbors ball tree structure
        self.mean_dict = mean_dict              # mean vector <-> website
        self.d2v_model = d2v_model              # description doc2vec model
        self.w2v_model = w2v_model              # keywords word2vec model
        self.loss = 1.0                             # loss score for the NOT FOUND elements
        self.method = 'linear'                      # method used by the total score function
        self.w2v_weight = 1.0                       # weight used in the total score function
        self.d2v_weight = 1.0                       # ditto
        self.tfidf_weight = 1.0                     # ditto
        self.counter = Counter(self.w2v_model, self.d2v_model,
                               self.tfidf_dict, self.tfidf)             # counter for keywords/token
        # to have the integration functions
        self.integrate = Integration(self.tfidf, self.index, self.tfidf_dict, self.tfidf_web,
                                     self.mean_dict, self.ball_tree, self.w2v_model, self.d2v_model)

    def inp_web_info(self, url, explicit=False):
        """information on the input website"""

        keywords = self.counter.count_keywords(url)             # get keywords number
        description = self.counter.count_description(url)       # get description tokens
        text_tokens = self.counter.count_text(url)              # get count of text tokens

        # if explicit = True, keywords and description tokens are explicitly written
        if explicit:
            input_dict = {'metadata': {'keywords': keywords, 'description': description,
                                       'keywords_number': len(keywords), 'desc_tokens': len(description),
                                       'text_tokens': text_tokens}}
        else:
            input_dict = {'metadata': {'keywords_number': len(keywords), 'desc_tokens': len(description),
                                       'text_tokens': text_tokens}}

        return input_dict

    def text_websites(self, url):
        """compute the 20 websites most similar according to tfidf, and compute their value also in the other models"""

        # get 20 most similar web according to tfidf
        tfidf_score, tfidf_rank, tfidf_l = self.integrate.ms_tfidf(url, n=20)
        text_dict = dict()              # empty dict for json obj creation

        for i in range(0, len(tfidf_rank)):         # for every similar website

            item = tfidf_rank[i]                    # get its name
            metadata = self.inp_web_info(item)      # and its metadata

            text_dict[item] = metadata              # json obj I part: metadata

            w2v_s = w2v_distance(self.mean_dict, url, item, self.loss)      # distance according to w2v model
            d2v_s = d2v_distance(self.d2v_model, url, item, self.loss)      # distance according to d2v model

            scores = {'w2v': w2v_s,                 # json obj II part: scores according to the three models
                      'd2v': d2v_s,
                      'tfidf': tfidf_score[i]}

            text_dict[item].update({'scores': scores})

            # json obj III part: the total score, computed as some function of scores and metadata
            w2v_d = metadata['metadata']['keywords_number']     # retrieve single metadata in order to use them for
            d2v_d = metadata['metadata']['desc_tokens']         # the score function
            tfidf_d = metadata['metadata']['text_tokens']

            # compute the total score
            total_score = self.score_func(self.method, w2v_s, d2v_s, tfidf_score[i], self.w2v_weight,
                                          self.d2v_weight, self.tfidf_weight, w2v_d, d2v_d, tfidf_d)

            text_dict[item].update({'total_score': total_score})

        return text_dict

    def d2v_websites(self, url):
        """compute the 20 websites most similar according to tfidf, and compute their value also in the other models"""
        d2v_score, d2v_rank, d2v_l = self.integrate.ms_d2v(url, n=20)    # get 20 most similar websites according to d2v
        d2v_dict = dict()           # empty dict for json obj creation

        for i in range(0, len(d2v_rank)):               # for every similar website

            item = d2v_rank[i]                  # get its name
            metadata = self.inp_web_info(item)  # and retrieve its metadata

            d2v_dict[item] = metadata               # json obj I part: metadata

            w2v_s = w2v_distance(self.mean_dict, url, item, self.loss)   # distance according to w2v model
            tfidf_s = tfidf_distance(self.tfidf_dict, self.tfidf, url, item, self.loss)  # and according to tfidf

            scores = {'w2v': w2v_s,                 # json obj II part: scores according to the three models
                      'd2v': d2v_score[i],
                      'tfidf': tfidf_s}

            d2v_dict[item].update({'scores': scores})

            # json obj III part: the total score, computed as some function of scores and metadata
            w2v_d = metadata['metadata']['keywords_number']     # retrieve single metadata in order to use them for
            d2v_d = metadata['metadata']['desc_tokens']         # the score function
            tfidf_d = metadata['metadata']['text_tokens']

            # compute the total score
            total_score = self.score_func(self.method, w2v_s, d2v_score[i], tfidf_s, self.w2v_weight,
                                          self.d2v_weight, self.tfidf_weight, w2v_d, d2v_d, tfidf_d)

            d2v_dict[item].update({'total_score': total_score})

        return d2v_dict

    def w2v_websites(self, url):
        """compute the 20 websites most similar according to tfidf, and compute their value also in the other models"""
        w2v_score, w2v_rank, w2v_l = self.integrate.ms_w2v_key(url, n=20)     # get 20 most similar web according to w2v
        w2v_dict = dict()             # empty dict for json obj creation

        for i in range(0, len(w2v_rank)):               # for every similar website

            item = w2v_rank[i]                          # get its name
            metadata = self.inp_web_info(item)          # and retrieve its metadata

            w2v_dict[item] = metadata                   # json obj I part: metadata

            d2v_s = d2v_distance(self.d2v_model, url, item, self.loss)    # compute the distance according to d2v model
            tfidf_s = tfidf_distance(self.tfidf_dict, self.tfidf, url, item, self.loss)     # and according to tfidf

            scores = {'w2v': w2v_score[i],              # json obj II part: scores according to the three models
                      'd2v': d2v_s,
                      'tfidf': tfidf_s}

            w2v_dict[item].update({'scores': scores})

            # json obj III part: the total score, computed as some function of scores and metadata
            w2v_d = metadata['metadata']['keywords_number']     # retrieve single metadata in order to use them for
            d2v_d = metadata['metadata']['desc_tokens']         # the score function
            tfidf_d = metadata['metadata']['text_tokens']

            # compute the total score
            total_score = self.score_func(self.method, w2v_score[i], d2v_s, tfidf_s, self.w2v_weight,
                                          self.d2v_weight, self.tfidf_weight, w2v_d, d2v_d, tfidf_d)

            w2v_dict[item].update({'total_score': total_score})

        return w2v_dict

    def get_json(self, url):
        """generate the json object with the wanted information"""
        txt_web = self.text_websites(url)               # construct dictionary with tfidf similar websites
        w2v_web = self.w2v_websites(url)                # construct dictionary with word2vec similar websites
        d2v_web = self.d2v_websites(url)                # construct dictionary doc2vec similar websites

        txt_web.update(w2v_web)                     # update first dictionary with the second, to avoid repetitions
        txt_web.update(d2v_web)                     # and update also with the third one.

        # now a json obj is created: metadata of the input website, with the output given by the three models
        json_obj = json.dumps({url: self.inp_web_info(url, explicit=True),
                               'output': txt_web},
                              indent=4, separators=(",", ":"))
        # should be ordered according to the total score

        return json_obj

    def score_func(self, method, w2v_score, d2v_score, tfidf_score, w2v_weight, d2v_weight, tfidf_weight,
                   w2v_meta, d2v_meta, tfidf_meta):

        # I don't know if it's necessary...
        return create_function(method, w2v_score, d2v_score, tfidf_score, w2v_weight, d2v_weight, tfidf_weight,
                               w2v_meta, d2v_meta, tfidf_meta)


def main():
    """run the main for an example :)"""
    tfidf, index, tfidf_dict, tfidf_web, mean_dict, ball_tree, w2v_model, d2v_model = loading()       # load the models

    # class for rank, len, score computation
    cs = CreateJson(tfidf, index, tfidf_dict, tfidf_web, mean_dict, ball_tree, w2v_model, d2v_model)

    print cs.get_json('www.spaziodati.eu')

if __name__ == '__main__':
    main()
