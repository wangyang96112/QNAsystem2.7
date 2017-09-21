# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 10:34:42 2017

@author: Diabetes.co.uk
"""

##############################################
# pass in a sentence, pass out it's features #
##############################################

import os
import sys
#os.chdir(os.path.dirname(sys.argv[0]))###change this file path to your local folder

import nltk
from nltk import word_tokenize
from nltk.tokenize import regexp_tokenize

lemma = nltk.wordnet.WordNetLemmatizer()
sno = nltk.stem.SnowballStemmer('english')
from nltk.corpus import stopwords

import pandas as pd  # Use Pandas to create pandas Series in features_series()  

import re
import string
import itertools

line = ["xxx","Oracle 12.2 will be released? for on-premises, users on. 15 March 2017",0,"S"]

pos = []           #list of PartsOfSpeech

output = ""        #comma separated string 
header = ""        #string for describing features header 

#VerbCombos = ['VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB','MD']

informationanddefinitionTriples = ['MD-PRP-VB']
 #                                  'PRP-VB-NN',
  #                                 'PRP-VB-NNS']
#
complicationsTriples = ['DT-NN-IN',
                        'VBZ-DT-NN',
                        'WP-VBZ-DT']
   #                     'NN-IN-NNP',
    #                    'IN-NNP-CC',
     #                   'NNP-CC-NNP']              

manifestationTriples= ['IN-JJ-NN',
                       'VBP-DT-NNS',
                       'VDT-NNS-IN',
                       'WP-VBP-DT',
                       'NNS-IN-JJ']
          #             'VBP-NNS-IN']              

causePattern = re.compile(r'(caus|contribut|root|sourc|origin|trigger)', re.IGNORECASE)
complicationsPattern = re.compile(r'affect|effect|damage|change|worsen|lead|result|consequen|complicat|relation|link|risk', re.IGNORECASE)
diagnosisPattern = re.compile(r'diagnos|associat|screen|test|examin', re.IGNORECASE)
#informationanddefinitionPattern = re.compile(r'define|tell|know', re.IGNORECASE)
managementPattern = re.compile(r'manag|cop|help|liv|cur|treat|prevent|drugs|medicin|deal|avoid|car|control', re.IGNORECASE)
manifestationPattern = re.compile(r'sign|symptom|show|indicat|appear|mark|condtion', re.IGNORECASE)

#causeTriples= ['MD-VB-NN' ,
 #              'VBP-DT-NNP' ,
  #             'DT-NNP-IN' ,
   #            'JJ-CD-NNS']

#diagnosisTriples= ['WRB-VBZ-NNP',
 #                  'NNS-IN-DT',
  #                 'VBZ-NNP-NN',
   #                'PRP-VB-IN',
    #               'WRB-VBZ-DT',
     #              'VBZ-DT-NN']

#managementTriples= ['VBZ-NNP-WP',
 #                   'NNP-WP-VBP',]

#informationanddefinitionTuples = ['MD-PRP',
  #                                'PRP-VB']
  #                                 'PRP-VB-NNS']
#
#complicationsTuples = ['NN-IN',
        #               'DT-NN',
                      # 'VBZ-DT']
 #                     'NN-IN-NNP',
  #                    'IN-NNP-CC',
     #                   'NNP-CC-NNP']              

#manifestationTuples= ['IN-JJ-NN',
 #                      'VBP-DT-NNS',
   #                    'VDT-NNS-IN',
   #                    'WP-VBP-DT',
     #                  'NNS-IN-JJ']
          #             'VBP-NNS-IN']              

#causeTuples= ['MD-VB-NN' ,
 #              'VBP-DT-NNP' ,
  #             'DT-NNP-IN' ,
   #            'JJ-CD-NNS']

#diagnosisTuples= ['WRB-VBZ-NNP',
 #                  'NNS-IN-DT',
  #                 'VBZ-NNP-NN',
   #                'PRP-VB-IN',
    #               'WRB-VBZ-DT',
     #              'VBZ-DT-NN']

#managementTuples= ['VBZ-NNP-WP',
 #                   'NNP-WP-VBP',]

startTuples = ['MD-PRP']                      

endTuples = ['JJ-NN',
             'CC-NNP',
             'IN-NN'] 

# Because python dict's return key-vals in random order, provide ordered list to pass to ML models
feature_keys = ["id",
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
#"endTuple2",
"verbBeforeNoun",
#"qMark",
#"qVerbCombo",
"informationanddefinitionTriplesScore",
"complicationsTriplesScore",
"manifestationTriplesScore",
"complicationsTuplesScore",
#"causeTriplesScore",
#"diagnosisTriplesScore",
#"managementTriplesScore",
"class"]


def strip_sentence(sentence):
    sentence = sentence.strip(",")
    sentence = ''.join(filter(lambda x: x in string.printable, sentence))  #strip out non-alpha-numerix
    #sentence = sentence.translate(str.maketrans('','',string.punctuation)) #strip punctuation
    sentence = ''.join(x.strip(string.punctuation)+' ' for x in sentence.split())
    return(sentence)

def word_extract(sentence, pattern):
    tokens = word_tokenize(sentence) #we first tokenise the word    
    lower_tokens = [t.lower() for t in tokens]
    results = regexp_tokenize(str(lower_tokens),pattern)
    return(len(results))

# Pass in a list of strings (i.e. PoS types) and the sentence to check PoS types for
# check if *Any Pair Combo* of the PoS types list exists in the sentence PoS types
# return a count of occurrence
def exists_pair_combos(comboCheckList, sentence):
    pos = get_pos(sentence)
    tag_string = "-".join([ i[1] for i in pos ])
    combo_list = []
    
    for pair in itertools.permutations(comboCheckList,2):
        if(pair[0] == "MD"):  # * Kludge - strip off leading MD *
            pair = ["",""]
        combo_list.append("-".join(pair))
    
    if any(code in tag_string for code in combo_list):
	    return 1
    else:
        return 0
    
# Parts Of Speech
def get_pos(sentence):
    sentenceParsed = word_tokenize(sentence)
    return(nltk.pos_tag(sentenceParsed))
    
# Count Q-Marks    
#def count_qmark(sentence):
#   return(sentence.count("?") )
    
# Count a specific POS-Type
#VBG = count_POSType(pos,'VBG')
def count_POSType(pos, ptype):
    count = 0
    tags = [ i[1] for i in pos ]
    return(tags.count(ptype))
    #if ptype in tags:
    #    VBG = 1
    #return(VBG)
    
# Does Verb occur before first Noun
def exists_vb_before_nn(pos):
    pos_tags = [ i[1] for i in pos ]
    #Strip the Verbs to all just "V"
    pos_tags = [ re.sub(r'V.*','V', str) for str in pos_tags ]
    #Strip the Nouns to all just "NN"
    pos_tags = [ re.sub(r'NN.*','NN', str) for str in pos_tags ]
    
    vi =99
    ni =99
    mi =99
    
    #Get first NN index
    if "NN" in pos_tags:
        ni = pos_tags.index("NN")
    #Get first V index
    if "V" in pos_tags:
        vi = pos_tags.index("V")
    #get Modal Index
    if "MD" in pos_tags:
        mi = pos_tags.index("MD")

    if vi < ni or mi < ni :
        return(1)
    else:
        return(0)

# Stemmed sentence ends in "NN-NN"?  
def exists_stemmed_end_NN(stemmed):
    stemmedEndNN = 0
    stemmed_end = get_first_last_tuples(" ".join(stemmed))[1]
    if stemmed_end == "NN-NN":
        stemmedEndNN = 1
    return(stemmedEndNN)

# Go through the predefined list of start-tuples, 1 / 0 if given startTuple occurs in the list
def exists_startTuple(startTuple):    
    exists_startTuples = []
    for tstring in startTuples:  #startTuples defined as global var
        if startTuple in tstring:
            exists_startTuples.append(1)
        else:
            exists_startTuples.append(0)
        return(exists_startTuples)

# Go through the predefined list of end-tuples, 1 / 0 if given Tuple occurs in the list    
def exists_endTuple(endTuple):
    exists_endTuples = []
    for tstring in endTuples:    #endTuples defined as global var
        if endTuple in tstring:
            exists_endTuples.append(1)
        else:
            exists_endTuples.append(0)
    return(exists_endTuples)

#loop round list of triples and construct a list of binary 1/0 vals if triples occur in list
def exists_triples(triples, tripleSet):
    exists = []
    for tstring in tripleSet:   
        if tstring in triples:
            exists.append(1)
        else:
            exists.append(0)
    return(exists)

def exists_tuples(tuples, tupleSet):
    exists = []
    for tstring in tupleSet:   
        if tstring in tuples:
            exists.append(1)
        else:
            exists.append(0)
    return(exists)

# Get a sentence and spit out the POS triples
def get_triples(pos):
    list_of_triple_strings = []
    pos = [ i[1] for i in pos ]  # extract the 2nd element of the POS tuples in list
    n = len(pos)
    
    if n > 2:  # need to have three items
        for i in range(0,n-2):
            t = "-".join(pos[i:i+3]) # pull out 3 list item from counter, convert to string
            list_of_triple_strings.append(t)
    return list_of_triple_strings 

def get_tuples(pos):
    list_of_triple_strings = []
    pos = [ i[1] for i in pos ]  # extract the 2nd element of the POS tuples in list
    n = len(pos)
    
    if n > 2:  # need to have three items
        for i in range(0,n-1):
            t = "-".join(pos[i:i+2]) # pull out 3 list item from counter, convert to string
            list_of_triple_strings.append(t)
    return list_of_triple_strings 
        
def get_first_last_tuples(sentence):
    first_last_tuples = []
    sentenceParsed = word_tokenize(sentence)
    pos = nltk.pos_tag(sentenceParsed) #Parts Of Speech
    pos = [ i[1] for i in pos ]  # extract the 2nd element of the POS tuples in list
    
    n = len(pos)
    first = ""
    last = ""
    
    if n > 1:  # need to have three items
        first = "-".join(pos[0:2]) # pull out first 2 list items
        last = "-".join(pos[-2:]) # pull out last 2 list items
    
    first_last_tuples = [first, last]
    return first_last_tuples

def lemmatize(sentence):    
    """
    pass  in  a sentence as a string, return just core text that has been "lematised"
    stop words are removed - could effect ability to detect if this is a question or answer
    - depends on import lemma = nltk.wordnet.WordNetLemmatizer() and from nltk.corpus import stopwords
    """
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)
    
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w.lower())  # also set lowercase
    lem = []        
    for w in filtered_sentence:
        lem.append(lemma.lemmatize(w))
  
    return lem    

def stematize(sentence):
    """
    pass  in  a sentence as a string, return just core text stemmed
    stop words are removed - could effect ability to detect if this is a question or answer
    - depends on import sno = nltk.stem.SnowballStemmer('english') and from nltk.corpus import stopwords
    """
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)
    
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    stemmed = []        
    for w in filtered_sentence:
        stemmed.append(sno.stem(w))
  
    return stemmed    

#########################################################################
# A wrapper function to put it all together - build a csv line to return
# A header string is also returned for optional use
def get_string(id,sentence,c="X"):
    header,output = "",""
    pos = get_pos(sentence)
    
#    qMark = count_qmark(sentence) #count Qmarks before stripping punctuation
    sentence = strip_sentence(sentence)
    #lemmed = lemmatize(sentence)
    stemmed = stematize(sentence)
    wordCount = len(sentence.split())
    stemmedCount = len(stemmed)
    
 #   qVerbCombo = exists_pair_combos(
        #    VerbCombos,sentence)
         
    verbBeforeNoun = exists_vb_before_nn(pos)
            
    output = id + ","  + str(wordCount) + "," + str(stemmedCount) + "," + str(verbBeforeNoun) #+ "," + str(qVerbCombo) + "," + str(qMark) 
    header = header + "id,wordCount,stemmedCount,verbBeforeNoun," #qVerbCombo,qMark,

    # list of POS-TYPES to count , generate a list of counts in the CSV line
    for ptype in ["VBG", "VBZ", "NNP", "NN", "NNS", "NNPS","PRP", "CD" ]:
        output = output + "," + str( count_POSType(pos,ptype) )
        header = header + "," + ptype

    output = output + "," + str(exists_stemmed_end_NN(stemmed))
    header = header + ",StemmedEndNN,"
            
    ## get Start Tuples and End Tuples Features ##
    startTuple,endTuple = get_first_last_tuples(sentence)

    l = exists_startTuple(startTuple)  #list [1/0] for exists / not exists
    output = output + "," + ",".join(str(i) for i in l)
    for i in range(0,len(l)):
        header = header + "startTuple" + str(i+1) + ","

    l = exists_endTuple(endTuple)  #list [1/0] for exists / not exists
    output = output + "," + ",".join(str(i) for i in l)
    for i in range(0,len(l)):
        header = header + "endTuple" + str(i+1) + ","

    ## look for special Triple Combinations ##
    triples = get_triples(pos)  # all the triple sequences in the sentence POS list
  #  tuples = get_tuples(pos) 
    
    l = exists_triples(triples, informationanddefinitionTriples)
    total = sum(l)
    output = output + "," + str(total)
    header = header + "informationanddefinitionTriplesScore" + ","

    l = exists_triples(triples, complicationsTriples)
    total = sum(l)
    output = output + "," + str(total)
    header = header + "complicationsTriplesScore" + ","
    
    l = exists_triples(triples, manifestationTriples)
    total = sum(l)
    output = output + "," + str(total)
    header = header + "manifestationTriplesScore" + ","
    
    #l = exists_triples(triples, causeTriples)
    #total = sum(l)
    #output = output + "," + str(total)
    #header = header + "causeTriplesScore" + ","
    
   # l = exists_triples(triples, diagnosisTriples)
   # total = sum(l)
   # output = output + "," + str(total)
   # header = header + "diagnosisTriplesScore" + ","
    
   
   # l = exists_triples(triples, managementTriples)
   # total = sum(l)
   # output = output + "," + str(total)
   # header = header + "managementTriplesScore" + ","
   
   ## look for special Tuple Combinations ##
 #   l = exists_triples(tuples, complicationsTuples)
  #  total = sum(l)
   # output = output + "," + str(total)
    #header = header + "complicationsTuplesScore" + ","
    l = word_extract(sentence, causePattern)
    output = output + "," + str(l)
    header = header + "causeScore" + ","
    
    l = word_extract(sentence, complicationsPattern)
    output = output + "," + str(l)
    header = header + "complicationsScore" + ","
    
    l = word_extract(sentence, diagnosisPattern)
    output = output + "," + str(l)
    header = header + "diagnosisScore" + ","
    
    l = word_extract(sentence, managementPattern)
    output = output + "," + str(l)
    header = header + "managementScore" + ","
    
    l = word_extract(sentence, manifestationPattern)
    output = output + "," + str(l)
    header = header + "manifestationScore" + ","
    
    output = output + "," + c  #Class Type on end
    header = header + "class"
    
    return output,header
    
# End of Get String wrapper   
#########################################################################  

# Build a dictionary of features
def features_dict(id,sentence,c="X"):
    features = {}
    pos = get_pos(sentence)
    
    features["id"] = id
#    features["qMark"] = count_qmark(sentence) #count Qmarks before stripping punctuation
    sentence = strip_sentence(sentence)
    stemmed = stematize(sentence)
    startTuple,endTuple = get_first_last_tuples(sentence)
    
    features["wordCount"] = len(sentence.split())
    features["stemmedCount"] = len(stemmed)
#    features["qVerbCombo"] = exists_pair_combos(VerbCombos,sentence)
    features["verbBeforeNoun"] = exists_vb_before_nn(pos)
    
    for ptype in ["VBG", "VBZ", "NNP", "NN", "NNS", "NNPS","PRP", "CD" ]:
        features[ptype] = count_POSType(pos,ptype)
        
    features["stemmedEndNN"] = exists_stemmed_end_NN(stemmed)
    
    l = exists_startTuple(startTuple)  #list [1/0] for exists / not exists
    for i in range(0,len(l)):
        features["startTuple" + str(i)] = l[i]

    l = exists_endTuple(endTuple)  #list [1/0] for exists / not exists
    for i in range(0,len(l)):
        features["endTuple" + str(i)] = l[i]
        
    ## look for special Triple Combinations ##
    triples = get_triples(pos)  # all the triple sequences in the sentence POS list
   # tuples = get_tuples(pos) 
    
    l = exists_triples(triples, informationanddefinitionTriples)  # a list of 1/0 for hits on this triple-set
    features["informationanddefinitionTriplesScore"] = sum(l)  # add all the triple matches up to get a score
    
    l = exists_triples(triples, complicationsTriples)  # a list of 1/0 for hits on this triple-set
    features["complicationsTriplesScore"] = sum(l)  # add all the triple matches up to get a score
    
    l = exists_triples(triples, manifestationTriples)  # a list of 1/0 for hits on this triple-set
    features["manifestationTriplesScore"] = sum(l)  # add all the triple matches up to get a score
    
   # l = exists_triples(triples, causeTriples)  # a list of 1/0 for hits on this triple-set
  #  features["causeTriplesScore"] = sum(l)  # add all the triple matches up to get a score
    
   # l = exists_triples(triples, diagnosisTriples)  # a list of 1/0 for hits on this triple-set
   # features["diagnosisTriplesScore"] = sum(l)  # add all the triple matches up to get a score
    
   # l = exists_triples(triples, managementTriples)  # a list of 1/0 for hits on this triple-set
   # features["managementTriplesScore"] = sum(l)  # add all the triple matches up to get a score
   
   ## look for special Tuple Combinations ##
#    l = exists_triples(tuples, complicationsTuples)  # a list of 1/0 for hits on this triple-set
  #  features["complicationsTuplesScore"] = sum(l)
    l = word_extract(sentence, causePattern)
    features["causeScore"] = l
    
    l = word_extract(sentence, complicationsPattern)
    features["complicationsScore"] = l
    
    l = word_extract(sentence, manifestationPattern)
    features["manifestationScore"] = l
    
    l = word_extract(sentence, diagnosisPattern)
    features["diagnosisScore"] = l
    
    l = word_extract(sentence, managementPattern)
    features["managementScore"] = l
      
    features["class"] = c  #Class Type on end
    
    return features

# pass in dict, get back series 
def features_series(features_dict):
    values=[]
    for key in feature_keys:
        values.append(features_dict[key])

    features_series = pd.Series(values)

    return features_series
       
## MAIN ##  
if __name__ == '__main__':

    #  ID, WordCount, StemmedCount, Qmark, VBG, StemmedEnd, StartTuples, EndTuples,   QuestionTriples, StatementTriples, Class
    #                                     [1/0] [NN-NN?]    [3 x binary] [3 x binary] [10 x binary]    [10 x binary]    

    print("Starting...")

    c = "X"        # Dummy class
    header = ""
    output = ""

    if len(sys.argv) > 1:
        sentence = sys.argv[1]
    else:
        sentence = line[1]  
        
    id = line[0]

    features = features_dict(id,sentence, c)
    pos = get_pos(sentence)       #NLTK Parts Of Speech, duplicated just for the printout
    print(pos)
 
    print(features)
    for key,value in features.items():
        print(key, value)
    
    #header string
    for key, value in features.items():
       header = header + ", " + key   #keys come out in a random order
       output = output + ", " + str(value)
    header = header[1:]               #strip the first ","" off
    output = output[1:]               #strip the first ","" off
    print("HEADER:", header)
    print("VALUES:", output)
    
    
            
