import sys
input_file = sys.argv[1]
output = open(sys.argv[2], "w")

with open(input_file, "r") as input_file:
    lines = input_file.readlines()

# Remove newline characters from each line
lines = [line.strip() for line in lines]

with open(output, "w") as output_file:
    output_file.write(",".join(lines))
