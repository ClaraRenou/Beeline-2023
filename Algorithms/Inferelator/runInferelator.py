from optparse import OptionParser
import os
import sys
import pandas as pd

from inferelator import utils
from inferelator import inferelator_workflow
from inferelator.preprocessing import single_cell
from inferelator.distributed.inferelator_mp import MPControl


def parseArgs(args):
    parser = OptionParser()

    parser.add_option('', '--regression', type = 'str',
                      help='Type of regression to run')
    
    parser.add_option('', '--workflow', type = 'str',
                      help='Type of workflow to run')

    parser.add_option('', '--inDir', type='str',
                      help='Path to input directory')
    
    parser.add_option('', '--outDir', type='str',
                      help='Path to output directory')
    
    parser.add_option('', '--inFile', type='str',
                      help='Path to input tab-separated expression SamplesxGenes file')

    parser.add_option('', '--outFile', type = 'str',
                      help='File where the output network is stored')
    
    parser.add_option('', '--tf_list', type = 'str',
                      help='File with TF names')
    
    parser.add_option('', '--ref_network', type = 'str',
                      help='File with reference network')

    (opts, args) = parser.parse_args(args)

    return opts, args

def main(args):
    opts, args = parseArgs(args)
    inDF = pd.read_csv(opts.inFile, sep = '\t', index_col = 0, header = 0)
    
    if __name__ == '__main__':
    MPControl.set_multiprocess_engine("multiprocessing")
    MPControl.client.processes = 4
    MPControl.connect()
    
    worker = workflow.inferelator_workflow(regression=opts.regression, workflow=opts.workflow)
    
    worker.set_file_paths(input_dir=opts.inDir,
                      output_dir=opts.outDir,
                      tf_names_file=opts.tf_list',
                      #priors_file='new_prior.tsv.gz',
                      gold_standard_file=opts.ref_network)
    worker.set_expression_file(tsv=opts.inFile)
    
    worker.run()

                        
if __name__ == "__main__":
    main(sys.argv)
