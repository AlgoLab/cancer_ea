# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

from bitstring import BitArray
from ga_node import GaNode


# creating GA tree
def initIndividual(ind_class, labels, size):
    rootBitArray = BitArray(int = 0, length = size)
    root = ind_class('--', rootBitArray)
    root.initializeSubtree( labels, size)
    return root;
        
x = initIndividual(GaNode, ['a','b','c','d','e'], 10)  
x.printGaSubtree() 




