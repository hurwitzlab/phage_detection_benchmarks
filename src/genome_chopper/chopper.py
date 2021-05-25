#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-05-25
Purpose: Chop a genome into simulated contigs
"""

import argparse
from Bio import SeqIO
import os
import sys
from typing import List, NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    genome: List[TextIO]
    out_dir: str
    length: int
    overlap: int


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Chop a genome into simulated contigs',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('genome',
                        metavar='FILE',
                        help='Input DNA file(s)',
                        type=argparse.FileType('rt'),
                        nargs='+')

    parser.add_argument('-o',
                        '--out_dir',
                        help='Output directory',
                        metavar='DIR',
                        type=str,
                        default='out')

    parser.add_argument('-l',
                        '--length',
                        help='Segment length (b)',
                        metavar='INT',
                        type=int,
                        default='100')

    parser.add_argument('-v',
                        '--overlap',
                        help='Overlap length (b)',
                        metavar='INT',
                        type=int,
                        default='10') 

    args = parser.parse_args()

    if args.length <= 0:
        parser.error(f'length "{args.length}" must be greater than 0')

    if args.overlap > args.length:
        parser.error(f'overlap "{args.overlap}" cannot be greater than length "{args.length}"')

    return Args(args.genome, args.out_dir, args.length, args.overlap)


# --------------------------------------------------
def warn(msg) -> None:
    """ Print a message to STDERR """
    print(msg, file=sys.stderr)


# --------------------------------------------------
def die(msg='Fatal error') -> None:
    """ warn() and exit with error """
    warn(msg)
    sys.exit(1)


# --------------------------------------------------
def main() -> None:
    """ The good stuff """

    args = get_args()
    files = args.genome
    out_dir = args.out_dir
    length = args.length
    overlap = args.overlap

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    for fh in files:
        for seq_record in SeqIO.parse(fh, "fasta"):
            
            seq_len = len(seq_record)
            min_overlap = 2*length - seq_len

            if length >= seq_len:
                die(f'Error: length "{length}" greater than sequence ({seq_record.id}) length ({seq_len})')
            elif overlap < min_overlap:
                die(f'Error: overlap "{overlap}" less than minimum overlap: {min_overlap} \n\tminimum overlap =  2 * length - seq_len (2*{length}-{seq_len}={min_overlap})')



# --------------------------------------------------
if __name__ == '__main__':
    main()
