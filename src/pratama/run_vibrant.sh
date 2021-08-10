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
source activate vibrant_env

# Get current directory to help establish paths
DIR="/xdisk/bhurwitz/mig2020/rsgrps/bhurwitz/schackartk/projects/phage_finders/src/pratama"

# Move to expected directory for proper sourcing
cd $DIR

# Source config file to get data and output paths
source config.txt

# Establish where results should be output
out_dir="$out_path/vibrant_out"

# Establish tool path
tool_path="$vibrant_path/VIBRANT_run.py"

# Run the tool
python3 $tool_path -i $mock_community_path -folder $out_dir

# Confirm Completion
echo "Done."
