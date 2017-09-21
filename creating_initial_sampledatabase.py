# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:52:06 2017

@author: Diabetes.co.uk
"""

#this module need to be used at the start, it will automatically extract all of the
#entities and nouns of the questions and answer, from the question and answers with class file,
#and append them to create the sampledatabsecsv file
#
#parsing the first sentence of the answer and store it as a dataframe
#this step can be omitted once we have a database that is annotated, and their features extracted.
#then it can be a sql query instead of a python query
#but this can be done using python, as the module can initiate by loading the database as a dataframe locally.
#the pograms below will be focusing on extracting the adjectives and nouns and entities, and use those as search and match.
import pandas as pd
import nltk
import os
import sys
os.chdir(os.path.dirname(sys.argv[0]))
import functions_for_extracting_pronouns_and_entities_using_api as extract


################################################################
##Parsing the 1st sentence of the answer and extracting the adjectives and nouns
################################################################

Questions = pd.read_csv('CSVfiles\\QuestionsWithAnswersAndClassCSV.csv', index_col = 'ID', encoding = 'utf-8')

Answers = Questions['ANSWER']
Questionsonly = Questions['QUESTION']

firstsent = []

for row in Answers:
    results = nltk.sent_tokenize(row)
    firstsent.append(results[0].lower())
    
Questions['Answerfirstsent'] = firstsent

#Extracting the adjectives, nouns, named entities of the sentences and storing it in new columns:
    
AnswerAdjectives = []
AnswerNouns = []
AnswerEntities = []

for rows in firstsent:
    tokens1 = extract.get_tokens(rows)
    aNOUN = extract.Nounswords(tokens1)
    AnswerNouns.append(aNOUN)
    #Adjectives
    aADJECTIVE = extract.Adjectivewords(tokens1)
    AnswerAdjectives.append(aADJECTIVE) 
    #Named entities
    named_entities1 = extract.entities_name1(rows)
    AnswerEntities.append(named_entities1)

QuestionsAdjectives = []
QuestionsNouns = []
QuestionsEntities = []

for rows in Questionsonly:
    tokens1 = extract.get_tokens(rows)
    aNOUN = extract.Nounswords(tokens1)
    QuestionsNouns.append(aNOUN)
    #Adjectives
    aADJECTIVE = extract.Adjectivewords(tokens1)
    QuestionsAdjectives.append(aADJECTIVE) 
    #Named entities
    named_entities1 = extract.entities_name1(rows)
    QuestionsEntities.append(named_entities1)

Questions['QuestionsAdjectives'] = QuestionsAdjectives
Questions['QuestionsNouns'] = QuestionsNouns
Questions['QuestionsEntities'] = QuestionsEntities
Questions['AnswerAdjectives'] = AnswerAdjectives
Questions['AnswerNouns'] = AnswerNouns
Questions['AnswerEntities'] = AnswerEntities
Questions.to_csv('sampledatabase.csv', encoding = 'utf-8')
#this part will take a while, so ill omit those part of the code, and store and load the result as another csv file
#can be implemented to parse a new annotated dataset

