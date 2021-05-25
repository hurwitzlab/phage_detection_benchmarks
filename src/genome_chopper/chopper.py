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
            
            if length >= len(seq_record):
                die(f'Error: --length "{length}" greater than sequence ({seq_record.id}) length ({len(seq_record)}).')



# --------------------------------------------------
if __name__ == '__main__':
    main()
