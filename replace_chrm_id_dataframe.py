import pandas as pd

# File paths (adjust these paths as necessary)
mapping_file_path = '/path/to/chromosome_mapping.tsv'  # Your mapping file
gff_file_path = '/path/to/gff_file.gff'  # Your GFF file

# Load the chromosome mapping file (tab-separated)
# Assuming the mapping file has no header: Column 1 is gff_id, Column 2 is current_id
chromosome_mapping = pd.read_csv(mapping_file_path, sep='\t', header=None, names=['gff_id', 'current_id'])

# Load the GFF file into a DataFrame
# Assuming standard GFF format
gff_columns = ['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes']
gff_df = pd.read_csv(gff_file_path, sep='\t', comment='#', names=gff_columns)

# Create a dictionary from the mapping file for replacing chromosome IDs
# Map current_id in GFF to gff_id from the mapping file
mapping_dict = dict(zip(chromosome_mapping['current_id'], chromosome_mapping['gff_id']))

# Function to replace chromosome IDs and filter out unmatched rows
def replace_chromosome_ids(df, id_column, mapping_dict):
    # Replace IDs based on mapping
    df[id_column] = df[id_column].map(mapping_dict)
    
    # Remove rows where IDs were not found in the mapping (NaN after mapping)
    df_filtered = df.dropna(subset=[id_column])
    
    return df_filtered

# Apply the replacement and filtering to the GFF DataFrame
filtered_gff_df = replace_chromosome_ids(gff_df, 'seqid', mapping_dict)

# Display the first few rows of the modified DataFrame
print(filtered_gff_df.head())

# Save the filtered DataFrame to a new file if needed
# filtered_gff_df.to_csv('/path/to/output_filtered_gff.gff', sep='\t', index=False, header=False)
