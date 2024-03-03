#!/bin/bash

### REQUIRED: 
### Research group/PI
#SBATCH --account=bhurwitz
### Job queue (standard|windfall|high_pri)
### If windfall, omit --account
#SBATCH --partition=standard
### Number of nodes
#SBATCH --nodes=1
### Number of CPUs per node 
#SBATCH --ntasks=14
### Amount of memory per node
#SBATCH --mem=64gb
### Job walltime (HHH:MM:SS)
#SBATCH --time=24:00:00
### OPTIONAL:
### Job name
# SBATCH --job-name=wget_refseq_archea
### Standard output filename
### SBATCH -o out_filename.txt
### Standard error filename
### SBATCH -e error_filename.txt
### Email notifications (BEGIN|END|FAIL|ALL)
# SBATCH --mail-type=ALL
### Email addresss
# SBATCH --mail-user=schackartk@email.arizona.edu

KINGDOM=$1

# Source ~/.bashrc for aliases and $PATH
source ~/.bashrc

# Get current directory to help establish paths
DIR="/xdisk/bhurwitz/mig2020/rsgrps/bhurwitz/schackartk/projects/phage_finders/src/refseq_wget_jobs"

echo "CD'ing into $DIR"

cd $DIR

TARGET_DIR="../../data/refseq/$KINGDOM"

if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
fi

cd ../../data/refseq/$KINGDOM

echo "Getting assembly summary"

wget ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/$KINGDOM/assembly_summary.txt

awk -F '\t' '{if($12=="Complete Genome") print $20}' assembly_summary.txt > assembly_summary_complete_genomes_$KINGDOM.txt

echo "Downloading genomes"

while IFS= read -r next; do
    wget "$next" -O "$(basename "$next")_genomic"
    while IFS= read -r line; do
        link=$(echo "$line" | grep -oP '(?<=href=")[^"]+')

    if [[ $link == *genomic.fna.gz && $link != *from_genomic.fna.gz ]]; then
            wget "$next/$link" 
            gzip -d "$link"
        fi
    done < "$(basename "$next")_genomic"
    rm "$(basename "$next")_genomic"
done < assembly_summary_complete_genomes_"$KINGDOM".txt

echo "Done."
