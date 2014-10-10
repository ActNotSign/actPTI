#!/usr/bin/python
# -*- coding: utf-8 -*-
# rank
#
# matrix = {1:[2,3],2:[3,1],3:[1,5,6,7],4:[2,1],5:[3,6,1],6:[7],7:[1,8]}
# print pagerank.rank(matrix)

import math
class pagerank(object):

    '''
        get in-degree matrix
        '''
    @staticmethod
    def rematrix(matrix):
        nodes = set()
        for key, outdegree in matrix.items():
            nodes = nodes.union(outdegree).union([key])
        rematrix = {}
        for node in nodes:
            for key, outdegree in matrix.items():
                if key != node and node in outdegree:
                    if rematrix.has_key(node):
                        rematrix[node].append(key)
                    else:
                        rematrix[node] = [key]
            if not rematrix.has_key(node):
                rematrix[node] = []
        return rematrix

    '''
        pagerank
        PR(X) = PR(A)+PR(B)+...+PR(N)
        '''
    @staticmethod
    def rank(outdegreematrix, repeat=10000):
        #get in-degree
        indegreematrix = pagerank.rematrix(outdegreematrix)
        #init node weight
        pr = {}
        for node, indegree in indegreematrix.items():
            pr[node] = 1
        #rank
        for index in range(0, repeat):
            for node, indegree in indegreematrix.items():
                __nodepr = 0
                for innode in indegree:
                    if outdegreematrix.has_key(innode):
                        __nodepr += float(pr[innode]) / float(len(outdegreematrix[innode]))
                    else:
                        __nodepr += 0
                if 0 < math.fabs(pr[node] - __nodepr) < 0.00001:
                    break
                pr[node] = __nodepr
        pr = sorted(pr.items(), key=lambda d: d[1])
        return pr