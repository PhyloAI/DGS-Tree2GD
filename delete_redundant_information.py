# -*- coding: utf-8 -*-
import os
import sys

def process_files(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".cds") or filename.endswith(".pep"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)

            with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
                for line in f_in:
                    if line.startswith('>'):
                        seq_name, _ = line.split(' ', 1)  # Split by space and discard the rest
                        f_out.write(seq_name + '\n')
                    else:
                        f_out.write(line)

def main():
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python remove.py <input directory> <output directory>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    
    process_files(input_folder, output_folder)

if __name__ == "__main__":
    main()
