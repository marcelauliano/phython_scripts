#lazy write without args

from __future__ import division
from Bio import SeqIO
output = open('CD.bionano.length', 'w')
for sequence in SeqIO.parse('/home/muliano/xenarthra/c.didactylus/bionano/CD.bionano.fasta', 'fasta'):
        id = sequence.id
        get = sequence[12477:28968]
        length = len(get)
        out = '> ' + 'length got is ' + str(length) + '\n' + get.format('fasta')
        output.write(out)
output.close()
#       print(str(length) +  get.format('fasta'))
