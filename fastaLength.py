#lazy write without args

from __future__ import division
from Bio import SeqIO
length = open('mChoDid1.pri.asm.20190228.fasta.length', 'w')
for sequence in SeqIO.parse('mChoDid1.pri.asm.20190228.fasta', 'fasta'):
        id = sequence.id
        count = len(sequence)
        out = '>' + id + '\t' + str(count) + '\n'
        length.write(out)
length.close()
