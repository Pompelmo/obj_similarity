# ------------------------------------------------------------
# script to compute the distance between two websites
# using the different models
# ------------------------------------------------------------

import numpy
import url_id_to_text as uitt
from gensim import matutils
from math import sqrt


def tfidf_distance(tfidf_dict, tfidf, web_1, web_2, loss_weight):
    """compute the distance (as a function of cosine similarity) between two websites using tfidf model"""
    try:
        text_1 = uitt.transform(web_1)               # given in input a website, return token/stem test
        text_2 = uitt.transform(web_2)
    except IndexError:                               # the website is not found in the model, return max distance
        return loss_weight

    txtbow_1 = tfidf_dict.doc2bow(text_1)           # transform in numeric vector
    txtbow_2 = tfidf_dict.doc2bow(text_2)
    vector_1 = matutils.unitvec(tfidf[txtbow_1])            # return tfidf vector of the text, normalized
    vector_2 = matutils.unitvec(tfidf[txtbow_2])

    cosine_sim = matutils.cossim(vector_1, vector_2)
    return sqrt(2.0 * (1.0 - cosine_sim)) / 2.0               # return the distance of the two vectors


def w2v_distance(mean_dict, web_1, web_2, loss_weight):
    """compute the distance (as a function of cosine similarity) between two websites using w2v model"""
    try:
        vector_1 = numpy.array(mean_dict[web_1])        # already unit vectors by construction
        vector_2 = numpy.array(mean_dict[web_2])
    except KeyError:
        return loss_weight                                  # return max distance if not found

    return float(numpy.linalg.norm(vector_1 - vector_2)) / 2.0      # return the distance of the two vectors


def d2v_distance(d2v_model, web_1, web_2, loss_weight):
    """compute the distance(as a function of cosine similarity) between two websites using d2v model"""
    try:
        cosine_sim = d2v_model.docvecs.similarity(web_1, web_2)
    except ValueError:
        return loss_weight                                  # if not present, return max distance

    if not isinstance(cosine_sim, float):
        return loss_weight

    return sqrt(2.0 * (1.0 - cosine_sim)) / 2.0     # return distance of unit vectors
