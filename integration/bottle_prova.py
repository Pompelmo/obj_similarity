from gen_json import CreateJson
from loading import loading
from bottle import Bottle, run, request
from parameters import parameters_choice

tfidf, index, tfidf_dict, tfidf_web, mean_dict, ball_tree, w2v_model, d2v_model = loading()       # load the models

# class for rank, len, score computation
c_json = CreateJson(tfidf, index, tfidf_dict, tfidf_web, mean_dict, ball_tree, w2v_model, d2v_model)

app = Bottle()


@app.route('/suggest')
def suggestions():

    website = request.query.website
    model = request.query.model
    only_website = boolean(request.query.only_website)

    c_json.loss, c_json.w2v_weight, c_json.d2v_weight, c_json.tfidf_weight, c_json.mu_in_w, c_json.mu_in_d, \
        c_json.mu_in_t, c_json.mu_out_w, c_json.mu_out_d, c_json.mu_out_t = parameters_choice(model)

    dictionary = c_json.get_json(website)

    if only_website:
        dictionary_sort = sorted(dictionary[u'output'].items(), key=lambda x: x[1][u'total_score'])
        dictionary = [(item[0], item[1][u'total_score']) for item in dictionary_sort]

    return dictionary

run(app, host='0.0.0.0', port=8080)


def boolean(string):
    if string in ['true', 'True', 't', 'T', 1]:
        return True
    elif string in ['false', 'False', 'f', 'F', 0]:
        return False
    else:
        raise Exception("Wrong input")


json_obj = json.dumps({url: inp_data,
                               'output': sorted_by_score},
                              indent=4, separators=(",", ":"))