#!/usr/bin/env python
# coding: utf-8

# In[3]:


import warnings;warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import re
import nltk
import spacy
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


# In[4]:


PUNCT_TO_REMOVE = string.punctuation
STOPWORDS = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


# In[5]:


def text_lower(df):
    df['text'] = df['text'].str.lower()
    return df


# In[6]:


def remove_punctuation(text):
    return text.translate(str.maketrans(PUNCT_TO_REMOVE,' '*len(PUNCT_TO_REMOVE)))


# In[7]:


def remove_stopwords(text):
    return [word for word in word_tokenize(str(text)) if word not in STOPWORDS]


# In[8]:


def stem_words(tokens):
    return [stemmer.stem(word) for word in tokens]


# In[9]:


def lemmatize_words(tokens):
    return [lemmatizer.lemmatize(word) for word in tokens]


# In[10]:


def get_pre_processed_text(list_of_strings):
    df = pd.DataFrame({'text':list_of_strings})
    df['text'] = text_lower(df)
    df['text'] = df['text'].apply(remove_punctuation)
    df['text'] = df['text'].apply(remove_stopwords)
    df['text'] = df['text'].apply(stem_words)
    df['text'] = df['text'].apply(lemmatize_words)
    return df


# In[ ]:





# In[ ]:




