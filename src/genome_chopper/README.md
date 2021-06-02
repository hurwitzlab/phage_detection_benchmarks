# genome_chopper

Create simulated assemblies from reference genome by chopping.

## Motivation

The effect of read errors on phage identification tools will be assessed through read simulation methods, such as with [InSilicoSeq](https://github.com/HadrienG/InSilicoSeq). However, we would also like to assess the effect of contig assembly size directly.

To achieve this, we can cut the genome into smaller substrings, which would be analogous to contigs assembled from reads.

## Method

The genome is input as FASTA file. Genome is then cut into small, overlapping pieces. These chopped genomes are output.

# Usage

```console
$ ./chopper.py

usage: chopper.py [-h] [-o DIR] [-l INT] [-v INT] FILE [FILE ...]

Chop a genome into simulated contigs

positional arguments:
  FILE                  Input DNA file(s), each with only 1 record

optional arguments:
  -h, --help            show this help message and exit
  -o DIR, --out_dir DIR
                        Output directory (default: out)
  -l INT, --length INT  Segment length (b) (default: 100)
  -v INT, --overlap INT
                        Overlap length (b) (default: 10)
```

## Input

Input files must be FASTA format. Multiple input files are allowed.

## Output

For each input file 2 files are generated: a FASTA file and a .tsv file.

The FASTA file contains all fragments generated from the input file. Each record corresponds to a fragment. Fragments are named based on the input record id followed by "_fragn" where n is the nth fragment generated from the input sequence.

The .tsv file contains metadata about the fragments. It is formatted in a table, with the first row being a header, and each subsequent row corresponding to a fragment. Information includes parent sequence and where on that sequence the fragment is located.

## Parameters

`-l|--length`: length of the fragments to be generated in number of nucleotides

`-v|--overlap`: amount of overlap between adjacent fragments in nucleotides

**Note:** When generating long fragments from short sequences, there is a limit to how small the overlap can be. 

*Minimum overlap = 2 * (fragment length) - (input sequence length)*. If the provided overlap is below the minimum, an error message is generated.

# Authorship

Kenneth Schackart (schackartk1@gmail.com)