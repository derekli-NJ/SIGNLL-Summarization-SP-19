# https://stackabuse.com/text-summarization-with-nltk-in-python/?fbclid=IwAR0hntNquE08NtGwK38KLH1Lut1axx8tor6TIYrztJKMP4VLgeHITzKQbQs
# Code copied from here ^ 

# BEFORE RUNNING THIS:
# 
# Run setup.py, install nltk data.
# Required: 
#   beautifulsoup (pip3 install beautifulsoup4)
#   nltk (pip install nltk)
#   lxml (pip install lxml)

import bs4 as bs  
import urllib.request
import re
import heapq  
import nltk


article_text = "Hi! My name is bob. Thomas R. Wright, Sr., said that today, 10.8.19, is St. Patrick's day."

# sent_tokenize breaks target text into sentences.
sentence_list = nltk.sent_tokenize(article_text)  
for s in sentence_list:
    print(s)
    print(nltk.word_tokenize(s))