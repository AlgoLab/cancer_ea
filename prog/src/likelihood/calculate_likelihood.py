""" Questo modulo permette di calcolare il valore di likelihood dati in input
    la matrice iniziale , la matrice finale , alpha e beta.
	Esempio = python calculate_likelihood.py matrix_in.txt matrix_out.txt 0.15 0.001
"""

import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

import sys
from likelihood import evaluate_dollo_node_direct1

#matrice iniziale
file_rows=[]
with open(sys.argv[1],'r') as input_file:
        for s in input_file:
                file_rows.append(s.split())
				
#matrice inferita
file_rows1=[]
with open(sys.argv[2],'r') as input_file:
        for s in input_file:
                file_rows1.append(s.split())
				
				
alpha=float(sys.argv[3])
beta=float(sys.argv[4])

print(evaluate_dollo_node_direct1(file_rows,alpha,beta,file_rows1))
