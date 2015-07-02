# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re

class Bayes_Classifier:

    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
        cache of a trained classifier has been stored, it loads this cache.  Otherwise,
        the system will proceed through training.  After running this method, the classifier
        is ready to classify input text."""
        self.Positive = {}
        self.Negative = {}
        if os.path.isfile('Positive.txt') is True and os.path.isfile('Negative.txt') is True:
            self.Positive = self.load('Positive.txt')  # why should add self ahead ????
            self.Negative = self.load('Negative.txt')
            # print self.Positive
        else:
            self.train()

    def train(self):
        """Trains the Naive Bayes Sentiment Classifier."""
        IFileList = []
        for fFileObj in os.walk('movies_reviews/'):
            IFileList = fFileObj[2]
            break
        for txt in IFileList:
            if txt.split('-')[1] == '1':
                path = 'movies_reviews/%s' % str(txt)
                st = self.loadFile(path)
                text = self.tokenize(st)
                for word in text:
                    if re.match('[a-zA-Z0-9]', str(word)) is not None:
                        if word in self.Negative:
                            self.Negative[str(word)] += 1
                        else:
                            self.Negative[str(word)] = 1
            elif txt.split('-')[1] == '5':
                path = 'movies_reviews/%s' % str(txt)
                st = self.loadFile(path)
                text = self.tokenize(st)
                for word in text:
                    if re.match('[a-zA-Z0-9]', str(word)) is not None:
                        if word in self.Positive:
                            self.Positive[str(word)] += 1
                        else:
                            self.Positive[str(word)] = 1
        return self.save(self.Negative, 'Negative.txt'), self.save(self.Positive, 'Positive.txt')
    
    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        P_pos = 0
        P_neg = 0
        text = self.tokenize(sText)
        for word in text:
            if re.match('[a-zA-Z0-9]', str(word)) is not None:
                if word in self.Positive:
                    P_pos = P_pos + math.log((float(self.Positive[str(word)] + 1) / sum(self.Positive.values())))
                else:
                    P_pos = P_pos + math.log(1 / float(sum(self.Positive.values())))
                if word in self.Negative:
                    P_neg = P_neg + math.log((float(self.Negative[str(word)] + 1) / sum(self.Negative.values())))
                else:
                    P_neg = P_neg + math.log(1 / float(sum(self.Negative.values())))
        # print P_pos
        # print P_neg
        difference = P_pos - P_neg
        # print difference
        if difference >= 1:
            return 'positive'
        elif difference <= -2:
            return 'negative'
        else:
            return 'neutral'

    def loadFile(self, sFilename):
        """Given a file name, return the contents of the file as a string."""

        f = open(sFilename, "r")
        sTxt = f.read()
        f.close()
        return sTxt
   
    def save(self, dObj, sFilename):
        """Given an object and a file name, write the object to the file using pickle."""

        f = open(sFilename, "w")
        p = pickle.Pickler(f)
        p.dump(dObj)
        f.close()
   
    def load(self, sFilename):
        """Given a file name, load and return the object stored in the file."""

        f = open(sFilename, "r")
        u = pickle.Unpickler(f)
        dObj = u.load()
        f.close()
        return dObj

    def tokenize(self, sText):
        """Given a string of text sText, returns a list of the individual tokens that
        occur in that string (in order)."""

        lTokens = []
        sToken = ""
        for c in sText:
            if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
                sToken += c
            else:
                if sToken != "":
                    lTokens.append(sToken)
                    sToken = ""
                if c.strip() != "":
                    lTokens.append(str(c.strip()))
               
        if sToken != "":
            lTokens.append(sToken)

        return lTokens
