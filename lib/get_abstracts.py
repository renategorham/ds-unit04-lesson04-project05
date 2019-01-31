#Get abstracts module
#-----------------------------------------------------------
#Takes a search term and a search size and
#returns a csv file of the corpus to study.
#

import numpy as np
import pandas as pd
from Bio import Entrez
import os
import csv

def get_abstracts(search_term, n, email, api_key):
    '''this file takes a search term and returns a list of abstracts
       from the PubMed database. PubMed requires an email account and
       api_key cf. https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/''' 

#get PID list. Entrez.esearch
    Entrez.email = email
    Entrez.api_key = api_key
    handle = Entrez.esearch(db='pubmed', retmax=35500, 
            term=search_term, idtype='pmid')
    record = Entrez.read(handle)
    handle.close()
    pmid_list = record['IdList'][0:n-1]

#get abstract list as dict. Entrez.efetch
    abstract_dict = {}
    without_abstract = []

    Entrez.email = email
    Entrez.api_key = api_key
    handle = Entrez.efetch(db='pubmed', id=pmid_list, 
            rettype='xml', retmode='text')
    records = Entrez.read(handle)
    handle.close()

#put abstracts in dict where key is PMID and value is abstract
    for pubmed_article in records['PubmedArticle']:
        pmid = str(pubmed_article['MedlineCitation']['PMID'])
        article = pubmed_article['MedlineCitation']['Article']
        if 'Abstract' in article:
            abstract = article['Abstract']['AbstractText'][0]
            # data_dir = './data/abstracts/'
            # file_name = pmid + '.csv'
            # with open(os.path.join(data_dir, file_name), 'w') as f:
            #     w = csv.writer(f)
            #     w.writerows(abstract)
            abstract_dict[pmid] = abstract
#some PMIDs amy not have an abstract, place those PMIDs in list
        else:
            without_abstract.append(pmid)

#write abstact dict to csv file
    data_dir = './data/'
    file_name = search_term + '.csv'
    with open(os.path.join(data_dir, file_name),'w') as f:
       w = csv.writer(f)
       w.writerows(abstract_dict.items())
        
