from Bio import SeqIO
import pylab
import sys
input = sys.argv[1]
output = open(sys.argv[2], "wb")
sizes = [len(rec) for rec in SeqIO.parse(input, "fasta")]
pylab.hist(sizes, bins=20)
pylab.title(
    "%i  sequences\nLengths %i to %i" % (len(sizes), min(sizes), max(sizes))
)
pylab.xlabel("Sequence length (bp)")
pylab.ylabel("Count")
pylab.savefig(output)
