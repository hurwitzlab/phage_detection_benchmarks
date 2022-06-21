#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-06-21
Purpose: Filter contigs in FASTA file by minimum length
"""

import argparse
import os
import pandas as pd
import sys
from typing import List, NamedTuple, TextIO
from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[TextIO]
    length: int
    out_dir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Filter contigs in FASTA file by minimum length',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('files',
                        metavar='FILE',
                        help='FASTA files to be filtered by length',
                        type=argparse.FileType('rt'),
                        nargs='+')

    parser.add_argument('-m',
                        '--min_length',
                        metavar='LEN',
                        help='Minimum contig length',
                        type=int,
                        default=200)

    parser.add_argument('-o',
                        '--out_dir',
                        metavar='DIR',
                        help='Output directory',
                        type=str,
                        default='out')

    args = parser.parse_args()

    if args.min_length < 1:
        parser.error(
            f'--min_length "{args.min_length}" must be greater than 1.')

    return Args(args.files, args.min_length, args.out_dir)


# --------------------------------------------------
def make_filename(outdir: str, name: str) -> str:
    """ Make output file path from outdir and original filename """

    _, basename = os.path.split(name)

    return os.path.join(outdir, basename)


# --------------------------------------------------
def test_make_filename() -> None:
    """ Test make_filename() """

    outdir = 'filtered_contigs'
    infile = 'assemblies/zeller_4506.fa'
    expected = 'filtered_contigs/zeller_4506.fa'

    assert make_filename(outdir, infile) == expected


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    out_dir = args.out_dir
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    for n_file, fh in enumerate(args.files, start=1):
        out_file = make_filename(out_dir, fh.name)
        seqs = []
        with open(out_file, 'wt') as out_fh:
            for n_seq, seq_record in enumerate(SeqIO.parse(fh, 'fasta'),
                                               start=1):
                if len(seq_record.seq) >= args.length:
                    seqs.append(seq_record)
            n_written = SeqIO.write(seqs, out_fh, 'fasta')

            plu = 's' if n_written != 1 else ''
            print(
                f'Wrote {n_written} sequence{plu} (out of {n_seq}) to {out_file}'
            )

    plu = 's' if n_file != 1 else ''
    print(f'Done. Wrote {n_file} file{plu} to {out_dir}.')


# --------------------------------------------------
if __name__ == '__main__':
    main()
