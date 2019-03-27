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
    summaries = []
    r = Rake(min_length=2)
    for i in range(len(blocks)):
        block = blocks[i]
        block = [[sentence, i] for sentence in block]
        # if (len(block) > 1):
        #     r.extract_keywords_from_text(" ".join(block))
        #     keyphrases = [list(x) for x in r.get_ranked_phrases_with_scores()[:1]]
        #     for sentence in block:
        #         for phrase in keyphrases:
        #             if (phrase[1] in sentence.lower()):
        #                 summaries.append(sentence)
        sentence_list.extend(block)

    #return "\n".join(summaries)

    r.extract_keywords_from_text(text)
    #temp_keywords = r.get_ranked_phrases_with_scores()[:10]
    #keywords = [x[1] for x in temp_keywords]
    keyphrases = [list(x) for x in r.get_ranked_phrases_with_scores()[:20]]

    for phrase in keyphrases:
        print(phrase)

    print()

    # important_sentences = [sentence_list[0][0]]
    important_sentences = []

    taken_paragraphs = []

    #prev_sentence = ""
    for i in sentence_list:
        is_important = False
        for j in keyphrases:
            for word in j[1:]:
                if (word in i[0].lower()):
                    is_important = True
                    break
        #if is_important and prev!= None and i not in important_sentences:
        #    important_sentences.append(prev + "\n" + i)
        #prev = i
        if is_important and not (i[1] in taken_paragraphs) and not (i in important_sentences):
            important_sentences.append(i)
            taken_paragraphs.append(i[1])

    if not (sentence_list[0] in important_sentences):
        important_sentences.append(sentence_list[0])


    return "\n".join([sent[0] for sent in important_sentences])

article = getFile(0).text
print(article)
print()
print(summarize(article))