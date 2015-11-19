import gensim
import pickle
from datetime import datetime

print datetime.now(), "loading corpus"
corpus = gensim.corpora.MmCorpus('source/web_text_mm_last.mm')

print datetime.now(), "loading model for tf-idf"
tfidf = gensim.models.TfidfModel.load('source/web_text_tifidf_last.tfidf_model')  # tfidf model

print datetime.now(), "loading sim matrix Similarity"
indexS = gensim.similarities.Similarity.load('source/tfidfSim_last_100.index')         # tfidf similarity matrix

print datetime.now(), "loading sim matrix SparseMatrixSimilarity"
indexL = gensim.similarities.SparseMatrixSimilarity('source/similarity_sparse')

print datetime.now(), "loading tfidf_dict"
tfidf_dict = gensim.corpora.Dictionary.load('source/web_text_dict_last.dict')     # dictionary for word <-> id

print datetime.now(), "loading dictionary for tf-idf"
tfidf_dict_file = open('source/web_text_doc_last.pkl', 'r')
tfidf_web = pickle.load(tfidf_dict_file)                                          # dictionary for doc n <-> website
tfidf_dict_file.close()


def confront(website):
    indx = tfidf_web.values().index(website)        # try to get the index of the website

    # indx = doc_num actually
    doc_num = tfidf_web.keys()[indx]                           # now get its id (same index)

    bow = corpus[doc_num]                                      # transform it in bow
    tf_rep = tfidf[bow]                                        # get its tfidf representation

    print datetime.now(), "Similarity"
    sims1 = indexS[tf_rep][:11]                                        # query for similarity
    print sims1

    print datetime.now(), "SparseMatrixSimilarity"
    sims3 = indexL[tf_rep][:11]
    print sims3

    print datetime.now(), "end"


if __name__ == '__main__':
    confront('www.spaziodati.eu')
    confront('spaziodati.eu')
    confront('www.birreriapedavena.com')
    confront('www.ravinacar.it')
