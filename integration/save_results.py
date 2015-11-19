import pickle
import requests

collect_result = dict()

api_url = 'endpoint_url'

parameters = {'website': 'www.spaziodati.eu',  # this has to be provided
              'model': 'linear',
              'num_max': 50,
              'only_website': False}

collect_result['www.spaziodati.eu'] = requests.get(api_url, params=parameters).json()

parameters['website'] = 'company.cerved.com'
collect_result['company.cerved.com'] = requests.get(api_url, params=parameters).json()

parameters['website'] = 'zanormac.net'
collect_result['zanormac.net'] = requests.get(api_url, params=parameters).json()

parameters['website'] = 'www.ceda.it'
collect_result['www.ceda.it'] = requests.get(api_url, params=parameters).json()

parameters['website'] = 'www.ravinacar.it'
collect_result['www.ravinacar.it'] = requests.get(api_url, params=parameters).json()

parameters['website'] = 'www.birreriaedavena.com'
collect_result['www.birreripedavena.com'] = requests.get(api_url, params=parameters).json()

parameters['website'] = ['www.spaziodati.eu', 'spaziodati.eu']
collect_result['spaziodati_list'] = requests.get(api_url, params=parameters).json()

output = open('source/results_03112015.pkl', 'wb')
pickle.dump(collect_result, output)
output.close()
