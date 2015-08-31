# --------------------------------------------------------
# load and test w2v and d2v models
# --------------------------------------------------------

import gensim


def main():
    # model_1 = gensim.models.Word2Vec.load('/Users/Kate/Desktop/SpazioDati/w2vmodel_description_stemmed')
    model_2 = gensim.models.Word2Vec.load('/Users/Kate/Desktop/SpazioDati/d2vmodel_keywords_stemmed_20')

    # 10 most similar d2v labels are accessed in this way:
    print model_2.docvecs.most_similar('www.anticapieve.net')

    # 10 most similar w2v and d2v words are accessed in this way:
    # print model_2.most_similar('pizz')
    # print model_2.most_similar('sush')
    # print model_2.most_similar('vacanz')

    # compute similarity between two (lists of) words
    # print model_1.similarity(u'sush', u'pizz')
    # print model_2.similarity(u'sush', u'pizz')

    # compute most similar words of a lists of words
    # print model_1.most_similar([u'sush', u'pizz'])
    # print model_2.most_similar([u'sush', u'pizz'])

    # if we want to explore w2v/d2v words
    # i = 0
    # for item in model_2.vocab:
    #     print item
    #     i += 1
    #     if i > 100:
    #         break

if __name__ == '__main__':
    main()
