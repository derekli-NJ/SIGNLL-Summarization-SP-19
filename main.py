import bs4 as bs  
import urllib.request
import re
import heapq  
import nltk
from rake_nltk import Rake
from parseStories import getFile

scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')  
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:  
    article_text += p.text


# Removing Square Brackets and Extra Spaces -- specific to wikipedia articles, wikipedia citations
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
article_text = re.sub(r'\s+', ' ', article_text)

# Removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)  

def summarize(text):
    # sent_tokenize breaks target text into sentences.
    blocks = [nltk.sent_tokenize(paragraph) for paragraph in text.split("\n")]
    sentence_list = []
    for block in blocks:
        sentence_list.extend(block)

    r = Rake(min_length=2)
    r.extract_keywords_from_text(text)
    #temp_keywords = r.get_ranked_phrases_with_scores()[:10]
    #keywords = [x[1] for x in temp_keywords]
    keyphrases = [list(x) for x in r.get_ranked_phrases_with_scores()[:20]]

    for phrase in keyphrases:
        print(phrase)

    print()

    important_sentences = [sentence_list[0]]

    #prev_sentence = ""
    for i in sentence_list:
        is_important = False
        for j in keyphrases:
            for word in j[1:]:
                if (word in i.lower()):
                    is_important = True
                    break
        #if is_important and prev!= None and i not in important_sentences:
        #    important_sentences.append(prev + "\n" + i)
        #prev = i
        if is_important and not (i in important_sentences):
            important_sentences.append(i)

    return "\n".join(important_sentences)

article = getFile(0).text
print(article)
print()
print(summarize(article))