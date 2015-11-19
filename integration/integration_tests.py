from loading import loading
from integration import Integration
import unittest

corpus, tfidf, index, tfidf_dict, tfidf_web, \
    mean_dict, ball_tree, d2v_model, des_dict, w2v_model, key_dict = loading()

integra = Integration(corpus, tfidf, index, tfidf_web, mean_dict, ball_tree, d2v_model)


class MyTestCase(unittest.TestCase):

    def test_ms_tfidf_website_full_attribute_scores(self):
        self.assertEqual(len(integra.ms_tfidf('www.spaziodati.eu', n=20)[0]), 20)

    def test_ms_tfidf_website_full_attribute_rank(self):
        self.assertEqual(len(integra.ms_tfidf('www.spaziodati.eu', n=20)[1]), 20)

    def test_ms_w2v_website_full_attribute_scores(self):
        self.assertEqual(len(integra.ms_w2v_key('www.spaziodati.eu', n=20)[0]), 20)

    def test_ms_w2v_website_full_attribute_rank(self):
        self.assertEqual(len(integra.ms_w2v_key('www.spaziodati.eu', n=20)[1]), 20)

    def test_ms_d2v_website_full_attribute_scores(self):
        self.assertEqual(len(integra.ms_d2v('www.spaziodati.eu', n=20)[0]), 20)

    def test_ms_d2v_website_full_attribute_rank(self):
        self.assertEqual(len(integra.ms_d2v('www.spaziodati.eu', n=20)[1]), 20)

    def test_ms_tfidf_wrong_web_score(self):
        self.assertEqual(len(integra.ms_tfidf('akjsdkjas', n=20)[0]), 0)

    def test_ms_tfidf_wrong_web_rank(self):
        self.assertEqual(len(integra.ms_tfidf('akjsdkjas', n=20)[1]), 0)

    def test_ms_w2v_wrong_web_score(self):
        self.assertEqual(len(integra.ms_w2v_key('akjsdkjas', n=20)[0]), 0)

    def test_ms_w2v_wrong_web_rank(self):
        self.assertEqual(len(integra.ms_w2v_key('akjsdkjas', n=20)[1]), 0)

    def test_ms_d2v_wrong_web_score(self):
        self.assertEqual(len(integra.ms_d2v('akjsdkjas', n=20)[0]), 0)

    def test_ms_d2v_wrong_web_rank(self):
        self.assertEqual(len(integra.ms_d2v('akjsdkjas', n=20)[1]), 0)

    def test_ms_tfidf_web_no_keywords_score(self):
        self.assertEqual(len(integra.ms_tfidf('company.cerved.com', n=20)[0]), 20)

    def test_ms_tfidf_web_no_keywords_rank(self):
        self.assertEqual(len(integra.ms_tfidf('company.cerved.com', n=20)[1]), 20)

    def test_ms_w2v_web_no_keywords_score(self):
        self.assertEqual(len(integra.ms_w2v_key('company.cerved.com', n=20)[0]), 0)

    def test_ms_w2v_web_no_keywords_rank(self):
        self.assertEqual(len(integra.ms_w2v_key('company.cerved.com', n=20)[1]), 0)

    def test_ms_d2v_web_no_keywords_score(self):
        self.assertEqual(len(integra.ms_d2v('company.cerved.com', n=20)[0]), 20)

    def test_ms_d2v_web_no_keywords_rank(self):
        self.assertEqual(len(integra.ms_d2v('company.cerved.com', n=20)[1]), 20)

if __name__ == '__main__':
    unittest.main()
