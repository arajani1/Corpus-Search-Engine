import json
import math
import pymongo
import numpy as np
from helper import findFreq, updateTags
from pymongo import MongoClient

cluster = MongoClient("")
db = cluster["cs121"]
collection = db["invertedIndex"]

with open("bookkeeping.json") as j:
    data = json.load(j)

totalDocs = 36682
count = 0
freqDict = {}
docMatrix = {}
queryList = []

search = input("Enter the words to search: ")
query = search.split(" ")
freqDict = findFreq(query)

for token, freq in freqDict.items():
    token = collection.find({"_id" : token.lower()})
    
    for t in token:
        word = t["_id"]
        result = t["docID"]
        count += 1
        
        if count == 1:
            for k in result:
                docMatrix[k[0]] = [k[1]]
        elif count > 1:
            for k in result:
                try: 
                    docMatrix[k[0]].append(k[1])
                except KeyError:
                    docMatrix[k[0]] = [0] 
                    while (len(docMatrix[k[0]]) < (count - 1)):
                        docMatrix[k[0]].append(0)
                    docMatrix[k[0]].append(k[1])
            
            for k in docMatrix.keys():
                while(len(docMatrix[k]) < count):
                    docMatrix[k].append(0)
        
        updateTags("higherData.json", docMatrix, word, 5)
        updateTags("midData.json", docMatrix, word, 3)
        updateTags("formatData.json", docMatrix, word, 2)

        tf = (math.log10(freq)) + 1 
        df = len(result)
        idf = math.log10(totalDocs/df)
        queryWeight = tf * idf

        queryList.append(queryWeight)

if count == 0:
    exit()
elif count == 1:
    output = sorted(docMatrix.items(), key= lambda _: _[1], reverse=True)
    urls = len(output)
    print(f"Number of URLs retrieved: {urls}")

    output = output[0:20]
    print()
    for i, elem in enumerate(output):
        if elem[0] in data.keys():
            print(f"{i} \t {data[elem[0]]}")
    #exit()

queryVector = np.array(queryList)
queryLength = np.linalg.norm(queryVector)

for idx, val in enumerate(queryVector):
    queryVector[idx] = val/queryLength

for k, docList in docMatrix.items():
    docVector = np.array(docList)
    docLength = np.linalg.norm(docVector)

    for idx, val in enumerate(docVector):
        docVector[idx] = val/docLength
    docMatrix[k] = docVector


score = {}
for url, vector in docMatrix.items():
    dot = np.dot(queryVector, vector)
    score[url] = dot

output = sorted(score.items(), key= lambda _: _[1], reverse=True)
urls = len(output)
print(f"Number of URLs retrieved: {urls}")

output = output[0:20]
print()

for i, elem in enumerate(output):
    if elem[0] in data.keys():
        print(f"{i} \t {data[elem[0]]}")
