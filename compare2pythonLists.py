# Assuming you have two files named 'file1.txt' and 'file2.txt'

# Read contents of file 1 into a Python list
with open('/lustre/scratch123/tol/teams/tola/users/mu2/mollusca/ALG/for_syngraphsfrom260124-complete-chr/ls1', 'r') as file1:
    content1 = file1.read().splitlines()

# Read contents of file 2 into a Python list
with open('/lustre/scratch123/tol/teams/tola/users/mu2/mollusca/ALG/busco_analyses/all.txt', 'r') as file2:
    content2 = file2.read().splitlines()

# Convert lists to sets to find unique elements
unique_to_file1 = set(content1) - set(content2)
unique_to_file2 = set(content2) - set(content1)
common_elements = set(content1) & set(content2)

# Print the results
print("Unique to file 1:", list(unique_to_file1))
print("Unique to file 2:", list(unique_to_file2))
print("Common elements:", list(common_elements))
