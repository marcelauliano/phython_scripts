import pandas as pd
import argparse

parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Parse *oatk.asm.annot_mito.txt file from oatk to understand how many genes and tRNAs are annotated in each graph node")
 
parser.add_argument("-i", help= "-i: annotation file called *oatk.asm.annot_mito.txt from oatk", required = "True")
parser.add_argument("-o1", help= "-o1: name for first output wich is a table of gene and tRNA counts")
parser.add_argument("-o2", help= "-o2: name for file showing which genes and tRNAs in each node. Only the ones annotated with evalue smaller or equal to 0.01")
parser.add_argument("-o3", help= "-o2: comma-separated list of query names to input to bandage to draw graph around those nodes")
parser.add_argument("-o4", help= "-o4: bed file to input annotations to bandage_NG")
parser.add_argument("-o5", help= "-o4: bed file to input all annotations to bandage_NG even with bad e-values")
args = parser.parse_args()

input_file = args.i

# Generate the output names automatically if options are not provided
output_name1 = args.o1 if args.o1 is not None else args.i + "_output1.txt"
output_name2 = args.o2 if args.o2 is not None else args.i + "_output2.txt"
output_name3 = args.o3 if args.o3 is not None else args.i + "_output3.txt"
output_name4 = args.o4 if args.o4 is not None else args.i + "_output4.evalue.bed"
output_name5 = args.o5 if args.o4 is not None else args.i + "_output4.all.bed"

#Remove lines starting with # and replace spaces by tab
data = []
with open(input_file, "r") as file:
    for line in file:
        if not line.startswith("#"):
            modified_line = "\t".join(line.split())
            data.append(modified_line.split("\t"))

#Then open it as a dataframe
column_names = ['gene_tRNA', 'ac', 'query', 'ac1', 'hmmfrom', 'hmmto', 'alifrom', 'alito', 'evnfrom', 'envto', 'modlen', 'strand', 'e-value', 'score', 'bias', 'description']
dtype = {'gene_tRNA': object, 'ac': object, 'query': object, 'ac1': object, 'hmmfrom': int, 'hmmto': int, 'alifrom': int, 'alito': int, 'evnfrom': int, 'envto': int, 'modlen': int, 'strand': object, 'e-value': float, 'score': float, 'bias': float, 'description': object}
df = pd.DataFrame(data, columns=column_names).astype(dtype)
df[['gene_tRNA', 'query', 'hmmfrom', 'hmmto', 'alifrom', 'alito', 'strand', 'e-value', 'score',]]

#Now let's filter and groupby some columns
result = df.groupby(['query', 'gene_tRNA', 'e-value']).size().reset_index(name='count')
result['e-value'] = pd.to_numeric(result['e-value'])
result1 = df.groupby('query')['gene_tRNA'].nunique().reset_index(name='gene_tRNA_count')

#Now let's filter by e-value as well. 

# Filter groups based on 'e-value' condition
filtered_counts = result[result['e-value'] <= 0.01].groupby(['query', 'gene_tRNA'])['count'].sum()

filtered_counts = result[result['e-value']  <= 0.01].groupby(['query', 'gene_tRNA'])['count'].sum().reset_index(name='filtered_count')
filtered_counts1= filtered_counts.groupby('query')['gene_tRNA'].nunique().reset_index(name='gene_tRNA_c_evalue<=0.01')
merged_df = result1.merge(filtered_counts1, on='query', how='inner')
merged_df.sort_values(by='gene_tRNA_c_evalue<=0.01', ascending=False).to_csv(output_name1, index=False, sep="\t")


#Now let's produce one more output file that shows which genes are present in each graph path. We will show only the ones with e-values smaller than 0.01

output_file = output_name2  # Specify the output file name

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
#Last, let's get a comma-separated list of nodes to past on bandage to draw graph around those nodes.        
with open(output_name3, 'w') as file:
    file.write(','.join(merged_df['query'].astype(str).tolist()))

# Now let's get the annotations in bed format so we can input in to bandage_NG

filtered_df = df[df['query'].isin(merged_df['query'])]
filtered_df1 =filtered_df[filtered_df['e-value'] <= 0.01]
filtered_df2 = filtered_df1[['query', 'alifrom', 'alito', 'gene_tRNA', 'score', 'strand']]
filtered_df2.to_csv(output_name4, sep="\t", index=False, header=None)
filtered_df3 = filtered_df[['query', 'alifrom', 'alito', 'gene_tRNA', 'score', 'strand']]
filtered_df3.to_csv(output_name5, sep="\t", index=False, header=None)
