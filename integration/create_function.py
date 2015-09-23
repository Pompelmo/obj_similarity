# ------------------------------------------------------------
# script to generate the function to compute the scores
# ------------------------------------------------------------


def create_function(method, w2v_score, d2v_score, tfidf_score, w2v_weight, d2v_weight, tfidf_weight,
                    w2v_meta, d2v_meta, tfidf_meta):

    if method == 'linear':
        score = w2v_weight * w2v_score + d2v_weight * d2v_score + tfidf_weight * tfidf_score

    elif method == 'multiplicative':
        score = w2v_weight * w2v_score * d2v_weight * d2v_score * tfidf_weight * tfidf_score

    elif method == 'linear_meta':
        score = w2v_weight * w2v_score * w2v_meta + d2v_weight * d2v_score * d2v_meta \
            + tfidf_weight * tfidf_score * tfidf_meta

    elif method == 'mult_meta':
        score = w2v_weight * w2v_score * w2v_meta * d2v_weight * d2v_score * d2v_meta \
            * tfidf_weight * tfidf_score * tfidf_meta

    else:
        return 0

    return score
