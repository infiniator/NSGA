from random import randrange
from src.chromosome import Chromosome


def initialisation(myChromosome):  # done
    tempChromosome = myChromosome()
    for i in range(Chromosome.numTasks):
        tempChromosome.append(0)
    for j in range(len(Chromosome.data)):
        k = randrange(0, Chromosome.numProcs)
        tempChromosome[j] = k
    return tempChromosome
