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

    return Args(args.dir, args.num, args.seed,
                args.out, args.replace)


# --------------------------------------------------
def main() -> None:
    """ Where the magic happens """

    args = get_args()
    in_dir = args.dir
    num_frags = args.num
    out_dir = args.out
    replacement = args.replace

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    if args.seed:
        random.seed(123)

    filenames = os.listdir(in_dir)
    filepaths = [os.path.join(in_dir, fn) for fn in filenames]
    frag_files = [fn for fn in filepaths if fnmatch.fnmatch(fn, '*.fasta')]

    chosen_frags = select_frags(frag_files, num_frags, replacement)

    out_file = os.path.join(out_dir, 'selected_frags.fasta')

    n_rec = SeqIO.write(chosen_frags, out_file, 'fasta')

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
def select_frags(frag_files, num_frags, replacement) -> list:
    """ Make fragment selection """

    # Initially choose a number of files equal to number of fragments
    chosen_files = select_files(frag_files, num_frags, replacement)

    # Lists for chosen fragments and their id's for list comparison
    chosen_frags = []
    chosen_frag_ids = []

    for fh in chosen_files:

        # Randomly select fragments from each file, without repeats
        chosen_frags, chosen_frag_ids, _ = check_frags(fh,
                                                       chosen_frags,
                                                       chosen_frag_ids)

    # Use variable to track files whose fragments have not been exhausted
    unexhausted_files = frag_files

    while len(chosen_frag_ids) < num_frags and replacement:

        fh = random.choice(unexhausted_files)

        chosen_frags, chosen_frag_ids, exhausted = check_frags(fh,
                                                               chosen_frags,
                                                               chosen_frag_ids)

        if exhausted:
            unexhausted_files.remove(fh)

        if len(unexhausted_files) == 0:
            warn(f'Directory does not have {num_frags} unique fragments. '
                 f'Returning {len(chosen_frag_ids)} fragments.')
            break

    return chosen_frags


# --------------------------------------------------
def select_files(frag_files, num_frags, replacement) -> list:
    """ Make file selection"""

    if replacement:
        chosen_files = random.choices(frag_files, k=num_frags)

    elif not replacement and num_frags > len(frag_files):
        warn(f'Number of requested fragments ({num_frags}) '
             f'is greater than number of files.\n'
             f'Consider allowing --replacement. '
             f'Returning 1 fragment from all '
             f'{len(frag_files)} files.')

        chosen_files = frag_files

    else:
        chosen_files = random.sample(frag_files, k=num_frags)

    return chosen_files


# --------------------------------------------------
def check_frags(fh, chosen_frags, chosen_frag_ids) -> tuple:
    """ Try to find unique frag in file """

    frag_recs = []

    for seq_record in SeqIO.parse(fh, 'fasta'):
        frag_recs.append(seq_record)

    if all(frag.id in chosen_frag_ids for frag in frag_recs):
        exhausted = True
        return chosen_frags, chosen_frag_ids, exhausted

    exhausted = False

    chosen_frag = random.choice(frag_recs)

    while chosen_frag.id in chosen_frag_ids:
        chosen_frag = random.choice(frag_recs)

    chosen_frags.append(chosen_frag)
    chosen_frag_ids.append(chosen_frag.id)

    return chosen_frags, chosen_frag_ids, exhausted


# --------------------------------------------------
if __name__ == '__main__':
    main()
