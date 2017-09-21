# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 13:38:56 2017

@author: Diabetes.co.uk
"""

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six
import os
import sys
os.chdir(os.path.dirname(sys.argv[0]))

# Instantiates a client
client = language.LanguageServiceClient()

#looking for the index of the argument with in the list
def index(self, elem):
  """Finds the index of a given item in the list. Similar to list.index(elem)."""
  return self._values.index(elem)

#returns the index of the pronoun after being syntax tokenised
def pron_index(tokens):
    for token in tokens:
        if token.part_of_speech.tag == 8:
            return(index(tokens,token))

#serching for a verb before the pronoun with in the tokens
def verbbefpron(tokens):
    PI = pron_index(tokens)
    for token in tokens[:PI]:
        if token.part_of_speech.tag == 11:
            return(token.text.content)
        
def verbaftpron(tokens):
    PI = pron_index(tokens)
    for token in tokens[PI:]:
        if token.part_of_speech.tag == 11:
            return(token.text.content)

#functions for looking for first verb and adv if pronoun is not present.
def firstAdverbs(tokens):
    for token in tokens:
        if token.part_of_speech.tag == 3:
            return(token.text.content)
        
def firstVerbs(tokens):
    for token in tokens:
        if token.part_of_speech.tag == 11:
            return(token.text.content)
      
    
#Searching thorugh the sentence for each individual of the 14 post tags
pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

def Unknownwords(tokens):
    a=[]
    for token in tokens:
        if token.part_of_speech.tag == 0:
            a.append(token.text.content)
    return(a)
            
def Adjectivewords(tokens):
    a=[]
    for token in tokens:        
        if token.part_of_speech.tag == 1:
            a.append(token.text.content)
    return(a)   
    
def Adpositionwords(tokens):
    a=[]
    for token in tokens:        
        if token.part_of_speech.tag == 2:
            a.append(token.text.content)
    return(a)
            
def Adverbwords(tokens):
    a=[]
    for token in tokens:        
        if token.part_of_speech.tag == 3:
            a.append(token.text.content)
    return(a)
    
def Conjunctionwords(tokens):
    a=[]
    for token in tokens:        
        if token.part_of_speech.tag == 4:
            a.append(token.text.content)
    return(a)
        
def Determinerwords(tokens):
    a=[]
    for token in tokens:        
        if token.part_of_speech.tag == 5:
            a.append(token.text.content)
    return(a)
    
def Nounswords(tokens):
    a=[]
    for token in tokens:
        if token.part_of_speech.tag == 6:
            a.append(token.text.content)
    return(a)
         
def Numberswords(tokens):
    a=[]
    for token in tokens:
        if token.part_of_speech.tag == 7:
            a.append(token.text.content)
    return(a)
    
def Pronounswords(tokens):
    a=[]
    for token in tokens:        
        if token.part_of_speech.tag == 8:
            a.append(token.text.content)
    return(a)
            
def Particleswords(tokens):
    a=[]
    for token in tokens:
        if token.part_of_speech.tag == 9:
            a.append(token.text.content)
    return(a)

def Punctuationwords(tokens):
    a=[]
    for token in tokens:        
        if token.part_of_speech.tag == 10:
            a.append(token.text.content)
    return(a)
            
def Verbswords(tokens):
    a=[]
    for token in tokens:        
        if token.part_of_speech.tag == 11:
            a.append(token.text.content)
    return(a)
            
def Otherwords(tokens):
    a=[]
    for token in tokens:
        if token.part_of_speech.tag == 12:
            a.append(token.text.content)
    return(a)
            
def Abbreviationswords(tokens):
    a=[]
    for token in tokens:
        if token.part_of_speech.tag == 13:
            a.append(token.text.content)
    return(a)

#entitie analysing single text
def entities_name1(text):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities
    entities1 = []
    for entity in entities:
        entities1.append(entity.name)
    return(entities1)

#syntax analysing single text
def syntax_text1(text):
    """Detects syntax in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    tokens = client.analyze_syntax(document).tokens
    
    for t in tokens:
        if t.part_of_speech.tag == 8:
            return(t.text.content)

def get_tokens(text):
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    tokens = client.analyze_syntax(document).tokens
    return(tokens)      
      


























