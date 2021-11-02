#!/usr/bin/env bash

# Concatenate the various sequence files from VirSorter

VIR_OUT_DIR=$1

cd $VIR_OUT_DIR

# Remove previous file if present
if [[ -f "combined_sequences.txt" ]]; then
    rm "combined_sequences.txt"
fi

# Begin sequences file
echo "sequences" > combined_sequences.txt

for prefix in "VIRSorter_cat-" "VIRSorter_prophages_cat-"; do
    # File name category number depends on prefix
    if [ $prefix == 'VIRSorter_cat-' ]; then
        categories=(1 2 3)
    else
        categories=(4 5 6)
    fi

    for category in ${categories[@]}; do
        file=${prefix}${category}.fasta

        grep ">" $file |
        sed 's/>//' |
        sed 's/VIRSorter_//' >> combined_sequences.txt
    done
done