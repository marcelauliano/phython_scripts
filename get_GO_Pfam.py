import pandas as pd
import sys
import argparse
parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Parsing interproscan to get one to one GO terms for proteins") 
parser.add_argument("-i", help= "-i: input file from interproscan command: interproscan.sh -i $e -cpu 20 -dp -t p --goterms -appl Pfam -f TSV,HTML,GFF3,XML iprlookup", required = "True")
parser.add_argument("-out1", help= "-o2: output only first GO term assigned to protein", required = "True")
parser.add_argument("-out2", help= "-o3: output pfam domain assigned to protein", required = "True")
args = parser.parse_args()

my_names=["species_protein", "thingy", "thingy1", "Pfam", "PF-id", "description", "151", "409", "evalue?", "T", "date", "IPR-d", "domain descript", "GO",]

input1=pd.read_csv(args.i, sep="\t", names=my_names)
GO = input1[['species_protein', 'GO']]
pfam = input1[['species_protein', 'PF-id']]
GO.to_csv("all_GOs_per_protein.txt", sep="\t", index=False, header=False)
pfam.to_csv(args.out1, sep="\t", index=False, header=False)
output=open(args.out2, "w")
all_go=open("all_GOs_per_protein.txt")
for l in all_go:
	lin=l.split("\t")
	spec=lin[0].rstrip()
	go=lin[1]
	slicego=go.split("|")
	firstgo=slicego[0].rstrip()
	out=spec + "\t " + firstgo + "\n"
	output.write(out)
output.close()
