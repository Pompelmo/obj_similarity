import csv
import dandelion
import scanTnWeb
import globalvariable as gv

gv.init()

dandelion.default_config['app_id'] = gv.app_id
dandelion.default_config['app_key'] = gv.app_key

datatxt = dandelion.DataTXT()

# print datatxt.sim(text1='https://it.wikipedia.org/wiki/Software',
#                   text2='https://it.wikipedia.org/wiki/Hardware', lang='it')

