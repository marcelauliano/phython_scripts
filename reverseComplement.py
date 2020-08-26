import sys
from Bio import SeqIO
input_file = sys.argv[1]
output_file = open(sys.argv[2], "w")

for record in SeqIO.parse(input_file, "fasta"):
        rever_comp_id = record.id
        RC = record.seq.reverse_complement()
        output_file.write(">RC_"+str(rever_comp_id)+"\n"+str(RC))
output_file.close()
