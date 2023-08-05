#!/usr/bin/python
# -*- coding: utf-8 -*-
import tempfile
import os
from Bio import AlignIO, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import re
import numpy as np
from scipy import stats
import codecs
from . import aminocode
import pandas as pd
from os import path
from sys import platform
from sweep import fas2sweep

def dendroscope(tree,dendroscope_exe_local='C:\Program Files\Dendroscope\Dendroscope.exe'):
    if platform != 'win32':
        print("Sorry, the dendroscope function is only available for the Windows system currently. Please wait for future versions of the dendroscope.")
        return
    if not path.exists(dendroscope_exe_local) and dendroscope_exe_local=='C:\Program Files\Dendroscope\Dendroscope.exe':
        print("Dendroscope not found in the default directory. If you don't use the default location, you can set the \"dendroscope_exe_local\" parameter to the location of the dendroscope executable on your computer.")
        return
    elif not path.exists(dendroscope_exe_local):
        print("Dendroscope not located at the specified location.")
        return
    fp = tempfile.TemporaryFile(mode='w',delete=False)
    pd.DataFrame(np.array([tree])).to_csv(fp.name, sep='\t', encoding='utf-8', index=False, header=False)
    os.system(dendroscope_exe_local+" -S +s +w -x \"open file='"+fp.name+"';\"" )
    fp.close()
    os.unlink(fp.name)

def clustalo(input_file_name):
    fp = tempfile.TemporaryFile(mode='w',delete=False)
    os.system("clustalo -i "+input_file_name+" -o "+fp.name+" --auto --outfmt clu --force")
    align = AlignIO.read(fp.name, "clustal")
    fp.close()
    os.unlink(fp.name)
    return align
clustalOmega = clustalomega = clustalo
    
def getCons(records):
    seq_list = list(records)
    fastaText = tempfile.TemporaryFile(mode='w',delete=False)
    for i in seq_list:
        fastaText.write('>'+str(i.description)+'\n'+str(i.seq)+'\n')
    fastaText.close()
    
    align = []
    if len(seq_list) > 1:
        align1 = clustalo(fastaText.name)
        align2 = []
        for i in align1:
            align2.append(list(i.seq))
            align.append(str(i.seq))
        align2 = np.array(align2)
        m = stats.mode(align2) # determine mode
        m = m[0][m[1]>=0] # filter characters by minimal occurrence
        consensus = re.sub('\-+','',''.join(m))
    else:
        consensus = str(seq_list[0].seq)
        align.append(consensus)
    
    os.unlink(fastaText.name)
    return consensus, align
getcons = getCons
    
def getCons_text(records,detailing='dp'):
    consensus=getCons(records)
    consensus_text = aminocode.dt(consensus,detailing=detailing)
    return consensus_text
    
# extract headers
def getHeader(records):
    records = list(records)
    headers = []
    for i in records:
        header = i.description
        headers.append (header)
    return headers

# extract seq
def getSeq(records):
    records = list(records)
    seqs = []
    for i in records:
        seq = i.seq
        seqs.append (str(seq))
    return seqs
getseq = getSeq

def list2bioSeqRecord(seq,header=None):
    if header == None:
        header = list(range(0,len(seq)))
    records = []
    for i in range(0,len(seq)):
        record = SeqRecord(Seq(seq[i]), description=str(header[i]), id=str(i))
        records.append(record)
    return records
list2SeqRecord = list2seqrecord = list2fasta = list2bioseqrecord = list2bioSeqRecord

def removePattern(records,rex):
    records = list(records)
    for i in range(0,len(records)):
        for ii in rex:
            s = re.sub(ii,'',str(records[i].seq)) # find and remove id
            records[i].seq=Seq(s)
    new_records = records
    return records
removepattern = removePattern
    
def fastaread(input_file_name):
    records = SeqIO.parse(codecs.open(input_file_name,'r','utf-8'), "fasta")
    return list(records)
fastaRead = fastaread
    
def fastawrite(records, output_file_name):
    fasta = list(records)
    outputFile = codecs.open(output_file_name,'w','utf-8')
    for i in fasta:
        if len(i.seq) > 0:
            outputFile.write('>'+i.description+'\n')
            seq = str(i.seq)
            seq = re.findall('[\w-]{0,'+str(100)+'}',seq)
            seq = '\n'.join(seq)
            outputFile.write(seq)
    outputFile.close()
    return records
fastaWrite = fastawrite

def fastawrite(records, output_file_name):
    fasta = list(records)
    outputFile = codecs.open(output_file_name,'w','utf-8')
    for i in fasta:
        if len(i.seq) > 0:
            outputFile.write('>'+i.description+'\n')
            seq = str(i.seq)
            seq = re.findall('[\w-]{0,'+str(100)+'}',seq)
            seq = '\n'.join(seq)
            outputFile.write(seq)
    outputFile.close()
    return records
fastaWrite = fastawrite

def fastatext2vect(fastatext):
    vect = fas2sweep(fastatext)
    return vect
fastaText2vect = fasta2vect = fastatext2vect