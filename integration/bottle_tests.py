import requests
import unittest

api_url = "http://0.0.0.0:8080/suggest"


class BottleTestCase(unittest.TestCase):

    # ------------------------test no query input-----------------------------
    def test_no_input(self):
        parameters = dict()
        req = requests.get(api_url, params=parameters).json()
        expected_answer = {"error": "parameter 'website' or 'company' is missing"}
        self.assertEqual(req, expected_answer)

    # --------------test wrong prameters (only one input, wrong )-----------------------------
    def test_wrong_parameter(self):
        parameters = dict()
        parameters['wbsi'] = 'boh'
        expected_answer = {"error": "wrong parameter(s) in input",
                           "expected": {"websites": ".../suggest?website=a_website"
                                                    "[&model=(default='linear)'&num_max=(default=60)&"
                                                    "only_website=(default=False)]",
                                        "companies": ".../suggest?company=atoka_company_id"
                                                     "[&model=(default='linear)'&num_max=(default=60)&"
                                                     "only_website=(default=False)&ateco=(false)]"}}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ---------------test wrong parameters (more input, one wrong)-----------------------------
    def test_wrong_just_one_parameter_website(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['num_max'] = 10
        parameters['gnegnegne'] = 'non so cosa scrivere'
        expected_answer = {"error": "wrong parameter(s) in input",
                           "expected": {"websites": ".../suggest?website=a_website"
                                                    "[&model=(default='linear)'&num_max=(default=60)&"
                                                    "only_website=(default=False)]",
                                        "companies": ".../suggest?company=atoka_company_id"
                                                     "[&model=(default='linear)'&num_max=(default=60)&"
                                                     "only_website=(default=False)&ateco=(false)]"}}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ---------------test wrong parameters (more input, one wrong)-----------------------------
    def test_wrong_just_one_parameter_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['num_max'] = 10
        parameters['gnegnegne'] = 'non so cosa scrivere'
        expected_answer = {"error": "wrong parameter(s) in input",
                           "expected": {"websites": ".../suggest?website=a_website"
                                                    "[&model=(default='linear)'&num_max=(default=60)&"
                                                    "only_website=(default=False)]",
                                        "companies": ".../suggest?company=atoka_company_id"
                                                     "[&model=(default='linear)'&num_max=(default=60)&"
                                                     "only_website=(default=False)&ateco=(false)]"}}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ---------------test wrong parameters (more input, one wrong)-----------------------------
    def test_wrong_just_one_parameter_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['num_max'] = 10
        parameters['gnegnegne'] = 'non so cosa scrivere'
        expected_answer = {"error": "wrong parameter(s) in input",
                           "expected": {"websites": ".../suggest?website=a_website"
                                                    "[&model=(default='linear)'&num_max=(default=60)&"
                                                    "only_website=(default=False)]",
                                        "companies": ".../suggest?company=atoka_company_id"
                                                     "[&model=(default='linear)'&num_max=(default=60)&"
                                                     "only_website=(default=False)&ateco=(false)]"}}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ---------------test wrong parameters (more input, one wrong)-----------------------------
    def test_wrong_just_one_parameter_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['num_max'] = 10
        parameters['gnegnegne'] = 'non so cosa scrivere'
        expected_answer = {"error": "wrong parameter(s) in input",
                           "expected": {"websites": ".../suggest?website=a_website"
                                                    "[&model=(default='linear)'&num_max=(default=60)&"
                                                    "only_website=(default=False)]",
                                        "companies": ".../suggest?company=atoka_company_id"
                                                     "[&model=(default='linear)'&num_max=(default=60)&"
                                                     "only_website=(default=False)&ateco=(false)]"}}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ------------------------
    # test wrong num_max
    # ------------------------

    # ------------------------test wrong num_max input, string-----------------------------
    def test_wrong_num_max(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['num_max'] = 'abc'
        expected_answer = {"error": "expected an integer in the 'num_max' field"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ------------------------test wrong num_max input, string-----------------------------
    def test_wrong_num_max_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['num_max'] = 'abc'
        expected_answer = {"error": "expected an integer in the 'num_max' field"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ------------------------test wrong num_max input, string-----------------------------
    def test_wrong_num_max_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['num_max'] = 'abc'
        expected_answer = {"error": "expected an integer in the 'num_max' field"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ------------------------test wrong num_max input, string-----------------------------
    def test_wrong_num_max_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['num_max'] = 'abc'
        expected_answer = {"error": "expected an integer in the 'num_max' field"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ------------------------
    # test wrong model
    # ------------------------

    # ---------------test wrong model, string, one website-----------------------------
    def test_wrong_model(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['model'] = 'miao'
        expected_answer = {"error": "wrong model in input, try: 'linear', 'simply_weighted', "
                                    "'weight_dist', 'w2v', 'd2v' or 'tfidf"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ----------------test wrong model, string, list of websites-----------------------------
    def test_wrong_model_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['model'] = 'miao'
        expected_answer = {"error": "wrong model in input, try: 'linear', 'simply_weighted', "
                                    "'weight_dist', 'w2v', 'd2v' or 'tfidf"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # -------------------test wrong model, string, company-----------------------------
    def test_wrong_model_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['model'] = 'miao'
        expected_answer = {"error": "wrong model in input, try: 'linear', 'simply_weighted', "
                                    "'weight_dist', 'w2v', 'd2v' or 'tfidf"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # -------------------test wrong model, string, company-----------------------------
    def test_wrong_model_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['model'] = 'miao'
        expected_answer = {"error": "wrong model in input, try: 'linear', 'simply_weighted', "
                                    "'weight_dist', 'w2v', 'd2v' or 'tfidf"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ------------------------
    # test wrong only_website
    # ------------------------

    # ------------test wrong only_website, string, one website-----------------------------
    def test_wrong_only_website(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['only_website'] = 'c'
        expected_answer = {"error": "wrong input on only_website: try 't', 'T', 'true', "
                                    "'True' or '1' to eliminate metadata"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # -------------test wrong only_website, string, list of websites--------------------------
    def test_wrong_only_website_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['only_website'] = 'c'
        expected_answer = {"error": "wrong input on only_website: try 't', 'T', 'true', "
                                    "'True' or '1' to eliminate metadata"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # -------------test wrong only_website, string, company--------------------------
    def test_wrong_only_website_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['only_website'] = 'c'
        expected_answer = {"error": "wrong input on only_website: try 't', 'T', 'true', "
                                    "'True' or '1' to eliminate metadata"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # -------------test wrong only_website, string, company--------------------------
    def test_wrong_only_website_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['only_website'] = 'c'
        expected_answer = {"error": "wrong input on only_website: try 't', 'T', 'true', "
                                    "'True' or '1' to eliminate metadata"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ------------------------
    # test company/website 'not found'
    # ------------------------

    # ------------------------test wrong website-----------------------------
    def test_website_not_present(self):
        parameters = dict()
        parameters['website'] = 'www.spazioda.eu'
        expected_answer = {'error': 'websites not present in the models'}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ------------------------test wrong weblist-----------------------------
    def test_websites_not_present(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodat.eu', 'www.ajshajk.it']
        expected_answer = {'error': 'websites not present in the models'}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ------------------------test wrong company-----------------------------
    def test_wrong_company(self):
        parameters = dict()
        parameters['company'] = '2e2a8211aa81'
        expected_answer = {"error": "no companies found"}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ------------------------test wrong company-----------------------------
    def test_wrong_companies(self):
        parameters = dict()
        parameters['company'] = ['2e2a8211aa81', '6da785b3adf3']
        expected_answer = {'error': 'no companies found'}
        self.assertEqual(requests.get(api_url, params=parameters).json(), expected_answer)

    # ------------------------
    # test a list with wrong websites
    # ------------------------

    def test_ugly_list(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'ciaone']
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(answer['input_website_metadata']['ciaone'], "website not present in the models")

    # ------------------------
    # test length
    # ------------------------

    # we don't test single company, already in gen_json_tests.py
    def test_default_num_max_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        answer = requests.get(api_url, params=parameters).json()
        self.assertLessEqual(len(answer['output']), 60)

    def test_default_num_max_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        answer = requests.get(api_url, params=parameters).json()
        self.assertLessEqual(len(answer['output']), 60)

    def test_default_num_max_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        answer = requests.get(api_url, params=parameters).json()
        self.assertLessEqual(len(answer['output']), 60)

    def test_default_num_max_companies_one_correct(self):
        parameters = dict()
        parameters['company'] = ['2e2a8211aa81', '6da785b3adf2']
        answer = requests.get(api_url, params=parameters).json()
        self.assertLessEqual(len(answer['output']), 60)

    def test_default_num_max_20_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_default_num_max_20_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_default_num_max_20_companies_one_correct(self):
        parameters = dict()
        parameters['company'] = ['2e2a8211aa81', '6da785b3adf2']
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_default_num_max_20_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    # ------------------------
    # test acceptance num_max
    # ------------------------

    def test_num_max_string_website(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['num_max'] = '20'
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_num_max_string_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['num_max'] = '20'
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    # ------------------------------
    # test acceptance model - linear
    # ------------------------------
    # still 20 are used, to be sure it works.
    # otherwise I should use LessEqual (so also 0 would be correct)

    def test_model_linear_website(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['model'] = 'linear'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_linear_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['model'] = 'linear'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_linear_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['model'] = 'linear'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_linear_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['model'] = 'linear'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    # ------------------------------
    # test acceptance model - simply_weighted
    # ------------------------------

    def test_model_simply_weighted_website(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['model'] = 'simply_weighted'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_simply_weighted_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['model'] = 'simply_weighted'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_simply_weighted_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['model'] = 'simply_weighted'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_simply_weighted_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['model'] = 'simply_weighted'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    # ------------------------------
    # test acceptance model - weight_dist
    # ------------------------------

    def test_model_weight_dist_website(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['model'] = 'weight_dist'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_weight_dist_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['model'] = 'weight_dist'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_weight_dist_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['model'] = 'weight_dist'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_weight_dist_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['model'] = 'weight_dist'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    # ------------------------------
    # test acceptance model - w2v
    # ------------------------------

    def test_model_w2v_website(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['model'] = 'w2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_w2v_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['model'] = 'w2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_w2v_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['model'] = 'w2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_w2v_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['model'] = 'w2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    # ------------------------------
    # test is it w2v ?
    # ------------------------------

    def test_model_w2v_score_website(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['model'] = 'w2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()['output'][0]['data']
        self.assertEqual(answer['scores']['w2v'], answer['total_score'])

    def test_model_w2v_score_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['model'] = 'w2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()['output'][0]['data']
        self.assertEqual(answer['scores']['w2v'], answer['total_score'])

    def test_model_w2v_score_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['model'] = 'w2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        answer = (answer['output'][0]['websites']).values()[0]
        self.assertEqual(answer['scores']['w2v'], answer['total_score'])

    def test_model_w2v_score_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['model'] = 'w2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        answer = (answer['output'][0]['websites']).values()[0]
        self.assertEqual(answer['scores']['w2v'], answer['total_score'])

    # ------------------------------
    # test acceptance model - d2v
    # ------------------------------

    def test_model_d2v_website(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['model'] = 'd2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_d2v_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['model'] = 'd2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_d2v_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['model'] = 'd2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_d2v_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['model'] = 'd2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    # ------------------------------
    # test is it d2v ?
    # ------------------------------

    def test_model_d2v_score_website(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['model'] = 'd2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()['output'][0]['data']
        self.assertEqual(answer['scores']['d2v'], answer['total_score'])

    def test_model_d2v_score_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['model'] = 'd2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()['output'][0]['data']
        self.assertEqual(answer['scores']['d2v'], answer['total_score'])

    def test_model_d2v_score_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['model'] = 'd2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        answer = (answer['output'][0]['websites']).values()[0]
        self.assertEqual(answer['scores']['d2v'], answer['total_score'])

    def test_model_d2v_score_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['model'] = 'd2v'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        answer = (answer['output'][0]['websites']).values()[0]
        self.assertEqual(answer['scores']['d2v'], answer['total_score'])

    # ------------------------------
    # test acceptance model - tfidf
    # ------------------------------

    def test_model_tfidf_website(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['model'] = 'tfidf'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_tfidf_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['model'] = 'tfidf'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_tfidf_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['model'] = 'tfidf'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_model_tfidf_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['model'] = 'tfidf'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    # ------------------------------
    # test is it tfidf ?
    # ------------------------------

    def test_model_tfidf_score_website(self):
        parameters = dict()
        parameters['website'] = 'www.spaziodati.eu'
        parameters['model'] = 'tfidf'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()['output'][0]['data']
        self.assertEqual(answer['scores']['tfidf'], answer['total_score'])

    def test_model_tfidf_score_weblist(self):
        parameters = dict()
        parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
        parameters['model'] = 'tfidf'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()['output'][0]['data']
        self.assertEqual(answer['scores']['tfidf'], answer['total_score'])

    def test_model_tfidf_score_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['model'] = 'tfidf'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        answer = (answer['output'][0]['websites']).values()[0]
        self.assertEqual(answer['scores']['tfidf'], answer['total_score'])

    def test_model_tfidf_score_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['model'] = 'tfidf'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        answer = (answer['output'][0]['websites']).values()[0]
        self.assertEqual(answer['scores']['tfidf'], answer['total_score'])

    # ------------------------------
    # test wrong ateco
    # ------------------------------

    def test_wrong_ateco_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['ateco'] = 'fall'
        answer = requests.get(api_url, params=parameters).json()
        expected = {"error": "wrong ateco in input", "expected": "'strict', 'distance', 'auto' or 'false'[default]"}
        self.assertEqual(answer, expected)

    def test_wrong_ateco_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['ateco'] = 'fall'
        answer = requests.get(api_url, params=parameters).json()
        expected = {"error": "wrong ateco in input", "expected": "'strict', 'distance', 'auto' or 'false'[default]"}
        self.assertEqual(answer, expected)

    # ------------------------------
    # test ateco output
    # ------------------------------

    def test_false_ateco_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['ateco'] = 'false'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_false_ateco_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['ateco'] = 'false'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertEqual(len(answer['output']), 20)

    def test_auto_ateco_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['ateco'] = 'auto'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertLessEqual(len(answer['output']), 20)

    def test_auto_ateco_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['ateco'] = 'auto'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertLessEqual(len(answer['output']), 20)

    def test_distance_ateco_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['ateco'] = 'distance'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertLessEqual(len(answer['output']), 20)

    def test_distance_ateco_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['ateco'] = 'distance'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertLessEqual(len(answer['output']), 20)

    def test_strict_ateco_company(self):
        parameters = dict()
        parameters['company'] = '6da785b3adf2'
        parameters['ateco'] = 'strict'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertLessEqual(len(answer['output']), 20)

    def test_strict_ateco_companies(self):
        parameters = dict()
        parameters['company'] = ['6da785b3adf2', '20533a607faf']
        parameters['ateco'] = 'strict'
        parameters['num_max'] = 20
        answer = requests.get(api_url, params=parameters).json()
        self.assertLessEqual(len(answer['output']), 20)


if __name__ == '__main__':

    unittest.main()
