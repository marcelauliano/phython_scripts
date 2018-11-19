#very quick write.

from __future__ import division
from Bio import SeqIO
Ns = open('contentNs.txt', 'w')
for sequence in SeqIO.parse('/home/muliano/VGP-running/pri.asm.20180817.fasta-buscos0', 'fasta'):
        id = sequence.id
        count1 = len(sequence)
        countNs = sequence.seq.upper().count('N')
        out = id + ' ' + str(countNs) + '\n'
        Ns.write(out)
Ns.close()
        
