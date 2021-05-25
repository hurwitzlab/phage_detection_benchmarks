#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-05-25
Purpose: Chop a genome into simulated contigs
"""

import argparse
import os
from typing import List, NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    genome: List[TextIO]
    out_dir: str


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

    args = parser.parse_args()

    return Args(args.genome, args.out_dir)


# --------------------------------------------------
def main() -> None:
    """ The good stuff """

    args = get_args()
    files = args.genome
    out_dir = args.out_dir

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    for fh in files:
        print(f'Genome file is {fh.name}')

# --------------------------------------------------
if __name__ == '__main__':
    main()
