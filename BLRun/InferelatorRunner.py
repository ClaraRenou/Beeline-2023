import os
import pandas as pd
from pathlib import Path
import numpy as np

def generateInputs(RunnerObj):
    '''
    Function to generate desired inputs for Inferelator.
    If the folder/files under RunnerObj.datadir exist, 
    this function will not do anything.

    :param RunnerObj: An instance of the :class:`BLRun`
    '''
    if not RunnerObj.inputDir.joinpath("Inferelator").exists():
        print("Input folder for Inferelator does not exist, creating input folder...")
        RunnerObj.inputDir.joinpath("Inferelator").mkdir(exist_ok = False)
        
    if not RunnerObj.inputDir.joinpath("Inferelator/ExpressionData.csv").exists():
        # input data
        ExpressionData = pd.read_csv(RunnerObj.inputDir.joinpath(RunnerObj.exprData),
                                     header = 0, index_col = 0)

        # Write gene expression data in Inferelator folder 
        ExpressionData.to_csv(RunnerObj.inputDir.joinpath("Inferelator/ExpressionData.csv"),
                             sep = ',', header  = True)

    if not RunnerObj.inputDir.joinpath("Inferelator/refNetwork.csv").exists():
        refNetworkData = pd.read_csv(RunnerObj.inputDir.joinpath(RunnerObj.trueEdges),
                                     header = 0, index_col = 0)

	  # Write reference network data in Inferelator folder 
        refNetworkData.to_csv(RunnerObj.inputDir.joinpath("Inferelator/refNetwork.csv"),
                             sep = ',', header  = True)    

    
def run(RunnerObj):
    '''
    Function to run Inferelator algorithm

    :param RunnerObj: An instance of the :class:`BLRun`
    '''
    inputPath = "data" + str(RunnerObj.inputDir).split(str(Path.cwd()))[1] + \
                    "/Inferelator/ExpressionData.csv"
    tf_list = "data" + "TF/human-tfs.csv
    # make output dirs if they do not exist:
    outDir = "outputs/"+str(RunnerObj.inputDir).split("inputs/")[1]+"/Inferelator/"
    os.makedirs(outDir, exist_ok = True)
    
    outPath = "data/" +  str(outDir) + 'outFile.txt'
    cmdToRun = ' '.join(['docker run --rm -v', str(Path.cwd())+':/data/ --expose=41269', 
                         'inferelator:base /bin/sh -c \"time -v -o', "data/" + str(outDir) + 'time.txt', 'python runInferelator.py --regression=bbsr',
                         '--workflow=single-cell','--inDir='+str(RunnerObj.inputDir),'--outDir='+outDir,'--inFile='+inputPath, '--tf_list='+tf_list, '--ref_network='+str(RunnerObj.trueEdges), '\"'])

    print(cmdToRun)
    os.system(cmdToRun)



def parseOutput(RunnerObj):
    '''
    Function to parse outputs from Inferelator.

    :param RunnerObj: An instance of the :class:`BLRun`
    '''
    # Quit if output directory does not exist
    outDir = "outputs/"+str(RunnerObj.inputDir).split("inputs/")[1]+"/Inferelator/"

        
    # Read output
    OutDF = pd.read_csv(outDir+'outFile.txt', sep = '\t', header = 0)
    
    if not Path(outDir+'outFile.txt').exists():
        print(outDir+'outFile.txt'+'does not exist, skipping...')
        return
    
    outFile = open(outDir + 'rankedEdges.csv','w')
    outFile.write('Gene1'+'\t'+'Gene2'+'\t'+'EdgeWeight'+'\n')

    for idx, row in OutDF.iterrows():
        outFile.write('\t'.join([row['TF'],row['target'],str(row['importance'])])+'\n')
    outFile.close()
