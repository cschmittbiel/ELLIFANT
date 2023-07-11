import numpy as np
import pandas as pd

def rebuildRtable(v, partition, beta, epsilon, rollAverages = True, request = 'none', verbose = False):
    #the request is to know what to apply the roll averages to (if anything)
    #ef = ellipsoid fitting
    #bga = beta genetic algorithm (colmuns)
    #pga = partitioning genetic algorithm (rolling window over edges)
    
    betaRad = beta*np.pi/180
    data = np.zeros((29,20))
    a = v[:,0] + v[:,1] -1
    b = v[:,0] - 2*v[:,1] -1
    c = v[:,1] - 2*v[:,0] -1
    g = v[:,2]
    p = v[:,3]
    s = v[:,4]

    #try to get the q and d values
    #depending on the number of parameters, they may not be there
    #(see how ellipses are fitted in Ellipsoidfitting.py)
    try:
        q = v[:,5]
        d = v[:,6]
    except IndexError:
        if verbose:
            print("No q and d values found. Setting them to 0.")
        q = np.zeros(len(v))
        d = np.zeros(len(v))

    if verbose:
        print("Rebuilding r-table...")

    for i ,j in np.ndindex(data.shape):
        group = int(partition[i,j])-1

        #I still don't know why or how or what, but this fixes the problem
        #I will try to figure it out later
        if request == 'cols':
            if j == 4:
                group = 0
            if j == 11:
                group = 1

        A = a[group]*(np.sin(epsilon[i])**2)*(np.cos(betaRad[j])**2) + b[group]*(np.sin(epsilon[i])**2)*(np.sin(betaRad[j])**2) + c[group]*(np.cos(epsilon[i])**2) + g[group]*np.sin(epsilon[i])*np.cos(epsilon[i])*np.cos(betaRad[j])

        #d != 0 makes us do much more math, so we don't do that if it's not needed
        if d[group] == 0:
            r_value_denom = A

            #convention
            if r_value_denom == 0:
                data[i,j] = 0
                continue

            r_value_numer = 2*p[group]*np.sin(epsilon[i])*np.cos(betaRad[j]) + 2*s[group]*np.cos(epsilon[i])
            
            data[i,j] = -r_value_numer/r_value_denom
            #print("epsilon: ", epsilon[i], "beta: ", betaRad[j], "a: ", a[group], "b: ", b[group], "c: ", c[group], "g: ", g[group], "p: ", p[group], "s: ", s[group], "q: ", q[group], "d: ", d[group], "r_value: ", data[i,j])
            continue

        B = p[group]*np.sin(epsilon[i])*np.cos(betaRad[j]) \
        + s[group]*np.cos(betaRad[j]) \
        + q[group]*np.sin(epsilon[i])*np.sin(betaRad[j]) 
        
        Disc = B**2 - 4*A*d[group]
        if Disc < 0:
            data[i,j] = 0
            continue
        data[i,j] = (-B + np.sqrt(Disc))/(2*A)

    for i,j in np.ndindex(data.shape):
        if data[i,j] < 0:
            data[i,j] = 0

    #the top row is set to it's average value (all joins at the top of the solid)
    data [0,:] = np.mean(data[0,:])
    
    newData = np.copy(data)
    #roll averages
    if rollAverages and request == 'cols':
        #look at the first line of the partition, if any two values are different, add 2 to a counter
        #if the counter is 2, then we have a partition
        cols = []
        for i in range(1, data.shape[1]-1):
            if (partition[0,i] != partition[0,i-1]) or (partition[0,i] != partition[0,i+1]):
                cols.append(i)
        if verbose:
            print('rolling averages over columns: ', cols)
        for i in cols:
            newData[:,i] = (data[:,i-1] + data[:,i] + data[:,i+1])/3

    if rollAverages and request == 'rp':#random partition
        if verbose:
            print('rolling averages over random partition')
        for j in range(1,19):
            for i in range(1,28):
                if partition[i,j] != partition[i-1,j]:
                    newData[i,j] = (data[i,j-1] + data[i,j] + data[i,j+1])/3
                if partition[i,j] != partition[i+1,j]:
                    newData[i,j] = (data[i-1,j] + data[i,j] + data[i+1,j])/3

    return newData