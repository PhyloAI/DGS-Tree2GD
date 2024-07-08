# -*- coding: utf-8 -*-
import os
import sys
import shutil

def process_fasta_file(input_file, output_folder):
    sequences = {}
    
    with open(input_file, 'r') as f:
        lines = f.readlines()

    current_sequence_name = ""
    current_sequence = []  # Store current sequence content
    for line in lines:
        if line.startswith('>'):
            if current_sequence_name:
                prefix = current_sequence_name.split('@')[0][1:]  # Remove '>' from prefix
                sequences.setdefault(prefix, [])
                sequences[prefix].append((current_sequence_name, current_sequence))
                current_sequence = []  # Reset current sequence
            current_sequence_name = line.strip()  # Keep '>' in sequence name
        else:
            current_sequence.append(line)

    # Process the last sequence
    if current_sequence_name:
        prefix = current_sequence_name.split('@')[0][1:]  # Remove '>' from prefix
        sequences.setdefault(prefix, [])
        sequences[prefix].append((current_sequence_name, current_sequence))

    # Write sequences with the same prefix to the same file
    os.makedirs(output_folder, exist_ok=True)  # Create output folder
    
    for prefix, sequence_list in sequences.items():
        output_file = os.path.join(output_folder, f"{prefix}.fasta")
        with open(output_file, 'a') as f:
            for sequence_name, sequence_content in sequence_list:
                # Replace '@' with '_' in sequence name
                sequence_name = sequence_name.replace('@', '_')
                f.write(sequence_name + '\n')
                for line in sequence_content:
                    f.write(line)

def main(input_folder, output_folder):
    # Clear existing output folder
    shutil.rmtree(output_folder, ignore_errors=True)
    
    # Process all FASTA files in input_folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".fas") or file_name.endswith(".fasta"):
            input_file = os.path.join(input_folder, file_name)
            process_fasta_file(input_file, output_folder)

if __name__ == "__main__":
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python sorted_by_species.py <input directory> <output directory>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    main(input_folder, output_folder)
