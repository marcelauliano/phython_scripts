#By Marcela Uliano-Silva 

from Bio import SeqIO
import gzip
import sys

input_file_R1 = sys.argv[1]
input_file_R2 = sys.argv[2]
#input_file is a variable. Line 8 states that something will be saved in the variable input_file. The something is the argv[1]. The sys is an object, and the argv (argument) that comes after the . is part of that object and its a list, and the [] allow you to access one of the itens on that list. In this case, the input, in argv, 0 prints the name of the script. 
if input_file_R1.endswith(".gz"):
	my_fastq_parse_R1 = gzip.open(input_file_R1)
else:
	my_fastq_parse_R1 = open(input_file_R1)
if input_file_R2.endswith(".gz"):
	my_fastq_parse_R2 = gzip.open(input_file_R2)
else:
	my_fastq_parse_R2 = open(input_file_R2)
output_file_R1 = open(sys.argv[3], "w")
output_file_R2 = open(sys.argv[4], "w")

fortheSecondToo = SeqIO.parse(my_fastq_parse_R2, "fastq")
for record_forThe_R1 in SeqIO.parse(my_fastq_parse_R1, "fastq"):
	#record is just a variable name
	record_forThe_R2 = next(fortheSecondToo)
	if record_forThe_R1.seq.count('N') == 0 and record_forThe_R2.seq.count('N') == 0: 
		output_file_R1.write(record_forThe_R1.format("fastq"))
		output_file_R2.write(record_forThe_R2.format("fastq"))
output_file_R1.close()
output_file_R2.close()



