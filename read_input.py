""" The :mod:`read_input` module is used for reading input file.

"""

from bitstring import BitArray

from read_element import ReadElement


def read_labels_reads(options, parameters):
    """ Reads labels and reads from input.

    Args:
        options : Parameter `options` represents options of the execution.
        parameters (:dictionary): Parameter `parameters` represents the 
            execution parameters.
 
    Returns:
        tuple: A pair where first component is list of labels and second 
            paramater is a list of :ReadElem objects.
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