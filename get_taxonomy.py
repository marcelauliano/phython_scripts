import pandas as pd
from ete3 import NCBITaxa
import sys
input_file = sys.argv[1]
output = open(sys.argv[2], "w")

#given a file with one taxID per row, output the complete taxonomy.
taxids = open(input_file).readlines()
lista=[]
for item in taxids:
    
    ncbi =NCBITaxa()
    lineage = ncbi.get_lineage(item)
    names = ncbi.get_taxid_translator(lineage)
    lista.append([names[taxid] for taxid in lineage])

data = pd.DataFrame(lista)
data.to_csv(output, sep="\t", index=False, header=None)
