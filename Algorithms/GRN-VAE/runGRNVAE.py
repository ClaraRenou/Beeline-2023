import os
import argparse
import pandas as pd 
import numpy as np
import sys
import scanpy as sc
sys.path.append('grnvae') #to add a path to search for the requested module

from grnvae.runner import runGRNVAE, DEFAULT_GRNVAE_CONFIGS


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run scSGL algorithm.') 
    parser.add_argument('--expression_file', 
        help='Path to ExpressionData file')
    parser.add_argument('--ref_net_file', 
        help='Path to refNetwork file')
    parser.add_argument('--out_file',
        help='Path to output file')
    
    return parser

def parse_arguments():
    parser = get_parser()
    opts = parser.parse_args()

    return opts

def main(args):

    opts = parse_arguments()
    expression_df = sc.read(f'opts.expression_file').transpose  #to read gene expression file
    ref_net_df = pd.read_csv(opts.ref_net_file) #to read reference network file

    #Learn signed graph with the parameters
    vae, _ = runGRNVAE(
    expression_df, DEFAULT_GRNVAE_CONFIGS, ground_truth=none)
    A = vae.get_adj()
    
    A.to_csv(opts.out_file, index = False, sep = '\t')  #to write the output file

if __name__ == "__main__":
    main(sys.argv)
