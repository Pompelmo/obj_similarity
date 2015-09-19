# ---------------------------------------------------------------
# script for query models for most similar / nearest
# websites, using:
# * n_similarity method on a word2vec models trained on keywords
# * query the doc2vec description model on tags(=websites)
# * tfidf similarity on tfidf model trained on websites text
#
# and print them in a table with scores and length of
# keywords / tokens used
# ---------------------------------------------------------------


from loading import loading
from integration import Integration
from prettytable import PrettyTable  # to generate the table to print


def tabella(url_id, n, integrate):
    """generate the table to print on the shell"""

    w2v_score, w2v_rank, w2v_l = integrate.ms_w2v_key(url_id, n)            # w2v score, rank and n of keywords used
    d2v_score, d2v_rank, d2v_l = integrate.ms_d2v(url_id, n)                # d2v score, rank and n of token used
    tfidf_score, tfidf_rank, tfidf_l = integrate.ms_tfidf(url_id, n)        # tfidf score, rank, and n of token used

    print
    print "table for ", n, "most similar websites to ", url_id

    table = PrettyTable(["w2v score (dist)", "w2v rank", "keywords in the model",           # header
                         "d2v score (sim)", "d2v rank", "tokens in d2v model",
                         "tfidf score (sim)", "tfidf rank", "tokens in tfidf model"])

    for i in range(0, n):                                           # create the rows for the table
        table.add_row([w2v_score[i], w2v_rank[i], w2v_l[i],
                       d2v_score[i], d2v_rank[i], d2v_l[i],
                       tfidf_score[i], tfidf_rank[i], tfidf_l[i]])

    return table


def main():
    print
    tfidf, index, tfidf_dict, tfidf_web, mean_dict, nbrs, d2v_model = loading()                 # load the models

    # class for rank, len, score computation
    integrate = Integration(tfidf, index, tfidf_dict, tfidf_web, mean_dict, nbrs, d2v_model)

    print
    print "Compute the ranking and scores for the most similar websites using the following models:"
    print "-> word2vec on websites keywords"
    print "-> doc2vec on websites descriptions"
    print "-> tfidf on websites text"
    print

    while True:
        print "insert a website and the length of the rankings that you want, or 'stop' to exit:"
        word = raw_input("insert website: ")
        if word == "stop":
            break
        n = ""
        while not n.isdigit():
            n = raw_input("insert an integer: ")

        n = int(n)
        print tabella(word, n, integrate)
        print "\n"

if __name__ == '__main__':
    main()
