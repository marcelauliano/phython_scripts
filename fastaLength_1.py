from __future__ import division
from Bio import SeqIO
import sys
input_fasta = sys.argv[1]
output_file = open(sys.argv[2], "w")
#length = open('mChoDid1.pri.asm.20190228.fasta.length', 'w')
for sequence in SeqIO.parse(input_fasta, 'fasta'):
        id = sequence.id
        count = len(sequence)
        out = '>' + id + '\t' + str(count) + '\n'
        output_file.write(out)
output_file.close()
