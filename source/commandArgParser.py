import argparse
import sys, os

class CommandLineArgs:

    def __init__(self, args):
        self.args = args

        #Location of the data sheet(s)
        self.folderPath = None
        self.patron = None
        self.sheets = None
        self.ignore = None

        #Where to save the results
        self.saveFolder = None
        self.saveDataName = None
        self.saveImageFolder = None
        
        #what to do with the data (these are mutually exclusive)
        self.ellipsoidAdjusting = None
        self.betaGeneticAlgorithm = None
        self.partitioningGeneticAlgorithm = None

        #Booleans for the different options
        self.showImages = None
        self.saveImages = None
        self.saveData = None

        #related to images
        self.plotStyle = None
        self.plotTypes = None

        #other
        self.stops = None
        self.verbose = None

    def parse_args(self):
    
        parser = argparse.ArgumentParser(description="This program will take a folder of data and process it as specified by the user.")
        parser.add_argument('-fp','--folderPath', required=False, type=str, default=".", help="The path to the folder containing the data sheets, starting in the adjacent data folder.")
        parser.add_argument('-p',"--patron", required=False, type=str, default="*.xlsx", help="The patron the files names should fit to be selected.")
        parser.add_argument('-s',"--sheets", required=False, type=str, default="None", help="By default, all sheets that are recognized as r-tables will be processed. \
                            If this argument is given, only these sheets will be processed. Example :  R1,R2,R3")
        parser.add_argument('-i', "--ignore", required=False, type=str, default="None", help="If this argument is given, sheets with these names will be ignored. Example : W1,W2,W3")

        parser.add_argument('-sf',"--saveFolder", required=False, type=str, default="../results", help="The path to the folder where the results should be saved, default is the adjacent folder 'results'.")
        parser.add_argument('-sdn',"--saveDataName", required=False, type=str, default="results", help="The name of the file where the results should be saved, without the extension.")
        parser.add_argument('-sif',"--saveImageFolder", required=False, type=str, default="../images", help="The path to the folder where the images should be saved, default is the adjacent folder 'images'.")

        parser.add_argument('-ea',"--ellipsoidAdjusting", required=False, action='store_true', default=None, help="If this argument is given, the ellipsoid adjusting algorithm will be run on the data once")
        parser.add_argument('-bga',"--betaGeneticAlgorithm", required=False, action='store_true', default=None, help="If this argument is given, the beta genetic algorithm will be run on the data once")
        parser.add_argument('-pga',"--partitioningGeneticAlgorithm", required=False, action='store_true', default=None, help="If this argument is given, the partitioning genetic algorithm will be run on the data once")

        parser.add_argument('-sh',"--showImages", required=False, action='store_true', help="If this argument is given, the images will be shown, may trigger a warning if there are too many")
        parser.add_argument('-si',"--saveImages", required=False, action='store_true', help="If this argument is given, the images will be saved in the folder specified by -sf")
        parser.add_argument('-sd',"--saveData", required=False, action='store_true', help="If this argument is given, the data will be saved in the file specified by -sdn")

        parser.add_argument('-ps',"--plotStyle", required=False, type=str, default="2D_side", choices=['2D_side','2D_top','3D'], help="The style of the plot, default is 2D_side, other options are 2D_top, 3D")
        parser.add_argument('-pt',"--plotTypes", required=False, type=str, default="", help="The types of plots to show, default is none, but input can 'o' (original table), 'r' (result), 'c' (comparison)")

        parser.add_argument('-st',"--stops", required=False, type=str, default='0,15,60,180', help="The stops for the ellipsoid adjusting algorithm, default is 0,15,60,180")

        parser.add_argument('-v',"--verbose", required=False, action='store_true', help="If this argument is given, the program will print more information")

        self.args = parser.parse_args()
        self.folderPath = self.args.folderPath
        self.patron = self.args.patron
        self.sheets = self.args.sheets
        self.ignore = self.args.ignore

        self.saveFolder = self.args.saveFolder
        self.saveDataName = self.args.saveDataName
        self.saveImageFolder = self.args.saveImageFolder

        self.ellipsoidAdjusting = self.args.ellipsoidAdjusting
        self.betaGeneticAlgorithm = self.args.betaGeneticAlgorithm
        self.partitioningGeneticAlgorithm = self.args.partitioningGeneticAlgorithm

        self.showImages = self.args.showImages
        self.saveImages = self.args.saveImages
        self.saveData = self.args.saveData

        self.plotStyle = self.args.plotStyle
        self.plotTypes = self.args.plotTypes

        self.stops = self.args.stops
        self.verbose = self.args.verbose

        return self.args
    
def checkCommandLineArguments(folderPath, saveFolder, saveImageFolder, saveDataName, \
                            plotTypes, ellipsoidAdjusting, betaGeneticAlgorithm, partitioningGeneticAlgorithm, \
                            stops, verbose):
    
    #check if the folder path is valid
    if not os.path.isdir(folderPath):
        print("The folder path given does not exist.")
        sys.exit(1)

    #check if the save folder is valid
    if not os.path.isdir(saveFolder):
        print("The save folder given does not exist.")
        sys.exit(1)

    #check if the save image folder is valid
    if not os.path.isdir(saveImageFolder):
        print("The save image folder given does not exist.")
        sys.exit(1)

    if verbose:
        print("\nCommand line arguments parsed successfully.")

    #check if the save data name is valid (either the extension is .xlsx or it is empty, 
    #in which case it will be added, anything else is invalid)
    if len(saveDataName.split(".")) == 1:
        saveDataName += ".xlsx"
    elif saveDataName.split(".")[-1] != "xlsx":
        print("The save data file name given is not valid, it must end with .xlsx or have no extension.")
        sys.exit(1)

    #check if the plot types are valid (any combination of o, r, c)
    if not all([i in ['o','r','c'] for i in plotTypes]):
        print("The plot types given are not valid.")
        sys.exit(1)

    #check if the user gave one of the three algorithms only
    if sum([ellipsoidAdjusting is not None, betaGeneticAlgorithm is not None, partitioningGeneticAlgorithm is not None]) != 1:
        print("You must give exactly one of the three algorithms, -ea, -bga or -pga.")
        sys.exit(1)

    #if the user specified stops, but didn't give the ellipsoid adjusting algorithm return an error
    if stops is not None and ellipsoidAdjusting is False:
        print("You can only give the stops for the ellipsoid adjusting algorithm.")
        sys.exit(1)
    
    #check if the stops vector is valid
    if stops[0] != 0:
        print('The first stop must be 0, found %d in vector : %s' % (stops[0], stops))
        exit()

    if stops[-1] != 180:
        print('The last stop must be 180, found %d in vector : %s' % (stops[-1], stops))
        exit()

    #check the stops vector is sorted
    for i in range(0, len(stops)-1):
        if stops[i] >= stops[i+1]:
            print('The stops vector must be in a strictly increasing order, found %d then %d in vector : %s' % (stops[i], stops[i+1], stops))
            exit()
        

    #ERRORS THAT DON'T STOP THE PROGRAM

    #if the user wants a model, set show and plot images to false, tell him if he wants verbose
    if betaGeneticAlgorithm is not None or partitioningGeneticAlgorithm is not None:
        showImages = False
        saveImages = False
        if verbose:
            print("You selected a model, so the images will not be shown or saved to avoid clutter.")