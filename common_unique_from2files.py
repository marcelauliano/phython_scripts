#giving two lists in two files, find intersections and uniques in python

file1_path = '/lustre/scratch123/tol/teams/tola/users/mu2/mollusca/ALG/logs_commands/species_with_fna.txt'  # Replace with the actual path to your first file
file2_path = '/lustre/scratch123/tol/teams/tola/users/mu2/mollusca/ALG/logs_commands/folders1'  # Replace with the actual path to your second file

# Read strings from file1
with open(file1_path, 'r') as file1:
    strings1 = set(file1.read().splitlines())

# Read strings from file2
with open(file2_path, 'r') as file2:
    strings2 = set(file2.read().splitlines())

# Find common strings
common_strings = strings1.intersection(strings2)

# Find strings specific to each file
unique_strings_file1 = strings1 - strings2
unique_strings_file2 = strings2 - strings1

# Print results
print("Common Strings:")
for common_string in common_strings:
    print(common_string)

print("\nStrings Specific to File 1:")
for unique_string_file1 in unique_strings_file1:
    print(unique_string_file1)

print("\nStrings Specific to File 2:")
for unique_string_file2 in unique_strings_file2:
    print(unique_string_file2)
