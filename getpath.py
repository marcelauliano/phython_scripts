import sys
import os
import shutil

#First I'm writing the full path from where I want to get some data. The full path will depend on the ID initials that are present in my input file.
input=open(sys.argv[1])
path= []
for i in input:
        if i.lower().startswith("m"):
                path.append("/Users/mu2/Sanger/COI/test19020202/" + i.rstrip("\n") + "/fasta/".rstrip("\n"))
        else:
                print("This not found" + " " + i.rstrip("\n"))
