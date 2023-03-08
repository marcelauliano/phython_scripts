import pandas as pd
from Bio import SeqIO
import argparse
import numpy as np
parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Get partial gfa from Graphaligner output given a pattern on patch_matching Field")
parser.add_argument("-g", help= "-g: gaf file output of Graphaligner", required = "True")
parser.add_argument("-l", help= "-l: list of patterns to search on patch_matching field", required = "True")
parser.add_argument("-q", help= "-q: aligment quality. Default 20", default=20)
parser.add_argument('-r', type=int, choices=[1, 2, 3], help='the type of regular expression to apply (1, 2, 3). Look code comments to see regex', default=1)
parser.add_argument("-p", help= "-p: pattern to be at the beginning and end of path_matching", nargs="?")
args = parser.parse_args()
terms = []
with open(args.l) as f:
 	for l in f:
 		terms.append(l.rstrip("\n"))
terms=['1', '2']
m_names=('queryname','query_length','query_start','query_end','strand', 'path_matching','path_length','path_start','path_end', 'residue_matches', 'alignm_length', 'mapping_qual', 'other1', 'ot
her2', 'other3', 'identity', 'other4')
mytypes={'mapping_qual':'Int64'}
df4=pd.read_csv(args.g, names=m_names,  sep="\t", dtype=mytypes)
df5 = df4[df4['path_matching'].str.contains('|'.join(terms), na=False)]
df6 = df5[df5['mapping_qual'] >= int(0)]
df5.to_csv("{}filtered1.gaf".format(args.l), index=False, header=None, sep="\t")

#This regular expression matches a sequence of one or more consecutive occurrences of a symbol followed by one or more digits, where the symbol can be either > or <. The sequence must occur at least twice in a row.
regex1 = r'^(>|<)(?=.*(?:' + '|'.join(terms) + ')).+$'

# regex for "string starts with > or < followed by all items in my list occurring at least once
regex2 = r"([><]\d+){2,}"

# regular expression that matches a string that starts with either > or < followed by u115, and then matches any character except for a line break (.*). The positive lookahead (?=.*u115$) asserts that u115 is at the end of the string. The ^ and $ anchors ensure that the entire string is matched from start to end.
regex3 = r'^[<>]{0}(?=.*{0}$).*'.format(args.p)
if args.r == 1:
	regex = regex1
elif args.r == 2:
	regex = regex2
elif args.r == 3:
	regex = regex3
else:
	# Handle invalid argument values here
	print('Error: Invalid regex_type argument')
	exit(1)
df7=df6[df6['path_matching'].str.match(regex)]
df7.sort_values('path_matching').to_csv("{}filtered2.gaf".format(args.g), index=False, header=None, sep="\t")

df8 = df7[['queryname','query_length','query_start','query_end','strand', 'path_matching','path_length','path_start','path_end', 'residue_matches', 'alignm_length', 'mapping_qual', 'identity']
].sort_values('path_matching')
df8.to_csv("{}filtered3.gaf".format(args.l), index=False, sep="\t")
df9 = df8['path_matching'].value_counts().rename_axis('unique_values').reset_index(name='counts')
df9.to_csv("{}filtered3.cov".format(args.l), index=False, sep="\t")
