#!/usr/bin/env bash

in_fasta="../../data/selected_frags_small/bacteria/5000/selected_frags.fasta"
out_dir="../../data/classified_chopped_small/bacteria/5000/phispy_out"
convert="../../src/pre_proc/fa_to_gb.py"
prokka_env="../prokka/env"

# Annotate using prokka
source activate $prokka_env

prokka $in_fasta --outdir $out_dir --force --prefix prokka_out

source deactivate

#$convert $in_fasta -o $out_dir

source activate ./env

PhiSpy.py -o $out_dir $out_dir/prokka_out.gbk -u 100
