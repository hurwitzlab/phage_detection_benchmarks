#!/usr/bin/env bash

# Activate a conda environment
source activate ./env
#in_file='../../data/selected_frags_small/viral/5000/selected_frags.fasta'
in_file='../../data/refseq/bacteria/GCF_902703185.1_PcyII-29_genomic.fna'
python3 VIBRANT/VIBRANT_run.py -i $in_file -folder my_output
