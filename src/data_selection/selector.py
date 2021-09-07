#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-09-02
Purpose: Select genome fragments for analysis
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
    level: str
    replace: bool


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Select genome fragments for analysis',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dir',
                        help='Directory containing genome fragment files',
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
                        help='Number of fragments to select',
                        metavar='int',
                        type=int,
                        default=3)

    parser.add_argument('-l',
                        '--level',
                        help='Level at which to sample',
                        metavar='int',
                        type=str,
                        choices=['file', 'fragment'],
                        default='file')

    parser.add_argument('-r',
                        '--replace',
                        help='Randomly select files with replacement',
                        action='store_true')

    parser.add_argument('-s',
                        '--seed',
                        help='Use seed to fix randomness',
                        action='store_true')

    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        parser.error(f'Input directory "{args.dir}" does not exist.')

    if args.num <= 0:
        parser.error(f'Number of fragments ({args.num})'
                     f' must be greater than 0')

    if args.replace and not args.level == 'file':
        parser.error('--replace can only be used when --level is "file".')

    return Args(args.dir, args.num, args.seed,
                args.out, args.level, args.replace)


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
    frag_files = [fn for fn in filepaths if fnmatch.fnmatch(fn, '*.fasta')]

    frag_recs = []

    for fh in frag_files:

        for seq_record in SeqIO.parse(fh, "fasta"):

            frag_recs.append(seq_record)

    if num_frags >= len(frag_recs):
        warn(f'Requested number of fragments ({num_frags}) '
             f'is greater than number of fragments present.\n'
             f'Returning all {len(frag_recs)} fragments.')

        chosen = frag_recs
    else:
        chosen = random.sample(frag_recs, k=num_frags)

    out_file = os.path.join(out_dir, 'selected_frags.fasta')

    n_rec = SeqIO.write(chosen, out_file, 'fasta')

    print(f'Done. Wrote {n_rec} records to {out_file}.')


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
if __name__ == '__main__':
    main()
