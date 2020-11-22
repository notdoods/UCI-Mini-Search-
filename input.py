import json
import os
import collections

JSON_FILE_NAME = os.path.join(".", 'WEBPAGES_RAW', "bookkeeping.json")
INDEX_FILE_NAME = os.path.join('.','index.json')

fileURLmap = json.load(open(JSON_FILE_NAME), encoding='utf-8')
indexMap = json.load(open(INDEX_FILE_NAME), encoding='utf-8')

while True:
    try:
        # Maximum is the input for how much result it will give. If maximum is greater than document frequency, then shows all info relating to word
        maximum = input('Enter # of top ranked search results (type /quit to exit program): ')
        print(maximum)
        if int(maximum) < 1:
            raise ValueError()
        elif maximum == '/quit':
            break
        query = str(input('Enter your query : '))
        if query == '/quit':
            break
        else:
            # Take into account multiple words
            queries = query.lower().split()
            queriesSize = len(queries)
            cumulativeScore = {}
            for q in queries:
                if q in indexMap.keys():
                    for docID in indexMap[q].keys():
                        # adds tf-idf score to new dictionary, cumulativeScore, key = docID, value = tf-idf of all queries.
                        cumulativeScore[docID] = cumulativeScore.get(docID, 0) + indexMap[q][docID]
                else:
                    continue
            
            for docID in cumulativeScore.keys():
                # divides cumulative score by # of words in query, resulting in average tf-idf of all words
                cumulativeScore[docID] = round(cumulativeScore[docID]/queriesSize, 7)
            
            if cumulativeScore == {}:
                print('No results found.')
            else:
                sortedList = sorted(cumulativeScore.items(), key=lambda kv: kv[1], reverse=True)
                print('\nTotal # of URLs of query: ' + str(len(sortedList)) + '\n')

                if int(maximum) > len(sortedList):
                    print('# of top ranked URLs is less than inputted, displaying all URLs. ')
                    for index in range(0,len(sortedList)):
                        print('Document ID: {} , with a score of: {}\n{}\n'.format(sortedList[index][0],sortedList[index][1],fileURLmap[sortedList[index][0]],len(sortedList)))
                else:
                    for index in range(0,int(maximum)):
                        print('Document ID: {} , with a score of: {}\n{}\n'.format(sortedList[index][0],sortedList[index][1],fileURLmap[sortedList[index][0]],len(sortedList)))
                    
        
    except ValueError:
        print('Invalid entry. Cannot be less 0 or negative,')
