#!/usr/bin/ python
# -*- coding: utf-8 -*-
import sys
sys.setrecursionlimit(1000000)
from dictionary import dictionary

class act_segment (object):

    '''
        init params
        '''
    def __init__(self):
        dictionary.loaddictionary()
        self.wordmap = []
        self.wordcode = 'utf-8'
        pass

    '''
        check char
        '''
    def isEnglish(self, __char):
        asciicode = ord(__char)
        if 97 <= asciicode <= 122 or 65 <= asciicode <= 90 or 48 <= asciicode <= 57 or \
            32 < asciicode <= 47 or 49 <= asciicode <= 64 or 91 <= asciicode <= 96 or \
            123 <= asciicode <= 126:
            return True
        else :
            return False

    '''
        check number
        '''
    def isnumber(self, a):
        try:
            float(a)
            return True
        except:
            return False

    '''
        precise verification
        '''
    def precise(self):
        __maplen = len(self.wordmap) - 1
        __ismapping = False
        for index in range(0, __maplen):
            __word, __attr = self.wordmap[index]
            __word = __word.decode(self.wordcode)
            __wordlen = len(__word)
            if (index+1) > __maplen or __wordlen < 2:
                if not __ismapping:
                    self.wordmap[index] = (__word, __attr)
                __ismapping = False
                continue
            __word2, __attr2 = self.wordmap[index+1]
            __word2 = __word2.decode(self.wordcode)
            __checkword = __word[__wordlen-1]+__word2

            __status_check = dictionary.check(__checkword)
            __status_word = dictionary.check(__word[0:__wordlen-1])

            if __status_check.get('status') and __status_word.get('status'):
                self.wordmap[index] = (__word[0:__wordlen-1], __status_word.get('s'))
                self.wordmap[index+1] = (__checkword, __status_check.get('s'))
                __ismapping = True
            else:
                __ismapping = False
        pass

    '''
        array to string
        '''
    def tostring(self, wordmap, in_tagging=True,  space_mark="    "):
        __string = ''
        for word, attr in wordmap:
            if in_tagging:
                __string += word+'/'+attr+space_mark
            else:
                __string += word+space_mark
        return __string

    '''
        chinese word segments
        '''
    def segment(self, in_content, in_tagging=False,  space_mark="    "):
        self.wordmap = []
        self.fullmapping(in_content.decode(self.wordcode))
        self.precise()
        return self.tostring(self.wordmap, in_tagging, space_mark)

    def fullmapping(self, in_content):
        __str_len = len(in_content)
        __tagging = 'comb'
        """
            last word
            """
        if 1 >= __str_len:
            if in_content != '':
                __status = dictionary.check(in_content)
                if __status.get('s') != None:
                    __tagging = __status.get('s')
            self.wordmap.append((in_content, __tagging))
            return

        """
            depath
            """
        __forward_char = __segment_word = __tmp_word = in_content[0]
        for index in range(1, __str_len):
            __char = in_content[index]
            if self.isEnglish(__forward_char) and self.isEnglish(in_content[index]):
                __segment_word += __char
                pass
            elif dictionary.check(__tmp_word).get('status'):
                __segment_word = __tmp_word
                __tmp_word += __char
                if __str_len == len(__tmp_word) and dictionary.check(__tmp_word).get('status'):
                    __segment_word = __tmp_word
                __tmp_s = dictionary.check(__segment_word).get('s')
                if __tmp_s != None:
                    __tagging = __tmp_s
                pass
            else:
                break
            __forward_char = in_content[index-1]

        if self.isnumber(__segment_word):
            __tagging = 'm'
        self.wordmap.append((__segment_word, __tagging))
        self.fullmapping(in_content[len(__segment_word):__str_len])
        pass
