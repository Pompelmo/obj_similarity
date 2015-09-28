from gen_json import CreateJson
from loading import loading

tfidf, index, tfidf_dict, tfidf_web, mean_dict, ball_tree, w2v_model, d2v_model = loading()       # load the models

# class for rank, len, score computation
c_json = CreateJson(tfidf, index, tfidf_dict, tfidf_web, mean_dict, ball_tree, w2v_model, d2v_model)


def loss():
    print
    print "insert loss score for the value not present in a model:"

    while True:
        print "insert loss score:"
        lss = raw_input("--> ")
        try:
            lss = float(lss)
            break
        except ValueError:
            print "wrong input"

    return lss


def weight():
    print
    print "insert weights (lambdas) to use"
    while True:
        print "insert weight for the word2vec model"
        w2v_weight = raw_input("--> ")
        try:
            w2v_weight = float(w2v_weight)
            break
        except ValueError:
            print "wrong input"

    while True:
        print "insert weight for the doc2vec model"
        d2v_weight = raw_input("--> ")
        try:
            d2v_weight = float(d2v_weight)
            break
        except ValueError:
            print "wrong input"

    while True:
        print "insert weight for the tfidf model"
        tfidf_weight = raw_input("--> ")
        try:
            tfidf_weight = float(tfidf_weight)
            break
        except ValueError:
            print "wrong input"

    return w2v_weight, d2v_weight, tfidf_weight

def parameters_inp():
    print
    print "insert exponential value for input websites"
    while True:
        print "insert exponential for the input website keywords normalized length:"
        mu_in_w = raw_input("--> ")
        try:
            mu_in_w = float(mu_in_w)
            break
        except ValueError:
            print "wrong input"

    while True:
        print "insert exponential for the input website description normalized length:"
        mu_in_d = raw_input("--> ")
        try:
            mu_in_d = float(mu_in_d)

            break
        except ValueError:
            print "wrong input"

    while True:
        print "insert exponential for the input website text normalized length:"
        mu_in_t = raw_input("--> ")
        try:
            mu_in_t = float(mu_in_t)
            break
        except ValueError:
            print "wrong input"

    print
    print "now insert exponential values for the suggested websites"

    while True:
        print "insert exponential for the suggested websites keywords normalized length:"
        mu_out_w = raw_input("--> ")
        try:
            mu_out_w = float(mu_out_w)
            break
        except ValueError:
            print "wrong input"

    while True:
        print "insert exponential for the suggested websites description normalized length"
        mu_out_d = raw_input("--> ")
        try:
            mu_out_d = float(mu_out_d)
            break
        except ValueError:
            print "wrong input"

    while True:
        print "insert exponential for the suggested websites text normalized length"
        mu_out_t = raw_input("--> ")
        try:
            mu_out_t = float(mu_out_t)
            break
        except ValueError:
            print "wrong input"

    return mu_in_w, mu_in_d, mu_in_t, mu_out_w, mu_out_d, mu_out_t


def change_function():
    c_json.loss = loss()

    c_json.w2v_weight, c_json.d2v_weight, c_json.tfidf_weight = weight()

    c_json.mu_in_w, c_json.mu_in_d, c_json.mu_in_t, c_json.mu_out_w, c_json.mu_out_d, c_json.mu_out_t = parameters_inp()


def get_right_url(url):

    while True:
        try:
            print c_json.get_json(url)
            break
        except IndexError:
            print "wrong input, try again"
            url = raw_input("--> ")


def main():
    print "get most similar websites according to: "
    print " * word2vec model on websites keywords"
    print " * doc2vec model on websites description "
    print " * tf-idf model on websites text"
    print
    print "function will be of the kind:"
    print "f(w_i,w_s) = lambda_1 * Similarity_1(w_in,w_s) * l_i_1 ** mu_i_1 * l_s_1 ** mu_s_1 + ..."
    print
    print "where w = websites, i = input, s = suggested, l = length, mu = exponent, numbers indicates the model"
    print
    print "define the lambdas to use:"
    print
    print "define parameters to use: "
    change_function()
    print
    print "insert website: "
    word = raw_input("--> ")
    get_right_url(word)

    while True:

        print
        print "insert a new website, 'change' to change total score function, or 'stop' to exit"
        word = raw_input("--> ")

        if word == 'stop':
            break

        elif word == 'change':
            change_function()

        else:
            get_right_url(word)


if __name__ == '__main__':
    main()
