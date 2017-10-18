#Learning process - this script filter out complete fastq sequences that have phred qualities bellow 14.
#By Marcela Uliano-Silva tutored by Felix Heeger, 2017.

from Bio import SeqIO
output = open("out.txt", "w")
for record in SeqIO.parse(open("example.fastq"), "fastq"):
	flag = True 
	for qual in record.letter_annotations["phred_quality"][0:4]:
		if qual <= 22:
			flag = False
	if flag == True:
		#print(record.format("fastq"))
		output.write(record.format("fastq"))
output.close()
