Given a website in input we suggest similar websites. 
The suggestions are given by some queries on three different models:
 * word2vec on websites keywords
 * doc2vec on websites descriptions
 * tfidf on websites crawled texts

<h2>Description of the functions on the integration directory </h2>
<h3> bottle_prova.py </h3>
In this script the bottle library is used in order to have an endpoint to query the models.
A dictionary with all the suggested websites is computed using the *CreateJson* class, in **gen_json.py**. The dictionary
is then ordered by means of the total score, a combination of information from the three models. 
Total score is computed using the *ScoreFunc* class, contained in **ScoreFunc.py**. 
The function to compute the total score can be chosen in a predefined set.
The **bottle_prova.py** is such that the model can be queried in the browser as 
*.../suggest?website=your_website&model=chosen_score_func(&only_website=boolean)*

<h3> compute_max.py </h3>
This script scan the index to find 10000 websites we used for the models and saves their number of keywords, number
of description tokens and number of text tokens. A plot of the sample distributions can then computed with an R script.

<h3> gen_json.py </h3>
This script contains the class *CreateJson* that is mainly used to create a json with suggested websites and 
their informations, related to the used models.
It depends on the class *Counter* from **how_many.py**, the class *Integration* from **integration.py** and 
*pairwise_distance*. *Counter* is used to retrieve websites metadata, *Integration* to retrieve the suggested
websites from a single model and *pairwise_distance* to compute the distance for 
suggested websites in the other models. For example, the distances in doc2vec and tfidf 
of a website suggested by word2vec 
(computed using *Integration*), is computed using some function in *pairwise_distance*.
In *CreateJson* the combined json is computed using *get_json* function, that relies on four functions.
The first one, **inp_web_info** retrieve the websites metadata:
keywords in w2v number, description tokens used in d2v number, text tokens used in tfidf number, 
and for the input websites also the keywords and description tokens.
The other three functions **model_websites** take a model, 
compute their first 20 suggested websites, and compute the distance of those
websites from the input website in the other models.
Then the dictionaries with all the suggested websites with all the informations are combined in *get_json*,
adding some metadata information on the input website. A complete dictionary is then returned, 
it is then ordered using the total_score in **bottle.py** script.

<h3> how_many.py </h3>
In **how_many.py** there is the *Counter* class. It is used to retrieve the following metadata of the websites:
 * Keywords list
 * description tokens list
 * text tokens number
 * keyword number
 * description token number
For keywords and description it is performed a query on the index, while for the text, the non-zero entries
on the tfidf vector are counted.

<h3> integration.py </h3>
In this script the class *Integration* is contained. This class has three similar methods. They are one
for every models, and they return:
* an ordered list of suggested websites
* an ordered list of scores (distance from the input url)
* an ordered list of attribute number (keywords number, ...) [if asked]

<h3> interactive.py </h3>
*Since other script have been heavily modificated, this doesn't work at the moment. It is used to query the*
*models from the terminal, it asks in input some parameters that affect the total_score function*

<h3> loading.py </h3>
This script simply loads the models that we need.

<h3> main.py </h3>
*In main it is possible to ask for the scores of the three models. A table is drawn on the terminal. This has*
*to be changed to match the modification done in the other scripts*

<h3> pairwise_distance.py </h3>
In this script there are three function, each of them is used to compute the distance between two websites 
(in their vectorial representation) in one of the models.

<h3> ScoreFunc.py </h3>
Here functions to compute the total score are defined changing the parameters. The function is then chosen 
in the bottle script, and used to order the suggested websites. The following function can be chosen (at the moment):
* linear: 1/3.0 * w2v distance + 1/3.0 * d2v distance + 1/3.0 * tfidf distance
* simple_weighted: 1/3.0 * w2v distance * # keywords/15 + 1/3.0 * d2v distance * # description tokens/700 + 1/3.0 *  tfidf distance * # text tokens/30000
* w2v: 1 * w2v distance + 0 * d2v distance + 0 * tfidf distance
* d2v: 0 * w2v distance + 1 * d2v distance + 0 * tfidf distance
* tfidf: 0 * w2v distance + 0 * d2v distance + 1 * tfidf distance

The numbers to normalize the keywords number, description tokens and text tokens have been chosen after computing
the sample distribution with **compute_max.py**.

<h3> TokenStem.py </h3>
This class is used to compute the tokenization and stemming of the list keywords or description or 
text of the websites. It relies on the library **re** for the tokenization and **nltk** for the stemming.
