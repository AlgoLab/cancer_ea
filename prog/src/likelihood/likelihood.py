"""funzioni di support per il modulo calculate_likelihood.py"""


import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

import math


def evaluate_dollo_node_direct1(reads,alpha,beta,individual):
    
    likelihood=0
    for i in reads:
        l=[]
        result=0
        for j in individual:
            result=sub_evaluate(i,j,alpha,beta)
            l.append(result)
        likelihood+=max(l)
    return likelihood

def sub_evaluate(node,read,alpha,beta):
    likelihood=0

    for j in range(len(read)):
        if read[j] == '0':
            if node[j] == '0':
                likelihood+=math.log(1-beta)
            elif node[j] == '1':
                likelihood+=math.log(alpha)
            elif node[j] == '-1':
                return print("error")
        elif read[j] == '1':
            if node[j] == '0':
                likelihood+=math.log(beta)
            elif node[j] == '1':
                likelihood+=math.log(1-alpha)
            elif node[j] == '-1':
                return print("error")
        elif read[j] == '?':
            likelihood+=0
    return likelihood
