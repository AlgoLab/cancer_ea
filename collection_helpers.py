""" The :mod:`collection_helpers` module contains  contains helper functions 
for collection.

"""


def count(collection):
    """ Helper function that count elements in collection.
    """
    i=0
    for node in collection:
        i+=1
    return i


def index_of(collection, element, start=0):
    """ Helper function that fids a postion of the element in collection.
    
    Search in this fuction is executed from the begining toward end.
    """
    for i in range(start, collection.length):
        if( i < start ):
            continue;
        if( collection[i]==element):
            return i;
    return -1

def last_index_of(collection, element):
    """     Helper function that fids a postion of the element in collection.
    
    Search in this fuction is executed from the end toward begining.
    """
    for i in range(collection.length-1, -1, -1):
        if( collection[i]==element):
            return i;
    return -1

def next_element_in_cyclic(element, collection):
        """     Helper function that fids next element in collection. Next 
                element for the last element is the first one in collection. 
    
        Returns: next element in collection. If element is not in collection, 
        function will return None. 
        """
        ind = collection.index(element)
        if(ind<0):
            return None
        ind = (ind+1)%len(collection)
        return collection[ind]