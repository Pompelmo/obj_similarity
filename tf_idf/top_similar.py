import pickle
import gensim
import url_id_to_text as uitt

# tfidf = gensim.models.TfidfModel.load('source/web_text_tifidf_2.tfidf_model')
index = gensim.similarities.Similarity.load('source/tfidfSim.index')

output = open('source/web_text_doc.pkl', 'r')
mean_dict = pickle.load(output)
output.close()


def most_similar(url_id):
    text = uitt.transform(url_id)
    vector = index[text]
    sims = sorted(enumerate(vector), key=lambda item: -item[1])
    for item in sims:
        print


def main():
    pass

if __name__ == '__main__':
    main()
