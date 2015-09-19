# -------------------------------------------------------------
# script to compute the top n similar or n nearest
# websites to a given website
# -------------------------------------------------------------


import url_id_to_text as uitt
from how_many import Counter
from gensim.models import Word2Vec


class Integration(object):
    def __init__(self, tfidf, index, tfidf_dict, tfidf_web, mean_dict, nrbs, d2v_model):
        self.tfidf = tfidf                      # tfidf model
        self.index = index                      # tfidf similarity matrix
        self.tfidf_dict = tfidf_dict            # dictionary for word <-> id
        self.tfidf_web = tfidf_web              # dictionary for doc n <-> website
        self.nrbs = nrbs                        # nearest neighbors ball tree structure
        self.mean_dict = mean_dict              # mean vector <-> website
        self.d2v_model = d2v_model              # description doc2vec model
        self.w2v_model = Word2Vec.load('source/w2vmodel_keywords_scan')                 # keywords word2vec model
        self.cc = Counter(self.w2v_model, self.d2v_model, self.tfidf_dict, self.tfidf)  # counter for keywords/token

    def ms_tfidf(self, url_id, n):
        """compute most similar websites using tfidf text model"""
        try:
            text = uitt.transform(url_id)                   # given in input a website, return token/stem test
        except IndexError:                                  # the website is not found in the model,
            return [""]*n, [""]*n, [0]*n                    # return empty scores and empty rank

        txtbow = self.tfidf_dict.doc2bow(text)              # transform in numeric vector
        vector = self.tfidf[txtbow]                         # return tfidf vector of the text
        sims = self.index[vector]                           # return similarity matrix index
        sims = sorted(enumerate(sims), key=lambda item: -item[1])[:n]  # compute similarity

        rank = []
        scores = []
        length_text = []

        for ite in sims:
            url = self.tfidf_web[ite[0]]                    # find document website name
            rank.append(url)                                # append website name
            scores.append(ite[1])                           # append score (the higher the better)
            length_text.append(self.cc.count_text(url))     # count non zero tfidf tokens

        return scores, rank, length_text

    def ms_w2v_key(self, url_id, n):
        """compute most similar websites using w2v keywords model"""
        try:                                            # try to find a website in the dictionary
            value = self.mean_dict[url_id]              # that associates name with mean vector value
        except KeyError:
            return [""]*n, [""]*n, [0]*n                # otherwise return empty rank and empty score

        # compute the nearest neighbors with the constructed ball_tree
        distance, index = self.nrbs.kneighbors([value], n_neighbors=n+1, return_distance=True)

        # transform the result in lists
        dist = distance.tolist()[0]
        ind = index.tolist()[0]

        keys = self.mean_dict.keys()
        # have the list of websites names:
        # recall that dict.keys()[i] = key and dict.values()[i] = value are such that dict[key] = value

        rank = []
        scores = []
        length_token = []

        for i in range(0, len(dist)):
            if keys[ind[i]] != url_id:              # do not return the same website
                url = keys[ind[i]]
                rank.append(url)                    # append website name
                scores.append(dist[i])              # append distance
                length_token.append(self.cc.count_keywords(url))

        return scores, rank, length_token

    def ms_d2v(self, url_id, n):
        """compute the most similar websites using d2v descriptions model"""
        try:
            ms = self.d2v_model.docvecs.most_similar(url_id, topn=n)        # compute most similar with d2v
        except KeyError:
            return [""]*n, [""]*n          # if the website is not present in the model, return empty rank and scores

        rank = []
        scores = []
        length_token = []

        for item in ms:
            rank.append(item[0])                    # compute rank and scores list
            scores.append(item[1])
            length_token.append(self.cc.count_description(item[0]))

        return scores, rank, length_token
