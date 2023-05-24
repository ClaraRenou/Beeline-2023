import os
import pandas as pd
from pathlib import Path
import numpy as np

def generateInputs(RunnerObj):
    '''
    Function to generate desired inputs for GRN-VAE.
    If the folder/files under RunnerObj.datadir exist, 
    this function will not do anything.
    :param RunnerObj: An instance of the :class:`BLRun`
    '''
    if not RunnerObj.inputDir.joinpath("GRNVAE").exists():
        print("Input folder for GRNVAE does not exist, creating input folder...")
        RunnerObj.inputDir.joinpath("GRNVAE").mkdir(exist_ok = False)
        
    if not RunnerObj.inputDir.joinpath("GRNVAE/ExpressionData.csv").exists():
        # input data
        ExpressionData = pd.read_csv(RunnerObj.inputDir.joinpath(RunnerObj.exprData),
                                     header = 0, index_col = 0)

        # Write gene expression data in GRNVAE folder 
        ExpressionData.to_csv(RunnerObj.inputDir.joinpath("GRNVAE/ExpressionData.csv"),
                             sep = ',', header  = True)

    if not RunnerObj.inputDir.joinpath("GRNVAE/refNetwork.csv").exists():
        refNetworkData = pd.read_csv(RunnerObj.inputDir.joinpath(RunnerObj.trueEdges),
                                     header = 0, index_col = 0)

	  # Write reference network data in GRNVAE folder 
        refNetworkData.to_csv(RunnerObj.inputDir.joinpath("GRNVAE/refNetwork.csv"),
                             sep = ',', header  = True)    

    
def run(RunnerObj):
    '''
    Function to run GRNVAE algorithm
    :param RunnerObj: An instance of the :class:`BLRun`
    '''
    inputPath = "data" + str(RunnerObj.inputDir).split(str(Path.cwd()))[1] + \
                    "/GRNVAE/ExpressionData.csv"

    # make output dirs if they do not exist:
    outDir = "outputs/"+str(RunnerObj.inputDir).split("inputs/")[1]+"/GRNVAE/"
    os.makedirs(outDir, exist_ok = True)
    
    outPath = "data/" +  str(outDir) + 'outFile.txt'
    cmdToRun = ' '.join(['docker run --rm -v', str(Path.cwd())+':/data/ --expose=41269', 
                         'grnvae:base /bin/sh -c \"time -v -o', "data/" + str(outDir) + 'time.txt', 'python runGRNVAE.py',
                         '--inFile='+inputPath, '--outFile='+outPath, '\"'])

    print(cmdToRun)
    os.system(cmdToRun)


def parseOutput(RunnerObj):
    '''
    Function to parse outputs from GRN-VAE.
    :param RunnerObj: An instance of the :class:`BLRun`
    '''
    # Quit if output directory does not exist
    outDir = "outputs/"+str(RunnerObj.inputDir).split("inputs/")[1]+"/GRNVAE/"

        
    # Read output file
    OutDF = pd.read_csv(outDir+'outFile.txt', sep = '\t', header = 0)

    OutDF.sort_values(by="EdgeWeight", ascending=False, inplace=True)
    
    if not Path(outDir+'outFile.txt').exists():
        print(outDir+'outFile.txt'+'does not exist, skipping...')
        return
    
    # Formats the outFile into a ranked edgelist comma-separated file
    outFile = open(outDir + 'rankedEdges.csv','w')
    outFile.write('Gene1'+'\t'+'Gene2'+'\t'+'EdgeWeight'+'\n')

    for idx, row in OutDF.iterrows():
        outFile.write('\t'.join([row['Gene1'],row['Gene2'],str(row['EdgeWeight'])])+'\n')
    outFile.close()
