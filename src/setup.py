import random
from deap import base
from deap import creator
from deap import tools

from src.chromosome import Chromosome
from src.chromosome import calculateFitness
from src.genetic_algorithm import initialisation


def main():
    temp = Chromosome(0)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    MU = 20
    NGEN = 100
    CXPB = 0.95

    toolbox = base.Toolbox()
    toolbox.register("individual", initialisation, creator.Individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", calculateFitness)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)

    pop = toolbox.population(n=MU)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for i in range(NGEN):
        pop = toolbox.select(pop, len(pop))
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        pop = toolbox.select(pop + offspring, MU)

    for i in pop:
        print(i, end='', flush=True)
        print(i.fitness.values)


main()
