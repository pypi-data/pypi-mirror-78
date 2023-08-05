#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import unidecode
from Bio import SeqIO
import codecs
from biotext import fastatools

aminoCode_table = {
      "a": "YA",
      "b": "E",
      "c": "C",
      "d": "D",
      "e": "YE",
      "f": "F",
      "g": "G",
      "h": "H",
      "i": "YI",
      "j": "I",
      "k": "K",
      "l": "L",
      "m": "M",
      "n": "N",
      "o": "YQ",
      "p": "P",
      "q": "Q",
      "r": "R",
      "s": "S",
      "t": "T",
      "u": "YV",
      "v": "V",
      "x": "W",
      "z": "A",
      "w": "YW",
      "y": "YY",
      ".": "YP",
      "9": "YD",
      " ": "YS",
}

aminoCode_table_d = {
      "0": "YDA",
      "1": "YDQ",
      "2": "YDT",
      "3": "YDH",
      "4": "YDF",
      "5": "YDI",
      "6": "YDS",
      "7": "YDE",
      "8": "YDG",
      "9": "YDN",
}

aminoCode_table_p = {
      ".": "YPE",
      ",": "YPC",
      ";": "YPS",
      "!": "YPW",
      "?": "YPQ",
      ":": "YPT",
}

def details(text,all_tables):
    table = dict()
    for i in all_tables:
        table.update(i)
    for k,v in table.items():
        text = text.replace(k, v)
    return text        

def encodetext(text,detailing=''):
    det = detailing
    try:
        text = text.decode('utf-8') #decode
    except:
        pass
    
    text = unidecode.unidecode(text) #remove accents
    text = text.lower() #lower case
    text = re.sub('\s',' ',text) #all spaces to " "
    
    # apply expanded coding
    all_tables = []
    if 'd' in det:
        all_tables.append(aminoCode_table_d)
    else:
        text = re.sub('\d','9',text) #all numbers to 9
    if 'p' in det:
        all_tables.append(aminoCode_table_p)
    else:
        text = re.sub('[,;!?:]','.',text) #all punctuation to "."
    if len (all_tables) > 0:
        text = details(text,all_tables)
        
    # apply minimal coding
    for k,v in aminoCode_table.items():
        text = text.replace(k, v)
        
    # apply joker 
    for c,i in enumerate(text.lower()):
        if i not in aminoCode_table:
            text=re.sub('\\'+i,'YK',text)
    enc_text = text
    return enc_text
et = encodeText = encodetext

def details_r(text,all_tables):
    table = dict()
    mm = ''
    for i in all_tables:
        table.update(i)
        m = list(i.values())[0]
        m = m[1]
        mm += m
    for key,value in table.items():
        if re.search('Y['+mm+']\w',value):
            text = re.sub(value,key,text)
    return text
    
def decodetext(text,detailing=''):
    det = detailing
    all_tables = []
    if 'd' in det:
        all_tables.append(aminoCode_table_d)
    if 'p' in det:
        all_tables.append(aminoCode_table_p)
    if len (all_tables) > 0:
        text = details_r(text,all_tables)
        
    for key,value in aminoCode_table.items():
        if re.search('Y\w',value):
            text = re.sub(value,key,text)
    text = re.sub('YK','-',text)
    for key,value in aminoCode_table.items():
        text = re.sub(value,key,text)
    dec_text = text
    return dec_text
dt = decodeText = decodetext

def encodefile(input_file,output_file=None,detailing='',header_format='number+originaltext',verbose=False):
    out = output_file
    det = detailing
    selectedEncoder = lambda x: et(x,detailing=det)
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
    records = fastatools.list2bioSeqRecord(seqs,headers)
    
    if not (out is None):
        records = fastatools.fastawrite(list(records),out)
    return records
ef = encodeFile = encodefile

def decodefile(input_file,output_file=None,detailing='',verbose=False):
    out = output_file
    det = detailing
    selectedEncoder = lambda x: dt(x,detailing=det)
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