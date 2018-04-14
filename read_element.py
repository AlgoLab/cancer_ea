# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from bitstring import BitArray

class ReadInfo(object):
    typeDescription = "ReadInfo"


class ReadElement(ReadInfo):  
    
    def __init__(self, readLabel, binaryRead):
        super(ReadInfo, self).__init__()
        self.readLabel = readLabel
        self.binaryRead = binaryRead
        
    def printElement(self, endS = '\n'):
        print( self.readLabel, ": ", self.binaryRead.bin, end=endS)
        
    
