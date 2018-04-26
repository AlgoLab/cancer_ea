"""
This module is used for reading input file.

Created on Thu Apr 19 22:37:58 2018

@author: vlado.filipovic
"""

from bitstring import BitArray

from read_element import ReadElement


def read_labels_reads(options, parameters):
    """
    Reads labels and reads from input.
    """
    fileInput = open(parameters['InputFile'], 'r')
    textLine = fileInput.readline().strip()
    # skip comments
    while textLine.startswith("//") or textLine.startswith(";"):
        textLine = fileInput.readline()
    # labels are in the first non-commented line
    labels = textLine.split()        
    # binary reads are in the rest of the file
    # one read is in one file
    i = 1
    textLine=fileInput.readline().strip()
    reads = [];
    while textLine!="":
        # skip comments
        if textLine.startswith("//") or textLine.startswith(";"):
            textLine = fileInput.readline()
            continue
        bitLine = textLine.replace(" ", "")
        ba = BitArray(bin = bitLine)
        readElem = ReadElement(i, ba)
        reads.append(readElem)
        textLine=fileInput.readline().strip()
        i= i+1
    return(labels, reads)