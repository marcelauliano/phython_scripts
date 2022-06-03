from Bio.SeqUtils import GC
import sys
from Bio import SeqIO

input_fasta = sys.argv[1]
out=open(sys.argv[2], "w")

for sequence in SeqIO.parse(input_fasta, 'fasta'):
    id = sequence.id
    length = len(sequence)
    gc = GC(sequence.seq)
    resul = id + ',' + str(length) + ',' + str(gc) + '\n'
    out.write(resul)
out.close()
