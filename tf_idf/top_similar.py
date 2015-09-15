import pickle
import gensim
import url_id_to_text as uitt

tfidf = gensim.models.TfidfModel.load('source/web_text_tifidf_2.tfidf_model')
index = gensim.similarities.Similarity.load('source/tfidfSim.index')
dictionary = gensim.corpora.Dictionary.load('source/web_text_dict.dict')

output = open('source/web_text_doc.pkl', 'r')       # read dictionary[number of input document] = relative website
mean_dict = pickle.load(output)
output.close()


def most_similar(url_id):
    text = uitt.transform(url_id)                   # given in input a website, return token/stem test
    txtbow = dictionary.doc2bow(text)
    vector = tfidf[txtbow]                            # return tfidf vector of the text
    sims = index[vector]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])  # compute similarity,
    for ite in sims:
        print ite, mean_dict[ite[0]]


def main():
    print "input a website to compute 10 most similar websites according to tf_idf, or 'stop' to exit"
    word = raw_input("--> ")

    while word != "stop":

        most_similar(word)
        print "input a website to compute 10 most similar websites according to tf_idf, or 'stop' to exit"
        word = raw_input("--> ")

if __name__ == '__main__':
    main()
