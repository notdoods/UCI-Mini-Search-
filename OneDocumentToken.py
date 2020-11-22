import os
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import math

class DocTokens:
    """
    This class is responsible for handling corpus related functionalities like mapping a url to its local file name
    """

    # The corpus directory name
    WEBPAGES_RAW_NAME = "WEBPAGES_RAW"
    stop = set(stopwords.words('english'))
    
    
    def __init__(self,folder,file):
        self.term_frequency = dict()
        self.docID = str(folder) + '/' + str(file)
        self.wordCount = 0

        
    def tokenize(self,folder,file):
        with open(os.path.join('.', self.WEBPAGES_RAW_NAME ,str(folder),str(file)), 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml')
            #Get rid of all text that is javascript or CSS
            for script in soup(['script','style']):
                script.decompose()
            allWords = soup.get_text()
        #Gets all base tokens
        tokens = word_tokenize(allWords)
        #if the token is a number, non-alphanumeric, or non-ascii, then it will filter it out
        tokens = [word.lower() for word in tokens if word.isalpha() and word.isascii() and len(word) > 1]
        #this filters out all the stop words
        tokens = [word for word in tokens if word not in self.stop]
        wordLemmatizer = WordNetLemmatizer()
        final = []
        #lemmatize each word in all available tokens
        for item in tokens:
            final.append(wordLemmatizer.lemmatize(item))
        #total word count is used for Term Frequency since Term Frequency = # of time term occurs/titak wordCount
        self.wordCount = len(final)
        #Removes numbers from list 
        for t in final:
            self.term_frequency[t] = self.term_frequency.get(t, 0) + 1
        #Term Frequency = # of time term occurs/total wordCount
        for t in self.term_frequency.keys():
            # perform log10 on term frequency to take into account for larger documents skewing answers
            self.term_frequency[t] = (math.log10(self.term_frequency[t]) + 1)
            
            
    
            
