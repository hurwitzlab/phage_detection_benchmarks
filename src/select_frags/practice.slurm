#!/bin/bash

### REQUIRED: 
### Research group/PI
### SBATCH --account=bhurwitz
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
#SBATCH --time=24:00:00
### OPTIONAL:
### Job name
### SBATCH --job-name=JobName
### Standard output filename
### SBATCH -o out_filename.txt
### Standard error filename
### SBATCH -e error_filename.txt
### Email notifications (BEGIN|END|FAIL|ALL)
### SBATCH --mail-type=ALL
### Email addresss
### SBATCH --mail-user=schackartk@email.arizona.edu

# Source ~/.bashrc for aliases and $PATH
source ~/.bashrc

# Activate a conda environment
source activate snakemake_env

DIR="/xdisk/bhurwitz/mig2020/rsgrps/bhurwitz/schackartk/projects/phage_finders/src/select_frags/"

cd $DIR

# Run snakemake cluster
snakemake --cluster \
"sbatch -A {cluster.group} -p {cluster.partition} -t {cluster.time} --mem-per-cpu=5gb --nodes=1 --ntasks={cluster.ntasks} -e {cluster.e} -o {cluster.o}" \
--cluster-config config/practice_cluster.yaml -j 16 --latency-wait 15 --configfile config/practice_config.yaml
