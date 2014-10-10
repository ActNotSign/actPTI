#!/usr/bin python
# -*- coding: utf-8 -*-
import sys, os, gzip
try:
    import cPickle as pickle
except ImportError:
    import pickle

reload(sys)
sys.setdefaultencoding('utf8')

class wordtree(object):

    tree = {}
    index_depath = 0
    dictpath = os.path.split(os.path.realpath(__file__))[0]
    coredict = dictpath+'/dict/core.dict'

    @staticmethod
    def insert(in_word, in_speechtagging):
        in_word = in_word.decode("utf-8")
        wordtree.createstems(in_word, wordtree.tree, in_speechtagging)
        pass

    @staticmethod
    def createstems(in_word, __stems, in_speechtagging):
        count = len(in_word)
        char = ord(in_word[0])
        if not __stems.has_key(char):
            __stems[char] = {}
        if not __stems.has_key('k'):
            __stems['k'] = {}
        __stems['k'][char] = in_speechtagging

        if count == 1:
            return True
        return wordtree.createstems(in_word[1:count], __stems.get(char), in_speechtagging)

    @staticmethod
    def check(in_word):
        in_word = in_word.decode("utf-8")
        wordtree.index_depath = 0
        return wordtree.depathcheck(in_word, wordtree.tree)

    @staticmethod
    def depathcheck(in_word, __tree):
        if __tree == None:
            return {'status': False}
        count = len(in_word)
        char = ord(in_word[0])
        if count == 1:
            if __tree.has_key(char):
                __tagging = __tree.get('k').get(char)
                if __tagging != None:
                    return {'s': __tagging, 'status': True}
            return {'status': False}
        wordtree.index_depath += 1
        return wordtree.depathcheck(in_word[1:count], __tree.get(char))

    @staticmethod
    def picksave():
        for line in open('words.txt'):
            wordsinfo = line.strip('\n').split('	')
            wordtree.insert(wordsinfo[0], wordsinfo[1])
        gfile = open(wordtree.coredict, 'wb')
        pickle.dump(wordtree.tree, gfile)
        gfile.close()

    @staticmethod
    def pickload():
        file = open(wordtree.coredict, 'rb')
        wordtree.tree = pickle.load(file)
        file.close()

    @staticmethod
    def unzipCore():
        file = open(wordtree.coredict, 'wb')
        pickle.dump(wordtree.tree, file)
        file.close()

    @staticmethod
    def zipCore():
        file = gzip.open(wordtree.coredict, 'wb')
        pickle.dump(wordtree.tree, file)
        file.close()