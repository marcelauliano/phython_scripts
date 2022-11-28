#giving a bam file do
#bedtools genomecov -ibam ptg000001l.rotated_rotatedg60.bam


import pandas as pd
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


n=['id', 'position', 'coverage']
df = pd.read_csv(sys.argv[1], sep="\t", names=n, )

#df2 is filtering to keep only the contig of interest, which in this case is ptg000001l.rotated_rotated
df2 = df.loc[df['id'] == "ptg000001l.rotated_rotated"]

sns.distplot(
    
    df2["coverage"].dropna(),
    
    kde=False,
)
plt.savefig("coverage.png")
