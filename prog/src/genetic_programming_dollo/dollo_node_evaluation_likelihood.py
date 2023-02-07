"""Questo modulo contiene le funzioni per il calcolo della funzione likelihood,
    evaluate_dollo_node_Evaluation e' la funzione principale e 
    sub evaluation e' la sotto funzione che prende una riga della matrice
    e il profilo genetico di un nodo.
    final matrix restituisce la matrice inferita E associata al valore likelihood di un albero
"""

import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

from reads.read_element import ReadElement

from bitstring import BitArray
from anytree import RenderTree
import math

from functools import lru_cache


def evaluate_dollo_node_likelihood(reads,alpha,beta,individual):

    likelihood=0
    for read in reads:
        result={}
        for pre,_,node in RenderTree(individual):
            value=sub_evaluate(node.binary_tag.bin,read,alpha,beta)
            result[value]=node.binary_tag.bin
        max_single=max(result.keys())
        likelihood+=max_single
    return (-likelihood,)


@lru_cache(maxsize=8192, typed=True)
def sub_evaluate(node,read,alpha,beta):

    likelihood=0
    for j in range(len(read.binary_read)):
        if read.binary_read.bin[j] == '0':
            if node[j] == '0':
                likelihood+=math.log(1-beta)
            elif node[j] == '1':
                likelihood+=math.log(alpha)
            elif node[j] == '-1':
                return print("error")
        elif read.binary_read.bin[j] == '1':
            if node[j] == '0':
                likelihood+=math.log(beta)
            elif node[j] == '1':
                likelihood+=math.log(1-alpha)
            elif node[j] == '-1':
                return print("error")
        elif read.binary_read.bin[j] == '2':
            likelihood+=0
    return likelihood
    
