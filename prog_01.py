# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

from bitstring import BitArray
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
linija = fileInput.readline()
labelsMutation = linija.split()
if options.debug:
    print("Mutation labels (from input):\n", labelsMutation)
    
i = 1
linija=fileInput.readline().strip()
reads = [];
while linija!="":
    bitovi = linija.replace(" ", "")
    ba = BitArray(bin = bitovi)
    readElem = ReadElement(i, ba)
    reads.append(readElem)
    linija=fileInput.readline().strip()
    i= i+1
if options.debug:
    print("Reads (from input):")
    for x in reads:
        x.printElement();






