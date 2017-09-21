
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:53:02 2017

@author: Diabetes.co.uk
"""
###############################################################
##Dependencies
###############################################################
import pickle as cPickle
import os 
import sys
import heapq
from collections import Counter
os.chdir(os.path.dirname(sys.argv[0]))
#os.chdir('C:\\Git\\SelfcontainedQNA - Copy')

FNAME1 = 'CSVfiles\\model.pickle'

with open(FNAME1, 'rb') as f:
    clf = cPickle.load(f)

import numpy as np
import pandas as pd

import ourfeatures2
import functions_for_extracting_pronouns_and_entities_using_api as extract

###############################################################
##Section for predicting the class of the question
###############################################################

keys = ["id",
"wordCount",
"stemmedCount",
"stemmedEndNN",
"CD",
"NN",
"NNP",
"NNPS",
"NNS",
"PRP",
"VBG",
"VBZ",
"startTuple0",
"endTuple0",
"endTuple1",
"verbBeforeNoun",
"informationanddefinitionTriplesScore",
"complicationsTriplesScore",
"manifestationTriplesScore",
"causeScore",
"complicationsScore",
"manifestationScore",
"diagnosisScore",
"managementScore",
"class"]

#Function for extracting the features of the questions based on clf
def Question_features(sentence):
    features = {}
    #Extracting the class
    myFeatures = ourfeatures2.features_dict('1',sentence, 'X')
    values=[]
    for key in keys:
        values.append(myFeatures[key])
    s = pd.Series(values)
    width = len(s)
    myFeatures = s[1:width-1]
    predictedclass = clf.predict([myFeatures])
    features['Class'] = str(predictedclass)[2:-2]
    
    #Extracting the adjectives and nouns of the questions:
    tokens = extract.get_tokens(sentence)
    #Nouns
    NOUN = extract.Nounswords(tokens)
    features['Nouns'] = NOUN
    #Adjectives
    ADJECTIVE = extract.Adjectivewords(tokens)
    features['Adjectives'] = ADJECTIVE 
    #Named entities
    named_entities = extract.entities_name1(sentence)
    features['Named Entities'] = named_entities
    
    return(features)
        


Questions = pd.read_csv('sampledatabase.csv', index_col = 'ID', encoding = 'utf-8')

##matching the questions with the informations stored in the database
#example    
sentence = 'what are the causes of type 2 diabetes?'
result = Question_features(sentence)# insert sentence of intrest, and run the file or code below to get the predicted class and named entites of the sentence entered.
print(result)

question_from_same_class = Questions[Questions['CLASS'] == result['Class'][1:]]


######################################################
#The for loops the functions above is based upon, the entire section below is the answer
#selection method based upon matching the entities of the question entered, and the 
#entities of the 1st sentence of the answers.
######################################################

AnswerAdjectives = []
AnswerEntities = []
AnswerNouns = []
for items in question_from_same_class['AnswerNouns']:
    item = items[1:-1].split(',')
    a=[]
    for i in item:
        c = i.strip().lower()[1:-1]
        a.append(c)
    AnswerNouns.append(set(a))


for items in question_from_same_class['AnswerEntities']:
    item = items[1:-1].split(',')
    a=[]
    for i in item:
        c = i.strip().lower()[1:-1]
        a.append(c)
    AnswerEntities.append(set(a))


for items in question_from_same_class['AnswerAdjectives']:
    item = items[1:-1].split(',')
    a=[]
    for i in item:
        c = i.strip().lower()[1:-1]
        a.append(c)
    AnswerAdjectives.append(set(a))

######################################################
#The code below is a match and selection method based with the same as the idea above,
#but it uses the entities of the questions instead of the 1st sentence of the answers.
######################################################

QuestionsAdjectives = []
QuestionsEntities = []
QuestionsNouns = []
for items in question_from_same_class['QuestionsNouns']:
    item = items[1:-1].split(',')
    a=[]
    for i in item:
        c = i.strip().lower()[1:-1]
        a.append(c)
    QuestionsNouns.append(set(a))


for items in question_from_same_class['QuestionsEntities']:
    item = items[1:-1].split(',')
    a=[]
    for i in item:
        c = i.strip().lower()[1:-1]
        a.append(c)
    QuestionsEntities.append(set(a))


for items in question_from_same_class['QuestionsAdjectives']:
    item = items[1:-1].split(',')
    a=[]
    for i in item:
        c = i.strip().lower()[1:-1]
        a.append(c)
    QuestionsAdjectives.append(set(a))


#####################################################
#####Appending the entities of the questions and 1st sentences
#####################################################
Entities = []
Nouns = []
Adjectives = []

for i in range(len(AnswerAdjectives)):
    result1 = AnswerAdjectives[i].union(QuestionsAdjectives[i])
    Adjectives.append(result1)
    result2 = AnswerEntities[i].union(QuestionsEntities[i])
    Entities.append(result2)
    result3 = AnswerNouns[i].union(QuestionsNouns[i])
    Nouns.append(result3)

#####################################################
#####The counting functions for each feature
#####################################################

def counting_adjectives(results,rows):
    counts = 0
    adjectives = results['Adjectives']
    for items in rows:
        if items in adjectives:
            counts += 1
    return(counts)


a = []
attl = []
for rows in Adjectives:
    attl.append(len(rows))
    unique = list(rows)
    d = counting_adjectives(result, rows)
    a.append(d)

###################################################### 
def counting_entities(results,rows):
    counts = 0
    entities = results['Named Entities']
    for items in rows:
        if items in entities:
            counts += 1
    return(counts)


b = []
bttl = []
for rows in Entities:
    bttl.append(len(rows))
    unique = list(rows)
    d = counting_entities(result, rows)
    b.append(d)


######################################################
def counting_nouns(results,rows):
    counts = 0
    nouns = results['Nouns']
    for items in rows:
        if items in nouns:
            counts += 1
    return(counts)


c = []
cttl = []
for rows in Nouns:
    cttl.append(len(rows))
    unique = list(rows)
    d = counting_nouns(result, rows)
    c.append(d)

######################################################
e = zip(a,b,c)
eeee = [sum(x) for x in e]
eeee1 = eeee

ettl = zip(attl,bttl,cttl)
eeeettl = [sum(x) for x in ettl]
eeee1ttl = eeeettl

new = zip(eeee,eeeettl)
ann = [float(x) / float(y) for x, y in zip(eeee,eeeettl)]
#ann = list(np.divide(eeee,eeeettl))

l22 = heapq.nlargest(3, ann)

######################################################

counts = Counter(l22) # so we have: {'name':3, 'state':1, 'city':1, 'zip':2}
for s,num in counts.items():
    if (num > 1) and (s != 0): # ignore strings that only appear once
        for suffix in range(1, num + 1): # suffix starts at 1 and increases by 1 each time
            ann[ann.index(s)] = s + suffix # replace each appearance of s

######################################################
l221 = heapq.nlargest(3, ann)

def retrieving_Questions(dataframe):
    n = []
    for i in l221:
        n.append(ann.index(i))
    Questionss = {}
    for i in n:
        Questionss[i] = dataframe['ANSWER'].iloc[i]
    return(Questionss)

nn = retrieving_Questions(question_from_same_class)
a = []
    
print(sentence)
for key, value in nn.items():
    print('AnswerID:', key,': ', value.encode('UTF-8'))






