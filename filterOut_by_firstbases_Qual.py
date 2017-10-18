#Learning process - this script filter out complete fastq sequences that have phred qualities bellow 14.
#By Marcela Uliano-Silva tutored by Felix Heeger and Max Driller, 2017.

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
	flag = True 
	for qual in record.letter_annotations["phred_quality"][0:4]:
		if qual <= 22:
			flag = False
	if flag == True:
		output.write(record.format("fastq"))
output.close()
