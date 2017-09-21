# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 11:23:46 2017

@author: Diabetes.co.uk
"""
###using a machine learning algorithm to train on the on the featuredump extracted from the questions.

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os
import sys
import pickle as cPickle

os.chdir(os.path.dirname(sys.argv[0]))

import ourfeatures2

FNAME = 'CSVfiles\\featuresDump2.csv' # !! Modify this to the CSV data location
FNAME1 = 'CSVfiles\\model.pickle'
FNAME2 = 'CSVfiles\\model1.pickle'
df = pd.read_csv(filepath_or_buffer = FNAME, encoding = 'utf-8')   
print(str(len(df)), "rows loaded")

# Strip any leading spaces from col names
df.columns = df.columns[:].str.strip()
df['class'] = df['class'].map(lambda x: x.strip())

width = df.shape[1]

#split into test and training (is_train: True / False col)
np.random.seed(seed=1)
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
train, test = df[df['is_train']==True], df[df['is_train']==False]
print(str(len(train)), " rows split into training set,", str(len(test)), "split into test set.")

features = df.columns[1:width-1]  #remove the first ID col and last col=classifier
print("FEATURES = {}".format(features))

# Fit an RF Model for "class" given features
clf = RandomForestClassifier(n_jobs=2, n_estimators = 100)
clf.fit(train[features], train['class'])

# Predict against test set
preds = clf.predict(test[features])
predout = pd.DataFrame({ 'id' : test['id'], 'predicted' : preds, 'actual' : test['class'] })

print(predout)

## Cross-check accuracy ##
#print(pd.crosstab(test['class'], preds, rownames=['actual'], colnames=['preds']))
#print("\n",pd.crosstab(test['class'], preds, rownames=['actual']
#                       , colnames=['preds']).apply(lambda r: round(r/r.sum()*100,2), axis=1) )

from sklearn.metrics import accuracy_score
print("\n\nAccuracy Score: ", round(accuracy_score(test['class'], preds),3) )

with open(FNAME1, 'wb') as f:
    cPickle.dump(clf, f, protocol = 2)

# in your prediction file                                                                                                                                                                                                           

with open(FNAME1, 'rb') as f:
    clf = cPickle.load(f)

#Example of using the classifier
sentence = 'what is the causes of type 1 diabetes?'

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

myFeatures = ourfeatures2.features_dict('1',sentence, 'X')
values=[]
for key in keys:
    values.append(myFeatures[key])
s = pd.Series(values)
width = len(s)
myFeatures = s[1:width-1]
predictedclass = clf.predict([myFeatures])

print(sentence)
print('predicited class is: ', predictedclass)