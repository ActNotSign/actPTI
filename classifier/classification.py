#!/usr/bin/ python
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.append(os.getcwd())

from utils import *
from segment.act import act_segment

try:
    import cPickle as pickle
except ImportError:
    import pickle

reload(sys)
sys.setdefaultencoding('utf8')

class classification(object):

    tfidf_root_dir = getrootpath()+'/words'
    dictpath = getrootpath()+'/classifier/train'
    datapath_tfidf = dictpath+'/tf-idf.dat'
    datapath_words = dictpath+'/words.rate'
    datapath_bayes = dictpath+'/trainresult.bayes'
    datapath_classes = dictpath+'/classes.bayes'

    classes = {}
    classesinfo = {}
    wordsum = 0
    wordcount = 0

    def __init__(self):
        pass

    def getpath(self):
        __path = ''
        for root, dirs, files in os.walk(classification.tfidf_root_dir, True):
            for name in files:
                if name != '.DS_Store':
                    __path = name
                    yield __path
        pass

    def formattfidftofile(self):
        categoryid = {}
        index_map = [0, 0, 0]
        for path in self.getpath():
            __nameinfo = path.split('_')
            __category = ''
            __id = ''
            for index in range(2, len(__nameinfo)):
                __tmpname = __nameinfo[index].replace('.txt', '')
                __category += __tmpname + ' '
                __tmpid = 0
                if categoryid.has_key(__tmpname):
                    __tmpid = categoryid.get(__tmpname)
                else :
                    index_map[index-2] += 1
                    __tmpid = index_map[index-2]
                    categoryid[__tmpname] = __tmpid
                __id += str(100 + __tmpid)
            self.classes[long(__id)] = {}
            self.classes[long(__id)]['name'] = __category
            self.classes[long(__id)]['word'] = {}

            for line in open(classification.tfidf_root_dir+'/'+path):
                wordinfo = line.strip('\n').split(' ')
                self.classes[long(__id)]['word'][wordinfo[0]] = float(wordinfo[1])
        file = open('classification.datapath', 'wb')
        pickle.dump(self.classes, file)
        file.close()
        pass

    def formatwordstofile(self):
        category = {}
        for path in self.getpath():
            __nameinfo = path.strip('.txt').split('_')
            __id = __nameinfo[0]
            if not category.has_key(__id):
                category[__id] = {}
            for line in open(classification.tfidf_root_dir+'/'+path):
                wordinfo = line.decode('utf-8').strip('\n').split('    ')
                wordinfo[0] = wordinfo[0].replace(' ', '')
                if len(wordinfo[0]) < 2 or \
                        isnumber(wordinfo[0]) or \
                        wordinfo[0].find('http') != -1 or \
                        wordinfo[0].find('=') != -1:
                    continue
                if category.get(__id).has_key(wordinfo[0]):
                    category.get(__id)[wordinfo[0]] += int(wordinfo[1])
                else:
                    category.get(__id)[wordinfo[0]] = int(wordinfo[1])
        index = 1
        output = open('words.dat', 'wb+')
        output_id = open('category_id.txt', 'wb+')
        for __id, words in category.items():
            output_id.write(__id+" "+str(index)+'\n')
            for word, rate in words.items():
                output.write(word+' '+str(rate)+' '+str(index)+'\n')
            index += 1
        output.close()
        output_id.close()

    def loadtfidf(self):
        file = open(classification.datapath_tfidf, 'rb')
        self.classes = pickle.load(file)
        file.close()
        pass

    def getcontent(self, content, regex):
        match = re.search(regex, content)
        if match:
            result = match.group(1)
        else:
            result = ""
        return result

    def segmentNews(self):
        title_regex = ur"<title>(.*?)</title>"
        content_regex = ur"<content>(.*?)</content>"
        seg = act_segment()
        for path in self.getpath():
            __tmp_words = {}
            for line in open(classification.tfidf_root_dir+'/'+path):
                line = line.strip('\n')
                __title = self.getcontent(line, title_regex)
                __content = ""
                __tmp_seg_words = ""
                if __title == "":
                    __content = self.getcontent(line, content_regex)
                    __tmp_seg_words  = seg.segment(__content)
                else:
                    __tmp_seg_words = seg.segment(__title)

                for word in __tmp_seg_words.split('    '):
                    if __tmp_words.has_key(word):
                        __tmp_words[word] += 1
                    else:
                        __tmp_words[word] = 1
            output = open('./words/'+path, 'wb+')
            for word, sum in __tmp_words.items():
                output.write(word+'    '+str(sum)+'\n')
            output.close()

    @staticmethod
    def loadwordsinfo():
        allwords = set()
        for line in open(classification.datapath_words):
            wordsinfo = line.strip('\n').split(' ')
            wordsinfo[2] = int(wordsinfo[2])
            if not classification.classes.has_key(wordsinfo[2]):
                classification.classes[wordsinfo[2]] = {}
                classification.classesinfo[wordsinfo[2]] = 0
            classification.classes[wordsinfo[2]][wordsinfo[0]] = int(wordsinfo[1])
            classification.classesinfo[wordsinfo[2]] += int(wordsinfo[1])
            classification.wordcount += int(wordsinfo[1])
            allwords.add(wordsinfo[0])
        classification.wordsum = len(allwords)
        del allwords

    @staticmethod
    def loadtrainbayes():
        for line in open(classification.datapath_bayes):
            wordsinfo = line.strip('\n').split(' ')
            wordsinfo[2] = int(wordsinfo[2])
            if not classification.classes.has_key(wordsinfo[2]):
                classification.classes[wordsinfo[2]] = {}
            classification.classes[wordsinfo[2]][wordsinfo[0]] = float(wordsinfo[1])

        for line in open(classification.datapath_classes):
            __info = line.strip('\n').split(' ')
            classification.classesinfo[int(__info[0])] = float(__info[1])

    @staticmethod
    def getwordposteriorbyid(__id, word):
        try:
            return classification.classes[__id][word]
        except:
            return 0.00001