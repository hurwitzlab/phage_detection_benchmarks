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

# Source ~/.bashrc for aliases and $PATH
source ~/.bashrc

# Get current directory to help establish paths
DIR="/xdisk/bhurwitz/mig2020/rsgrps/bhurwitz/schackartk/projects/phage_finders/src/refseq_wget_jobs"

echo "CD'ing into $DIR"

cd $DIR

cd ../../data/refseq/plasmid

echo "Getting assembly summary"

wget ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/archaea/assembly_summary.txt

awk -F '\t' '{if($12=="Complete Genome") print $20}' assembly_summary.txt > assembly_summary_complete_genomes_archaea.txt

echo "Downloading genomes"

for next in $(cat assembly_summary_complete_genomes_archaea.txt); do
          wget "$next"/*genomic.fna.gz
done

echo "Done."
