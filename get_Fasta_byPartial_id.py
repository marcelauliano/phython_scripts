from Bio import SeqIO
import argparse
parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Get specific fasta from multifasta (-f) by partial ids in a list (-l)")
parser.add_argument("-f", help= "-f: multifasta file", required = "True")
parser.add_argument("-l", help= "-l: list of partial ids", required = "True")
parser.add_argument("-o", help= "-o: output file", required = "True")

args = parser.parse_args()

dna_records = []
input_patterID=open(args.l)
file=input_patterID.read().splitlines()
for seq in SeqIO.parse(args.f,"fasta"):
        for line in file:
                if line in seq.id:
                        dna_records.append(seq)
SeqIO.write(dna_records, args.o,"fasta")
print("all done")
