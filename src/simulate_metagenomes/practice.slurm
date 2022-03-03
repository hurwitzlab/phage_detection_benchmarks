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
#SBATCH --ntasks=8
### Amount of memory per node
#SBATCH --mem-per-cpu=5gb
### Job walltime (HHH:MM:SS)
#SBATCH --time=8:00:00
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

source activate ../../tool_envs/bowtie2/env

contigs='../../data/metagenome_simulation/assembled_reads/WGS_adult1_bracken_species_miseq/final.contigs.fa'
reads1='../../data/metagenome_simulation/simulated_reads/WGS_adult1_bracken_species_miseq_R1.fastq'
reads2='../../data/metagenome_simulation/simulated_reads/WGS_adult1_bracken_species_miseq_R2.fastq'

indexdir='../../data/metagenome_simulation/bowtie_indices/WGS_adult1_bracken_species_miseq'
index=$indexdir'/index'

mapdir='../../data/metagenome_simulation/bowtie_mappings'
mapfile=$mapdir'/WGS_adult1_bracken_species_miseq.sam'
sorted_bam=$mapdir'/WGS_adult1_bracken_scpecies_miseq_sorted.bam'
depthfile=$mapdir'/WGS_adult1_bracken_species_miseq_depth.txt'
bins='../../data/metagenome_simulation/binned_contigs/WGS_adult1_bracken_species_miseq/bin'

# rm -rf $indexdir
# mkdir -p $indexdir

# rm -rf $mapdir
# mkdir -p $mapdir

# bowtie2-build \
#	$contigs \
#	$index \
#	--offrate 4

# bowtie2 \
#	-x $index \
#	-1 $reads1 \
#	-2 $reads2 \
#	-p 8 \
#	-S $mapfile

# source deactivate
# source activate ../../tool_envs/samtools/env

# samtools view \
#	-u $mapfile | \
#	samtools sort \
#	-o $sorted_bam

# conda deactivate
source activate ../../tool_envs/metabat2/env

mkdir -p ../../data/metagenome_simulation/binned_contigs

# jgi_summarize_bam_contig_depths \
#	--outputDepth $depthfile \
#	$sorted_bam

metabat2 \
	-o $bins \
	-i $contigs \
	-a $depthfile

