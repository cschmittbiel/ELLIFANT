import numpy as np
import multiprocessing as mp


from partition import randomPartition
from ellipsoidFitting import ellipsoidFitting
from rebuildRtable import rebuildRtable
from extractData import deltaR

def fitPartitionGenetic(r_tables, beta, epsilon, nMaxGen, nIndiv, nEll, verbose):

    # Initialize population of nIndiv partitions, each with nEll ellipsoids
    partitions = np.array([randomPartition(nEll) for i in range(nIndiv)])
    # This is to make sure that each partition has nEll ellipsoids

    # TODO
    # One annoying one in a million chance that a partition has less than nEll ellipsoids bug
    # This is a temporary fix, we should find the bug and fix it but it's not a priority
    # It's not a big deal because the algorithm will still work and this loop runs only once

    for i in range(nIndiv):
        while nEll != len(np.unique(partitions[i])):
            partitions[i] = randomPartition(nEll)

    # Initialize fitnessLogs map to store fitness values (key: partition, value: fitness)
    fitnessLogs = {}

    counter, reign = 0, 0
    while reign < nMaxGen and counter < 10000:
        counter += 1
        print("Generation " + str(counter))

        # Compute fitness of each partition
        OldChampion = partitions[0]
        partitions, fitnessLogs = Generation(partitions, fitnessLogs, r_tables, beta, epsilon, nEll, nIndiv, nMaxGen, reign)
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

def Generation(partitions, fitnessLogs, r_tables, beta, epsilon, nEll, nIndiv, nMaxGen, reign):

    args = [(partitions[i], fitnessLogs, r_tables, beta, epsilon, nEll) for i in range(len(partitions))]

    fitnesses = []

    processes = mp.cpu_count()//2
    pool = mp.Pool(processes=processes)

    with pool as p:
        fitnesses = p.starmap(fitness, args)

    # Update fitnessLogs (the processes need to put the results in the fitnessLogs map so they agree)
    for i in range(len(partitions)):
        fitnessLogs[str(partitions[i])] = fitnesses[i]

    
    # Sort the fitnesses and remember the order to order the partitions
    order = np.argsort(fitnesses)
    
    # Order the partitions
    partitions = partitions[order]
    
    # Select the best half of the partitions
    partitions = partitions[:len(partitions)//2]

    mutationAmount = 15
    if reign > nMaxGen // 2:# We refine the search once we have a good partition
        mutationAmount = 5
    elif reign > nMaxGen // 10:
        mutationAmount = 2

    # Generate new partitions
    newPartitions = np.array([generatePartition(partitions[i], nEll, mutationAmount) for i in range(len(partitions))])

    # Add the new partitions to the population
    partitions = np.concatenate((partitions, newPartitions))
    
    partitions = partitions[:nIndiv]

    return partitions, fitnessLogs

def generatePartition(partition1, nEll, mutationAmount=15):
    #A partition is a 29x20 matrix of strictly positive integers
    #each integers is a region of the table, to be adjusted by the ellipsoid fitting
    partition2 = np.copy(partition1)

    #expand the regions
    for i in range(mutationAmount):

        #count the number of elements in each region
        nElsperRegion = np.zeros(nEll)
        flatten_partition = partition2.flatten().astype(int)
        unique_regions, region_counts = np.unique(flatten_partition, return_counts=True)
        nElsperRegion[unique_regions - 1] = region_counts

        #select a random region to expand
        region = np.random.choice(nEll)

        #we need to fudge the region selection if we don't want to lose regions
        if min(region_counts) < 30:
            region = np.argmin(region_counts)

        #select a random direction to expand the region
        direction = np.random.choice(4)

        #expand the region  
        partition2 = expand(partition2, float(region+1), direction)  

    #if there are less regions than the number of ellipsoids, generate a new partition 
    #(brings in new blood to the population)
    if len(unique_regions) < nEll:
        partition1 = randomPartition(nEll)

    #verify that the new partition has the same number of regions
    #if not, generate a new one
    return partition2

#expand a region in a given direction (0: left, 1: right, 2: up, 3: down)                             
def expand(matrix, region, direction):
    if direction == 0:
        # Expand the region one block to the left
        mask = (matrix[:, 1:] == region) & (matrix[:, :-1] != region)
        matrix[:, :-1][mask] = region

    elif direction == 1:
        # Expand the region one block to the right
        mask = (matrix[:, :-1] == region) & (matrix[:, 1:] != region)
        matrix[:, 1:][mask] = region

    elif direction == 2:
        # Expand the region one block upwards
        mask = (matrix[1:, :] == region) & (matrix[:-1, :] != region)
        matrix[:-1, :][mask] = region

    elif direction == 3:
        # Expand the region one block downwards
        mask = (matrix[:-1, :] == region) & (matrix[1:, :] != region)
        matrix[1:, :][mask] = region

    return matrix

def fitness(partition, fitnessLogs, r_tables, beta, epsilon, nEll):
    # Check if the fitness of the partition has already been calculated
    if str(partition) in fitnessLogs:
        return fitnessLogs[str(partition)]

    # Calculate fitness of the partition
    fitness = 0
    for r_table in r_tables:
        try :
            v = ellipsoidFitting(r_table, partition, beta, epsilon, freeConstant=True)
        except:
            print("Error in ellipsoid fitting")
            print("Partition: " + str(partition))
            print("Table: " + str(r_table))
            exit()
        adjustedR_table = rebuildRtable(v, partition, beta, epsilon, request='rp')
        fitness += deltaR(r_table, adjustedR_table)

    fitness /= len(r_tables)

    # Store the fitness of the partition
    fitnessLogs[str(partition)] = fitness

    return fitness

