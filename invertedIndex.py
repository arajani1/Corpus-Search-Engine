import os
import math
import re
import json
import pymongo
from pymongo import MongoClient
from helper import tokenize, transferDict
from bs4 import BeautifulSoup

if __name__ == "__main__":
    
    cluster = MongoClient("mongodb+srv://phogbt:abc12345abc@cluster0-amher.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster["cs121"]
    collection = db["invertedIndex"]

    myDict = {}
    freqDict = {}
    tempList = []
    metaTempList = []

    higherDict = {}
    midDict = {}
    formatDict = {}  
    highTags = ["title", "h1"]
    midTags = ["h2", "h3", "h4", "h5", "h6"]
    formatTags = ["b", "i", "strong", "em"]

    with open("bookkeeping.json") as j:
        data = json.load(j)
    fileCounter = 0 # total is 36682
    # https://stackoverflow.com/questions/19587118/iterating-through-directories-with-python
    for subdir, dirs, files in os.walk("WEBPAGES_RAW"):
        for innerFile, urlNum in zip(files, data):
            finalFile = os.path.join(subdir, innerFile)
            
            idx = finalFile.split('/')[1].strip()       
            urlNum = idx + urlNum[urlNum.find('/'):]

            with open(finalFile, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "lxml") 

                for textFormat in soup.find_all(highTags):
                    tempList.extend(tokenize(textFormat.text))
                if tempList:
                    higherDict.update(transferDict(tempList, urlNum))
                tempList.clear()

                for textFormat in soup.find_all(midTags):
                    tempList.extend(tokenize(textFormat.text))
                if tempList:
                    midDict.update(transferDict(tempList, urlNum))
                tempList.clear()
                
                for textFormat in soup.find_all(formatTags):
                    tempList.extend(tokenize(textFormat.text))
                if tempList:
                    formatDict.update(transferDict(tempList, urlNum))
                tempList.clear()

                for script in soup(["script", "style"]):
                    script.extract()
                
                text = soup.get_text()
                tempList = tokenize(text)

                if tempList:
                    fileCounter += 1

                if tempList:
                    for word in tempList:
                        try:
                            freqDict[word] += 1
                        except KeyError:
                            freqDict[word] = 1
                    
                    for k, v in freqDict.items():
                        tf = round((math.log10(v) + 1), 2)
                        try:
                            myDict[k].append([urlNum, tf])
                        except KeyError:
                            myDict[k] = [[urlNum, tf]]
                    freqDict.clear()
                tempList.clear()

    totalDocs = fileCounter # total is 36682

    for k, v in myDict.items():
        df = len(v)
        idf = round((math.log10(totalDocs/df)), 2)

        for elem in v:
            elem[1] = round((elem[1] * idf), 2)
        collection.save({'_id' : k, 'docID' : v})

    with open("higherData.json", 'w') as f:
        json.dump(higherDict, f)
    
    with open("midData.json", 'w') as f:
        json.dump(midDict, f)

    with open("formatData.json", 'w') as f:
        json.dump(formatDict, f)
