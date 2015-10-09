#!/usr/bin/python
# -*- coding: utf-8 -*-
# text similarity
import math
class cosinesimilarity(object):

    weight = 1

    '''
        format words array to vector
        '''
    @staticmethod
    def wordstovector(words=[], wordscompare=[]):
        __allwords = set(words).union(set(wordscompare))
        __words = {}
        __wordscompare= {}
        for word in words:
            if not __words.has_key(word):
                __words[word] = cosinesimilarity.weight
            else:
                __words[word] += cosinesimilarity.weight

        for word in wordscompare:
            if not __wordscompare.has_key(word):
                __wordscompare[word] = cosinesimilarity.weight
            else:
                __wordscompare[word] += cosinesimilarity.weight

        vector = [[], []]
        for word in __allwords:
            if __words.has_key(word):
                vector[0].append(__words.get(word))
            else:
                vector[0].append(0)

            if __wordscompare.has_key(word):
                vector[1].append(__wordscompare.get(word))
            else:
                vector[1].append(0)

        del __allwords
        del __words
        del __wordscompare
        return vector

    '''
        consine
        cos0 = (x1*y1 + x2*y2)/sqrt(x1,2)+sqrt(y1,2)
        '''
    @staticmethod
    def similarity(words=[], wordscompare=[]):
        vector = cosinesimilarity.wordstovector(words, wordscompare)
        x1 = 0
        y1 = 0
        z1 = 0
        for index in range(0, len(vector[0])):
            x1 += math.pow(vector[0][index], 2)
            y1 += math.pow(vector[1][index], 2)
            z1 += vector[0][index] * vector[1][index]
        cosine = float(z1) / float(math.sqrt(x1) * math.sqrt(y1))
        return cosine
