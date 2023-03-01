import pandas as pd
from Bio import SeqIO
import argparse
import numpy as np
parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Get partial gfa from Graphaligner output given a pattern on patch_matching Field")
parser.add_argument("-g", help= "-g: gaf file output of Graphaligner", required = "True")
parser.add_argument("-l", help= "-l: list of patterns to search on patch_matching field", required = "True")
parser.add_argument("-q", help= "-q: aligment quality. Default 20", default=20)
args = parser.parse_args()
terms = []
with open(args.l) as f:
	for l in f:
		terms.append(l.rstrip("\n"))
m_names=('queryname','query_length','query_start','query_end','strand', 'path_matching','path_length','path_start','path_end', 'residue_matches', 'alignm_length', 'mapping_qual', 'other1', 'other2', 'other3', 'identity', 'other4')
mytypes={'mapping_qual':'Int64'}
df4=pd.read_csv(args.g, names=m_names,  sep="\t", dtype=mytypes)
df5 = df4[df4['path_matching'].str.contains('|'.join(terms), na=False)]
df6 = df5[df5['mapping_qual'] >= int(args.q)]
df5.to_csv("{}filtered1.gaf".format(args.l), index=False, header=None, sep="\t")
df7=df6[df6['path_matching'].str.match(r"([><]\d+){2,}")]
df7.sort_values('path_matching').to_csv("{}filtered2.gaf".format(args.g), index=False, header=None, sep="\t")
df8 = df7[['queryname','query_length','query_start','query_end','strand', 'path_matching','path_length','path_start','path_end', 'residue_matches', 'alignm_length', 'mapping_qual', 'identity']].sort_values('path_matching')
df8.to_csv("{}filtered3.gaf".format(args.l), index=False, sep="\t")
df9 = df8['path_matching'].value_counts().rename_axis('unique_values').reset_index(name='counts')
df9.to_csv("{}filtered3.cov".format(args.l), index=False, sep="\t")
