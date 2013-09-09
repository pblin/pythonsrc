#!/usr/bin/env python

from pymongo import MongoClient

dictDir = '/home/bernard/storia_dictionary/'

def getWords (txt):
    words = str(txt).strip('\n').split('\t')
    del words[0]
    return words

client = MongoClient('localhost', 27017)
db = client['ePub']

words = db.dict

with open(dictDir+'WordFormTable.txt') as wordFormText:
    wordFormTable = [ getWords(line) for line in wordFormText ]
    
for entry in wordFormTable:
    word = { "word": entry[0].lower(), "orig": entry[1], "ver":entry[3].upper() }
    words.insert (word)



