"""
The :mod:`collection_helpers` module contains  contains helper functions for collection.

"""


def count(collection):
    """
    Helper function that count elements in collection.
    """
    i=0
    for node in collection:
        i+=1
    return i


def index_of(collection, element, start=0):
    """
    Helper function that fids a postion of the element in collection
    (from the begining toward end).
    """
    for i in range(start, collection.length):
        if( i < start ):
            continue;
        if( collection[i]==element):
            return i;
    return -1

def last_index_of(collection, element):
    """
    Helper function that fids a postion of the element in collection
    (from the end toward begining).
    """
    for i in range(collection.length-1, -1, -1):
        if( collection[i]==element):
            return i;
    return -1