##################################################################
# Use the ourfeatures2.py module to dump out features
# read in a CSV of sentences and bulk-dump to dump.csv of features
##################################################################

#Input CSV fmt:  1st field is sentence ID, 2nd field is text to process, 3rd field is class

import os
import sys
import io
import csv
os.chdir(os.path.dirname(sys.argv[0]))###change this file path to your local folder

import ourfeatures2 # ourfeatures2.py is bepoke util to extract NLTK POS features from sentences

if len(sys.argv) > 1:
    FNAME = sys.argv[1]
else:
    FNAME = 'CSVfiles\\QuestionsWithClassCSV.csv'
print("reading input from ", FNAME)


if len(sys.argv) > 2:
    FOUT = sys.argv[2]
else:
    FOUT = 'CSVfiles\\featuresDump2.csv'
print("Writing output to ", FOUT)

fin = io.open(FNAME, 'rt')
fout = io.open(FOUT, 'wt', newline='')

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
#"endTuple2",
"verbBeforeNoun",
#"qMark",
#"qVerbCombo",
"informationanddefinitionTriplesScore",
"complicationsTriplesScore",
"manifestationTriplesScore",
"causeScore",
"complicationsScore",
#"informationanddefinitionScore",
"manifestationScore",
"diagnosisScore",
"managementScore",
#"complicationsTuplesScore",
#"causeTriplesScore",
#"diagnosisTriplesScore",
#"managementTriplesScore",
"class"]

reader = csv.reader(fin)

loopCount = 0
next(reader)  #Assume we have a header 
for line in reader:
    sentence = line[1]  
    c = line[2]        #class-label
    id = line[0] # generate a unique ID
    
    output = ""  
    header = ""
    
    #get header and string output
    #output, header = features.get_string(id,sentence,c)
    f = ourfeatures2.features_dict(id,sentence, c)
     
    for key in keys:
        value = f[key]
        header = header + ", " + key 
        output = output + ", " + str(value)

    if loopCount == 0:   # only extract and print header for first dict item
        header = header[1:]               #strip the first ","" off
        print(header)
        fout.writelines(header + '\n')
    
    output = output[1:]               #strip the first ","" off
    
    loopCount = loopCount + 1            
    print(output)
    fout.writelines(output + '\n')
        

fin.close()
fout.close()
