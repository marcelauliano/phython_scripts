#Learning process - this script filter out complete fastq sequences that have at least one N.
#By Marcela Uliano-Silva 

from Bio import SeqIO
import gzip
import sys

input_file = sys.argv[1]
#input_file is a variable. Line 8 states that something will be saved in the variable input_file. The something is the argv[1]. The sys is an object, and the argv that comes after the . is part of that object and its a list, and the [] allow you to access one of the itens on that list. In this case, the input, in argv, 0 prints the name of the script. 
if input_file.endswith(".gz"):
	my_fastq_parse = gzip.open(input_file)
else:
	my_fastq_parse = open(input_file)
output = open(sys.argv[2], "w")

for record in SeqIO.parse(my_fastq_parse, "fastq"):
	#record is just a variable name
	if record.seq.count('N') == 0:
		output.write(record.format("fastq"))
output.close()
