

#Marcela Uliano-Silva, Wellcome Sanger Institute


import argparse
import pandas as pd
from Bio import SeqIO

parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Concatenate the fasta sequences into a file giving a text file with the path to each fasta per line") 
parser.add_argument("-i", help= "-i: list of fasta paths, one per line", required = "True")
parser.add_argument("-o", help= "-o: concatenated fasta sequence", required = "True")

args = parser.parse_args()

oi=('path', 'oi')
paths = pd.read_csv(args.i, names=oi)

paths_list = paths["path"].values.tolist()

with open(args.o, 'w') as outfile:
    for f in paths_list:
        with open(f) as infile:
            outfile.write(infile.read())
