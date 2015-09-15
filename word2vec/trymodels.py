# --------------------------------------------------------
# load and test w2v and d2v models
# --------------------------------------------------------

import gensim


def load_model():
    # load model:
    model = []
    mtype = []
    condition = True
    while condition:
        print "Which model do you want to load?"
        print "Write 'A' for w2v keywords, 'B' for w2v description, 'C' for d2v keywords, 'D' for d2v description"
        mod = raw_input('--> ')
        if mod == "A":
            model = gensim.models.Word2Vec.load('source/w2vmodel_keywords_stemmed')
            mtype = "w2v"
            condition = False
        elif mod == "B":
            model = gensim.models.Word2Vec.load('source/w2vmodel_description_stemmed')
            mtype = "w2v"
            condition = False
        elif mod == "C":
            model = gensim.models.Doc2Vec.load('source/d2vkeywords')
            mtype = "d2v"
            condition = False
        elif mod == "D":
            model = gensim.models.Doc2Vec.load('source/d2vdescription')
            mtype = "d2v"
            condition = False
        elif mod == "stop":
            condition = False
        else:
            print "wrong input. retry or write 'stop' to exit"

    return model, mtype


def trymodel(model, mtype):
    if model:
        if mtype == "w2v":
            word = ""

            print "Input a (tokenized and stemmed) word for query the model, or 'stop' for exit"
            word = raw_input("--> ")

            while word != "stop":
                try:
                    ms = model.most_similar(word)
                    print ms, "\n"
                except KeyError:
                    print "Ops! The word is not in the model. Try again...\n"

                print "Input a (tokenized and stemmed) word for query the model, or 'stop' for exit"
                word = raw_input("--> ")

        elif mtype == "d2v":
            word = ""

            while word != "stop":

                print "Input 'W' for querying a website, 'P' for querying a word, 'stop' for exit"
                word = raw_input("--> ")

                if word == "W":
                    print "Input a website (without http://):"
                    word = raw_input("--> ")

                    try:
                        ms = model.docvecs.most_similar(word), "\n"
                        print ms, "\n"
                    except KeyError:
                        print "Ops! The website is not in the model. Try again...", "\n"

                elif word == "P":
                    print "Input a (tokenized and stemmed) word for query the model:"
                    word = raw_input("--> ")

                    try:
                        ms = model.most_similar(word)
                        print ms, "\n"
                    except KeyError:
                        print "Ops! The word is not in the model. Try again...", "\n"


def main():
    condition = True
    while condition:
        model, mtype = load_model()
        trymodel(model, mtype)

        print "\n", "Do you want to try another model? [Y/N]"
        a = raw_input("--> ")
        if a == "N":
            condition = False


if __name__ == '__main__':
    main()
