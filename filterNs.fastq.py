#Learning process - this script filter out complete fastq sequences that have at least one N.
#By Marcela Uliano-Silva 

from Bio import SeqIO
import gzip
import sys

mainfile = sys.argv[1]
if mainfile.endswith(".gz"):
	my_fastq_parse = gzip.open(mainfile)
else:
	my_fastq_parse = open(mainfile)
output = open(sys.argv[2], "w")

for record in SeqIO.parse(my_fastq_parse, "fastq"):
	if record.seq.count('N') == 0:
		output.write(record.format("fastq"))
output.close()
