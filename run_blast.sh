#!/bin/bash

# Check if all required arguments are provided
if [ $# -ne 4 ]; then
    echo "Usage: $0 <input_fasta_file1> <output_db_path> <input_fasta_file2> <output_txt_file>"
    exit 1
fi

# Assign arguments to variables
input_fasta_file1=$1
output_db_path=$2
input_fasta_file2=$3
output_txt_file=$4

# Step 1: Create BLAST database
makeblastdb -in "$input_fasta_file1" -dbtype nucl -out "$output_db_path"

# Step 2: Run BLAST
time blastn -task blastn -query "$input_fasta_file2" -db "$output_db_path" -out "$output_txt_file" -outfmt 6 -num_threads 11
