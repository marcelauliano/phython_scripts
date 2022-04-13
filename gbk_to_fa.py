from Bio import SeqIO
import sys
input_fasta = sys.argv[1]
output = open(sys.argv[2], "w")

input_handle  = open(input_fasta, "r")

for seq_record in SeqIO.parse(input_handle, "genbank") :
    print("Dealing with GenBank record %s" % seq_record.id)
    for seq_feature in seq_record.features :
        if seq_feature.type=="CDS" :
            assert len(seq_feature.qualifiers['translation'])==1
            output.write(">%s->%s\n%s\n" % (
                   seq_record.name,
                   seq_feature.qualifiers['gene'][0],
                   seq_feature.qualifiers['translation'][0]))

input_handle.close()
