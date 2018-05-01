""" The :mod:`deap_cancer_ga_02` module contains an example how to use Deap for GA
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
from read_input import read_labels_reads

from ga_node import GaNode
from ga_node_operators import init_ga_node_individual  
from ga_node_operators import evaluate_ga_node_individual
from ga_node_operators import crossover_ga_node_individuals
from ga_node_operators import mutate_ga_node_individual

def main():
    """  This function is an entry  point of the application.
    """
    # reading command-line argumets and options
    parser = optparse.OptionParser()
    parser.set_defaults(debug=False,xls=False)
    parser.add_option('--debug', action='store_true', dest='debug')
    parser.add_option('--verbose', action='store_true', dest='verbose')
    parser.add_option('--randomized', action='store_true', dest='randomized')
    (options, args) = parser.parse_args()
    
    # obtaining execution paramters
    parameters = get_execution_parameters(options, args)
    if(options.debug or options.verbose):
        print("Execution parameters: ", parameters);
    
    # seeding random process
    if( not options.randomized ):
        random.seed(parameters['RandomSeed'])
     
    # reading read elements from input file
    (labels, reads) = read_labels_reads(options, parameters)
    if(options.debug or options.verbose):
        print("Mutation labels:", labels);
        print("Reads (from input):")
        for x in reads:
            print(x);
    
    # create fitness function
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
   
    # create strucute of the individual
    creator.create("Individual", GaNode, fitness=creator.FitnessMin)
    
    # create toolbox for execution of the genetic algorithm
    toolbox = base.Toolbox()
    
    # register bolean attribute to toolbbox 
    toolbox.register("attr_bool", random.randint, 0, 1)

    # register individual creation to toolbbox 
    toolbox.register("individual", 
                     init_ga_node_individual, 
                     creator.Individual, 
                     labels=labels, 
                     size=2 * len(labels))
      
    # register population to toolbbox 
    toolbox.register("population", 
                     tools.initRepeat, 
                     list, 
                     toolbox.individual)
 
    # register evaluation function
    toolbox.register("evaluate", 
                     evaluate_ga_node_individual, 
                     reads)

    # register the crossover operator
    toolbox.register("mate", 
                     crossover_ga_node_individuals)
    
    # register a mutation operator 
    toolbox.register("mutate", 
                     mutate_ga_node_individual)
     
    # operator for selecting individuals for breeding the next
    # generation: each individual of the current generation
    # is replaced by the 'fittest' (best) of three individuals
    # drawn randomly from the current generation.
    toolbox.register("select", 
                     tools.selTournament, 
                     tournsize=3)

    # create an initial population, where each individual is a GaTree
    population_size = 150
    pop = toolbox.population(n=population_size)
    if( options.verbose):
        print("Population (size %d) - initial\n"%len(pop))
        print (pop)
 
    # Probability with which two individuals are crossed
    crossover_probability = 0.5
       
    # Probability for mutating an individual
    mutation_probability = 0.2

    if( options.debug or options.verbose):
        print("Start of evolution")
 
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    if( options.debug):
        print("Fitnesses of individuals in population - initial")
        print (fitnesses)
    
    # Assign fitness to individuals in population
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        
    # Variable keeping track of the number of generations
    generation = 0
  
    # Begin the evolution
    while True:
        if( options.debug or options.verbose):
            print("-- Generation %i --" % generation)

        if( options.debug or options.verbose):
            fits = [ind.fitness.values[0] for ind in pop]
            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean**2)**0.5
            print("  Fitness: ", fits)
            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))
            print("  Avg %s" % mean)
            print("  Std %s" % std)
            best_in_generation = tools.selBest(pop, 1)[0]
            print("  Best individual: \n %s", best_in_generation)
      
        # A new generation
        generation += 1
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
    
        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            # cross two individuals with previously determined probability 
            if random.random() < crossover_probability:
                toolbox.mate(child1, child2)
                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring:
            # mutate an individual with previously determined probability 
            if random.random() < mutation_probability:
                toolbox.mutate(mutant)
                # fitness values of the mutant
                # must be recalculated later
                del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        
        # Check if any of finishing criteria is meet
        # Criteria based on number of generations
        if( generation > 10 ):
            break
        # Criteria based on standard deviation of fitness in population
        fits = [ind.fitness.values[0] for ind in pop]
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5 
        if( std <= 0):
            break
          
    if( options.debug or options.verbose):
        print("-- End of evolution --")
    if( options.verbose):
        print("Population (size %d) - at end\n"%len(pop))
        print (pop)  
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is\n%s\n, with fitness %s" % (best_ind, best_ind.fitness.values))
    return

# this means that if this script is executed, then 
# main() will be executed
if __name__ == '__main__':
    main()



