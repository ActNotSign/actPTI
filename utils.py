#!/usr/bin/ python
import os
def isnumber(a):
    try:
        float(a)
        return True
    except:
        return False

def getrootpath():
    return os.path.split(os.path.realpath(__file__))[0]
