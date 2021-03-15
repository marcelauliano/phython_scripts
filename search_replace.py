#Replace multiple filds in a file from a python dict given in a file with two columns. Key is the value to be searched, value is the one to replace it.

import sys
import argparse 


parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Replace multiple fields in a file from a python dict given in a file with two columns. Key is the value to be searched, value is the one to replace it.") 
parser.add_argument("-l", help= "-l: list of two columns separared by tab to be key and value", required = "True")
parser.add_argument("-f1", help= "-f1: file to search", required = "True")
parser.add_argument("-f2", help= "-f2: Output. Same as f1 but with replaced fields", required = "True")

args = parser.parse_args()

list1=sys.argv[1]
fin=sys.argv[2]
fout=sys.argv[3]


d={}

with open(args.l) as f:
    for line in f:
        lin = line.split("\t")
        key =lin[0]
        value=lin[1].rstrip('\n')
        d[key] = value

fin = open(args.f1)
fout = open(args.f2, "w")
for line in fin:

    for key, value in d.items():
        if key in line:
            eu=line.replace(key, value)
            print(eu)
            fout.write(eu)
fout.close()
print("all done")
