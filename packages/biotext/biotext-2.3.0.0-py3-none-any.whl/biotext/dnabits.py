#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import numpy as np
from Bio import SeqIO
import codecs
from biotext import fastatools

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def to_bin(string):
    res = ''
    for char in string:
        tmp = bin(ord(char))[2:]
        tmp = '%08d' %int(tmp)
        tmp=tmp[::-1]
        res += tmp
    return res
def to_str(string):
    res = ''
    for idx in range(int(len(string)/8)):
        cstr = string[idx*8:(idx+1)*8]
        cstr=cstr[::-1] #???
        tmp = chr(int(cstr, 2))
        res += tmp
    return res

def encodetext(text):
    text=to_bin(text)
    text_0 = re.findall('.',text[0:len(text)-1:2])
    text_1 = re.findall('.',text[1:len(text):2])
    text = np.transpose(np.array([(text_0),(text_1)]))
    text = text.astype(int)
    text = text * [1,2]
    text = np.sum(text,1)
    text = text.astype(str)
    text[text=='0']='A'
    text[text=='1']='C'
    text[text=='2']='G'
    text[text=='3']='T'
    text=''.join(text)
    enc_text = text
    return enc_text
et = encodeText = encodetext

def decodetext(dna):
    text = np.zeros((len(dna),2)).astype(int)
    dna=np.array(re.findall('.',dna))
    text[dna=='A']=[0,0]
    text[dna=='C']=[1,0]
    text[dna=='G']=[0,1]
    text[dna=='T']=[1,1]
    text=text.astype(str)
    text=''.join(np.concatenate(text))
    text=to_str(text)
    dec_text = text
    return dec_text
dt = decodeText = decodetext

def encodefile(input_file,output_file=None,header_format='number+originaltext',verbose=False):
    out = output_file
    selectedEncoder = lambda x: et(x)
    # head file if necessary
    if isinstance(input_file, str): # if string consider filename and read
        read_file = list(SeqIO.parse(codecs.open(input_file,'r','utf-8'), "fasta"))
        if len(read_file) > 0:
            records = []
            for i in read_file:
                records.append (i.description)
        else:
            read_file = codecs.open(input_file,'r','utf-8')
            records = [line.strip() for line in read_file]
            read_file.close()
    else:
        read_file = input_file
        try:
            read_file[0].description #return exception if not fasta
            records = []
            for i in read_file:
                records.append (i.description)
        except:
            records = [line.strip() for line in read_file]
            
    # create header list
    count = 0
    headers = []
    for i in records:
        count += 1
        if header_format == 'number':
            headers.append(count)
        elif header_format == 'originaltext':
            i = re.sub('\n$','',i)
            headers.append(i)
        elif header_format == 'number+originaltext':
            i = re.sub('\n$','',i)
            headers.append(str(count)+' '+i)
        
    seqs = []    
    for c,i in enumerate(records):
        i = re.sub('\n$','',i)
        try:
            i = i.decode('utf-8')
        except:
            pass
        seq = selectedEncoder(i)
        seqs.append(seq)
        if verbose and (c+1) % 10000 == 0:
            print (str(c+1)+'/'+str(count))
    if verbose:
        print (str(count)+'/'+str(count))
    records=fastatools.list2bioSeqRecord(seqs,headers)
    
    if not (out is None):
        records = fastatools.fastawrite(list(records),out)
    return records
ef = encodeFile = encodefile

def decodefile(input_file,output_file=None,verbose=False):
    out = output_file
    selectedEncoder = lambda x: dt(x)
    if verbose:
        print('Decoding text...')
    
    if isinstance(input_file, str): # if string consider filename and read
        records = list(SeqIO.parse(codecs.open(input_file,'r','utf-8'), "fasta"))
    else:
        records = list(input_file)
    num_lines = len(records)
    c=0
    dec_list = []
    for i in records:
        c+=1
        if verbose and (c+1) % 10000 == 0:
            print(str(c+1)+'/'+str(num_lines))
        dec_list.append((selectedEncoder(str(i.seq))))
    if verbose:
        print(str(num_lines)+'/'+str(num_lines))
    if not (out is None):
        outputFile = codecs.open(out,'w','utf-8')
        for i in dec_list:
            outputFile.write(i+'\n')
        outputFile.close()
    
    return dec_list
df = decodeFile = decodefile