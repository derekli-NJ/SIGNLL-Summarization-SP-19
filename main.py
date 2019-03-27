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
article = """
When I was three, having spent only one year in America, my dad took me to the local library every week. One day, I picked up The New Way Things Work, a 400-page thick illustrated encyclopedia covering everything from levers to computers. My parents were surprised by my choice for a children’s book, but they read it to me anyway, introducing me to the wonderful world of engineering. I’ve been pursuing my interest in machines ever since, tinkering with LEGOs to build a four-wheel-drive car, complete with a realistic suspension, from my own imagination, and designing wooden marble machines for woodshop class in middle school, cutting gears and chain links using blueprints that I drew up on graph paper. 
I joined my high school’s FIRST robotics team in my freshman year, and it quickly became the focus of my life. I learned how to use computer aided design software to create 3D models of our robot’s parts, using it to analyze how the robot would interact with itself before any part was built. With these tools, I designed a set of levers for lifting and rotating our robot’s ball shooter to the correct position simultaneously, using physics I learned at school to design a spring counterbalance that made the 20-pound arm move as if it was weightless. Seeing the results of my calculations and hours of careful design work come to life on our robot, I gained a new respect for using math and physics to solve real-world problems. 
Over this past summer, I participated in the COSMOS program at UC Davis. For four weeks, I absorbed information about differential equations and linear algebra, learning how to solve problems relating to fluids and aerodynamics. Wanting to learn more, I downloaded a differential equations textbook PDF and started doing practice problems, teaching myself how to solve these problems with equations and calculus, as well as with brute force calculations. By the end, I was able to apply these concepts for myself, calculating the optimum gear ratio for our robot by solving partial differential equations. COSMOS not only gave me new tools to apply to my work in robotics club, but also furthered my interest in higher level math. 
From toying with LEGOs to carefully crafting robots from aluminum, I’ve experienced the power of engineering firsthand, and I plan on continuing to pursue this interest at UIUC and into the workplace. 
"""
print(article)
print()
print(summarize(article))