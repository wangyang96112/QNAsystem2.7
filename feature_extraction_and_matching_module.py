
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

Question = 'what are the causes of type 2 diabetes?'

nterms = 5

###################################################################################        
## The line of code below is for loading the database into the dataframe
## this can be modified so it can interact with sql, and use the tables from sql
###################################################################################
Questions = pd.read_csv('CSVfiles\\sampledatabase.csv', index_col = 'ID', encoding = 'utf-8')

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
        



##matching the questions with the informations stored in the database
#example    
result = Question_features(Question)# insert question of intrest, and run the file or code below to get the predicted class and named entites of the sentence entered.
#print(result)

question_from_same_class = Questions[Questions['CLASS'] == result['Class'][1:]]


######################################################
#The for loops the functions above is based upon, the entire section below is the answer
#selection method based upon matching the entities of the question entered, and the 
#entities of the 1st sentence of the answers.
######################################################

#an empty list is created for each of the current intrested features used for matching for the answers
AnswerAdjectives = []
AnswerEntities = []
AnswerNouns = []

#creating for loop to separate each of the items in the list of the csv, and then append it to the empty list
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

#an empty list is created for each of the current intrested features used for matching for the questions
QuestionsAdjectives = []
QuestionsEntities = []
QuestionsNouns = []

#creating for loop to separate each of the items in the list of the csv, and then append it to the empty list
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

#an empty list is created for each of the current intrested features
Entities = []
Nouns = []
Adjectives = []

#creating for loop to join both of the words extracted from the answers and questions within the database.
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

#The counting functions below would search through each row of our list from above,
#then it would count at how many of the items within the list mathches the words extracted from the question entered.

def counting_adjectives(results,rows):
    counts = 0
    adjectives = results['Adjectives']
    for items in rows:
        if items in adjectives:
            counts += 1
    return(counts)

# a empty list a is created to store each of the counts from using the definition.
a = []
# a empty list attl is created to store the length of the total amount of words
# with in the words extrated from the answer and question entrie of the database.
attl = []

#a for loop is then used to append the results from the function and the question to the empty list created above.
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

#the codes below would sum the total matches of the entities, nouns and adjectives between the questions
# and each entries within the database.
e = zip(a,b,c)
eeee = [sum(x) for x in e]
eeee1 = eeee

#The code below sums the total entries of adjectives of entities, nouns and adjectives from each entries within the database with the same class.
ettl = zip(attl,bttl,cttl)
eeeettl = [sum(x) for x in ettl]
eeee1ttl = eeeettl

#The code below calculates the percentage of how many words has matched with the question entered, against the total counts of 
#unique adjective entities and nouns from each of the entries of the questions with the same class as the answer.
new = zip(eeee,eeeettl)
ann = [float(x) / float(y) for x, y in zip(eeee,eeeettl)]

#extracting the top 3 percentages entries within the entries from the questions with the same class as the answer.
l22 = heapq.nlargest(nterms, ann)

######################################################

#Making sure the 3 entries above have unqiue results and no repetitions.
counts = Counter(l22)
for s,num in counts.items():
    if (num > 1) and (s != 0): # ignore strings that only appear once
        for suffix in range(1, num + 1): # suffix starts at 1 and increases by 1 each time
            ann[ann.index(s)] = s + suffix # replace each appearance of s

######################################################

#reextracting the best 3 matches from the list.
l221 = heapq.nlargest(nterms, ann)

#defining a function that would extract the best 3 matches from the above using their index and append the id and answer into a dictionary.
def retrieving_Questions(dataframe):
    n = []
    for i in l221:
        n.append(ann.index(i))
    n1 = []
    for i in n:
        a = dataframe.iloc[i].name
        n1.append(a)
    Questionss = {}
    for i in n1:
        Questionss[i] = dataframe['ANSWER'].loc[i]        
    return(Questionss)

#extracting the answers
nn = retrieving_Questions(question_from_same_class)
 
#printing the extracted answers
print(Question)

#Printing out the id of the answers thats recorded in the database.
print(list(nn.keys()))
   
#Printing out the id of the answers with their respective answer.
for key, value in nn.items():
    print('AnswerID:', key,': ', value.encode('UTF-8'))






