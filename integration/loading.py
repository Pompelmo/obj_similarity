import pickle
import gensim
import numpy as np
from sklearn.neighbors import NearestNeighbors


def loading():

    print "loading model for tf-idf"
    tfidf = gensim.models.TfidfModel.load('source/web_text_tifidf.tfidf_model')
    index = gensim.similarities.Similarity.load('source/tfidfSim.index')
    tfidf_dict = gensim.corpora.Dictionary.load('source/web_text_dict.dict')

    print "loading dictionary for tf-idf"
    tfidf_dict_file = open('source/web_text_doc.pkl', 'r')
    tfidf_web = pickle.load(tfidf_dict_file)
    tfidf_dict_file.close()

    print "loading dictionary for w2v keywords n_similarity"
    mean_dict_file = open('source/mean_dict_key_scan.pkl', 'r')
    mean_dict = pickle.load(mean_dict_file)
    mean_dict_file.close()

    print "computing nearest neighbor ball tree"
    values = mean_dict.values()
    arrays = np.array(values)
    nbrs = NearestNeighbors(n_neighbors=11, radius=1.0, algorithm='ball_tree', p=2, metric='euclidean')
    nbrs.fit(arrays)

    print "loading d2v description model"
    d2v_model = gensim.models.Doc2Vec.load('source/d2vdescription')

    return tfidf, index, tfidf_dict, tfidf_web, mean_dict, nbrs, d2v_model
