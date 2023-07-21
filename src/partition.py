import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# The standard CIE angles for beta and tan epsilon :
beta = np.array([0, 2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180])
tanEpsilon = np.array([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12])
epsilon = np.arctan(tanEpsilon)

def loadPartition(filename, sheetname):
    #load the partition from the excel file
    partition = np.zeros((29,20))
    with pd.ExcelFile(filename) as path:
        partition = pd.read_excel(path, sheet_name=sheetname, header=None).to_numpy()
    return partition

def stopsToPartition(stops):
    #convert the stops to a partition of integers
    partition = np.zeros((29,20))
    c=0
    for i in range(20):
        if beta[i] in stops and beta[i] != 180:
            c += 1
        partition[:,i] = c
    return partition

#Four way flood fill algorithm + rolling average
def randomPartition(n=3, show=False):
    partition = np.zeros((29,20))
    databis = np.zeros((29,20))
    startpoints = np.zeros((n,2))

    #choose n random distinct starting points
    for i in range(n):
        startpoints[i,0] = np.random.randint(0,29)
        startpoints[i,1] = np.random.randint(0,20)
        while np.any(startpoints[i,:] == startpoints[:i,:]):
            startpoints[i,0] = np.random.randint(0,29)
            startpoints[i,1] = np.random.randint(0,20)

    #assign the starting points to the partition
    for i in range(n):
        partition[int(startpoints[i,0]), int(startpoints[i,1])] = i+1
 
    while np.any(partition==0):

        #choose a random permutation of the table to ensure the algorithm is not biased
        perm = np.random.permutation(580)

        for k, l in np.ndindex(partition.shape):
            
            i, j = perm[(k*20+l)%580]//20, perm[(k*20+l)%580]%20

            if partition[i,j] != 0:
                #spread the value to the surrounding cells
                if i != 0:
                    if partition[i-1,j] == 0:
                        databis[i-1,j] = partition[i,j]
                if i != 28:
                    if partition[i+1,j] == 0:
                        databis[i+1,j] = partition[i,j]
                if j != 0:
                    if partition[i,j-1] == 0:
                        databis[i,j-1] = partition[i,j]
                if j != 19:
                    if partition[i,j+1] == 0:
                        databis[i,j+1] = partition[i,j]
        partition = databis.copy()

    #now we do a discrete rolling 3x3 average to smooth the partition
    count = np.zeros((27, 18, n), dtype=int)
    neighborhood = partition[1:28, 1:19]

    for k in range(-1, 2):
        for l in range(-1, 2):
            for i in range(n):
                count[:,:,i] += (partition[(1 + k):(28 + k), (1 + l):(19 + l)] == i+1) * 1

    partition[1:28, 1:19] = np.argmax(count, axis=2) + 1

    #make an imshow plot if the user wants to see the result
    if show:
        plt.imshow(partition, cmap='Set2')
        plt.show()
    
    return partition