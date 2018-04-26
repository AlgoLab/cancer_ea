"""
This module contains an example how to use Deap for GA
that solves problem we are dealing with.

Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

import optparse
import random


from deap import base
from deap import creator
from deap import tools

from command_line import get_execution_parameters
from read_input import read_labels_reads
from ga_node import GaNode
from ga_node import init_ga_node_individual, evaluation_ga_node, mutation_ga_node
from ga_node import assign_reads_to_tree

def main():
    """
    This function is an entry  point of the application.
    """
    # reading command-line argumets and options
    parser = optparse.OptionParser()
    parser.set_defaults(debug=False,xls=False)
    parser.add_option('--debug', action='store_true', dest='debug')
    parser.add_option('--randomized', action='store_true', dest='randomized')
    (options, args) = parser.parse_args()
    
    # obtaining execution paramters
    parameters = get_execution_parameters(options, args)
    if(options.debug):
        print("Execution parameters: ", parameters);
    
    # seeding random process
    if( not options.randomized ):
        random.seed(parameters['RandomSeed'])
     
    # reading read elements from input file
    (labels, reads) = read_labels_reads(options, parameters)
    if( options.debug):
        print("Mutatuion labels:", labels);
        print("Reads (from input):")
        for x in reads:
            print(x);
    
    # creating fitness function
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    # creating strucute of the individual
    creator.create("Individual", GaNode, fitness=creator.FitnessMax)
    
    # creating toolbox for execution of the genetic algorithm
    toolbox = base.Toolbox()
    
    # registering bolean attribute to toolbbox 
    toolbox.register("attr_bool", random.randint, 0, 1)
    # registering individual creation to toolbbox 
    toolbox.register("individual", 
                     init_ga_node_individual, 
                     creator.Individual, 
                     labels=labels, 
                     size=3 * len(labels))
    # registering mutation operator to toolbbox 
    toolbox.register("mutate", mutation_ga_node)
    # registering population to toolbbox 
    toolbox.register("population", 
                     tools.initRepeat, 
                     list, 
                     toolbox.individual)
 
    toolbox.register("evaluate", evaluation_ga_node, reads)

    
    # creating one individual via toolbox
    test_ind = toolbox.individual()
    
    # printing test individual 
    print( test_ind )
    
    # testing if created individual is inherited from GaMode
    # and printing output
    if(issubclass(type(test_ind), GaNode)):
        print( "Class Individual is sublass of class GaNode")
    else:
        print( "Class Individual is NOT sublass of class GaNode")
    
    # setting fitness of the individual
    test_ind.fitness.values = (12, 0)
    
    # executiong mutation on the individual
    toolbox.mutate(test_ind)
    
    # assign reads to nodes and calculate total distance
    (assignment, diff) = assign_reads_to_tree(test_ind, reads)
    print(assignment)
    print( diff )    
    return

# this means that if this script is executed, then 
# main() will be executed
if __name__ == '__main__':
    main()



