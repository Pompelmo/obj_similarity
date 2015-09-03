# obj_similarity

train word2vec model using trainw2v.py or doc2vec model using traind2v.py

for a doc2vec with some iteration (see also https://github.com/piskvorky/gensim/blob/develop/docs/notebooks/doc2vec-IMDB.ipynb)
use doc2vecEpoch.py

once you constructed your model you can query them using trymodels.py

you can also used them to compute some kind of similarity between two websites using suggestion_2.py
use suggestion_1.py insted for using information to perform an elasticsearch query!

it is possible to have some kind of similarity between two websites using their wikipedia entities! 
use entities_similarity_v1.py to compute similarity of all possible Trento companies websites, and then 
ask for the similarity using tryEntities.
