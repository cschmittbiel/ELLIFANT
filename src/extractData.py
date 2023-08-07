import numpy as np

#This script contains the functions to extract the standard coefficients from the R-table S1, Q0 and Qd
beta = np.array([0, 2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180])
tanEpsilon = np.array([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12])
sinEpsilon = np.sin(np.arctan(tanEpsilon))
Epsilon = np.arctan(tanEpsilon)

def S1(r_tb):
    return r_tb[8,0] / r_tb[0,0]

def mean(r_tb):
    return np.sum(np.sum(r_tb)) / 580

def Q0(r_tb, weights):
    #create a matrix where everyline is tanEpsilon, with 20 lines
    tanEpsilonMatrix = np.repeat(tanEpsilon, 20).reshape(29,20)

    Q0m = np.multiply(r_tb, tanEpsilonMatrix)
    Q0m = np.multiply(Q0m, weights)
    Q0 = np.sum(np.sum(Q0m))
    Q0 /= 9.936e7
    return Q0

def Qd(r_tb, weights):
    #create a matrix where everyline is sinEpsilon, with 20 lines
    sinEpsilonMatrix = np.repeat(sinEpsilon, 20).reshape(29,20)

    QDm = np.multiply(r_tb, sinEpsilonMatrix)
    QDm = np.multiply(QDm, weights)
    QD = np.sum(np.sum(QDm))
    QD /= 6.097e7
    return QD

# This is a translation of some matlab code from Vincent Boucher to python :)
def Q0_Trapezes(r_tb):
    #load the weights from file and get the values for q
    q1 = r_tb[:, 1:] / (np.cos(Epsilon[:, np.newaxis]) ** 3) / 1e4
    q2 = r_tb[:, :-1] / (np.cos(Epsilon[:, np.newaxis]) ** 3) / 1e4
    
    # Calculate the integral using the trapeze method
    N = np.sum(np.sin(Epsilon[:, np.newaxis]) * (q1 + q2) / 2 * np.diff(beta), axis=1)
    
    # Calculate the integral of the denominator 
    omega1 = (r_tb[:, 1:] != 0) * 1
    omega2 = (r_tb[:, :-1] != 0) * 1

    # Compute the sum over the angles for the denominator
    D = np.sum(np.sin(Epsilon[:, np.newaxis]) * (omega1 + omega2) / 2 * np.diff(beta), axis=1)
    
    # final sum along the angles
    N2 = np.sum((N[1:] + N[:-1]) / 2 * np.diff(Epsilon))
    D2 = np.sum((D[1:] + D[:-1]) / 2 * np.diff(Epsilon))

    #return the final result
    Q0 = N2 / D2
    return Q0

def RMSE(original_Rtable, adjusted_Rtable):
    """
    This function calculates the RMSE between the original table and the adjusted one
    """
    # we first check that the two tables have the same dimensions
    if original_Rtable.shape != adjusted_Rtable.shape:
        print('The two tables must have the same dimensions')
        exit()

    # we calculate the RMSE
    RMSE = np.sum((original_Rtable - adjusted_Rtable)**2, axis = 0)
    RMSE = np.sum(RMSE, axis = 0)
    RMSE = np.sqrt(RMSE/(original_Rtable.shape[0]*original_Rtable.shape[1]))

    return RMSE

def deltaQ0S1(original_Rtable, adjusted_Rtable):
    Q = (Q0_Trapezes(original_Rtable) - Q0_Trapezes(adjusted_Rtable)) ** 2
    S = (S1(original_Rtable) - S1(adjusted_Rtable)) ** 2
    return np.sqrt((np.pi ** 2 * Q + S) / 2)

def deltaR(original_Rtable, adjusted_Rtable):
    err = RMSE(original_Rtable, adjusted_Rtable)
    meanO = mean(original_Rtable)
    meanA = mean(adjusted_Rtable)
    return 2 * err / (meanO + meanA)

def Entropy(r_table):
    """
    This function calculates the entropy of the R-table
    which is relevant, because the entropy is a measure of the
    uniformity of the R-table the smaller the entropy, the more
    compressable the R-table is.
    """

    #carefull r-tables have 0 in them, so we need to add a small value to avoid log(0)
    #convert r-table to float 
    r_table = r_table.astype(float)
    r_table += 1e-10

    #flatten the r-table
    r_table = r_table.flatten()

    #calculate the probability of each element by dividing the count of each individual value by the total number of elements
    values, counts = np.unique(r_table, return_counts=True)
    probabilities = counts / len(r_table)
    entropy = -np.sum(probabilities * np.log2(probabilities))

    return entropy

def Smoothness(r_table):
    """
    This function calculates a smoothness of the R-table
    """

    # we calculate the smoothness
    smoothness = np.sum(np.abs(r_table[1:,:] - r_table[:-1,:]), axis = 0)
    smoothness = np.sum(smoothness, axis = 0)

    # normalize the smoothness
    smoothness /= np.sum(np.sum(r_table, axis = 0), axis = 0)
    smoothness /= r_table.shape[0] - 1

    return smoothness