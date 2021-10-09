#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-10-08
Purpose: Post processing DeepVirFinder predictions
"""

import argparse
# import pandas as pd
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO
    out_dir: str
    length: int
    actual: str
    tool: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Post processing DeepVirFinder predictions',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='DVF Predictions',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default=None)

    parser.add_argument('-o',
                        '--out_dir',
                        help='Output directory',
                        metavar='str',
                        type=str,
                        default='out')

    parser.add_argument('-l',
                        '--length',
                        help='Length of fragments',
                        metavar='LENGTH',
                        type=int,
                        choices=[500, 1000, 3000, 5000],
                        required=True)

    parser.add_argument('-a',
                        '--actual',
                        help='True classification',
                        metavar='CLASS',
                        type=str,
                        choices=['archaea', 'bacteria', 'fungi', 'viral'],
                        required=True)

    parser.add_argument('-t',
                        '--tool',
                        help='Classifier tool',
                        metavar='TOOL',
                        type=str,
                        choices=['dvf', 'seeker'],
                        required=True)

    args = parser.parse_args()

    return Args(args.file, args.out_dir, args.length, args.actual, args.tool)


# --------------------------------------------------
def main() -> None:
    """ Do the stuff """

    args = get_args()

    tool = args.tool

    reformatted = reformatters[tool](args)

    print(reformatted)


# --------------------------------------------------
def reformat_dvf(args: Args):
    """ Reformat DeepVirFinder output """

    return args.tool


# --------------------------------------------------
def reformat_seeker(args: Args):
    """ Reformat Seeker output """

    return args.tool


reformatters = {'dvf': reformat_dvf,
                'seeker': reformat_seeker}


# --------------------------------------------------
if __name__ == '__main__':
    main()
