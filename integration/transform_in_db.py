import shelve
import pickle

# open dictionary website -> keywords
inp_key = open('source/key_dict.pkl', 'r')
key_dict = pickle.load(inp_key)
inp_key.close()

key_len = dict()  # store the length of the keywords

# open the database, to write
key_db = shelve.open('source/key_dict_db.db')

# write on the database and create a dictionary with the length of the keywords
for key in key_dict:
    key_db[str(key)] = key_dict[key]
    key_len[key] = len(key_dict[key])

key_db.close()

# --------------------------------------------

# open the dictionary website -> tokenized description
inp_des = open('source/des_dict.pkl', 'r')
des_dict = pickle.load(inp_des)
inp_des.close()

des_len = dict()  # store the length of the description

# open the database in order to store the descriptions
des_db = shelve.open('source/des_dict_db.db')

# write the descriptions on the database and create a dictionary with the lengths
for key in des_dict:
    des_db[str(key)] = des_dict[key]
    des_len[key] = len(des_dict[key])

des_db.close()

# retrieve keys that are in the web->description dict or in the web->keywords dict
keys = set(des_dict.keys() + key_dict.keys())

# dictionary with both info
len_dict = dict()

d_key = set(des_dict.keys())
k_key = set(key_dict.keys())
# now create a new dictionary that store them togheter, to gain memory
for key in keys:

    if key in d_key and key in k_key:  # it appears in both dictionaries?
        len_dict[key] = (key_len[key], des_len[key])

    elif key in d_key:                           # it appears only in des? (the both case is already excluded)
        len_dict[key] = (0, des_len[key])

    else:                                                  # or it appears only in key (other cases excluded)
        len_dict[key] = (key_len[key], 0)


out_des = open('source/key_des_len.pkl', 'wb')
pickle.dump(len_dict, out_des, protocol=pickle.HIGHEST_PROTOCOL)
out_des.close()
