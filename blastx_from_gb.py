import argparse
import subprocess
from Bio import SeqIO

def extract_protein_sequences(genbank_files, protein_fasta_file):
    if protein_fasta_file:
        return load_protein_sequences_from_file(protein_fasta_file)
    else:
        return extract_protein_sequences_from_genbank(genbank_files)

def extract_protein_sequences_from_genbank(genbank_files):
    protein_sequences = []
    for genbank_file in genbank_files:
        for record in SeqIO.parse(genbank_file, "genbank"):
            for feature in record.features:
                if feature.type == "CDS" and "translation" in feature.qualifiers:
                    protein_sequence = feature.qualifiers["translation"][0]
                    gene_name = feature.qualifiers.get("gene", ["Unknown"])[0]
                    organism = record.annotations.get("organism", "")
                    if organism:
                        fasta_id = f"{organism}|{gene_name}"
                    else:
                        fasta_id = gene_name
                    protein_sequences.append((fasta_id, protein_sequence))
    return protein_sequences

def load_protein_sequences_from_file(protein_fasta_file):
    protein_sequences = []
    for record in SeqIO.parse(protein_fasta_file, "fasta"):
        fasta_id = record.id
        protein_sequence = str(record.seq)
        protein_sequences.append((fasta_id, protein_sequence))
    return protein_sequences

def save_sequences_to_fasta(sequences, output_file):
    with open(output_file, "w") as fasta_file:
        for fasta_id, sequence in sequences:
            fasta_file.write(f">{fasta_id}\n{sequence}\n")

def create_protein_database(protein_fasta_file, database_path):
    command = f"makeblastdb -in {protein_fasta_file} -dbtype prot -out {database_path}"
    subprocess.run(command, shell=True, check=True)

def run_blastx(nucleotide_file, protein_database_path, blast_output):
    command = f"blastx -query {nucleotide_file} -db {protein_database_path} -outfmt '6 std qlen slen' -evalue 0.1 -out {blast_output}"
    subprocess.run(command, shell=True, check=True)

def main(genbank_files, nucleotide_file, blast_output, protein_fasta_file):
    # Extract protein sequences
    protein_sequences = extract_protein_sequences(genbank_files, protein_fasta_file)

    # Save protein sequences to a fasta file if not provided
    if not protein_fasta_file:
        protein_fasta_file = "protein_sequences.fasta"
        save_sequences_to_fasta(protein_sequences, protein_fasta_file)

    # Create protein database    
    protein_database_path = "protein_database"
    create_protein_database(protein_fasta_file, protein_database_path)

    # Run blastx
    run_blastx(nucleotide_file, protein_database_path, blast_output)

    # Add header line to blast output file
    header_line = "qseqid\tsseqid\t%_identity\talig_length\tmismatch\tgapopen\tqstart\tqend\tsstart\tsend\tevalue\tbit score\tqlen\tslen\n"
    with open(blast_output, "r+") as output_file:
        content = output_file.read()
        output_file.seek(0, 0)
        output_file.write(header_line + content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Protein sequence extraction and blastx pipeline")
    parser.add_argument("genbank_files", nargs="*", help="GenBank file(s) containing protein coding sequences")
    parser.add_argument("nucleotide_file", help="Input nucleotide FASTA file")
    parser.add_argument("-o", "--output", dest="blast_output", default="blast_results.txt", help="Blast output file")
    parser.add_argument("-p", "--protein-fasta", dest="protein_fasta_file", help="Input protein FASTA file")
    args = parser.parse_args()

    main(args.genbank_files, args.nucleotide_file, args.blast_output, args.protein_fasta_file)
