import numpy
from deap import base
from deap import creator
from deap import tools

from src.chromosome import Chromosome
from src.chromosome import calculateFitness
from src.genetic_algorithm import initialisation

temp = Chromosome(0)
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("individual", initialisation, creator.Individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", calculateFitness)
toolbox.register("select", tools.selNSGA2)

MU = 20
pop = toolbox.population(n=MU)

fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit

pop = toolbox.select(pop, len(pop))

for i in pop:
    print(i.fitness.values, end=' ', flush=True)
