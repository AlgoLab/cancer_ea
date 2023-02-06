""" The :mod:`deap_cancer_ga_01` module contains an example how to use Deap for GA
that solves problem we are dealing with.

Example for command-line parameters:
inputFile=example_01.in randomSeed=1113 --debug

"""

import optparse
import random


from deap import base
from deap import creator
from deap import tools

from command_line import get_execution_parameters
from read_input import read_labels_scrs_format_in
from ea_node import EaNode
from ea_node_operators import init_ea_node_individual  
from ea_node_operators import assign_reads_to_ea_tree 
from ea_node_operators import evaluate_ea_node_individual
from ea_node_operators import mutate_ea_node_individual

def main():
    """ This function is an entry  point of the application.
    """
    # reading command-line argumets and options
    parser = optparse.OptionParser()
    parser.set_defaults(debug=False,xls=False)
    parser.add_option('--debug', action='store_true', dest='debug')
    parser.add_option('--verbose', action='store_true', dest='verbose')
    (options, args) = parser.parse_args()
    
    # obtaining execution paramters
    parameters = {'InputFile': 'XXX.in', 
                  'InputFormat': 'in',
                  'RandomSeed': -1,
                  'PopulationSize': 5}
    parameters = get_execution_parameters(options, args, parameters)
    if(options.debug):
        print("Execution parameters: ", parameters);
    
    # seeding random process
    if( int(parameters['RandomSeed'])>0 ):
        random.seed(parameters['RandomSeed'])
     
    # reading read elements from input file
    (labels, reads) = read_labels_scrs_format_in(options, parameters)
    if( options.debug):
        print("Mutatuion labels:", labels);
        print("Reads (from input):")
        for x in reads:
            print(x);
    
    # creating fitness function
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    # creating strucute of the individual
    creator.create("Individual", EaNode, fitness=creator.FitnessMax)
    
    # creating toolbox for execution of the genetic algorithm
    toolbox = base.Toolbox()
    
    # registering bolean attribute to toolbbox 
    toolbox.register("attr_bool", random.randint, 0, 1)
    # registering individual creation to toolbbox 
    toolbox.register("individual", 
                     init_ea_node_individual, 
                     creator.Individual, 
                     labels=labels, 
                     size=3 * len(labels))
    # registering mutation operator to toolbbox 
    toolbox.register("mutate", mutate_ea_node_individual)
    # registering population to toolbbox 
    toolbox.register("population", 
                     tools.initRepeat, 
                     list, 
                     toolbox.individual)
 
    toolbox.register("evaluate", evaluate_ea_node_individual, reads)

    
    # creating one individual via toolbox
    test_ind = toolbox.individual()
    
    # printing test individual 
    print( test_ind )
    
    # testing if created individual is inherited from GaMode
    # and printing output
    if(issubclass(type(test_ind), EaNode)):
        print( "Class Individual is sublass of class EaNode")
    else:
        print( "Class Individual is NOT sublass of class EaNode")
    
    # setting fitness of the individual
    test_ind.fitness.values = (12, 0)
    
    # executiong mutation on the individual
    toolbox.mutate(test_ind)
    
    # assign reads to nodes and calculate total distance
    (assignment, diff) = assign_reads_to_ea_tree(test_ind, reads)
    print(assignment)
    print( diff )    
    return

# this means that if this script is executed, then 
# main() will be executed
if __name__ == '__main__':
    main()



