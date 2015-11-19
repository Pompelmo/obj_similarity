import unittest
from loading import loading
from gen_json import CreateJson
from ScoreFunc import ScoreFunc

# load the models needed
corpus, tfidf, index, tfidf_dict, tfidf_web, \
    mean_dict, ball_tree, d2v_model, des_dict, w2v_model, key_dict = loading()

# class for rank, len, score computation
cj = CreateJson(corpus, tfidf, index, tfidf_dict, tfidf_web,
                mean_dict, ball_tree, d2v_model, des_dict, w2v_model, key_dict)

sf = ScoreFunc()  # class for total_score computation


class MyTestCase(unittest.TestCase):

    # -----------------------------------------------------------------------
    # -------------------tests for CreateJson.inp_web_info-------------------
    # with a websites that has text, keywords and description
    # -----------------------------------------------------------------------
    def test_iwi_false_website_full_attribute(self):
        self.assertIsInstance(cj.inp_web_info('www.spaziodati.eu'), dict)

    def test_iwi_false_partial_kn_website_full_attribute(self):
        self.assertIsInstance(cj.inp_web_info('www.spaziodati.eu', False)['metadata']['keywords_number'], int)

    def test_iwi_false_partial_dn_website_full_attribute(self):
        self.assertIsInstance(cj.inp_web_info('www.spaziodati.eu', False)['metadata']['desc_tokens'], int)

    def test_iwi_false_partial_tn_website_full_attribute(self):
        self.assertIsInstance(cj.inp_web_info('www.spaziodati.eu', False)['metadata']['text_tokens'], int)

    def test_iwi_true_website_full_attribute(self):
        self.assertIsInstance(cj.inp_web_info('www.spaziodati.eu', True), dict)

    def test_iwi_true_partial_k_website_full_attribute(self):
        self.assertIsInstance(cj.inp_web_info('www.spaziodati.eu', True)['metadata']['keywords'], list)

    def test_iwi_true_partial_d_website_full_attribute(self):
        self.assertIsInstance(cj.inp_web_info('www.spaziodati.eu', True)['metadata']['description'], list)

    def test_iwi_true_partial_kn_website_full_attribute(self):
        self.assertIsInstance(cj.inp_web_info('www.spaziodati.eu', True)['metadata']['keywords_number'], int)

    def test_iwi_true_partial_dn_website_full_attribute(self):
        self.assertIsInstance(cj.inp_web_info('www.spaziodati.eu', True)['metadata']['desc_tokens'], int)

    def test_iwi_true_partial_tn_website_full_attribute(self):
        self.assertIsInstance(cj.inp_web_info('www.spaziodati.eu')['metadata']['text_tokens'], int)

    # -----------------------------------------------------------------------
    # -------------------tests for CreateJson.inp_web_info-------------------
    # with a website that doesn't exist anywhere
    # -----------------------------------------------------------------------

    def test_iwi_false_wrong_web(self):
        self.assertIsInstance(cj.inp_web_info('akjsdkjas'), dict)

    def test_iwi_false_partial_kn_wrong_web_key(self):
        self.assertEqual(cj.inp_web_info('akjsdkjas', False)['metadata']['keywords_number'], 0)

    def test_iwi_false_partial_kn_wrong_web_des(self):
        self.assertEqual(cj.inp_web_info('akjsdkjas', False)['metadata']['desc_tokens'], 0)

    def test_iwi_false_partial_kn_wrong_web_text(self):
        self.assertEqual(cj.inp_web_info('akjsdkjas', False)['metadata']['text_tokens'], 0)

    def test_iwi_true_wrong_web(self):
        self.assertIsInstance(cj.inp_web_info('akjsdkjas', True), dict)

    def test_iwi_true_partial_k_wrong_web(self):
        self.assertEqual(len(cj.inp_web_info('akjsdkjas', True)), 0)

    # -----------------------------------------------------------------------
    # -------------------tests for CreateJson.inp_web_info-------------------
    # with ha website that has only text and description, not keywords
    # -----------------------------------------------------------------------

    def test_iwi_false_web_no_keywords(self):
        self.assertIsInstance(cj.inp_web_info('company.cerved.com'), dict)

    def test_iwi_false_partial_kn_web_no_keywords(self):
        self.assertEqual(cj.inp_web_info('company.cerved.com', False)['metadata']['keywords_number'], 0)

    def test_iwi_false_partial_dn_web_no_keywords(self):
        self.assertIsInstance(cj.inp_web_info('company.cerved.com', False)['metadata']['desc_tokens'], int)

    def test_iwi_false_partial_tn_web_no_keywords(self):
        self.assertIsInstance(cj.inp_web_info('company.cerved.com', False)['metadata']['text_tokens'], int)

    def test_iwi_true_web_no_keywords(self):
        self.assertIsInstance(cj.inp_web_info('company.cerved.com', True), dict)

    def test_iwi_true_partial_k_web_no_keywords(self):
        self.assertEqual(cj.inp_web_info('company.cerved.com', True)['metadata']['keywords'], [])

    def test_iwi_true_partial_d_web_no_keywords(self):
        self.assertIsInstance(cj.inp_web_info('company.cerved.com', True)['metadata']['description'], list)

    def test_iwi_true_partial_kn_web_no_keywords(self):
        self.assertEqual(cj.inp_web_info('company.cerved.com', True)['metadata']['keywords_number'], 0)

    def test_iwi_true_partial_dn_web_no_keywords(self):
        self.assertIsInstance(cj.inp_web_info('company.cerved.com', True)['metadata']['desc_tokens'], int)

    def test_iwi_true_partial_tn_web_no_keywords(self):
        self.assertIsInstance(cj.inp_web_info('company.cerved.com')['metadata']['text_tokens'], int)

    # -----------------------------------------------------------------------
    # -------------------tests for CreateJson.inp_web_info-------------------
    # with a websites that has only text, not keywords nor description
    # -----------------------------------------------------------------------

    def test_iwi_false_web_only_text(self):
        self.assertIsInstance(cj.inp_web_info('zanormac.net'), dict)

    def test_iwi_false_partial_kn_web_only_text(self):
        self.assertEqual(cj.inp_web_info('zanormac.net', False)['metadata']['keywords_number'], 0)

    def test_iwi_false_partial_dn_web_only_text(self):
        self.assertEqual(cj.inp_web_info('zanormac.net', False)['metadata']['desc_tokens'], 0)

    def test_iwi_false_partial_tn_web_only_text(self):
        self.assertIsInstance(cj.inp_web_info('zanormac.net', False)['metadata']['text_tokens'], int)

    def test_iwi_true_web_only_text(self):
        self.assertIsInstance(cj.inp_web_info('zanormac.net', True), dict)

    def test_iwi_true_partial_k_web_only_text(self):
        self.assertEqual(cj.inp_web_info('zanormac.net', True)['metadata']['keywords'], [])

    def test_iwi_true_partial_d_web_only_text(self):
        self.assertEqual(cj.inp_web_info('zanormac.net', True)['metadata']['description'], [])

    def test_iwi_true_partial_kn_web_only_text(self):
        self.assertEqual(cj.inp_web_info('zanormac.net', True)['metadata']['keywords_number'], 0)

    def test_iwi_true_partial_dn_web_only_text(self):
        self.assertEqual(cj.inp_web_info('zanormac.net', True)['metadata']['desc_tokens'], 0)

    def test_iwi_true_partial_tn_web_only_text(self):
        self.assertIsInstance(cj.inp_web_info('zanormac.net')['metadata']['text_tokens'], int)

    # -----------------------------------------------------------------------
    # -------------------tests for CreateJson.inp_web_info-------------------
    # with a websites that has text, keywords but no description
    # -----------------------------------------------------------------------
    def test_iwi_false_website_no_des(self):
        self.assertIsInstance(cj.inp_web_info('www.ceda.it'), dict)

    def test_iwi_false_partial_kn_website_no_des(self):
        self.assertIsInstance(cj.inp_web_info('www.ceda.it', False)['metadata']['keywords_number'], int)

    def test_iwi_false_partial_dn_website_no_des(self):
        self.assertEqual(cj.inp_web_info('www.ceda.it', False)['metadata']['desc_tokens'], 0)

    def test_iwi_false_partial_tn_website_no_des(self):
        self.assertIsInstance(cj.inp_web_info('www.ceda.it', False)['metadata']['text_tokens'], int)

    def test_iwi_true_website_no_des(self):
        self.assertIsInstance(cj.inp_web_info('www.ceda.it', True), dict)

    def test_iwi_true_partial_k_website_no_des(self):
        self.assertIsInstance(cj.inp_web_info('www.ceda.it', True)['metadata']['keywords'], list)

    def test_iwi_true_partial_d_website_no_des(self):
        self.assertEqual(cj.inp_web_info('www.ceda.it', True)['metadata']['description'], [])

    def test_iwi_true_partial_kn_website_no_des(self):
        self.assertIsInstance(cj.inp_web_info('www.ceda.it', True)['metadata']['keywords_number'], int)

    def test_iwi_true_partial_dn_website_no_des(self):
        self.assertEqual(cj.inp_web_info('www.ceda.it', True)['metadata']['desc_tokens'], 0)

    def test_iwi_true_partial_tn_website_no_des(self):
        self.assertIsInstance(cj.inp_web_info('www.ceda.it')['metadata']['text_tokens'], int)

    # -----------------------------------------------------------------------
    # -------------------tests for CreateJson.get_weight---------------------
    # websites with text, description and keywords
    # -----------------------------------------------------------------------

    def test_gw_0_website_full_attribute(self):
        self.assertIsInstance(cj.get_weight('www.spaziodati.eu')[0], int)

    def test_gw_1_website_full_attribute(self):
        self.assertIsInstance(cj.get_weight('www.spaziodati.eu')[1], int)

    def test_gw_2_website_full_attribute(self):
        self.assertIsInstance(cj.get_weight('www.spaziodati.eu')[2], int)

    def test_gw_0_wrong_web(self):
        self.assertEqual(cj.get_weight('akjsdkjas')[0], 0)

    def test_gw_1_wrong_web(self):
        self.assertEqual(cj.get_weight('akjsdkjas')[1], 0)

    def test_gw_2_wrong_web(self):
        self.assertEqual(cj.get_weight('akjsdkjas')[2], 0)

    def test_gw_0_web_no_keywords(self):
        self.assertEqual(cj.get_weight('company.cerved.com')[0], 0)

    def test_gw_1_web_no_keywords(self):
        self.assertIsInstance(cj.get_weight('company.cerved.com')[1], int)

    def test_gw_2_web_no_keywords(self):
        self.assertIsInstance(cj.get_weight('company.cerved.com')[2], int)

    def test_gw_0_web_only_text(self):
        self.assertEqual(cj.get_weight('zanormac.net')[0], 0)

    def test_gw_1_web_only_text(self):
        self.assertEqual(cj.get_weight('zanormac.net')[1], 0)

    def test_gw_2_web_only_text(self):
        self.assertIsInstance(cj.get_weight('zanormac.net')[2], int)

    def test_gw_0_web_no_des(self):
        self.assertIsInstance(cj.get_weight('www.ceda.it')[0], int)

    def test_gw_1_web_no_des(self):
        self.assertEqual(cj.get_weight('www.ceda.it')[1], 0)

    def test_gw_2_web_no_des(self):
        self.assertIsInstance(cj.get_weight('www.ceda.it')[2], int)

    # -----------------------------------------------------------------------
    # -------------------tests for CreateJson.text_websites------------------
    # -----------------------------------------------------------------------

    def test_tw_true_website_full_attribute(self):
        self.assertIsInstance(cj.text_websites(['www.spaziodati.eu'], sf, n=10, only_web=True), dict)

    def test_tw_true_len_website_full_attribute(self):
        self.assertEqual(len(cj.text_websites(['www.spaziodati.eu'], sf, n=10, only_web=True)), 10)

    def test_tw_false_website_full_attribute(self):
        self.assertIsInstance(cj.text_websites(['www.spaziodati.eu'], sf, n=10, only_web=False), dict)

    def test_tw_false_len_website_full_attribute(self):
        self.assertEqual(len(cj.text_websites(['www.spaziodati.eu'], sf, n=10, only_web=False)), 10)

    def test_tw_true_wrong_web(self):
        self.assertIsInstance(cj.text_websites(['akjsdkjas'], sf, n=10, only_web=True), dict)

    def test_tw_true_len_wrong_web(self):
        self.assertEqual(len(cj.text_websites(['akjsdkjas'], sf, n=10, only_web=True)), 0)

    def test_tw_false_wrong_web(self):
        self.assertIsInstance(cj.text_websites(['akjsdkjas'], sf, n=10, only_web=False), dict)

    def test_tw_false_len_wrong_web(self):
        self.assertEqual(len(cj.text_websites(['akjsdkjas'], sf, n=10, only_web=False)), 0)

    def test_tw_true_web_no_keywords(self):
        self.assertIsInstance(cj.text_websites(['company.cerved.com'], sf, n=10, only_web=True), dict)

    def test_tw_true_len_web_no_keywords(self):
        self.assertEqual(len(cj.text_websites(['company.cerved.com'], sf, n=10, only_web=True)), 10)

    def test_tw_false_web_no_keywords(self):
        self.assertIsInstance(cj.text_websites(['company.cerved.com'], sf, n=10, only_web=False), dict)

    def test_tw_false_len_web_no_keywords(self):
        self.assertEqual(len(cj.text_websites(['company.cerved.com'], sf, n=10, only_web=False)), 10)

    def test_tw_true_website_only_text(self):
        self.assertIsInstance(cj.text_websites(['zanormac.net'], sf, n=10, only_web=True), dict)

    def test_tw_true_len_website_only_text(self):
        self.assertEqual(len(cj.text_websites(['zanormac.net'], sf, n=10, only_web=True)), 10)

    def test_tw_false_website_only_text(self):
        self.assertIsInstance(cj.text_websites(['zanormac.net'], sf, n=10, only_web=False), dict)

    def test_tw_false_len_website_only_text(self):
        self.assertEqual(len(cj.text_websites(['zanormac.net'], sf, n=10, only_web=False)), 10)

    def test_tw_true_website_no_des(self):
        self.assertIsInstance(cj.text_websites(['www.ceda.it'], sf, n=10, only_web=True), dict)

    def test_tw_true_len_website_no_des(self):
        self.assertEqual(len(cj.text_websites(['www.ceda.it'], sf, n=10, only_web=True)), 10)

    def test_tw_false_website_no_des(self):
        self.assertIsInstance(cj.text_websites(['www.ceda.it'], sf, n=10, only_web=False), dict)

    def test_tw_false_len_website_no_des(self):
        self.assertEqual(len(cj.text_websites(['www.ceda.it'], sf, n=10, only_web=False)), 10)

    # -----------------------------------------------------------------------
    # -------------------tests for CreateJson.d2v_websites-------------------
    # -----------------------------------------------------------------------

    def test_dw_true_website_full_attribute(self):
        self.assertIsInstance(cj.d2v_websites(['www.spaziodati.eu'], sf, n=10, only_web=True), dict)

    def test_dw_true_len_website_full_attribute(self):
        self.assertEqual(len(cj.d2v_websites(['www.spaziodati.eu'], sf, n=10, only_web=True)), 10)

    def test_dw_false_website_full_attribute(self):
        self.assertIsInstance(cj.d2v_websites(['www.spaziodati.eu'], sf, n=10, only_web=False), dict)

    def test_dw_false_len_website_full_attribute(self):
        self.assertEqual(len(cj.d2v_websites(['www.spaziodati.eu'], sf, n=10, only_web=False)), 10)

    def test_dw_true_wrong_web(self):
        self.assertIsInstance(cj.d2v_websites(['akjsdkjas'], sf, n=10, only_web=True), dict)

    def test_dw_true_len_wrong_web(self):
        self.assertEqual(len(cj.d2v_websites(['akjsdkjas'], sf, n=10, only_web=True)), 0)

    def test_dw_false_wrong_web(self):
        self.assertIsInstance(cj.d2v_websites(['akjsdkjas'], sf, n=10, only_web=False), dict)

    def test_dw_false_len_wrong_web(self):
        self.assertEqual(len(cj.d2v_websites(['akjsdkjas'], sf, n=10, only_web=False)), 0)

    def test_dw_true_web_no_keywords(self):
        self.assertIsInstance(cj.d2v_websites(['company.cerved.com'], sf, n=10, only_web=True), dict)

    def test_dw_true_len_web_no_keywords(self):
        self.assertEqual(len(cj.d2v_websites(['company.cerved.com'], sf, n=10, only_web=True)), 10)

    def test_dw_false_web_no_keywords(self):
        self.assertIsInstance(cj.d2v_websites(['company.cerved.com'], sf, n=10, only_web=False), dict)

    def test_dw_false_len_web_no_keywords(self):
        self.assertEqual(len(cj.d2v_websites(['company.cerved.com'], sf, n=10, only_web=False)), 10)

    def test_dw_true_website_only_text(self):
        self.assertIsInstance(cj.d2v_websites(['zanormac.net'], sf, n=10, only_web=True), dict)

    def test_dw_true_len_website_only_text(self):
        self.assertEqual(len(cj.d2v_websites(['zanormac.net'], sf, n=10, only_web=True)), 0)

    def test_dw_false_website_only_text(self):
        self.assertIsInstance(cj.d2v_websites(['zanormac.net'], sf, n=10, only_web=False), dict)

    def test_dw_false_len_website_only_text(self):
        self.assertEqual(len(cj.d2v_websites(['zanormac.net'], sf, n=10, only_web=False)), 0)

    def test_dw_true_website_no_des(self):
        self.assertIsInstance(cj.d2v_websites(['www.ceda.it'], sf, n=10, only_web=True), dict)

    def test_dw_true_len_website_no_des(self):
        self.assertEqual(len(cj.d2v_websites(['www.ceda.it'], sf, n=10, only_web=True)), 0)

    def test_dw_false_website_no_des(self):
        self.assertIsInstance(cj.d2v_websites(['www.ceda.it'], sf, n=10, only_web=False), dict)

    def test_dw_false_len_website_no_des(self):
        self.assertEqual(len(cj.d2v_websites(['www.ceda.it'], sf, n=10, only_web=False)), 0)

    # -----------------------------------------------------------------------
    # -------------------tests for CreateJson.w2v_websites-------------------
    # -----------------------------------------------------------------------

    def test_ww_true_website_full_attribute(self):
        self.assertIsInstance(cj.w2v_websites(['www.spaziodati.eu'], sf, n=10, only_web=True), dict)

    def test_ww_true_len_website_full_attribute(self):
        self.assertEqual(len(cj.w2v_websites(['www.spaziodati.eu'], sf, n=10, only_web=True)), 10)

    def test_ww_false_website_full_attribute(self):
        self.assertIsInstance(cj.w2v_websites(['www.spaziodati.eu'], sf, n=10, only_web=False), dict)

    def test_ww_false_len_website_full_attribute(self):
        self.assertEqual(len(cj.w2v_websites(['www.spaziodati.eu'], sf, n=10, only_web=False)), 10)

    def test_ww_true_wrong_web(self):
        self.assertIsInstance(cj.w2v_websites(['akjsdkjas'], sf, n=10, only_web=True), dict)

    def test_ww_true_len_wrong_web(self):
        self.assertEqual(len(cj.w2v_websites(['akjsdkjas'], sf, n=10, only_web=True)), 0)

    def test_ww_false_wrong_web(self):
        self.assertIsInstance(cj.w2v_websites(['akjsdkjas'], sf, n=10, only_web=False), dict)

    def test_ww_false_len_wrong_web(self):
        self.assertEqual(len(cj.w2v_websites(['akjsdkjas'], sf, n=10, only_web=False)), 0)

    def test_ww_true_web_no_keywords(self):
        self.assertIsInstance(cj.w2v_websites(['company.cerved.com'], sf, n=10, only_web=True), dict)

    def test_ww_true_len_web_no_keywords(self):
        self.assertEqual(len(cj.w2v_websites(['company.cerved.com'], sf, n=10, only_web=True)), 0)

    def test_ww_false_web_no_keywords(self):
        self.assertIsInstance(cj.w2v_websites(['company.cerved.com'], sf, n=10, only_web=False), dict)

    def test_ww_false_len(self):
        self.assertEqual(len(cj.w2v_websites(['company.cerved.com'], sf, n=10, only_web=False)), 0)

    def test_ww_true_website_only_text(self):
        self.assertIsInstance(cj.w2v_websites(['zanormac.net'], sf, n=10, only_web=True), dict)

    def test_ww_true_len_website_only_text(self):
        self.assertEqual(len(cj.w2v_websites(['zanormac.net'], sf, n=10, only_web=True)), 0)

    def test_ww_false_website_only_text(self):
        self.assertIsInstance(cj.w2v_websites(['zanormac.net'], sf, n=10, only_web=False), dict)

    def test_ww_false_len_website_only_text(self):
        self.assertEqual(len(cj.w2v_websites(['zanormac.net'], sf, n=10, only_web=False)), 0)

    def test_ww_true_website_no_des(self):
        self.assertIsInstance(cj.w2v_websites(['www.ceda.it'], sf, n=10, only_web=True), dict)

    def test_ww_true_len_website_no_des(self):
        self.assertEqual(len(cj.w2v_websites(['www.ceda.it'], sf, n=10, only_web=True)), 10)

    def test_ww_false_website_no_des(self):
        self.assertIsInstance(cj.w2v_websites(['www.ceda.it'], sf, n=10, only_web=False), dict)

    def test_ww_false_len_website_no_des(self):
        self.assertEqual(len(cj.w2v_websites(['www.ceda.it'], sf, n=10, only_web=False)), 10)

    # -----------------------------------------------------------------------
    # -------------------tests for CreateJson.gen_json-----------------------
    # -----------------------------------------------------------------------
    def test_gj_len_len_website_full_attribute(self):
        dictionary = cj.get_json(['www.spaziodati.eu'], sf, n=10, only_web=False)
        output = dictionary['output']
        self.assertLessEqual(len(output), 30)

    def test_gj_len_wrong_web(self):
        dictionary = cj.get_json(['akjsdkjas'], sf, n=10)
        self.assertEqual(len(dictionary), 0)

    def test_gj_dict_wrong_web(self):
        dictionary = cj.get_json(['akjsdkjas'], sf, n=10)
        self.assertIsInstance(dictionary, dict)

    def test_gj_len_web_no_keywords(self):
        dictionary = cj.get_json(['company.cerved.com'], sf, n=10, only_web=False)
        output = dictionary['output']
        self.assertLessEqual(len(output), 20)

    def test_gj_len_len_website_only_text(self):
        dictionary = cj.get_json(['zanormac.net'], sf, n=10, only_web=False)
        output = dictionary['output']
        self.assertLessEqual(len(output), 10)

    def test_gj_len_len_website_no_des(self):
        dictionary = cj.get_json(['www.ceda.it'], sf, n=10, only_web=False)
        output = dictionary['output']
        self.assertLessEqual(len(output), 20)


if __name__ == '__main__':

    unittest.main()

