# Inpput File Preprocessing

Simple pre-processing scripts for converting input files to the format required for the classifier tools.

## **Convert FASTA to GenBank**: `fa_to_gb.py`

Convert FASTA file(s) to GenBank format using `Bio.SeqIO.convert()`

### Usage

Print the help message

```
$ ./fa_to_gb.py --help
usage: fa_to_gb.py [-h] [-o DIR] FILE [FILE ...]

Convert from FASTA to GenBank

positional arguments:
  FILE                  FASTA file(s)

optional arguments:
  -h, --help            show this help message and exit
  -o DIR, --outdir DIR  Output directory (default: out)
```

Usage example
```
$ ./fa_to_gb.py tests/inputs/input2.fasta
Wrote 1 converted record to out/input2.gb
Done. Wrote 1 file to out.

$ head tests/inputs/input2.fasta 
>NC_001367.1 Tobacco mosaic virus, complete genome
GTATTTTTACAACAATTACCAACAACAACAAACAACAAACAACATTACAATTACTATTTACAATTACAAT
GGCATACACACAGACAGCTACCACATCAGCTTTGCTGGACACTGTCCGAGGAAACAACTCCTTGGTCAAT
GATCTAGCAAAGCGTCGTCTTTACGACACAGCGGTTGAAGAGTTTAACGCTCGTGACCGCAGGCCCAAGG
TGAACTTTTCAAAAGTAATAAGCGAGGAGCAGACGCTTATTGCTACCCGGGCGTATCCAGAATTCCAAAT
TACATTTTATAACACGCAAAATGCCGTGCATTCGCTTGCAGGTGGATTGCGATCTTTAGAACTGGAATAT
CTGATGATGCAAATTCCCTACGGATCATTGACTTATGACATAGGCGGGAATTTTGCATCGCATCTGTTCA
AGGGACGAGCATATGTACACTGCTGCATGCCCAACCTGGACGTTCGAGACATCATGCGGCACGAAGGCCA
GAAAGACAGTATTGAACTATACCTTTCTAGGCTAGAGAGAGGGGGGAAAACAGTCCCCAACTTCCAAAAG
GAAGCATTTGACAGATACGCAGAAATTCCTGAAGACGCTGTCTGTCACAATACTTTCCAGACAATGCGAC

$ head -20 out/input2.gb 
LOCUS       NC_001367.1             6395 bp    DNA              UNK 01-JAN-1980
DEFINITION  NC_001367.1 Tobacco mosaic virus, complete genome.
ACCESSION   NC_001367
VERSION     NC_001367.1
KEYWORDS    .
SOURCE      .
  ORGANISM  .
            .
FEATURES             Location/Qualifiers
ORIGIN
        1 gtatttttac aacaattacc aacaacaaca aacaacaaac aacattacaa ttactattta
       61 caattacaat ggcatacaca cagacagcta ccacatcagc tttgctggac actgtccgag
      121 gaaacaactc cttggtcaat gatctagcaa agcgtcgtct ttacgacaca gcggttgaag
      181 agtttaacgc tcgtgaccgc aggcccaagg tgaacttttc aaaagtaata agcgaggagc
      241 agacgcttat tgctacccgg gcgtatccag aattccaaat tacattttat aacacgcaaa
      301 atgccgtgca ttcgcttgca ggtggattgc gatctttaga actggaatat ctgatgatgc
      361 aaattcccta cggatcattg acttatgaca taggcgggaa ttttgcatcg catctgttca
      421 agggacgagc atatgtacac tgctgcatgc ccaacctgga cgttcgagac atcatgcggc
      481 acgaaggcca gaaagacagt attgaactat acctttctag gctagagaga ggggggaaaa
      541 cagtccccaa cttccaaaag gaagcatttg acagatacgc agaaattcct gaagacgctg
```

The program can also take multiple files
```
$ ./fa_to_gb.py tests/inputs/input*.fasta
Wrote 2 converted records to out/input1.gb
Wrote 1 converted record to out/input2.gb
Done. Wrote 2 files to out.
```

This program is safe even for very large files. Since it uses `Bio.SeqIO.convert`, whole files are never read into memory, instead the `SeqRecord` iterator is used to get the records for conversion individually.

### Tests

The test suite can be run as
```
$ make test
python3 -m pytest -xv --flake8 --pylint --mypy
============================== test session starts ==============================
platform linux -- Python 3.9.6, pytest-6.2.4, py-1.10.0, pluggy-0.13.1 -- /home/ken/mambaforge/bin/python3
cachedir: .pytest_cache
rootdir: /home/ken/documents/research/challenging-phage-finders/src/pre_proc
plugins: flake8-1.0.7, mypy-0.8.1, pylint-0.18.0
collected 13 items     
--------------------------------------------------------------------------------
Linting files
..
--------------------------------------------------------------------------------

fa_to_gb.py::PYLINT PASSED                                                [  7%]
fa_to_gb.py::mypy PASSED                                                  [ 15%]
fa_to_gb.py::mypy-status PASSED                                           [ 23%]
fa_to_gb.py::FLAKE8 PASSED                                                [ 30%]
tests/fa_to_gb_test.py::PYLINT PASSED                                     [ 38%]
tests/fa_to_gb_test.py::mypy PASSED                                       [ 46%]
tests/fa_to_gb_test.py::FLAKE8 PASSED                                     [ 53%]
tests/fa_to_gb_test.py::test_exists PASSED                                [ 61%]
tests/fa_to_gb_test.py::test_usage PASSED                                 [ 69%]
tests/fa_to_gb_test.py::test_bad_file PASSED                              [ 76%]
tests/fa_to_gb_test.py::test_runs_file1 PASSED                            [ 84%]
tests/fa_to_gb_test.py::test_runs_file2 PASSED                            [ 92%]
tests/fa_to_gb_test.py::test_runs_multiple PASSED                         [100%]
===================================== mypy =====================================

Success: no issues found in 2 source files
============================== 13 passed in 5.19s ==============================