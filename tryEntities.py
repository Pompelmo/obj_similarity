import pickle


def load_en_dict():
    boh = open('source/EntitiesSimilarity.pkl', "r")
    print "start loading the dictionary of the entity similarity model!"
    asd = pickle.load(boh)
    print "loaded!!!"
    return asd


def most_similar(website, entity_dict, length=10):
    ranked = []

    for key in entity_dict:
        if key[0] == website or key[1] == website:
            ranked.append((key, entity_dict[key]))

    ranked = sorted(ranked, key=lambda x: x[1], reverse=True)

    return ranked[:length]


def main():
    entity_dict = load_en_dict()

    print '\n', "Insert a website to start computing its most similar websites,"
    print "according to entities similarity, or 'stop' to exit: "
    word = raw_input("--> ")

    while word != "stop":
        ranked = most_similar(word, entity_dict)
        if ranked:
            for item in ranked:
                print item
        else:
            print "Ooops, seems your website it's not in the dictionary"

        print '\n', "Insert a website to start computing its most similar websites,"
        print "according to entities similarity, or 'stop' to exit: "
        word = raw_input("--> ")


if __name__ == '__main__':
    main()
