import json
from nltk.stem import WordNetLemmatizer

def tokenize(string):
    
    temp = []
    output = []

    stopword = ["a",     "about",   "above",  "after", "again", "against", "all",    "am",    "an",    "and",     "any",  "are", \
                    "aren't", "as",     "at",      "be",   "because",  "been", "before", "being", "below", "between", "both", "but", \
                    "by",   "can't",  "cannot",  "could", "couldn't", "did",    "didn't",  "do",   "does", "doesn't", "doing", "don't", \
                   "down", "during",   "each",   "few",     "for",   "from",   "further",  "had", "hadn't",  "has", "hasn't",  "have", \
                 "haven't", "having",   "he",   "he'd",    "he'll",   "he's",     "her",   "here", "here's", "hers", "herself", "him", \
                 "himself",  "his",    "how",  "how's",     "i",     "i'd",     "i'll",   "i'm",   "i've",   "if",    "in",   "into", \
                    "is",  "isn't",    "it",   "it's",     "its",   "itself",   "let's",   "me",   "more",   "most", "mustn't", "my", \
                "myself",   "no",     "nor",    "not",     "of",     "off",      "on",    "once",  "only",   "or",   "other", "ought", \
                  "our",   "ours",  "ourselves", "out",   "over",     "own",    "same",   "shan't",  "she",  "she'd", "she'll", "she's", \
                "should", "shouldn't", "so",    "some",   "such",    "than",    "that",   "that's",  "the",  "their",  "theirs", "them", \
             "themselves", "then",  "there", "there's",  "these",    "they",  "they'd",  "they'll", "they're", "they've","this", "those", \
                "through", "to",    "too",   "under",    "until",    "up",    "very",    "was",     "wasn't",   "we",   "we'd", "we'll", \
                "we're",  "we've",  "were", "weren't",   "what",  "what's",  "when",   "when's",   "where",  "where's", "which", "while", \
                "who",   "who's",  "whom",   "why",     "why's",    "with", "won't",   "would",   "wouldn't", "you",   "you'd", "you'll", \
             "you're",  "you've",  "your",  "yours",  "yourself", "yourselves"]
    
    lemmatizer = WordNetLemmatizer()

    for char in string:
        if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z') or (char >= '0' and char <= '9') or (char == "'"):
            temp.append(char.lower())
        else:
            if len(temp) > 1 and len(temp) < 28:
               
                if temp[0] == "'" or temp[-1] == "'":
                    temp.clear()
                    continue

                word = ''.join(temp)

                if word in stopword:
                    temp.clear()
                    continue
                
                word = lemmatizer.lemmatize(word)
                output.append(word)

            temp.clear()

    if len(temp) > 1 and len(temp) < 28:
        word = ''.join(temp)
    
        if word in stopword:
            temp.clear()
        elif temp[0] == "'" or temp[-1] == "'":
            temp.clear()
        else:
            word = lemmatizer.lemmatize(word)
            output.append(word)

    temp.clear()

    return output


def transferDict(theList, string):
    theDict = {}

    for word in theList:
        try:
            theDict[word].append(string)
        except KeyError:
            theDict[word] = [string]
    
    return theDict


def findFreq(theList):
    theDict = {}

    for word in theList:
        try:
            theDict[word] += 1
        except KeyError:
            theDict[word] = 1
    
    return theDict

def updateTags(srcDict, targetDict, word, value):
    temp = []
    with open(srcDict) as f:
        data = json.load(f)

        try:
            temp = data[word]
            for k, v in targetDict.items():
                if k in temp:
                    v[-1] += value
        except KeyError:
            pass
    
    

            
    
