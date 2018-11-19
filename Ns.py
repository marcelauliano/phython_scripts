#very quick write.
from __future__ import division
from Bio import SeqIO
import sys
input = sys.argv[1]
inputopen = open(input)
Ns = open(sys.argv[2], 'w')
for sequence in SeqIO.parse(inputopen, 'fasta'):
        id = sequence.id
        count1 = len(sequence)
        countNs = sequence.seq.upper().count('N')
        out = id + ' ' + str(countNs) + '\n'
        Ns.write(out)
Ns.close()

        
