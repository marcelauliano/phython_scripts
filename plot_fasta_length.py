from Bio import SeqIO
import pylab
import sys
import gzip
input = sys.argv[1]
output = open(sys.argv[2], "wb")
if input.endswith(".gz"):
        my_fasta_parse = gzip.open(input, "rt")
else:
        my_fasta_parse = open(input)


sizes = [len(rec) for rec in SeqIO.parse(my_fasta_parse, "fasta")]
pylab.hist(sizes, bins=20)
pylab.title(
    "%i  sequences\nLengths %i to %i" % (len(sizes), min(sizes), max(sizes))
)
pylab.xlabel("Sequence length (bp)")
pylab.ylabel("Count")
pylab.savefig(output)
