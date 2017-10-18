#Learning process - this script filter out complete fastq sequences that have phred qualities bellow 14.
#By Marcela Uliano-Silva tutored by Felix Heeger and Max Driller, 2017.

from Bio import SeqIO
import gzip


mainfile = "example.fastq"
if mainfile.endswith(".gz"):
	my_fastq_parse = gzip.open(mainfile)
else:
	my_fastq_parse = open(mainfile)
output = open("out.txt", "w")

for record in SeqIO.parse(my_fastq_parse, "fastq"):
	flag = True 
	for qual in record.letter_annotations["phred_quality"][0:4]:
		if qual <= 14:
			flag = False
	if flag == True:
		#print(record.format("fastq"))
		output.write(record.format("fastq"))
output.close()
