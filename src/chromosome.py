from functools import cmp_to_key
from src.dataset import readData
from src.comparator import compare


class Chromosome:
    numTasks = 0  # number of input tasks
    numProcs = 0  # number of input processors
    initialized = False  # used to ensure readData() is called only once
    data = None  # data from the Kasahara dataset

    def __init__(self, file=0):
        if not Chromosome.initialized:
            Chromosome.initialized = True
            Chromosome.data = readData(file)
            Chromosome.numProcs = Chromosome.data['numProcs']
            Chromosome.numTasks = Chromosome.data['numTasks']
            del Chromosome.data['numProcs']
            del Chromosome.data['numTasks']
            Chromosome.data = list(Chromosome.data.values())
            # now, data is a list of task dictionaries sorted topologically
            # sort according to heights
            Chromosome.data.sort(key=cmp_to_key(compare))
            j = 0
            for i in Chromosome.data:  # save key for internal calculation later
                i['key'] = j
                j += 1
                # self.schedule = [[] for i in range(0, Chromosome.numProcs)]


# the fitness of a chromosome, currently, is its finishing time
def calculateFitness(chromosome):
    finishTime = [0] * Chromosome.numTasks
    for i in range(len(Chromosome.data)):  # for every task, do the following
        pre = []  # holds predecessors of i, including the forced predecessor
        p = chromosome[i]  # extract processor on which i is running
        j = False
        for _ in range(i):  # find if i is the first task to run
            if chromosome[_] == p:
                j = True
                break
        if j:  # if i isn't first task, find the task that runs just before i
            for k in range(i - 1, -1, -1):
                if p == chromosome[k]:  # forced predecessor
                    pre.append(Chromosome.data[k]['procID'])
        for k in Chromosome.data[i]:
            if 'pre' in k:
                pre.append(Chromosome.data[i][k])
        if len(pre) > 0:
            for i in range(len(pre)):
                for j in range(len(Chromosome.data)):
                    if Chromosome.data[j]['procID'] == pre[i]:
                        pre[i] = Chromosome.data[j]['key']
                        break
            finishTime[i] = max(
                [finishTime[j] for j in pre]
            ) + Chromosome.data[i]['procTime']
        else:
            finishTime[i] = Chromosome.data[i]['procTime']
    return max(finishTime),
