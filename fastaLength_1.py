from __future__ import division
from Bio import SeqIO
import sys
input_fasta = sys.argv[1]
output = open(sys.argv[2], "w")
for sequence in SeqIO.parse(input_fasta, 'fasta'):
        id = sequence.id
        get = sequence[8618:]
        length = len(get)
        out1 = '> ' + 'length got is ' + str(length)
        out2 = get.format('fasta')
        output.write(out2)
        print(out1)
output.close()
