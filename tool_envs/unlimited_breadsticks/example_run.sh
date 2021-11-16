#!/usr/bin/env bash

breadsticks="Cenote_Unlimited_Breadsticks/unlimited_breadsticks.py"
input="../../data/selected_frags_small/viral/5000/selected_frags.fasta"
out_name="breadsticks_example_out_viral_5000"

python3 $breadsticks -c $input -r $out_name --minimum_length_linear 1 -p False -m 5 -t 8
