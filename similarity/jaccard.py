#!/usr/bin/python
# -*- coding: utf-8 -*-
# similarity

class jaccard(object):

    '''
        jaccard similarity
        j(A,B) = |A interseciton B| / |A union B|
        '''
    @staticmethod
    def similarity(vector_1=[], vector_2=[]):
        tmp_intersection = len(set(vector_1) & set(vector_2))
        tmp_union = len(set(vector_1).union(set(vector_2)))
        return float(tmp_intersection)/float(tmp_union)