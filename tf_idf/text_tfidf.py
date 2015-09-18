import gensim
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)  # print info

dictionary = gensim.corpora.Dictionary.load('source/web_text_dict_last.dict')

corpus = gensim.corpora.MmCorpus('source/web_text_mm_last.mm')  # load the bow corpus

print corpus  # it prints number of documents, of features (unique tokens) and non-zero entities

tfidf = gensim.models.TfidfModel(corpus, normalize=True)    # initialize a model, normalize the vectors to unit length

corpus_tfidf = tfidf[corpus]  # create a wrapper around the old corpus document stream

tfidf.save('source/web_text_tifidf_last.tfidf_model')  # save tfidf model

index = gensim.similarities.Similarity('source/similarity_index_last', corpus_tfidf, num_features=len(dictionary))

index.save('source/tfidfSim_last.index')  # save the similarity matrix
