from BCBio import GFF
from Bio import SeqIO
import sys

in_file = sys.argv[1]
out_file = sys.argv[2]
in_handle = open(in_file)
out_handle = open(out_file, "w")

GFF.write(SeqIO.parse(in_handle, "genbank"), out_handle)

in_handle.close()
out_handle.close()
