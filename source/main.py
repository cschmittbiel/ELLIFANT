import numpy as np
import pandas as pd
import time
import glob
import sys
import os

from ellipsoidFitting import ellipsoidFitting
from rebuildRtable import rebuildRtable
from commandArgParser import CommandLineArgs, checkCommandLineArguments
from cuttingTablesUp import randomPartition, stopsToPartition
from plotRtables import plotRtable

def main():
    try:

        # The standard CIE angles for beta and tan epsilon :
        beta = np.array([0, 2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180])    
        tanEpsilon = np.array([0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12])
        epsilon = np.arctan(tanEpsilon)

        # ----------------------------------
        # ----- COMMAND LINE ARGUMENTS -----
        # ----------------------------------
        
        #get the command line arguments
        cmd_args = CommandLineArgs(sys.argv)
        cmd_args.parse_args()

        #extract the arguments
        folderPath = cmd_args.folderPath
        patron = cmd_args.patron
        sheets = cmd_args.sheets
        ignore = cmd_args.ignore

        saveFolder = cmd_args.saveFolder
        saveDataName = cmd_args.saveDataName
        saveImageFolder = cmd_args.saveImageFolder

        ellipsoidAdjusting = cmd_args.ellipsoidAdjusting
        betaGeneticAlgorithm = cmd_args.betaGeneticAlgorithm
        partitioningGeneticAlgorithm = cmd_args.partitioningGeneticAlgorithm

        showImages = cmd_args.showImages
        saveImages = cmd_args.saveImages
        saveData = cmd_args.saveData

        plotStyle = cmd_args.plotStyle
        plotTypes = cmd_args.plotTypes

        stops = cmd_args.stops
    
        verbose = cmd_args.verbose

        folderPath = '../data/' + folderPath

        ignore = ignore.split(",")
        sheets = sheets.split(",")
        
        stops = stops.split(",")
        stops = [int(stop) for stop in stops]

        checkCommandLineArguments(folderPath, saveFolder, saveImageFolder, saveDataName, \
                                  plotTypes, ellipsoidAdjusting, betaGeneticAlgorithm, partitioningGeneticAlgorithm, \
                                  stops, verbose)
        
        # ----------------------------------
        # ---------- LOAD THE DATA ---------
        # ----------------------------------

        if verbose:
            print("Searching for data in the folder " + folderPath + "...")
        
        #get the list of files in the folder that match the patron
        fileList = glob.glob(os.path.join(folderPath, patron))

        # If there are no files, tell the user and exit
        if len(fileList) == 0:
            print('No files found in %s that match %s' % (folderPath, patron))
            return 0

        if verbose:
            print("Found " + str(len(fileList)) + " file(s).\n")

        #load the data from the files

        r_tables = []
        r_tables_names = []

        for filePath in fileList:
            with pd.ExcelFile(filePath) as file:
                for i, sheet in enumerate(file.sheet_names):
                    
                    #Feuil1 is the default name of the first sheet in an excel file, we don't want to use it for most databases
                    if file.sheet_names[i] == 'Feuil1'or file.sheet_names[i] in ignore:
                        if verbose:
                            print('Sheet %s in file %s is ignored, skipping' % (file.sheet_names[i], filePath))
                        continue

                    #if the user specified the sheets to use, we only want to use those
                    if sheets != ["None"] and file.sheet_names[i] not in sheets:
                        if verbose:
                            print('Sheet %s in file %s is not in the list of sheets to use, skipping' % (file.sheet_names[i], filePath))
                            print('looking for sheets: ' + str(sheets))
                        continue
                        
                    # read the data from the excel file and store it in a dataframe
                    r_tb = pd.read_excel(filePath, sheet_name=sheet, header=None)

                    # resize the r_tb to be 20*29
                    r_tb = r_tb.iloc[0:29, 0:20]

                    # if the dataframe is smaller than 20*29, return an error and exit
                    if r_tb.shape[0] < 29 or r_tb.shape[1] < 20:
                        continue
                    
                    # if there are any Nan values, retrun an error and exit
                    if r_tb.isnull().values.any():
                        print('Error: File %s contains NaN values in sheet %s, this is not an r-table, call it \
                              \'Feuil1\' for it to be skipped or correct the error' % (filePath, sheet.title))
                        continue

                    # this test is to remove the first column and the first row if B1==0, no r-table should have B1==0, so this means that the r-table starts at B2
                    if r_tb.iloc[0, 1] == 0:
                        print("This format is no longer supported, please use the new format, bare r-tables that should start at A1 adn end at T29 in excel file.")
                        sys.exit(1)

                    # add the r-table to the list
                    r_tables.append(r_tb)
                    r_tables_names.append(sheet)

        # if there are no r-tables, return the info to the user and exit
        if len(r_tables) == 0:
            print('No r-tables found in %s that match %s' % (folderPath, patron))
            return 0
        
        if verbose:
            print("Done, data loaded successfully, found " + str(len(r_tables)) + " r-table(s).\n")
        
        # ----------------------------------
        # ---------- PROCESS DATA ----------
        # ----------------------------------

        #convert the r_table from lists to numpy arrays
        r_tables = [r_table.to_numpy() for r_table in r_tables]

        #convert the stops to a partition
        partition = randomPartition(3)

        if verbose:
            if ellipsoidAdjusting:
                print("Starting ellipsoid adjusting algorithm using stops " + str(stops) + "...")
            elif betaGeneticAlgorithm:
                print("Starting beta genetic algorithm...")
            elif partitioningGeneticAlgorithm:
                print("Starting partitioning genetic algorithm...")

        #plot Original r-tables if needed
        if 'o' in plotTypes:
            #plot the original r-tables
            for i, r_table in enumerate(r_tables):
                plotRtable(r_table, partition, beta, epsilon, name= r_tables_names[i], \
                            store=saveImages, show=showImages, style=plotStyle, verbose=verbose)

        # ELLIPSOID ADJUSTING ALGORITHM

        if ellipsoidAdjusting:
            #run the ellipsoid adjusting algorithm
            for i, r_table in enumerate(r_tables):
                v = ellipsoidFitting(r_table, partition, beta, epsilon, freeConstant=True)
                r_tb = rebuildRtable(v, partition, beta, epsilon)
                plotRtable(r_tb, partition, beta, epsilon, name= r_tables_names[i], \
                        store=saveImages, show=showImages, style=plotStyle, verbose=verbose)
                
    except ValueError:
        print("An error occured.")
        sys.exit(1)

if __name__ == "__main__":
    main()