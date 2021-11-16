#!/usr/bin/env bash

source activate ./env

IN_FILE="../../data/selected_frags_small/viral/500/selected_frags.fasta"

./run_virfinder.R -o example_out $IN_FILE
