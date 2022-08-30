#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-08-30
Purpose: Get lengths of each contig in FASTA files
"""

import argparse
import os
import pandas as pd
from typing import List, NamedTuple, TextIO
from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[TextIO]
    out_dir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Get lengths of each contig in FASTA files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('files',
                        metavar='FILE',
                        help='FASTA files',
                        type=argparse.FileType('rt'),
                        nargs='+')

    parser.add_argument('-o',
                        '--out_dir',
                        metavar='DIR',
                        help='Output directory',
                        type=str,
                        default='out')

    args = parser.parse_args()

    return Args(args.files, args.out_dir)


# --------------------------------------------------
def main() -> None:
    """ Main function """

    args = get_args()
    out_dir = args.out_dir

    contigs = []
    for file in args.files:
        sample, _ = os.path.splitext(os.path.basename(file.name))

        for rec in SeqIO.parse(file, 'fasta'):
            contigs.append(f'{sample},{rec.id},{len(rec)}')

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    out_file = os.path.join(out_dir, 'contig_lengths.csv')

    with open(out_file, 'wt') as out_fh:
        out_fh.write('\n'.join(contigs))

    print(f'Done. Wrote to {out_file}')


# --------------------------------------------------
if __name__ == '__main__':
    main()
