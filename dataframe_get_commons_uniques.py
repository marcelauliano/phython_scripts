import pandas as pd
import argparse

parser= argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help= "Get common and unique values from two panda dataframe columns")
parser.add_argument("-d1", help= "-d1: dataframe 1", required = "True")
parser.add_argument("-d2", help= "-d2: dataframe 2", required = "True")
parser.add_argument('-oc', help='Output a table for the common values', required=False)
parser.add_argument('-od1', help='Output a table for values unique to dataframe1', required=False)
parser.add_argument('-od2', help='Output a table for values unique to dataframe2', required=False)
args = parser.parse_args()


df1=pd.read_csv(args.d1, names=['Column1'])
df2=pd.read_csv(args.d2, names=['Column2'])

df1['Column1'] = df1['Column1'].str.strip()
df2['Column2'] = df2['Column2'].str.strip()

# (i) Show common values
common_values = pd.merge(df1, df2, left_on='Column1', right_on='Column2', how='inner')
print("Common Values:")
print(common_values)

# (ii) Show values only on DataFrame 1
df1_only = pd.merge(df1, df2, left_on='Column1', right_on='Column2', how='left')
df1_only = df1_only[df1_only['Column2'].isnull()]
df1_only.drop('Column2', axis=1, inplace=True)
print("Values only in DataFrame 1:")
print(df1_only)

# (iii) Show values only on DataFrame 2
df2_only = pd.merge(df1, df2, left_on='Column1', right_on='Column2', how='right')
df2_only = df2_only[df2_only['Column1'].isnull()]
df2_only.drop('Column1', axis=1, inplace=True)
print("Values only in DataFrame 2:")
print(df2_only)

# Access the optional file argument
if args.oc:
    common_values.to_csv('common_values.txt', index=False, sep="\t")
if args.od1:
    df1_only.to_csv('df1_only.txt', index=False, sep="\t")
if args.od2:
    df2_only.to_csv('df2_only.txt', index=False, sep="\t")
