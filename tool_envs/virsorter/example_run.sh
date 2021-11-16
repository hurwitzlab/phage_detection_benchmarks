#!/usr/bin/env bash

PRG="wrapper_phage_contigs_sorter_iPlant.pl"
IN="../../data/selected_frags_small/archaea/1000/selected_frags.fasta"
#IN="../../data/refseq/bacteria/GCF_904863395.1_INF250_genomic.fna"
OUT_DIR="example_out"
PREDS="example_out/Predicted_viral_sequences"
DB="./virsorter-data"

rm -rf $OUT_DIR

$PRG -f $IN --db 1 --wdir $OUT_DIR --ncpu 4 --data-dir $DB

if ! [ "$(ls -A $PREDS)" ]; then
    echo "No viruses found, creating empty output files."
    echo "sequences" > $PREDS/VIRSORTER_cat-1.fasta
    echo "sequences" > $PREDS/VIRSORTER_cat-2.fasta
    echo "sequences" > $PREDS/VIRSORTER_cat-3.fasta
    echo "sequences" > $PREDS/VIRSORTER_prophages_cat-4.fasta
    echo "sequences" > $PREDS/VIRSORTER_prophages_cat-5.fasta
    echo "sequences" > $PREDS/VIRSORTER_prophages_cat-6.fasta
fi
