#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from Bio import Entrez, Medline
import time
import pandas as pd
import sys
    
def pubSearch(term,email,max_results=None,batch_size=1000,verbose=True,output_file=None):
    Entrez.email = email
    if verbose:
        print(term)
    # VERIFICAR TOTAL
    h = Entrez.esearch(db='pubmed', term=term)

    record = Entrez.read(h)
    MAX_COUNT = int(record['Count'])
    if max_results == None:
        MAX_COUNT = int(record['Count'])
    else:
        MAX_COUNT = max_results
        if max_results < batch_size:
            batch_size = max_results
    r=[]
    # FAZER DOWNLOAD
    c=0
    print('0/'+str(MAX_COUNT))
    if output_file != None:
        pd.DataFrame(r).to_csv(output_file, encoding='utf-8', header=False, index=False, sep='\t')
    for start in range(0, MAX_COUNT, batch_size):
        tudoCerto = False
        while tudoCerto == False:
            try:
                h = Entrez.esearch(db='pubmed', retstart=start, retmax=batch_size, term=term)
                result = Entrez.read(h)
                ids = result['IdList']
                h = Entrez.efetch(db='pubmed', id=ids, rettype='medline', retmode='text')
                records = Medline.parse(h)
                for record in records:

                    ab = record.get('AB', '')
                    ab = re.sub('\s+',' ',ab)
                    ti = record.get('TI', '')
                    ti = re.sub('\s+',' ',ti)
                    pmid = record.get('PMID', '')
                    aut = record.get('FAU', '')
                    dp = record.get('DP', '')
                    seperator = ';'
                    aut = re.sub('\s+',' ',seperator.join(aut))
                    row = {
                    'pmid': int(pmid),
                    'ti': ti,
                    'ab': ab,                 
                    'fau': aut,
                    'dp': dp,
                    }
                    r.append(row)
                tudoCerto = True
            except KeyboardInterrupt:
                sys.exit()
            except Exception as e:
                print ('Error: ' + str(e))
                if verbose:
                    print('Trying again in 3 seconds...')
                tudoCerto = False
                if verbose:
                    print(str(min([c,MAX_COUNT]))+'/'+str(MAX_COUNT))
            # se nao for o ultimo loop, aguardar 3 segundos antes de continuar
            if (start+batch_size) < MAX_COUNT:
                time.sleep(3)    
        c += batch_size
        if verbose:
            print(str(min([c,MAX_COUNT]))+'/'+str(MAX_COUNT))
        if output_file != None:
            pd.DataFrame(r).to_csv(output_file, mode='a', encoding='utf-8', header=False, index=False, sep='\t')
            r = []
    if max_results != None:
        r = r[0:max_results]
    return pd.DataFrame(data=r)