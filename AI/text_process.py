from autocorrect import Speller
import re

import nltk
import nltk.corpus
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

spell = Speller(lang='en')
stop = stopwords.words('english')

def process_text(prompt):
    prompt = prompt.lower()
    prompt = correct_prompt(prompt)
    prompt = remove_unicode(prompt)
    prompt = remove_stop_words(prompt)
    return prompt

def correct_prompt(prompt):
    return spell(prompt)

def remove_unicode(prompt):
    return re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", prompt)

def remove_stop_words(prompt):
    output = ""
    stop_words = set(stopwords.words('english'))
  
    word_tokens = word_tokenize(prompt)
    output = [w for w in word_tokens if not w in stop_words]
  
    return output