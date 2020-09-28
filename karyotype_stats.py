#Marcela Uliano-Silva, Wellcome Sanger Institute


import argparse
import pandas as pd
from Bio import SeqIO

parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Giving a assembled genome (-s ) and it's expected karyotype (-k) calculate multiple metrics. Saves output to karyo_stats.tsv") 
parser.add_argument("-s", help= "-s: the scaffolds of the assembly in fasta format", required = "True")
parser.add_argument("-k", help= "-k: the karyotype of the species", required = "True")

args = parser.parse_args()

output_table=open("karyo_stats.tsv", "w")
input_fasta = open(args.s)
output_file = open("scaffolds.sizes.txt", "w")
for sequence in SeqIO.parse(input_fasta, 'fasta'):
        id = sequence.id
        count = len(sequence)
        out = '>' + id + '\t' + str(count) + '\n'
        output_file.write(out)
output_file.close()

#(i) open file with scaffolds sizes, (ii) sort by larger to small and (iii) calculate % of bases in the number of scaffolds equals to the karyotype 

ka=int(args.k)
my_names = ['scaf', 'size']
scaff_s = pd.read_csv("scaffolds.sizes.txt", sep="\t", names=my_names, )

scaff_s.sort_values('size')
how_many_scaffstotal=len(scaff_s)
scaff_s.set_index('scaf', inplace=True)
karyo = scaff_s.iloc[:ka].sum()
total = scaff_s.iloc[0:].sum()
total1=int(total)
perc_of_karyo_in_assembly = (100*karyo)/total
perc_of_karyo_in_assembly
one=float(perc_of_karyo_in_assembly)

#We can also calculate how much of the first scaffolds larger than 5Mb correspond of the total assembly:

scaff_5M = scaff_s[scaff_s["size"] >= 5000000]
scaff_5M_t = scaff_5M.iloc[:].sum()
perc_of_5M_in_assembly = (100*scaff_5M_t)/total
perc_of_5M_in_assembly
two=float(perc_of_5M_in_assembly)

#calculate karyotipc congruence and fragmentation score and save to table

how_many = len(scaff_s[scaff_s["size"] >= 5000000])
karyotypic_congruence = 31/ how_many
karyotypic_congruence
fragmentation_score = how_many/ 31
round(fragmentation_score)
table = {'Description': ['karyotype is', 'total number of scaffolds', 'total bp in assembly', '% of total bp in largest scaffs according to karyo','% of total bp in scaffs >= 5Mb','karyotypic congruence (scaffs >= 5Mb)','fragmentation score (scaffs >= 5Mb
)'],
         'Values' : [ka, how_many_scaffstotal, total1, one, two, karyotypic_congruence, fragmentation_score]
        }

df = pd.DataFrame(table, columns = ['Description', 'Values'])
roundTwoDecimals = df.round(decimals=2)
roundTwoDecimals
roundTwoDecimals.to_csv("karyo_stats.tsv", index=False, sep="\t")
print ("ALL DONE!! \n Please have a look at the created file 'karyo.stats.tsv' for your final statistics. \n And have a look at 'scaffolds.sizes.txt' for the size of each scaffold in your assembly.")
