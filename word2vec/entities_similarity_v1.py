import scan_tn_web_idg as stwi
import globalvariable as gv
import pickle
import requests
from math import sqrt

gv.init()

r = 'http://api.dandelion.eu/datatxt/rel/v1?' + '$app_id=' + gv.app_id + '&$app_key=' + gv.app_key + '&lang=it'


def entity_sim(company_ent_1, company_ent_2):
    """given two companies' sets of entities, compute the similarity between them"""
    # should we use also the score of the entities?

    s1 = '&topic1='         # this is needed to create the request
    s2 = '&topic2='         # this is needed to create the request

    company_ent_1 = [item[0] for item in company_ent_1]     # take only entities, not scores
    company_ent_2 = [item[0] for item in company_ent_2]     # take only entities, not scores

    k = len(company_ent_1) // 10        # this is not needed for idg, because we have a
    l = len(company_ent_2) // 10        # maximum entities cardinality of 10

    # for the resulting matrix we're gonna use a L2 norm
    under_square = 0                # prepare the variable to sum everything

    for i in range(0, k+1):                     # "hack" since the request can't hold more than 10 keywords

        imax = min((i+1)*10, len(company_ent_1))  # to avoid out of index

        for j in range(0, l+1):                 # still needed for the request limit

            jmax = min((j+1)*10, len(company_ent_2))  # to avoid out of index

            # now we're constructing the request
            req = requests.get(r + '&topic1=' + s1.join(company_ent_1[i*10:imax])  # max ten at a time
                               + '&topic2=' + s2.join(company_ent_2[j*10:jmax]))   # also max ten at a time

            try:
                jsondict = req.json()  # read it in a json format, usable by python

            except ValueError:
                print 'Error'
                return "Error"

            if u'relatedness' in jsondict.keys():  # if the query produced some results

                for item in jsondict[u'relatedness']:  # let's retrieve every combination

                    under_square += item[u'weight']**2  # part of the formula for the L2 norm

    return sqrt(under_square)   # return the L2 norm (-> sqrt(a_1^2 +...+a_n^2) )


def extract_entities():
    """from a dictionary[website]=source entities are extracted"""

    entities = dict()           # instance the dictionary that's gonna be dict[website] = entities

    # get the dictionary[website]=source
    sources = stwi.scan_tn_web_idg()

    for key in sources:                             # for every item tha we have retrieved
        entiti = []
        if u'entities' in sources[key].keys():      # check if it has entities
            for item in sources[key][u'entities']:  # then retrieve all entities
                entiti.append((item[u'entity'], item[u'score']))

        if entiti:                                  # if entity is non-empty
            entities[key] = entiti                  # then create an instance in the dictionary

    return entities     # return a dictionary[website] = entity


def main():
    sim_dict = dict()

    # this is a dictionary[website_id] = [list of url wikipedia pages of the entities]
    entities = extract_entities()
    keys = entities.keys()

    for i in range(0, len(keys)):
        for j in range(i+1, len(keys)):
            sim_dict[(keys[i], keys[j])] = entity_sim(entities[keys[i]], entities[keys[j]])

        print i

    output = open('source/EntitiesSimilarity.pkl', 'wb')

    # save the similarity dictionary constructed as pickle obj
    pickle.dump(sim_dict, output)

    output.close()


if __name__ == '__main__':
    main()
