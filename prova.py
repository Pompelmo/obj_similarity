import pickle


def main():
    # load dictionary[website1,website2] = similarity
    boh = open('/Users/Kate/Desktop/SpazioDati/TnWsSimJac.pkl', "r")
    print "start loading"
    asd = pickle.load(boh)
    print "finish loading"

    asdf = rank('yourtnwebsite', asd)
    asdf2 = rank('yourtnwebsite', asd)
    asdf3 = rank('yourtnwebsite', asd)

    for item in asdf:
        print item

    for item in asdf2:
        print item

    for item in asdf3:
        print item


def rank(website_id, score_dict, length=10):
    ranked = []
    for key in score_dict:
        if key[0] == website_id or key[1] == website_id:
            ranked.append((key, score_dict[key]))

    ranked = sorted(ranked, key=lambda x: (x[1][0] + x[1][1])/2, reverse=True)

    return ranked[:length]

if __name__ == '__main__':
    main()
