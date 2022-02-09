#!/usr/bin/env bash

infile='../../data/selected_frags_small/viral/5000/selected_frags.fasta'
hmm_db='./nbc_hmms.hmm'
out_dir='./out'

viralverify -f $infile --hmm $hmm_db -o $out_dir
