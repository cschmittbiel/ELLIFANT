import numpy as np
import matplotlib.pyplot as plt
import sys

# I love colors
colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown', 'black', 'grey']

def plotRtable(data, partition, beta, epsilon, style='2D_side', name='r-table', savPath='../images/', store=False, show=True, verbose=False):

    if verbose:
        print('Plotting the r-table of '+name)

    plt.figure(figsize=(12,9))
    data.transpose()

    if partition.shape != (29,20):
        print('The partition array is not the right size')
        sys.exit(1)

    EpsiTable = np.repeat(epsilon,20).reshape(29,20)
    BetaTable = np.repeat(beta*np.pi/180,29).reshape(20,29).transpose()

    dataAbs = data * np.sin(EpsiTable) * np.cos(BetaTable)
    dataOrd = data * np.sin(EpsiTable) * np.sin(BetaTable)
    dataApp = data * np.cos(EpsiTable)
    
    if style == '2D_side':
        plt.title('2D side view of the photometric solid of '+ name)
        plt.xlabel('r sin(epsilon) cos(beta)')
        plt.ylabel('r cos(epsilon)')

        #connect the dots along epsilon and beta with lines
        plt.plot(dataAbs, dataApp, color='black', linewidth=0.5)
        plt.plot(dataAbs.transpose(), dataApp.transpose(), color='black', linewidth=0.5)

        #plot the dots with the right colors (in partitions)
        for i in range(10):
            plt.scatter(dataAbs[partition==i], dataApp[partition==i], color=colors[i-1])

    elif style == '2D_top':
        plt.title('2D top view of the photometric solid of '+ name)
        plt.xlabel('r sin(epsilon) cos(beta)')
        plt.ylabel('r sin(epsilon) sin(beta)')

        #connect the dots along epsilon and beta with lines
        plt.plot(dataAbs, dataOrd, color='black', linewidth=0.5)
        plt.plot(dataAbs, -dataOrd, color='black', linewidth=0.5)
        plt.plot(dataAbs.transpose(), dataOrd.transpose(), color='black', linewidth=0.5)
        plt.plot(dataAbs.transpose(), -dataOrd.transpose(), color='black', linewidth=0.5)

        #plot the dots with the right colors (in partitions)
        for i in range(10):
            plt.scatter(dataAbs[partition==i], dataOrd[partition==i], color=colors[i-1])
            plt.scatter(dataAbs[partition==i], -dataOrd[partition==i], color=colors[i-1])

    elif style == '3D':
        plt.title('3D view of the photometric solid of '+ name)
        ax = plt.axes(projection='3d')
        ax.set_xlabel('r sin(epsilon) cos(beta)')
        ax.set_ylabel('r sin(epsilon) sin(beta)')
        ax.set_zlabel('r cos(epsilon)')

        #connect the dots along epsilon and beta with lines
        for i in range(29):
            ax.plot(dataAbs[i,:], dataOrd[i,:], dataApp[i,:], color='black', linewidth=0.5)
            ax.plot(dataAbs[i,:], -dataOrd[i,:], dataApp[i,:], color='black', linewidth=0.5)
        for i in range(20):
            ax.plot(dataAbs[:,i], dataOrd[:,i], dataApp[:,i], color='black', linewidth=0.5)
            ax.plot(dataAbs[:,i], -dataOrd[:,i], dataApp[:,i], color='black', linewidth=0.5)

        #plot the dots with the right colors (in partitions)
        for i in range(10):
            ax.scatter(dataAbs[partition==i], dataOrd[partition==i], dataApp[partition==i], color=colors[i-1])
            ax.scatter(dataAbs[partition==i], -dataOrd[partition==i], dataApp[partition==i], color=colors[i-1])

    else:
        print("The style given is not valid.")
        sys.exit(1)

    if store:
        plt.savefig(savPath+name+'_'+style+'.png')
    if show:
        plt.show()
    plt.close()