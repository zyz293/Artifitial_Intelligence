# Name: 
# Date:
# Description:
#
#

# from __future__ import division
import math, os, pickle, re
import random
import copy

class Bayes_Classifier:

    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
        cache of a trained classifier has been stored, it loads this cache.  Otherwise,
        the system will proceed through training.  After running this method, the classifier
        is ready to classify input text."""
        self.Positive = {}
        self.Negative = {}
        # self.CV_Pos = {}
        # self.CV_Neg = {}
        if os.path.isfile('Positive_best.txt') is True and os.path.isfile('Negative_best.txt') is True:
            self.Positive = self.load('Positive_best.txt')  # why should add self ahead ????
            self.Negative = self.load('Negative_best.txt')
            # print self.Positive
        else:
            self.train()

    def crossvalidation(self):
        Precision = []
        Recall = []
        Fvalue = []
        IFileList = []
        for fFileObj in os.walk('movies_reviews/'):
            IFileList = fFileObj[2]
            break
        filelist = random.sample(IFileList, len(IFileList))
        i = 0
        while i < 10:
            self.trainCV(i, filelist, Precision, Recall, Fvalue)
            i += 1
        print 'average precision: ' ,float(float(sum(Precision)) / float(len(Precision)))
        print 'average recall: ' ,float(float(sum(Recall)) / float(len(Recall)))
        print 'average fvalue: ' ,float(float(sum(Fvalue)) / float(len(Fvalue)))

    def trainCV(self, i, filelist, Precision, Recall, Fvalue):
        CV_Pos = {}
        CV_Neg = {}
        test = filelist[(i*1386):(i*1386+1390)]
        # print len(test)
        # print 'test: ' ,test
        # test = filelist[(i*1386):(i*1386+20)]
        filecopy = copy.deepcopy(filelist)
        for m in test:
            filecopy.remove(m)
        # print len(filecopy)
        train = filecopy
        # print len(train)
        for txt in train:
            if txt.split('-')[1] == '1':
                path = 'movies_reviews/%s' % str(txt)
                st = self.loadFile(path)
                text = self.tokenize(st)
                for word in text:
                    if re.match('[a-zA-Z0-9]', str(word)) is not None:
                        if word in CV_Neg:
                            CV_Neg[word] += 1
                        else:
                            CV_Neg[word] = 1
            elif txt.split('-')[1] == '5':
                path = 'movies_reviews/%s' % str(txt)
                st = self.loadFile(path)
                text = self.tokenize(st)
                for word in text:
                    if re.match('[a-zA-Z0-9]', str(word)) is not None:
                        if word in CV_Pos:
                            CV_Pos[word] += 1
                        else:
                            CV_Pos[word] = 1
            
        self.save(CV_Neg, 'Negative_CV.txt'), self.save(CV_Pos, 'Positive_CV.txt')
        self.classifyCV(test, Precision, Recall, Fvalue)

    def classifyCV(self, test, Precision, Recall, Fvalue):
        CV_Pos = self.load('Positive_CV.txt')
        CV_Neg = self.load('Negative_CV.txt')
        pos_right = 0
        neg_right = 0
        pos_counter = 0
        neg_counter = 0
        # P_pos = 0
        # P_neg = 0
        # flag = 'neutral'
        flag = 2
        pos_review = 0
        neg_review = 0

        for txt in test:
            P_pos = 0
            P_neg = 0
            if txt.split('-')[1] == '1':
                neg_review += 1
                # print 'neg_review: ' ,neg_review
                # flag = 'negative'
                flag = 1
            elif txt.split('-')[1] == '5':
                pos_review += 1
                # print 'pos_review: ' ,pos_review
                # flag = 'positive'
                flag = 5
            path = 'movies_reviews/%s' % str(txt)
            st = self.loadFile(path)
            testtext = self.tokenize(st)
            for word in testtext:
                if re.match('[a-zA-Z0-9]', str(word)) is not None:
                    if word in CV_Pos:
                        P_pos = P_pos + math.log((float(CV_Pos[word] + 1) / sum(CV_Pos.values())))
                    else:
                        P_pos = P_pos + math.log(1 / float(sum(CV_Pos.values())))
                    if word in CV_Neg:
                        P_neg = P_neg + math.log((float(CV_Neg[word] + 1) / sum(CV_Neg.values())))
                    else:
                        P_neg = P_neg + math.log(1 / float(sum(CV_Neg.values())))
            # print P_pos, P_neg
            

            difference = P_pos - P_neg
            # print difference
            # if difference >= 1:
            if difference >=0:
                # classfication = 'positive'
                classfication = 5
                pos_counter += 1
                    # print 'pos_counter: ' ,pos_counter
                # elif difference <= -2:
            elif difference < 0:
                # classfication = 'negative'
                classfication = 1
                neg_counter += 1
                # print 'neg_counter: ' ,neg_counter
                # else:
                #    classfication = 'neutral'
            if classfication == flag and flag == 5:
                pos_right += 1
                    # print 'pos_right: ' ,pos_right
            elif classfication == flag and flag == 1:
                neg_right += 1
                    # print 'neg_right: ' ,neg_right
        print 'pos_right: ' ,pos_right
        print 'pos_counter: ' ,pos_counter
        print 'pos_review: ' ,pos_review
        precision = float(pos_right) / float(pos_counter)
        print 'precision: ' ,precision
        recall = float(pos_right) / float(pos_review)
        print 'recall: ' ,recall
        fvalue = float(2.0 * float(precision) * float(recall) / float(float(precision) + float(recall)))
        print 'fvalue: ' ,fvalue
        Precision.append(precision)
        Recall.append(recall)
        Fvalue.append(fvalue)
        print '----------------------------------------------------------------------'






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
            if txt.split('-')[1] == '1':
                path = 'movies_reviews/%s' % str(txt)
                st = self.loadFile(path)
                text = self.tokenize(st)
                for i in range(len(text)-1):
                    bigrams = text[i] + ' ' + text[i+1]
                    if bigrams in self.Negative:
                        self.Negative[str(bigrams)] += 1
                    else:
                        self.Negative[str(bigrams)] = 1
            elif txt.split('-')[1] == '5':
                path = 'movies_reviews/%s' % str(txt)
                st = self.loadFile(path)
                text = self.tokenize(st)
                for i in range(len(text)-1):
                    bigrams = text[i] + ' ' + text[i+1]
                    if bigrams in self.Positive:
                        self.Positive[str(bigrams)] += 1
                    else:
                        self.Positive[str(bigrams)] = 1
        return self.save(self.Negative, 'Negative_best.txt'), self.save(self.Positive, 'Positive_best.txt')
    
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
        print P_pos, P_neg
        for i in range(len(text) - 1):
            bigrams = text[i] + ' ' + text[i+1]
            # print bigrams
            if bigrams in self.Positive:
                P_pos = P_pos + math.log((float(self.Positive[str(bigrams)] + 1) / sum(self.Positive.values())))
            else:
                P_pos = P_pos + math.log(1 / float(sum(self.Positive.values())))
            if bigrams in self.Negative:
                P_neg = P_neg + math.log((float(self.Negative[str(bigrams)] + 1) / sum(self.Negative.values())))
            else:
                P_neg = P_neg + math.log(1 / float(sum(self.Negative.values())))
        print P_pos, P_neg
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
