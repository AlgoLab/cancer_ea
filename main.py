"""  The :mod:`cancer_gp` module represents an entry  point of the application.

Example for command-line parameters:
inputFile=example_01.in randomSeed=1113 --debug

"""

import optparse
import random

from datetime import datetime

from deap import base
from deap import creator
from deap import tools


from command_line import get_execution_parameters
from read_input import read_labels_scrs_format_in

from dollo_node import DolloNode
from dollo_node_operators import init_dollo_node_individual
from dollo_node_operators import evaluate_dollo_node_individual 
from dollo_node_operators import crossover_dollo_node_individuals
from dollo_node_operators import mutate_dollo_node_individual

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
                  'DolloK': 2,
                  'Alpha': 0.35,
                  'Beta': 0.005,
                  'RandomSeed': -1,
                  'PopulationSize': 5,
                  'CrossoverProbability': 0.85,
                  'MutationProbability': 0.05}
    parameters = get_execution_parameters(options, args, parameters)
    if(options.debug or options.verbose):
        print("Execution parameters: ", parameters);
    
    # setting random seed
    if( int(parameters['RandomSeed']) > 0 ):
        random.seed(int(parameters['RandomSeed']))
    else:
        random.seed(datetime.now())

    # reading read elements from input file
    if( parameters['InputFormat'] == 'in' ):
        (labels, reads) = read_labels_scrs_format_in(options, parameters)
        if(options.debug or options.verbose):
            print("Mutation labels (from input file):\n", labels);
            print("Reads[Unknowns] (from input file):")
            for x in reads:
                print(x);
    else:
        print("Input format is not right.")
        return
    
    # create fitness function
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
   
    # create strucute of the individual
    creator.create("Individual", DolloNode, fitness=creator.FitnessMin)
    # parameter k in Dollo model
    dollo_k = int(parameters['DolloK'])
    
    # create toolbox for execution of the genetic algorithm
    toolbox = base.Toolbox()
    
    # register bolean attribute to toolbbox 
    toolbox.register("attr_bool", random.randint, 0, 1)

    # register individual creation to toolbbox 
    toolbox.register("individual", 
                     init_dollo_node_individual, 
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
                     evaluate_dollo_node_individual, 
                     reads)
    # probability of false positives and false negatives
    alpha = float(parameters['Alpha'])
    beta = float(parameters['Beta'])

    # register the crossover operator
    toolbox.register("mate", 
                     crossover_dollo_node_individuals)
    # probability with which two individuals are crossed
    crossover_probability = float(parameters['CrossoverProbability'])
       
    
    # register a mutation operator 
    toolbox.register("mutate", 
                     mutate_dollo_node_individual)
    # probability for mutating an individual
    mutation_probability = float(parameters['MutationProbability'])
 
    # operator for selecting individuals for breeding the next
    # generation: each individual of the current generation
    # is replaced by the 'fittest' (best) of three individuals
    # drawn randomly from the current generation.
    toolbox.register("select", 
                     tools.selTournamentFineGrained, 
                     fgtournsize=3.5)

    # create an initial population, where each individual is a tree
    population_size = int(parameters['PopulationSize'])
    pop = toolbox.population(n=population_size)
    if( options.verbose):
        print("Population (size %d) - initial\n"%len(pop))
        print (pop)
 
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



