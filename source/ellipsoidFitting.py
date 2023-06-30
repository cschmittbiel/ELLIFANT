import numpy as np

def ellipsoidFitting(data, partition, beta, epsilon, freeConstant =False, freeY = False):

    nEllipsoids = len(np.unique(partition))

    dataGroups = [[] for i in range(nEllipsoids)]
    dataBetas = [[] for i in range(nEllipsoids)]
    dataEpsilons = [[] for i in range(nEllipsoids)]

    #each group is a list of the data points in that group, and the corresponding beta and tan epsilon (580 loop)
    for i, j in np.ndindex(partition.shape):
        dataGroups[int(partition[i,j]-1)].append(data[i,j])
        dataBetas[int(partition[i,j]-1)].append(beta[j])
        dataEpsilons[int(partition[i,j]-1)].append(epsilon[i])

    #by default, we have 5 parameters per ellipsoid (see the paper), but we can add more,
    #for example to allow for a free y parameter or to allow for ellipsoids that pass through the origin
    v = np.zeros((nEllipsoids, 5 + freeY + freeConstant))

    for index, group in enumerate(dataGroups):
        
        N = len(group)

        #the data points in this group
        betas = np.array(dataBetas[index])
        epsilons = np.array(dataEpsilons[index])

        #fill the points vector    
        X = group * np.sin(epsilons) * np.cos(np.radians(betas))
        Y = group * np.sin(epsilons) * np.sin(np.radians(betas))
        Z = group * np.cos(epsilons)

        norms = X**2 + Y**2 + Z**2

        #the matrix D
        D = np.zeros((N, 5 + freeY + freeConstant))

        #fill the matrix D following the paper
        D[:,0] = X**2 + Y**2 - 2*Z**2
        D[:,1] = X**2 + Z**2 - 2*Y**2
        D[:,2] = 2*X*Z
        D[:,3] = 2*X
        D[:,4] = 2*Z

        #adding more parameters to the ellipsoid
        if freeY:
            D[:,5] = 2*Y
            if freeConstant:
                D[:,6] = 1
        elif freeConstant:
            D[:,5] = 1

        #the matrices for the least squares solution
        DTD = np.dot(D.T, D)
        DTnorms = np.dot(D.T, norms)

        #least squares solution
        v[index] = np.linalg.lstsq(DTD, DTnorms, rcond = None)[0]

    print(v)

    return v

