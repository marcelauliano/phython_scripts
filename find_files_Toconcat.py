#giving a list of directories with files, print them as space separated

import os
import pandas as pd
import sys
path =[]
with open('/lustre/scratch123/tol/teams/tola/users/mu2/mitohifi-paper/new_Hymenoptera_runs/Andrena_bucephala/lista') as f:
    for l in f:
        path.append(l.rstrip("\n"))
lista=[]
for item in path:
    for root, directories, files in os.walk(item, topdown=False):
        for name in files:
            if name.endswith('mitogenome.rotated.fa'):
                lista.append(os.path.join(root, name))
print(*lista)
for i in lista:
        print(i)
