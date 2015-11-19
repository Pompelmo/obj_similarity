from pairwise_distance import *
from loading import loading
import unittest

# load the models needed
corpus, tfidf, index, tfidf_dict, tfidf_web, \
    mean_dict, ball_tree, d2v_model, des_dict, w2v_model, key_dict = loading()


class MyTestCase(unittest.TestCase):

    # ----------------------- tfidf distance
    def test_tfidf_dist_correct_float(self):
        self.assertIsInstance(tfidf_distance(corpus, tfidf, tfidf_web,
                                             'www.spaziodati.eu', 'spaziodati.eu', 1.0), float)

    def test_tfidf_dist_correct_le_1(self):
        self.assertLessEqual(tfidf_distance(corpus, tfidf, tfidf_web,
                                            'www.spaziodati.eu', 'spaziodati.eu', 1.0), 1.0)

    def test_tfidf_dist_correct_ge_0(self):
        self.assertGreaterEqual(tfidf_distance(corpus, tfidf, tfidf_web,
                                               'www.spaziodati.eu', 'spaziodati.eu', 1.0), 0.0)

    def test_ttfidf_same_website(self):
        self.assertEqual(tfidf_distance(corpus, tfidf, tfidf_web,
                                        'www.spaziodati.eu', 'www.spaziodati.eu', 1.0), 0.0)

    def test_tfidf_first_incorrect(self):
        self.assertEqual(tfidf_distance(corpus, tfidf, tfidf_web,
                                        'asjdbnamsx', 'www.spaziodati.eu', 1.0), 1.0)

    def test_tfidf_second_incorrect(self):
        self.assertEqual(tfidf_distance(corpus, tfidf, tfidf_web,
                                        'www.spaziodati.eu', 'asjdbnamsx', 1.0), 1.0)

    def test_tfidf_both_incorrect(self):
        self.assertEqual(tfidf_distance(corpus, tfidf, tfidf_web,
                                        'akcnmsnalk', 'asjdbnamsx', 1.0), 1.0)

    # ----------------------- w2v distance
    def test_w2v_dist_correct_float(self):
        self.assertIsInstance(w2v_distance(mean_dict, 'www.spaziodati.eu', 'spaziodati.eu', 1.0), float)

    def test_w2v_dist_correct_le_1(self):
        self.assertLessEqual(w2v_distance(mean_dict, 'www.spaziodati.eu', 'spaziodati.eu', 1.0), 1.0)

    def test_w2v_dist_correct_ge_0(self):
        self.assertGreaterEqual(w2v_distance(mean_dict, 'www.spaziodati.eu', 'spaziodati.eu', 1.0), 0.0)

    def test_w2v_same_website(self):
        self.assertEqual(w2v_distance(mean_dict, 'www.spaziodati.eu', 'www.spaziodati.eu', 1.0), 0.0)

    def test_w2v_first_incorrect(self):
        self.assertEqual(w2v_distance(mean_dict, 'asjdbnamsx', 'www.spaziodati.eu', 1.0), 1.0)

    def test_w2v_second_incorrect(self):
        self.assertEqual(w2v_distance(mean_dict, 'www.spaziodati.eu', 'asjdbnamsx', 1.0), 1.0)

    def test_w2v_both_incorrect(self):
        self.assertEqual(w2v_distance(mean_dict, 'akcnmsnalk', 'asjdbnamsx', 1.0), 1.0)

    # ----------------------- w2v distance
    def test_d2v_dist_correct_float(self):
        self.assertIsInstance(d2v_distance(d2v_model, 'www.spaziodati.eu', 'spaziodati.eu', 1.0), float)

    def test_d2v_dist_correct_le_1(self):
        self.assertLessEqual(d2v_distance(d2v_model, 'www.spaziodati.eu', 'spaziodati.eu', 1.0), 1.0)

    def test_d2v_dist_correct_ge_0(self):
        self.assertGreaterEqual(d2v_distance(d2v_model, 'www.spaziodati.eu', 'spaziodati.eu', 1.0), 0.0)

    def test_d2v_same_website(self):
        self.assertEqual(d2v_distance(d2v_model, 'www.spaziodati.eu', 'www.spaziodati.eu', 1.0), 0.0)

    def test_d2v_first_incorrect(self):
        self.assertEqual(d2v_distance(d2v_model, 'asjdbnamsx', 'www.spaziodati.eu', 1.0), 1.0)

    def test_d2v_second_incorrect(self):
        self.assertEqual(d2v_distance(d2v_model, 'www.spaziodati.eu', 'asjdbnamsx', 1.0), 1.0)

    def test_d2v_both_incorrect(self):
        self.assertEqual(d2v_distance(d2v_model, 'akcnmsnalk', 'asjdbnamsx', 1.0), 1.0)

if __name__ == '__main__':
    unittest.main()
