#!/usr/bin/ python

from segment.act import act_segment
from classifier.naivebayesclassifier import naivebayesclassifier
from similarity.cosinesimilarity import cosinesimilarity
#segments
seg = act_segment()
words = seg.segment('福布斯：苹果为何放抛弃GT Advanced？】福布斯杂志今日发表题目为“美梦破碎：iPhone无缘蓝宝石玻璃”的文章称，苹果之所以放弃蓝宝石玻璃合作伙伴GT ，都是因为iPhone 6屏幕的曲线边缘惹得祸。没有蓝宝石玻璃的iPhone 6同样热卖，但合作伙伴GT 却遭受致命打击。', False, ' ')
print words
#classifier
words = words.split(' ')
classifier = naivebayesclassifier()
print classifier.classifier(words)
# #text similarity
# print cosinesimilarity.similarity(['我','不是','很','爱你'],['我','不是','爱你'])