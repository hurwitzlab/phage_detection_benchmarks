#!/usr/bin/env bash

# Create multifasta file with one record per input genome file

# File containing the names of files which must be concatenated
FILENAMES_FILE=$1

# Output filename
OUT_FILE=$2

# Remove old concatenated file
rm $OUT_FILE

# Remove all except the first record headers in genome file
# Write results to new file
for file in $(cat $FILENAMES_FILE); do
	BASE="$(basename -- $file)"
	FILENAME="${BASE%.*}"
	echo Concatenating $BASE
	head -n 1 $file > $FILENAME"_cat.fna"
	cat $file | grep -v ">" >> $FILENAME"_cat.fna"
done

# Concatenate all the modified genomes files into a single file
for file in `ls *_cat.fna`; do
	cat $file >> cat_genomes.fasta
done

# Remove intermediate files
rm *_cat.fna
