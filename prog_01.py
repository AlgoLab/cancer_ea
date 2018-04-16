# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

from ga_node import GaNode

from read_element import ReadElement


import sys, re, optparse

first_re = re.compile(r'.*\.in')

parser = optparse.OptionParser()
parser.set_defaults(debug=False,xls=False)
parser.add_option('--debug', action='store_true', dest='debug')
parser.add_option('--xls', action='store_true', dest='xls')
(options, args) = parser.parse_args()

if options.debug:
    print( 'option debug is activated')
if options.xls:
    print ('option xls is activated')

if len(args) > 1:
    raise ValueError("Too many command line arguments.")
if len(args) == 0:
    raise ValueError("Too few command line arguments.")  
if not first_re.match(args[0]):
    raise ValueError("First argument should be input file name, with extension 'in'.")
    
if options.debug:
    print("Input file name is: ", args[0])
fileInput = open(args[0], 'r')
textLine = fileInput.readline().strip()
while textLine.startswith("//") or textLine.startswith(";"):
    textLine = fileInput.readline()
labelsMutation = textLine.split()
if options.debug:
    print("Mutation labels (from input):\n", labelsMutation)
    
i = 1
textLine=fileInput.readline().strip()
reads = [];
while textLine!="":
    if textLine.startswith("//") or textLine.startswith(";"):
        textLine = fileInput.readline()
        continue
    bitLine = textLine.replace(" ", "")
    ba = BitArray(bin = bitLine)
    readElem = ReadElement(i, ba)
    reads.append(readElem)
    textLine=fileInput.readline().strip()
    i= i+1
if options.debug:
    print("Reads (from input):")
    for x in reads:
        x.printElement();

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", GaNode, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator 
toolbox.register("attr_bool", random.randint, 0, 1)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr_bool, 100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)






