with open("input.txt", "r") as input_file:
    lines = input_file.readlines()

# Remove newline characters from each line
lines = [line.strip() for line in lines]

with open("output.txt", "w") as output_file:
    output_file.write(",".join(lines))
