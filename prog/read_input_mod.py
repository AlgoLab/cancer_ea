
from bitstring import BitArray

from read_element import ReadElement


def read_labels_scrs_format_in(parameters):
    """ Reads labels and single cell reads from input.
    Input file has the custom 'in' format.
    Symbol for unknown in SCRs is '?'
    Args:
        options : Parameter `options` represents options of the execution.
        parameters (:dictionary): Parameter `parameters` represents the
            execution parameters.

    Returns:
        tuple: A pair where first component is list of labels and second
            paramater is a list of :ReadElem objects.
    """
    input_file = open(parameters, 'r')
    text_line = input_file.readline().strip()
    # skip comments
    while text_line.startswith("//") or text_line.startswith(";"):
        text_line = input_file.readline()
    # labels are in the first non-commented line
    labels = text_line.split()
    # binary reads are in the rest of the file
    # one read is in one file
    i = 1
    text_line=input_file.readline().strip()
    reads = [];
    while text_line!="":
        # skip comments
        if text_line.startswith("//") or text_line.startswith(";"):
            text_line = input_file.readline()
            continue
        bit_line = text_line.replace(" ", "")
        bit_line = bit_line.replace("?", "0")
        ba = BitArray(bin = bit_line)
        unknown_line = text_line.replace(" ", "")
        unknown_line = unknown_line.replace("1", "0")
        unknown_line = unknown_line.replace("?", "1")
        ua = BitArray(bin = unknown_line)
        readElem = ReadElement(i, ba, ua)
        reads.append(readElem)
        text_line=input_file.readline().strip()
        i= i+1
    return(labels, reads)
