import numpy as np

from partition import randomStops
from partitionGenetic import Generation

def fitBetaGenetic(r_tables, beta, epsilon, nMaxGen, nIndiv, nEll, verbose):

    # Initialize population of nIndiv betaPartitions, each with nEll ellipsoids
    partitions = np.array([randomStops(nEll) for i in range(nIndiv)])
    # This is to make sure that each partition has nEll ellipsoids

    for i in range(nIndiv):
        while nEll != len(np.unique(partitions[i])):
            partitions[i] = randomStops(nEll)
            
    # Initialize fitnessLogs map to store fitness values (key: partition, value: fitness)
    fitnessLogs = {}

    counter, reign = 0, 0
    while reign < nMaxGen and counter < 10000:
        counter += 1
        print("Generation " + str(counter))

        # Compute fitness of each partition
        OldChampion = partitions[0]
        partitions, fitnessLogs = Generation(partitions, fitnessLogs, r_tables, beta, epsilon, nEll, nIndiv, nMaxGen, reign)
        adjustPartitions(partitions, nEll)
        Champion = partitions[0]

        # Check if the best partition has changed, if not, increment the counter
        if np.array_equal(OldChampion, Champion):
            reign += 1
        else :
            reign = 1
        if verbose:
            print("Best partition of generation " + str(counter) + " has a deltaR over this data of " + \
                str(round(fitnessLogs[str(partitions[0])], 3)) + ", it has won the last " + str(reign) + " generations.")

    # Return the best partition (smaller fitness value is better)
    return partitions[0], fitnessLogs[str(partitions[0])]

def adjustPartitions(partitions, nEll):
    #every partition gets its first column set to ones and its last column set to nEll
    for p in partitions:
        for i in range(len(p)):
            p[i][0] = 1
            p[i][-1] = nEll