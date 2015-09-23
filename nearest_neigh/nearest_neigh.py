from sklearn.neighbors import NearestNeighbors
import numpy as np
import pickle


def load_dictionary(method):

    path = ""
    if method == 'keywords':
        path = 'source/mean_dict_key.pkl'
    elif method == 'description':
        path = 'source/mean_dict_des.pkl'

    print 'load dictionary'
    dict_input = open(path, 'r')
    mean_dictionary = pickle.load(dict_input)
    dict_input.close()
    print 'dictionary loaded'

    return mean_dictionary


def nearest_neighbors(mean_dictionary):

    values = mean_dictionary.values()
    arrays = np.array(values)

    nbrs = NearestNeighbors(n_neighbors=11, radius=1.0, algorithm='ball_tree', p=2, metric='euclidean')

    nbrs.fit(arrays)

    return nbrs


def query(url_id, mean_dictionary):

    try:
        value = mean_dictionary[url_id]
    except KeyError:
        return False

    nbrs = nearest_neighbors(mean_dictionary)

    distance, index = nbrs.kneighbors([value], n_neighbors=11, return_distance=True)
    dist = distance.tolist()[0]
    # print dist
    ind = index.tolist()[0]
    # print ind

    keys = mean_dictionary.keys()

    print "computing rank"
    for i in range(0, len(dist)):
        print keys[ind[i]], dist[i]

    return True


def main():

    print "query similarity using mean value of keywords(k) or description(d) in word2vec"
    print "input 'k' for keyword or 'd' for description, anything else to exit"
    word = raw_input("--> ")

    if word == "k":
        md = load_dictionary('keywords')
    elif word == "d":
        md = load_dictionary('description')
    else:
        return None

    while word != "stop":
        print
        print "input a website or 'stop' to exit"
        word = raw_input("--> ")
        similar = query(word, md)

        if not similar and word != 'stop':
            print "website not present"

    return None

if __name__ == '__main__':
    main()
