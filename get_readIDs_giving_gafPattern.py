import pandas as pd
from Bio import SeqIO
import argparse
import numpy as np

parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Given a path_matching pattern, get reads and subgaf for it")
parser.add_argument("-g", help= "-g: gaf file output of Graphaligner", required = "True")
parser.add_argument("-p", help= "-p: pattern to search on patch_matching field", required = "True")
args = parser.parse_args()
m_names=('queryname','query_length','query_start','query_end','strand', 'path_matching','path_length','path_start','path_end', 'residue_matches', 'alignm_length', 'mapping_qual', 'other1', 
'other2', 'other3', 'identity', 'other4')
mytypes={'mapping_qual':'Int64'}
df4=pd.read_csv(args.g, names=m_names,  sep="\t", dtype=mytypes)
df5=df4[df4['path_matching' ]== args.p]
df5.to_csv("{}_filtered.gaf".format(args.p), index=False, sep="\t")
df5[['queryname']].to_csv("{}_filtered.reads.id".format(args.p), index=False, sep="\t", header=None)
