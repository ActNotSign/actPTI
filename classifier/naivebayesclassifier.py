#!/usr/bin/ python
# -*- coding: utf-8 -*-
# classifier
import sys
from classification import classification
from utils import *
reload(sys)
sys.setdefaultencoding('utf8')

class naivebayesclassifier(object):

    def __init__(self):
        classification.loadtrainbayes()
        pass

    '''
        train bayes
        P(A|B) = P(B|A)P(A)/P(B)
        '''
    @staticmethod
    def trainnaivebayes():
        classification.loadwordsinfo()
        trainresult = {}
        for __id, words in classification.classes.items():
            for word, rate in words.items():
                p = float(rate + 1)/float(classification.classesinfo[__id] + classification.wordsum)
                if not trainresult.has_key(__id):
                    trainresult[__id] = {}
                trainresult[__id][word] = p

        output = open(classification.datapath_bayes, 'wb+')
        for __id, words in trainresult.items():
            for word, p in words.items():
                output.write(word+' '+str(p)+' '+str(__id)+'\n')
        output.close()

        output_classes_p = open(classification.datapath_classes, 'wb+')
        for __id, count in classification.classesinfo.items():
            output_classes_p.write(str(__id)+' '+str(float(count)/float(classification.wordcount))+'\n')
        output_classes_p.close()

    '''
        posterior probability
        P(C) = P(W|C)P(C)
        '''
    def posteriorprobability(self, words = []):
        classprobability = {}
        for __id, PC in classification.classesinfo.items():
            PP = float(1.0)
            for word in words:
                WP = classification.getwordposteriorbyid(__id, word) * 100000.0
                PP = PP * WP
            PP = float(PP) * float(PC)
            classprobability[__id] = PP
        return classprobability

    '''
        classifier
        '''
    def classifier(self, words = []):
        return sorted(self.posteriorprobability(words).items(), key=lambda d: d[1])
