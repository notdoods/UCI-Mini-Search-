from OneDocumentToken import DocTokens
import json
import math
import time
import collections

totalDocs = 0
#Word: informatics

uniqueWords = set()
invertedIndex = dict()
start = time.time()
DF = dict()

for folder in range(0,75):
    for file in range(0,500):
        if folder == 74 and file > 496:
            break
        else:
            #Create Total Doc count for IDF
            totalDocs += 1
            postings = dict()
            document = DocTokens(folder,file)
            document.tokenize(folder,file)
            # for the try/except, to help with debugging
            for word in document.term_frequency.keys():
                if word not in invertedIndex.keys():
                    invertedIndex[word] = dict()
                #Create new dictionary for DF of a word
                DF[word] = DF.get(word,0) + 1
                #Dictionary of a dictionary - {token: {docID: tf}} (The pair {docID: tf} is used only currently, it'll change to {docID: tf-idf})
                invertedIndex[word][document.docID] = document.term_frequency[word]
            print('Currently on: ' + document.docID)
            

for word in invertedIndex.keys():
    # logarithmic smoothing weight
    IDF = math.log10(totalDocs/(DF[word] + 1))
    docIDs = list(invertedIndex[word].keys())
    for docID in docIDs:
        invertedIndex[word][docID] = invertedIndex[word][docID] * IDF
        if invertedIndex[word][docID] < 0.000001:
            invertedIndex[word].pop(docID, None)

# Data for an extra file that gives some information, just time elapsed to create index and # of unique words
end = time.time()
elapsedTime = str(end - start)
uniqueWordCount = str(len(invertedIndex.keys()))

# Write into json file to use to read index in input
with open('index.json', 'w', encoding='utf-8') as text:
    json.dump(invertedIndex, text, indent=4, separators=(',',': '))

# Write into file for other information
with open('info.file', 'w', encoding='utf-8') as text:   
    text.write('This is the total time it took: ' + str(elapsedTime) + '\n')
    text.write("Here is the count for unique words: " + str(len(invertedIndex.keys())))

    
