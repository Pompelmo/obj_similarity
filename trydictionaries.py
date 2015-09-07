import pickle


def main():
    # load dictionary[website1,website2] = similarity
    boh = open('source/TnWsSimJac.pkl', "r")
    print "start loading"
    asd = pickle.load(boh)
    print "finish loading"

    print '\n', "Insert a website to start computing its most similar websites,"
    print "according to entities similarity, or 'stop' to exit: "
    word = raw_input("--> ")

    while word != "stop":
        ranked = most_similar(word, asd)
        if ranked:
            for item in ranked:
                print item
        else:
            print "Ooops, seems your website it's not in the dictionary"

        print '\n', "Insert a website to start computing its most similar websites,"
        print "according to entities similarity, or 'stop' to exit: "
        word = raw_input("--> ")


def most_similar(website_id, score_dict, length=10):
    ranked = []
    for key in score_dict:
        if key[0] == website_id or key[1] == website_id:
            ranked.append((key, score_dict[key]))

    ranked = sorted(ranked, key=lambda x: (x[1][0] + x[1][1])/2, reverse=True)

    return ranked[:length]

if __name__ == '__main__':
    main()
