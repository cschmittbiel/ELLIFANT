import numpy as np
import matplotlib.pyplot as plt
import sys

# I love colors
colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown', 'black', 'grey']

def plotRtable(data, partition, beta, epsilon, style='2D_side', name='r-table', savPath='../images/', store=False, show=True, coloredOT=True,verbose=False):
    
    # Ensure to write in big letters in the plot
    plt.rcParams['axes.labelsize'] = 20
    plt.rcParams['axes.titlesize'] = 20

    # Ensure to write in big letters in the markings of the axis
    plt.rcParams['xtick.labelsize'] = 15
    plt.rcParams['ytick.labelsize'] = 15

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
            if coloredOT:
                plt.scatter(dataAbs[partition==i], dataApp[partition==i], color=colors[i-1])
            else:
                plt.scatter(dataAbs[partition==i], dataApp[partition==i], color='black')

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
            if coloredOT:
                plt.scatter(dataAbs[partition==i], dataOrd[partition==i], color=colors[i-1])
                plt.scatter(dataAbs[partition==i], -dataOrd[partition==i], color=colors[i-1])
            else:
                plt.scatter(dataAbs[partition==i], dataOrd[partition==i], color='black')
                plt.scatter(dataAbs[partition==i], -dataOrd[partition==i], color='black')

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
            if coloredOT:
                ax.scatter(dataAbs[partition==i], dataOrd[partition==i], dataApp[partition==i], color=colors[i-1])
                ax.scatter(dataAbs[partition==i], -dataOrd[partition==i], dataApp[partition==i], color=colors[i-1])
            else:
                ax.scatter(dataAbs[partition==i], dataOrd[partition==i], dataApp[partition==i], color='black')
                ax.scatter(dataAbs[partition==i], -dataOrd[partition==i], dataApp[partition==i], color='black')

    elif style.startswith("q"):
        plt.close()
        style = style[1:]
        data = RtoQ(data, epsilon)
        if style == '2D_side':
            plotRtable(data, partition, beta, epsilon, style='2D_side', name=name, savPath=savPath, store=store, show=show, verbose=verbose)
            return 
        elif style == '2D_top':
            plotRtable(data, partition, beta, epsilon, style='2D_top', name=name, savPath=savPath, store=store, show=show, verbose=verbose)
            return
        elif style == '3D':
            plotRtable(data, partition, beta, epsilon, style='3D', name=name, savPath=savPath, store=store, show=show, verbose=verbose)
            return
        else:
            print("The style given is not valid.")
            sys.exit(1)   

    else:
        print("The style given is not valid.")
        sys.exit(1)

    if store:
        plt.savefig(savPath+name+'_'+style+'.png')
    if show:
        plt.show()
    plt.close()

#Compare plots
def plotRtableCompare(data1, data2, partition, beta, epsilon, style='2D_side', name='r-table', savPath='../images/', store=False, show=True, verbose=False):

    # Ensure to write in big letters in the plot
    plt.rcParams['axes.labelsize'] = 20

    if verbose:
        print('Plotting the comparison of the r-table of '+name)

    if style.startswith("q"):
        print("q styles are not available for comparison plots.")

    plt.figure(figsize=(12,9))
    data1.transpose()
    data2.transpose()

    if partition.shape != (29,20):
        print('The partition array is not the right size')
        sys.exit(1)

    EpsiTable = np.repeat(epsilon,20).reshape(29,20)
    BetaTable = np.repeat(beta*np.pi/180,29).reshape(20,29).transpose()

    data1Abs = data1 * np.sin(EpsiTable) * np.cos(BetaTable)
    data1Ord = data1 * np.sin(EpsiTable) * np.sin(BetaTable)
    data1App = data1 * np.cos(EpsiTable)

    data2Abs = data2 * np.sin(EpsiTable) * np.cos(BetaTable)
    data2Ord = data2 * np.sin(EpsiTable) * np.sin(BetaTable)
    data2App = data2 * np.cos(EpsiTable)

    if style == '2D_side':
        plt.title('2D side comparison of the photometric solid of '+ name)
        plt.xlabel('r sin(epsilon) cos(beta)')
        plt.ylabel('r cos(epsilon)')

        #connect the dots along epsilon and beta with lines
        plt.plot(data1Abs, data1App, color='black', linewidth=0.5)
        plt.plot(data1Abs.transpose(), data1App.transpose(), color='black', linewidth=0.5)

        #scatter the dots of data1 in black
        plt.scatter(data1Abs, data1App, color='black')

        #plot the dots of data2 with the right colors (in partitions)
        for i in range(10):
            plt.scatter(data2Abs[partition==i], data2App[partition==i], color=colors[i-1])

    elif style == '2D_top':
        plt.title('2D top comparison of the photometric solid of '+ name)
        plt.xlabel('r sin(epsilon) cos(beta)')
        plt.ylabel('r sin(epsilon) sin(beta)')

        #connect the dots along epsilon and beta with lines
        plt.plot(data1Abs, data1Ord, color='black', linewidth=0.5)
        plt.plot(data1Abs, -data1Ord, color='black', linewidth=0.5)

        #scatter the dots of data1 in black
        plt.scatter(data1Abs, data1Ord, color='black')
        plt.scatter(data1Abs, -data1Ord, color='black')

        #plot the dots of data2 with the right colors (in partitions)
        for i in range(10):
            plt.scatter(data2Abs[partition==i], data2Ord[partition==i], color=colors[i-1])
            plt.scatter(data2Abs[partition==i], -data2Ord[partition==i], color=colors[i-1])

    elif style == '3D':
        plt.title('3D comparison of the photometric solid of '+ name)
        ax = plt.axes(projection='3d')
        ax.set_xlabel('r sin(epsilon) cos(beta)')
        ax.set_ylabel('r sin(epsilon) sin(beta)')
        ax.set_zlabel('r cos(epsilon)')

        #connect the dots along epsilon and beta with lines
        for i in range(29):
            ax.plot(data1Abs[i,:], data1Ord[i,:], data1App[i,:], color='black', linewidth=0.5)
            ax.plot(data1Abs[i,:], -data1Ord[i,:], data1App[i,:], color='black', linewidth=0.5)
        for i in range(20):
            ax.plot(data1Abs[:,i], data1Ord[:,i], data1App[:,i], color='black', linewidth=0.5)
            ax.plot(data1Abs[:,i], -data1Ord[:,i], data1App[:,i], color='black', linewidth=0.5)

        #plot the dots of data1 in black
        ax.scatter(data1Abs, data1Ord, data1App, color='black')
        ax.scatter(data1Abs, -data1Ord, data1App, color='black')

        #plot the dots of data2 with the right colors (in partitions)
        for i in range(10):
            ax.scatter(data2Abs[partition==i], data2Ord[partition==i], data2App[partition==i], color=colors[i-1])
            ax.scatter(data2Abs[partition==i], -data2Ord[partition==i], data2App[partition==i], color=colors[i-1])

    else:
        print("The style given is not valid.")
        sys.exit(1)

    if store:
        plt.savefig(savPath+name+'_'+style+'.png')
    if show:
        plt.show()
    plt.close()

    

def RtoQ(r_table, epsilon):
    """
    This function transforms the r-table into a q-table.
    The q-table is the same as the r-table but the values are divided by cos(epsilon).
    """
    epsilon = np.repeat(epsilon,20).reshape(29,20)
    q_table = r_table / (np.cos(epsilon)**3) / 10e4
    return q_table