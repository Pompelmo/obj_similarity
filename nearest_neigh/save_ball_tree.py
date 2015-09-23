# -------------------------------------------------
# create and save ball_tree for nearest neighbors
# -------------------------------------------------

import pickle
import numpy as np
from sklearn.neighbors import BallTree
from datetime import datetime


print datetime.now(), "loading dictionary for w2v keywords n_similarity"
mean_dict_file = open('source/mean_dict_key_scan.pkl', 'r')
mean_dict = pickle.load(mean_dict_file)
mean_dict_file.close()


values = mean_dict.values()
arrays = np.array(values)
nbrs = BallTree(arrays, leaf_size=30)
output = open("source/ball_tree", "wb")
pickle.dump(nbrs, file=output)
output.close()
