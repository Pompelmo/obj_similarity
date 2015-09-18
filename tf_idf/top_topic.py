import gensim
import url_id_to_text as uitt

tfidf = gensim.models.TfidfModel.load('source/web_text_tifidf.tfidf_model')
dictionary = gensim.corpora.Dictionary.load('source/web_text_dict.dict')


def top_words(url_id):
    try:
        text = uitt.transform(url_id)                   # given in input a website, return token/stem test
    except IndexError:
        print "this website is not in the index, try again..."
        return None

    txtbow = dictionary.doc2bow(text)
    vector = tfidf[txtbow]
    highest = sorted(vector, key=lambda item: -item[1])[:10]
    for el in highest:
        print el[1], dictionary[el[0]]


def main():
    print "write a website to see its top topic, or 'stop' to exit"
    word = raw_input("--> ")

    while word != "stop":
        top_words(word)
        print
        print "write a website to see its top topic, or 'stop' to exit"
        word = raw_input("--> ")


if __name__ == '__main__':
    main()
