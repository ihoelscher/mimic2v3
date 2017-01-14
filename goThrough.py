# A simple scraper to get the directory
# structure for all records at the MIMIC II Waveform Database.
# Each intermediate levels will be a dictionary where:
#   for each key (record), the value is a list of files in the record directory.
#
# Example:
# intermediate level 30 - DBstructure/30.pkl
# { '3000003': ['3000003.hea', '3000003_001.dat', ..., '3000003n.hea']
#   ...
#   '3099997': ['3099997.hea', '3099997_001.dat', ..., '309997n_005.dat']   }


from bs4 import BeautifulSoup as bs
import requests

mimic2wb = "https://www.physionet.org/physiobank/database/mimic2wdb/"
intermediate_levels = ['%s/' % i for i in range(31, 40)]

def getMimicFiles(html, level):
    """ Create the dictionary for a intermediate level """

    rec_files = dict()

    lvl_link = html+level
    soup = bs(requests.get(lvl_link).text, "lxml")
    records = [a['href'] for a in soup.find_all('a') if a['href'].startswith(level.split('/')[0])]

    for rec in records:
        rec_link = lvl_link+rec
        soup = bs(requests.get(rec_link).text, "lxml")
        files = [a['href'] for a in soup.find_all('a') if a['href'].startswith(level.split('/')[0])]

        rec_files[rec.split('/')[0]] = files

    return rec_files

import pickle
def saveMimicStructure(dict, name):
    with open('DBstructure/'+name+'.pkl', 'wb') as f:
        pickle.dump(dict, f, pickle.HIGHEST_PROTOCOL)

for i in intermediate_levels:
    files = getMimicFiles(mimic2wb, i)
    saveMimicStructure(files, i.split('/')[0])

print 'ok'

