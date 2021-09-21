#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-09-02
Purpose: Select genomes for read simulation
"""

import argparse
import fnmatch
import os
import random
import sys
from Bio import SeqIO
from typing import NamedTuple


class Args(NamedTuple):
    """ Command-line arguments """
    dir: str
    num: int
    seed: bool
    out: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Select genome fragments for analysis',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dir',
                        help='Directory containing genome files',
                        metavar='dir',
                        type=str,
                        default=None)

    parser.add_argument('-o',
                        '--out',
                        help='Output directory',
                        metavar='dir',
                        type=str,
                        default='out')

    parser.add_argument('-n',
                        '--num',
                        help='Number of genomes to select',
                        metavar='int',
                        type=int,
                        default=1)

    parser.add_argument('-s',
                        '--seed',
                        help='Use seed to fix randomness',
                        action='store_true')

    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        parser.error(f'Input directory "{args.dir}" does not exist.')

    if args.num <= 0:
        parser.error(f'Number of genomes ({args.num})'
                     f' must be greater than 0')

    return Args(args.dir, args.num, args.seed,
                args.out)


# --------------------------------------------------
def main() -> None:
    """ Where the magic happens """

    args = get_args()
    in_dir = args.dir
    num_frags = args.num
    out_dir = args.out

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    if args.seed:
        random.seed(123)

    filenames = os.listdir(in_dir)
    filepaths = [os.path.join(in_dir, fn) for fn in filenames]
    fasta_files = [fn for fn in filepaths if fnmatch.fnmatch(fn, '*.fna')]

    chosen_genomes, chosen_files = select_genomes(fasta_files, num_frags)

    out_fasta = os.path.join(out_dir, 'selected_genomes.fasta')
    out_txt = os.path.join(out_dir, 'selected_genome_files.txt')

    n_rec = SeqIO.write(chosen_genomes, out_fasta, 'fasta')

    with open(out_txt, 'w') as output:
        for f in chosen_files:
            output.write(f+'\n')

    print(f'Done. Wrote {n_rec} records to {out_fasta}.')


# --------------------------------------------------
def warn(msg) -> None:
    """ Warn with a messsage """
    print(msg, file=sys.stderr)


# --------------------------------------------------
def die(msg='Error') -> None:
    """ warn() and exit """
    warn(msg)
    sys.exit(1)


# --------------------------------------------------
def select_genomes(files, num) -> tuple:
    """ Make genome selection """

    chosen_files = select_files(files, num)

    chosen_genomes = []

    for fh in chosen_files:

        for seq_record in SeqIO.parse(fh, 'fasta'):
            chosen_genomes.append(seq_record)

    return chosen_genomes, chosen_files


# --------------------------------------------------
def select_files(files, num) -> list:
    """ Make file selection"""

    if num > len(files):
        warn(f'Number of requested genomes ({num}) '
             f'is greater than number of files.\n'
             f'Returning all {len(files)} files.')

        chosen_files = files

    else:
        chosen_files = random.sample(files, k=num)

    return chosen_files


# --------------------------------------------------
if __name__ == '__main__':
    main()
