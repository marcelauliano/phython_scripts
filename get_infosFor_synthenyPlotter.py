import argparse
import os

def process_input(input_file, output_file, id_output_file):
    # Extract file name without extension for naming outputs
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile, open(id_output_file, 'w') as id_outfile:
        # Write header to the first output file
        outfile.write("chr\torder\torientation\n")

        # Write header to the second output file
        id_outfile.write("chr\n")

        for line in infile:
            if 'chromosome' in line:
                # Extract chromosome ID and number
                parts = line.strip().split(' ')
                chromosome_id = parts[0][1:]
                chromosome_number = parts[-1].split(':')[-1]

                # Write to the first output file
                outfile.write(f"{chromosome_id}\t{chromosome_number}\tF\n")

            # Extract ID from lines starting with '>'
            if line.startswith('>'):
                identifier = line.split()[0][1:]
                # Write to the second output file
                id_outfile.write(f"{identifier}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get genome IDs and produce info tables for Wright's syntey_plotter. Only needs a genome as input")
    parser.add_argument('input_file', help='Path to genome fasta')

    args = parser.parse_args()

    # Create output file names
    output_file_name = f"{os.path.splitext(args.input_file)[0]}_infoChr.tsv"
    id_output_file_name = f"{os.path.splitext(args.input_file)[0]}_infoAll.tsv"

    process_input(args.input_file, output_file_name, id_output_file_name)
