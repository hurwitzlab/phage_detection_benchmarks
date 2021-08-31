#!/bin/bash

### REQUIRED: 
### Research group/PI
###SBATCH --account=bhurwitz
### Job queue (standard|windfall|high_pri)
### If windfall, omit --account
#SBATCH --partition=windfall
### Number of nodes
#SBATCH --nodes=1
### Number of CPUs per node 
#SBATCH --ntasks=1
### Amount of memory per node
#SBATCH --mem-per-cpu=5gb
### Job walltime (HHH:MM:SS)
#SBATCH --time=72:00:00
### OPTIONAL:
### Job name
# SBATCH --job-name=Chop_genomes
### Standard output filename
# SBATCH -o out/cluster_job.out
### Standard error filename
# SBATCH -e err/cluster_job.err
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

snakemake --cluster "sbatch -p {cluster.partition} -t {cluster.time} --mem-per-cpu={cluster.mem-per} --nodes={cluster.nodes} -e {cluster.e} -o {cluster.o}" --cluster-config config/cluster.yaml -j 94 --latency-wait 15 --keep-going
