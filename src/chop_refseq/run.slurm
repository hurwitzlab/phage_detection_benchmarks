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
#SBATCH --ntasks=7
### Amount of memory per node
#SBATCH --mem=64gb
### Job walltime (HHH:MM:SS)
#SBATCH --time=168:00:00
### OPTIONAL:
### Job name
# SBATCH --job-name=Chop_genomes
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

# Activate a conda environment
source activate snakemake_env

# Load any necessary modules
# module load my_modules

# Get current directory to help establish paths
DIR="/xdisk/bhurwitz/mig2020/rsgrps/bhurwitz/schackartk/projects/phage_finders/src/chop_refseq/"


cd $DIR

snakemake --cluster "sbatch -A {cluster.group} -p {cluster.partition} -t {cluster.time} --mem={cluster.m}" --cluster-config config/cluster.yaml -j 60 --latency-wait 15
