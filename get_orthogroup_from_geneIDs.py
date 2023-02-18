from Bio import SeqIO
import argparse

parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Get the orthogroup giving a list of protein IDs") 
parser.add_argument("-l", help= "-l: list of protein IDs", required = "True")
parser.add_argument("-f", help= "-f: file of Orthogroups.txt", required = "True")
parser.add_argument("-o", help= "-o: outputfile", required = "True")

args = parser.parse_args()

output = open(args.o, "w")
orthodb=[]
input_patterID=open(args.l)
file=input_patterID.read().splitlines()

with open(args.f) as topo_file:
    for seq in topo_file:
        for line in file:
            if line in seq:
                output.write(seq)               
output.close()
