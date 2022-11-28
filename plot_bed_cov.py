#giving a bam file do
#bedtools genomecov -ibam ptg000001l.rotated_rotatedg60.bam

#sys.argv[1] <- bed file with coverage
#sys.arg2[2] <- name of contig to plot
#sys.arg3[3] <- name of final plot

import pandas as pd
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


n=['id', 'position', 'coverage']
df = pd.read_csv(sys.argv[1], sep="\t", names=n, )

#df2 is filtering to keep only the contig of interest, which in this case is ptg000001l.rotated_rotated
df2 = df.loc[df['id'] == sys.argv[2]]

sns.distplot(
    
    df2["coverage"].dropna(),
    
    kde=False,
)
plt.savefig(sys.argv[3] + ".png")
