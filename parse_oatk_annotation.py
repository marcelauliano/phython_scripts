import pandas as pd
import argparse

parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Parse *oatk.asm.annot_mito.txt file for oatk to understand how many genes and tRNAs are annotated in each graph node") 
parser.add_argument("-i", help= "-i: annotation file *oatk.asm.annot_mito.txt from oatk", required = "True")
parser.add_argument("-o1", help= "-o1: name for first output wich is a table of gene and tRNA counts", required = "True")
parser.add_argument("-o2", help= "-o2: name for file showing which genes and tRNAs in each node. Only the ones annotated with evalue smaller or equal to 0.01", required = "True")

args = parser.parse_args()


input_file = args.i

#Remove lines starting with # and replace spaces by tab
data = []
with open(input_file, "r") as file:
    for line in file:
        if not line.startswith("#"):
            modified_line = "\t".join(line.split())
            data.append(modified_line.split("\t"))

#Then open it as a dataframe
column_names = ['gene_tRNA', 'ac', 'query', 'ac1', 'hmmfrom', 'hmmto', 'alifrom', 'alito', 'evnfrom', 'envto', 'modlen', 'strand', 'e-value', 'score', 'bias', 'description']
df = pd.DataFrame(data, columns=column_names)
df[['gene_tRNA', 'query', 'hmmfrom', 'hmmto', 'alifrom', 'alito', 'strand', 'e-value', 'score',]]

#Now let's filter and groupby some columns
result = df.groupby(['query', 'gene_tRNA', 'e-value']).size().reset_index(name='count')
result['e-value'] = pd.to_numeric(result['e-value'])
result1 = df.groupby('query')['gene_tRNA'].nunique().reset_index(name='gene_tRNA_count')
result1

#Now let's filter by e-value as well. 
# Filter groups based on 'e-value' condition
filtered_counts = result[result['e-value'] <= 0.01].groupby(['query', 'gene_tRNA'])['count'].sum()

filtered_counts = result[result['e-value']  <= 0.01].groupby(['query', 'gene_tRNA'])['count'].sum().reset_index(name='filtered_count')
filtered_counts1= filtered_counts.groupby('query')['gene_tRNA'].nunique().reset_index(name='gene_tRNA_c_evalue<=0.01')
merged_df = result1.merge(filtered_counts1, on='query', how='inner')
merged_df.sort_values(by='gene_tRNA_c_evalue<=0.01', ascending=False).to_csv(args.o1, index=False, sep="\t")


#Now let's produce one more output file that shows which genes are present in each graph path. We will show only the ones with e-values smaller than 0.01

output_file = args.o2  # Specify the output file name

# Extract unique values of 'query' column
unique_queries = filtered_counts['query'].unique()

# Open the output file
with open(output_file, 'w') as file:
    # Write the header line
    file.write("# Those are the genes found by hmmer with e-value <= 0.01\n")
    
    # Iterate over each unique query
    for query in unique_queries:
        # Filter the dataframe for the current query
        filtered_df = filtered_counts[filtered_counts['query'] == query]
        
        # Extract the unique target values for the current query
        unique_targets = filtered_df['gene_tRNA'].unique()
        
        # Create the line with query and target values separated by commas
        line = query + ':' + ','.join(unique_targets) + '\n'
        
        # Write the line to the output file
        file.write(line)
