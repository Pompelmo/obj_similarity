import gensim
import csv
from TokenStem import TokenStem
import numpy
import pickle
import sys

csv.field_size_limit(sys.maxsize)


def get_mean_dictionary(method):

    path = csv_path = ""

    if method == 'keywords':
        path = 'source/w2vmodel_keywords_stemmed'
        csv_path = 'source/websites_keywords.csv'
    elif method == 'description':
        path = 'source/w2vmodel_description_stemmed'
        csv_path = 'source/websites_description.csv'

    print "loading w2v"
    model = gensim.models.Word2Vec.load(path)
    print "loaded"
    ts = TokenStem()

    mean_dict = dict()
    i = 0

    print "start reading"

    with open(csv_path) as asd:
        read = csv.reader(asd)
        if method == 'keywords':
            for line in read:
                i += 1
                if i % 1000 == 0:
                    print "line readed: ", i
                key_list = line[1].split(";")
                keywords = ts.tokenize_keywords(key_list)
                if len(keywords) <= 30:
                    vectors = []
                    for item in keywords:
                        try:
                            vectors.append(model[item])

                        except KeyError:
                            continue

                    if vectors:
                        mean_dict[line[0]] = numpy.mean(vectors, axis=0)

        elif method == 'description':
            for line in read:
                i += 1
                if i % 1000 == 0:
                    print "line readed: ", i
                key_list = line[1]
                des_list = ts.tokenize_description(key_list)
                vectors = []
                for item in des_list:
                    try:
                        vectors.append(model[item])

                    except KeyError:
                        continue

                if vectors:
                    mean_dict[line[0]] = numpy.mean(vectors, axis=0)

    return mean_dict


def main(save_path, method):

    mean_dict = get_mean_dictionary(method)

    output = open(save_path, 'wb')

    pickle.dump(mean_dict, output)

    output.close()


if __name__ == '__main__':

    print "construct dictinary with mean vectors: input 'k' for keywords, 'd' for description, " \
          "everything else to exit"
    word = raw_input("-->")

    if word == "k":
        sp = 'source/mean_dict_key.pkl'
        main(sp, 'keywords')
        print "keyword mean vectors dictionary saved in ", sp

    elif word == "d":
        sp = 'source/mean_dict_des.pkl'
        main(sp, 'description')
        print "description mean vectors dictionary saved in ", sp

    else:
        print "Nothing done, have a nice day"
