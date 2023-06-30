import numpy as np

def rebuildRtable(v, partition, beta, epsilon, rollAverages = True):

    betaRad = np.radians(beta)
    data = np.zeros((20,29))
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
        q = np.zeros(len(v))
        d = np.zeros(len(v))

    for i,j in np.ndindex(data.shape):
        group = int(partition[j,i]-1)

        A = a[group]*(np.sin(epsilon[j])**2)*(np.cos(betaRad[i])**2) \
          + b[group]*(np.sin(epsilon[j])**2)*(np.sin(betaRad[i])**2) \
          + c[group]*(np.cos(epsilon[j])**2) \
          + g[group]*np.sin(epsilon[j])*np.cos(epsilon[j])*np.cos(betaRad[i])

        #d != 0 makes us do much more math, so we don't do that if it's not needed
        if d[group] == 0:
            r_value_denom = A

            #convention
            if r_value_denom == 0:
                data[i,j] = 0
                continue

            r_value_numer = 2*p[group]*np.sin(epsilon[j])*np.cos(betaRad[i]) \
                          + 2*s[group]*np.cos(epsilon[j])
            
            data[i,j] = -r_value_numer/r_value_denom
            continue
        
        B = p[group]*np.sin(epsilon[j])*np.cos(betaRad[i]) \
          + s[group]*np.cos(betaRad[i]) \
          + q[group]*np.sin(epsilon[j])*np.sin(betaRad[i]) 
        
        Disc = B**2 - 4*A*d[group]

        data[i,j] = (-B + np.sqrt(Disc))/(2*A)
        if data[i,j] < 0:
            data[i,j] = 0

    return data.transpose()
        
        
        



    return 0