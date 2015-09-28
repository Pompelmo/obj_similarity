from gen_json import CreateJson
from loading import loading
from bottle import Bottle, route, run, template
import re

tfidf, index, tfidf_dict, tfidf_web, mean_dict, ball_tree, w2v_model, d2v_model = loading()       # load the models

# class for rank, len, score computation
c_json = CreateJson(tfidf, index, tfidf_dict, tfidf_web, mean_dict, ball_tree, w2v_model, d2v_model)

app = Bottle()


@app.route('/suggestions/<loss:float>/<w2v_weight:float>/<d2v_weight:float>/'
           '<tfidf_weight:float>/<mu_in_w:float>/<mu_in_d:float>/<mu_in_t:float>/'
           '<mu_out_w:float>/<mu_out_d:float>/<mu_out_t:float>/<website:re:[\w\.]+>')
def suggestions(loss,
                w2v_weight, d2v_weight, tfidf_weight,
                mu_in_w, mu_in_d, mu_in_t,
                mu_out_w, mu_out_d, mu_out_t, website):

    assert isinstance(loss, float)
    assert isinstance(w2v_weight, float)
    assert isinstance(d2v_weight, float)
    assert isinstance(tfidf_weight, float)
    assert isinstance(mu_in_w, float)
    assert isinstance(mu_in_d, float)
    assert isinstance(mu_in_t, float)
    assert isinstance(mu_out_w, float)
    assert isinstance(mu_out_d, float)
    assert isinstance(mu_out_t, float)

    # url = re.compile(r'[\w\.]+')
    assert re.match(r'[\w\.]+', website) is not None

    c_json.loss = loss
    c_json.w2v_weight = w2v_weight
    c_json.d2v_weight = d2v_weight
    c_json.tfidf_weight = tfidf_weight
    c_json.mu_in_w = mu_in_w
    c_json.mu_in_d = mu_in_d
    c_json.mu_in_t = mu_in_t
    c_json.mu_out_w = mu_out_w
    c_json.mu_out_d = mu_out_d
    c_json.mu_out_t = mu_out_t

    return c_json.get_json(website)

run(app, host='127.0.0.1', port=8080)
