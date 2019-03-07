import os

os.chdir(".\\stories")
path = os.getcwd()

class Article:
    
    def __init__(self, text, highlights):
        self.text = text
        self.highlights = highlights

filenames = os.listdir(path)

index = 0

def nextFile():
    global index
    index = index + 1
    return getFile(index)

def getFile(index):
    filename = filenames[index]
    with open(filename, 'r') as f:
        allText = f.read()
        allTextList = filter(lambda x: x != '', allText.split("\n"))
        text = ""
        highlights = []
        highlightFlag = False
        for line in allTextList:
            if highlightFlag:
                if line != "@highlight":
                    highlights.append(line)
            elif line == "@highlight":
                highlightFlag = True
            else:
                text += line + "\n"

        #print(text)
        #print(highlights)
        return Article(text, highlights)

print(nextFile().text)