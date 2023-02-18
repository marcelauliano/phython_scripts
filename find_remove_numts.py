import subprocess
import argparse
import pandas as pd
import sys
import filterfasta

parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Find and remove numts from your nuclear genome using a mito seq
uence as reference for the search")
parser.add_argument("-d", help= "-d: blast database. Your mito sequence", required = "True")
parser.add_argument("-f", help= "-f: blast query senquences. Your nuclear assembly", required = "True")
parser.add_argument("-t", help= "-t: number of threads. Default 1", default=1)
parser.add_argument("-p", help= "-p: Percentage of scaffold length in blast match to be considered mito, default 95", default=95)
args = parser.parse_args()


#First run blast
makeblastdb = "makeblastdb -in " + str(args.d) + " -dbtype nucl"
subprocess.run(makeblastdb, shell=True)

blast = "blastn -query " + args.f + " -db " + args.d + " -num_threads " + str(args.t) + " -out contigs.blastn -outfmt '6 std qlen slen'"
subprocess.run(blast, shell=True)

#Now parse blast output

my_names = ["qseqid", "sseqid", "pident", "alilength" , "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue" , "bitscore", "leng_quer
y", "s_length",]

blast_cov = pd.read_csv("contigs.blastn", sep="\t", names = my_names)
#Get the percentage of the query in the blast aligment
blast_cov['alilength']*100 / (blast_cov['leng_query'])
blast_cov['%q_in_match'] = blast_cov['alilength']*100 / (blast_cov['leng_query'])

#sum percentages of query sequence in blast match based on column id
a= blast_cov.groupby('qseqid')['%q_in_match'].sum().to_frame().rename(columns={'qseqid':'%q_in_match'}).reset_index()

#get size of query and subject and drop duplicates
seqsizes = blast_cov[['qseqid', 'leng_query', 's_length']].drop_duplicates(subset='qseqid')

#merge 'a' and 'seqsizes' dataframes by 'qseqid'
result = pd.merge(a, seqsizes, on='qseqid')
result.to_csv("contigs.blastn.parse", index=False, sep="\t")

#Get ids of mitos in the nuclear assembly

my_names2 = ["qseqid", "%q_in_match", "leng_query", "s_length"]
blast_parse = pd.read_csv("contigs.blastn.parse", sep="\t", names = my_names2, skiprows=1)
blast_parse.astype({'%q_in_match': 'float'}).dtypes
#blast_parse.dtypes
blast_parse1 = blast_parse[blast_parse["%q_in_match"] >= float(args.p)]

blast_parse1['qseqid'].to_csv("contigs_to_remove.ids", index=False, header=None)
#filterfasta.filterFasta(idList="contigs_to_remove.ids", neg=True, inStream=args.f, outPath="gbk.HiFiMapped.bam.filtered.fasta")

outputfile = "{}_numtsRemoved.fa".format(args.f)
filter ="python filterfasta.py -i contigs_to_remove.ids " + args.f + " -n > " + outputfile
subprocess.run(filter, shell=True)
