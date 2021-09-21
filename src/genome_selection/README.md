# Genome Selection

`genome_selector.py` selects `-n` random FASTA (.fna) files from a specified directory (`dir`). All records from the selected files are written to a single output file `{--out}`/*selected_genomes.fasta*. A text file, `{--out}`/*selected_genome_files.txt* is also written containing the names of all files from which the records were drawn.

## Usage

```console
$ ./genome_selector.py --help
usage: genome_selector.py [-h] [-o dir] [-n int] [-s] dir

Select genomes for analysis

positional arguments:
  dir                Directory containing genome files (.fna)

optional arguments:
  -h, --help         show this help message and exit
  -o dir, --out dir  Output directory (default: out)
  -n int, --num int  Number of genomes to select (default: 1)
  -s, --seed         Use seed to fix randomness (default: False)
```

*Note*: genome FASTA files are found using a regular expression that searches for *.fna* files since this is how they come from refseq. Changes may need to be made if intended usage is changed.

## Expected behavior

```console
$ ./genome_selector.py -n 3 tests/inputs/genomes/non_viral/
Done. Wrote 3 records to out/selected_genomes.fasta.

$ ls out/
selected_genome_files.txt  selected_genomes.fasta

$ head out/selected_genomes.fasta 
>NC_023473.1 Lactobacillus novia, complete genome
TATAGAAAGACTCATAATCAATACCTTACATTAATGCTAAATTAAATTTTCATATGTAAA
AAAAAAGAAGGAAAAAAATTTATGGACCACTTTACGAATTACGCTGCTATCATATAACGT
GCTAGGGTAAAAATTGCTAGTGCTCTGAACGTGTTACGTAGTGCACCGTGATCAGGTATT
ATC
>NC_048843.1 Saccharomyces tilapia, complete genome
TATAGAAAGACTCATAATCAATACCTTACATTAATGCTAAATTAAATTTTCATATGTAAA
AAAAAAGAAGGAAAAAAATTTATGGACCACTTTACGAATTACGCTGCTATCATATAACGT
GCTAGGGTAAAAATTGCTAGTGCTCTGAACGTGTTACGTAGTGCACCGTGATCAGGTATT
ATC
```

### Number of Requested Genomes May Exceed Files

A warning is supplied, and the records of all files are returned

```console
$ ./genome_selector.py -n 10 tests/inputs/genomes/non_viral/
Number of requested genomes (10) is greater than number of files.
Returning all 6 files.
Done. Wrote 6 records to out/selected_genomes.fasta.
```