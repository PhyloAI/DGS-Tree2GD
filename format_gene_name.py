# -*- coding: utf-8 -*-
import os
import sys

def process_fasta_file(input_file, output_folder):
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_folder, f"output_{file_name}.fasta")
    
    with open(input_file, 'r') as f:
        lines = f.readlines()

    output_sequences = []
    for line in lines:
        if line.startswith('>'):
            line = line.strip() + f"_{file_name}\n"
        output_sequences.append(line)

    with open(output_file, 'w') as f:
        for line in output_sequences:
            f.write(line)

def main(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".fasta"):
            input_file = os.path.join(input_folder, file_name)
            process_fasta_file(input_file, output_folder)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python add_gene_name.py input_directory output_directory")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    main(input_folder, output_folder)
