########################################
# Author : Earl Timothy D. Malaki
# User Experience Designer
# Plaza 2 6th Floor C'10 6
# Lexmark Research and Development Cebu
########################################

########################################
# Introduction
# This script does multiple preprocessing algorithms on the scraped amazon reviews
# The final output is then exported to a folder containing .csv of preprocessed files
# Last Update: February 03, 2020
########################################


# Import necessary libraries
import re
import string

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer, SnowballStemmer

########################################
# Helper Methods
########################################

# Converts a string of words into tokens
def tokenize(text):
    tokens = word_tokenize(text)
    return tokens

# Converts tokens to lowercase
def lowercase(tokens):
    return [w.lower() for w in tokens]

# Remove punctuations from tokens
def remove_punctuations(tokens):
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    return [word for word in stripped if word.isalpha()]

# Remove stopwords
def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    return [w for w in tokens if not w in stop_words]
    
# Stem
def stem(tokens):
    porter = PorterStemmer()
    return [porter.stem(word) for word in tokens]

# Stem and lemmatize
# Method 2
def lemmatize_stemming(tokens):
    stemmer = SnowballStemmer('english')
    return [stemmer.stem(WordNetLemmatizer().lemmatize(word, pos='v')) for word in tokens]
    

def preprocess(text):
    tokens = tokenize(text)
    tokens = lowercase(tokens)
    tokens = remove_punctuations(tokens)
    tokens = remove_stopwords(tokens)
    # tokens = stem(tokens)
    # tokens = lemmatize_stemming(tokens)
    # return tokens
    temp = " "
    return temp.join(tokens) 