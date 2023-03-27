import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the chromosome length file into a Pandas DataFrame
chrom_lengths = pd.read_csv('partial.sizes', sep='\t', header=None, names=['chrom', 'length'])

# Load the coverage file into a Pandas DataFrame
coverage = pd.read_csv('partial.out.test.bed', sep='\t', header=None, names=['chrom', 'start', 'end', 'coverage'])

# Define the number of rows and columns for the subplot grid
num_chroms = len(chrom_lengths)
num_cols = 2
num_rows = (num_chroms - 1) // num_cols + 1

# Create the subplot grid
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 4*num_rows))

# Loop through each chromosome and plot its coverage
for i, chrom_name in enumerate(chrom_lengths['chrom']):
    # Filter the coverage DataFrame to include only the current chromosome
    chrom_coverage = coverage[coverage['chrom'] == chrom_name]

    # Merge the chromosome length and coverage DataFrames
    merged = pd.merge(chrom_lengths[chrom_lengths['chrom'] == chrom_name], chrom_coverage, on='chrom')

    # Calculate the position of each base pair along the chromosome
    merged['pos'] = merged['start'] + (merged['end'] - merged['start']) / 2

    # Plot the coverage on the corresponding subplot
    row_idx = i // num_cols
    col_idx = i % num_cols
    ax = axes[row_idx][col_idx]
    sns.lineplot(x='pos', y='coverage', data=merged, ax=ax)
    ax.set_title(f'Chromosome {chrom_name}')
    ax.set_xlabel('Chromosome position')
    ax.set_ylabel('Coverage')

# Adjust the layout and spacing of the subplots
plt.tight_layout()

# Save the plot to a file
fig.savefig('coverage_plot.png', dpi=300)
