from Bio import SeqIO
import sys

def transform_to_rna(input_file, output_file):
    # Open the input multifasta file for reading
    with open(input_file, 'r') as fasta_file:
        # Open the output multifasta file for writing
        with open(output_file, 'w') as output:
            # Iterate over the sequences in the input file
            for record in SeqIO.parse(fasta_file, 'fasta'):
                # Convert T to U in the sequence
                rna_seq = record.seq.transcribe()

                # Create a new SeqRecord with the transformed sequence
                rna_record = record
                rna_record.seq = rna_seq

                # Write the transformed sequence to the output file
                SeqIO.write(rna_record, output, 'fasta')

# Provide the paths to your input and output files
input_file = sys.argv[1]
output_file = sys.argv[2]

# Call the function to transform the multifasta file
transform_to_rna(input_file, output_file)
