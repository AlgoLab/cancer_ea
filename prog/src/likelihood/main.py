"""input file = example.in alpha beta seed"""

import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

from read_input import read_labels_scrs_format_in
from ea_node import EaNode
from ea_node_operators import init_ea_node_individual, mutate_ea_node_individual
from likelihood import sub_evaluate
from bitstring import BitArray
import random
import sys
import re


def main():
        if(len(sys.argv)==1):
                f = "./files/inputs/example_01.txt"
                alpha = 0.01
                beta = 0.0005
                seed = 11147
        else:        
                f=sys.argv[1]
                alpha=float(sys.argv[2])
                beta=float(sys.argv[3])
                seed=int(sys.argv[4])
        ex='\A(\w+): ((0|1)+)'
        (mutations,matrix) =read_labels_scrs_format_in(f)

        rows_matrix=[]
        for row in matrix:
                tmp=str(row)
                obj=re.search(ex,tmp)
                rows_matrix.append(obj.group(2))

        random.seed(seed)
        tree=init_ea_node_individual(EaNode,mutations,5)

        (new_tree,likelihood_tree)=evaluate(tree,rows_matrix,alpha,beta)

        for i in new_tree:
                print("parent : ",i[0].node_label," child : ",i[1]," likelihood_node : ",i[2])
        print("valore di likelihood per l'albero : ",likelihood_tree)



if __name__ =='__main__':
        main()
