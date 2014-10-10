#!/usr/bin/ python
# -*- coding: utf-8 -*-
import sys,os
from wordtree import wordtree
reload(sys)
sys.setdefaultencoding('utf8')

class dictionary (object):

    symbol = {}
    dictpath = os.path.split(os.path.realpath(__file__))[0]

    '''
        load default dictionary
        '''
    @staticmethod
    def loadcoredict():
        wordtree.pickload()
        pass

    '''
        load custom dictionary
        '''
    @staticmethod
    def loadcustomdict():
        for line in open (dictionary.dictpath+"/dict/custom.dict"):
            wordinfo = line.strip("\n").split("	")
            wordtree.insert(wordinfo[0],wordinfo[1])
        pass

    @staticmethod
    def loadsymbolict():
        for line in open (dictionary.dictpath+"/dict/symbol.dict"):
            wordlist = line.split(" ")
            len_list = len(wordlist)
            for i in range(0,len_list,2):
                if i+1 < len_list:
                    dictionary.symbol[long(wordlist[i])] = wordlist[i+1]
        pass

    @staticmethod
    def loaddictionary():
        dictionary.loadcoredict()
        dictionary.loadcustomdict()
        dictionary.loadsymbolict()
        pass

    @staticmethod
    def check(in_word):
        if len(in_word) == 1:
            if dictionary.symbol.get(ord(in_word)) != None :
                return {'status': True, 's': 'wp'}
        return wordtree.check(in_word)

    @staticmethod
    def checksymbol(word):
        return dictionary.symbol.get(word)

