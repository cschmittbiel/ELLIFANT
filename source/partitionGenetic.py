import numpy as np
import matplotlib.pyplot as plt

from multiprocessing import Pool

from cuttingTablesUp import randomPartition
from ellipsoidFitting import ellipsoidFitting
from rebuildRtable import rebuildRtable
from extractData import RMSE

def fitPartitionGenetic(r_tables, beta, epsilon, nGen, nIndiv, nEll):

    # Initialize population of nIndiv partitions
    partitions = np.array([randomPartition(nEll) for i in range(nIndiv)])

    # Initialize fitnessLogs map to store fitness values (key: partition, value: fitness)
    fitnessLogs = {}

    for i in range(nGen):
        print("Generation " + str(i+1) + " of " + str(nGen))
        Generation(partitions, fitnessLogs, r_tables, beta, epsilon, nEll, nIndiv)

    # Return the best partition (smaller fitness value is better)
    return min(fitnessLogs, key=fitnessLogs.get)

def Generation(partitions, fitnessLogs, r_tables, beta, epsilon, nEll, nIndiv):

    args = [(partitions[i], fitnessLogs, r_tables, beta, epsilon, nEll) for i in range(len(partitions))]

    fitnesses = []

    # Evaluate fitness of each partition
    with Pool() as pool:
        fitnesses = pool.starmap(fitness, args)

    # Sort the fitnesses and remember the order to order the partitions
    order = np.argsort(fitnesses)
    
    # Order the partitions
    partitions = partitions[order]

    # Select the best half of the partitions
    partitions = partitions[:len(partitions)//2]

    # Generate new partitions
    newPartitions = np.array([generatePartition(partitions[i], nEll) for i in range(len(partitions))])

    # Add the new partitions to the population
    partitions = np.concatenate((partitions, newPartitions))

    partitions = partitions[:nIndiv]

def generatePartition(partition1, nEll, mutationAmount=25):
    #A partition is a 29x20 matrix of strictly positive integers
    #each integers is a region of the table, to be adjusted by the ellipsoid fitting

    newPartition = np.copy(partition1)

    #expand the regions
    for i in range(mutationAmount):

        #count the number of elements in each region
        nElsperRegion = np.zeros(nEll)
        flatten_partition = partition1.flatten().astype(int)
        unique_regions, region_counts = np.unique(flatten_partition, return_counts=True)
        nElsperRegion[unique_regions - 1] = region_counts

        #select a random region to expand using the weights of the number of elements in each region
        region = np.random.choice(nEll)
        if min(nElsperRegion) < 30:
            region = np.argmin(nElsperRegion)

        #select a random direction to expand the region
        direction = np.random.randint(4)
        #expand the region in the selected direction
        if direction == 0:
            for j in range(1, 20):
                newPartition[:, j-1] = np.where(partition1[:, j] == region, region, newPartition[:, j-1])

        elif direction == 1:
            for j in range(19):
                newPartition[:, j+1] = np.where(partition1[:, j] == region, region, newPartition[:, j+1])

        elif direction == 2:
            for j in range(1, 29):
                newPartition[j-1, :] = np.where(partition1[j, :] == region, region, newPartition[j-1, :])

        elif direction == 3:
            for j in range(28):
                newPartition[j+1, :] = np.where(partition1[j, :] == region, region, newPartition[j+1, :])

        partition1 = np.copy(newPartition)
    
    if np.unique(newPartition).size < nEll:
        #if the new partition has less regions than the original, add regions
        #the new regions are added in the same way as the original partition
        while np.unique(newPartition).size < nEll:
            missingRegions = np.setdiff1d(np.arange(1, nEll+1), np.unique(newPartition))
            for region in missingRegions:
                x=np.random.randint(29-5)
                y=np.random.randint(20-5)
                newPartition[x:x+5, y:y+5] = region

    #verify that the new partition has the same number of regions
    #if not, generate a new one
    return newPartition

def fitness(partition, fitnessLogs, r_tables, beta, epsilon, nEll):

    # Check if the fitness of the partition has already been calculated
    if str(partition) in fitnessLogs:
        return fitnessLogs[str(partition)]

    # Calculate fitness of the partition
    fitness = 0
    for r_table in r_tables:

        v = ellipsoidFitting(r_table, partition, beta, epsilon)
        adjustedR_table = rebuildRtable(v, partition, beta, epsilon)
        fitness += RMSE(r_table, adjustedR_table)

        print("Fitness of partition " + str(partition.shape) + " for table " + str(r_table.shape) + " is " + str(fitness))

    fitness /= len(r_tables)

    # Store fitness of the partition
    fitnessLogs[str(partition)] = fitness

    return fitness
