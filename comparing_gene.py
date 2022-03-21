from Bio import SeqIO,SeqFeature
import sys
import pandas as pd

input_gb = open(sys.argv[1])
#output = open(sys.argv[2], "w")


genes =[ 'atp1', 'atp4', 'atp6', 'atp8', 'atp9', 'ccmB', 'ccmC', 'ccmFc', 'ccmFn', 'cytb', 'cox1', 'cox2', 'cox3', 'mttB', 'nd1', 'nd2', 'nd3', 'nd4', 'nd4L', 'nd5', 'nd6', 'nad7', 'nad9', 'rpl2', 'rpl5', 'rpl6', 'rpl10', 'rpl16', 'rps1', 'rps2', 'rps3', 'rps4', 'rps7', 'rps8', 'rps10', 'rps11', 'rps12', 'rps13', 'rps14', 'rps19', 'sdh3', 'sdh4']
genes1 = [element.lower() for element in genes]
df_genes = pd.DataFrame(genes1,columns =['All_genes'])

listinha =[]

for rec in SeqIO.parse(input_gb, "genbank"):
    if rec.features:
        for feature in rec.features:
            if feature.type == "CDS":
                listinha.append(feature.qualifiers["gene"][0])

list2 =[element.lower() for element in listinha]               
df = pd.DataFrame(list2,columns =['Names'])


df3 = df_genes.merge(df, left_on='All_genes', right_on='Names', left_index=False, right_index=False, how='outer')

df3

df3.to_csv("genes-comparison.tsv", index=False, sep="\t")
