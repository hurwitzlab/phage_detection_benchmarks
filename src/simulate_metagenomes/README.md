# Simulate Reads using InSilicoSeq

This is a Snakemake pipeline for generating simulated reads from reference genomes with specified abundances, and processing them for classification.

To run the full pipeline, execute:

```
$ sbatch run.slurm
```

Additional profiles can be placed in the bracken output directory (see `config/config.yaml`), and no changes need to be made to any files for the pipeline to be executed on the new profiles.

# Pipeline description

1. Generate a profile from Bracken output
2. Concatenate the genomes present in the profile to a multifasta file
3. Simulate reads using InSilicoSeq
4. Assemble contigs using MegaHit
5. Bin contigs using MetaBAT2
6. Map reads to input genomes with BLAST

The following diagram shows the main portions of the pipeline. *Note* the pipeline in this directory ends with 3 results:

* Contigs
* Bins
* Mappings

`Classification` and `assessment` will be in pipelines in their own directories. I will create a master snakemake to run all 3 pipelines in the root of this repo.

```mermaid
graph TD
    input(Bracken output) --> profiler{make_profiles};
    taxa(taxonomy.csv) --> profiler;
    profiler --> profile(profile.txt);
    profiler --> globs(files.txt);
    refseq[(local refseq)];
    cat{cat_genomes};
    globs --> cat;
    refseq ----> cat;
    cat --> genomes(genomes.fasta);
    iss{simulate_reads};
    profile --> iss;
    genomes --> iss;
    iss --> reads(reads.fastq);
    reads --> megahit{MegaHit};
    megahit --> contigs(contigs.fa);
    contigs --> metabat{MetaBAT2};
    contigs ----> tools{classifiers}
    metabat --> bins(bins)
    genomes --> dbizer{makeblastdb};
    dbizer ---> db[(BLAST DB)];
    db --> blast{BLASTn};
    contigs --> blast;
    blast --> mappings(mapped_contigs.out);
    mappings --> assess;
    bins --> marvel{MARVEL};
    subgraph classification
        marvel --> preds(predictions);
        tools --> preds;
    end
    subgraph assessment
        preds --> assess{analysis}
        assess --> results(results);
        
    end
```

## Genome Concatenation

InSiicoSeq treats each record in a multi-FASTA file as a genome, and requires a profile file giving the abundance of head record/genome. However, some genome files have multiple records (*e.g.* separated by chromosome).

The two files are created using scripts located here. First, `bracken_profiler.py` parses bracken output and creates two files: one with the profile, ready for input to InSilicoSeq, and a file with information on the genomes that need to be retrieved, such as file name globs and the record ID that was written in the profile.

Next, `cat_genomes.py` reads the information file, retrieves all the genomes in the profile, removes the record headers for each genome (except the one that matches that in the profile), and writes them all to one large file, which is the other input to InSilicoSeq

## Read Simulation

Several abundance profiles can be created, and the specified genomes must have identifiers that match those in `cat_genomes.fasta`. The list of desired abundance profiles should be given in the `--configfile`, as well as other `iss generate` parameters. Multiple error models can be automatically executed by inclusion in the config["model"] field, which currently includes all pre-built error models.

## Assembly

Megahit is used for assembling the simulated reads into contigs.

## Binning

MetaBAT2 is used for binning the contigs. Default values are used currently, since MetaBAT2 has improved default values over MetaBAT.

## BLAST alignment

To determine the true origins of the contigs, BLAST is run. Each BLAST database is created from the same file of genomes that is passed to InSilicoSeq. Therefore, each profile will have its own BLAST database, containing only those organisms that constitute the profile. This prevents spurious hits to other organisms.

BLASTn is run, querying the contigs created by MegaHit against the genomes in that profile.

# Programs

## `bracken_profiler.py`

This script takes Bracken output and creates a profile for use in ISS. Taxonomic IDs are used to join the Bracken output with my list of refseq genomes. Since not all genomes may be found, the abundances are rescaled so they still add to 1. The abundance profile is written to `*_profile.txt`.

Additionally, a file is created (`*_files.txt`) that contains acession numbers, file globs, and sequence record IDs that are in the profile. The files that match these globs are the files that contain the sequences in the profile.

Example usage
```
 $ ./bracken_profiler.py tests/inputs/bracken_profiler/input_1.txt
Making profile for file "tests/inputs/bracken_profiler/input_1.txt"...
Finished.
Done. Wrote 1 profile to out.

$ ls out/
input_1_files.txt  input_1_profile.txt

# File globs do not include the parent directory (refseq)
$ head -n 5 out/input_1_files.txt 
filename,accession
archaea/GCF_000006175.1*.fna,GCF_000006175.1
bacteria/GCF_001742205.1*.fna,GCF_001742205.1
viral/GCF_000891875.6*.fna,GCF_000891875.6
fungi/GCF_013402915.1*.fna,GCF_013402915.1

$ head -n 5 out/input_1_profile.txt
GCF_000006175.1 0.6525
GCF_001742205.1 0.21977
GCF_000891875.6 0.12644
GCF_013402915.1 0.0013
```
## `cat_genomes.py`

This script concatenates all the genomes that are required for ISS based on the profile.

There are 3 inputs:

* File containing genome information (`*_files.txt` output from `bracken_profiler.py`)
* `-p|--parent`: the parent directory from which the file globs are defined.
* `-o|--outdir`: output directory to write concatenated genomes.

The file globs are not full relative paths, such as *archaea/GCF_000006175.1\*.fna*, so the `--parent` directory is provided to complete the relative path. For instance, if `--parent` = *../../data/refseq*, the full file glob that will be used is *../../data/refseq/archaea/GCF_000006175.1\*.fna*

Example usage
```
$ ./cat_genomes.py -p tests/inputs/cat_genomes/refseq/ tests/inputs/cat_genomes/input_1_files.txt 
Concatenated 4 files to out/input_1_genomes.fasta
Done. Concatenated files for 1 profile.

$ head -n 5 out/input_1_genomes.fasta
>GCF_000006175.1
AATTTAAAGATTAAAATTAGTAGACTGTCGATTTACAATATCATATTTATGAGTAATGATAATAACATTATCAAAGTATT
ATCTAAATATTTAGATTTAATATGTTTCTCAATGGAATATGTTAAATTTTATATTTATACATTATTGTAAAATCATAAAA
ATTTTTTAGAAAAATGTCTTAATCTTGCTAATTTTTGATTTATTGCCAAAATACACATTACTCATCAAATGAAAATTAGT
TCAAATATTGTGTATAATGTCCTGTGTAATATTACAAATTACTGTATGTAATATACCGTATGCAATATACAATAGTAAAT

$ grep ">" out/input_1_genomes.fasta 
>GCF_000006175.1
>GCF_001742205.1
>GCF_000891875.6
>GCF_013402915.1
```

