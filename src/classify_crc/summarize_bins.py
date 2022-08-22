#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-10-12
Purpose: Create file summarizing the contents of the bins
"""

import argparse
import os
from typing import List, NamedTuple, TextIO

import pandas as pd
from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    bin_dir: str
    out_dir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Gather the contents of bins from a sample',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('bin_dir',
                        metavar='DIR',
                        help='Bin directory',
                        type=str)

    parser.add_argument('-o',
                        '--out_dir',
                        metavar='DIR',
                        help='Output directory',
                        type=str,
                        default='out')

    args = parser.parse_args()

    if not os.path.isdir(args.bin_dir):
        parser.error(f'Input directory ("{args.bin_dir}") does not exist.')

    return Args(args.bin_dir, args.out_dir)


# --------------------------------------------------
def get_bin_name(filename: str) -> str:
    """ Get bin name from file name """

    _, bin_num, _ = filename.split('.')

    return bin_num


# --------------------------------------------------
def test_get_bin_name() -> None:
    """ Test get_bin_name() """

    assert get_bin_name('bin.1.fa') == '1'
    assert get_bin_name('bin.4.fa') == '4'
    assert get_bin_name('bin.10.fa') == '10'


# --------------------------------------------------
def get_sample_name(dir: str) -> str:
    """ Get sample name from directory path """

    return os.path.basename(os.path.normpath(dir))


# --------------------------------------------------
def test_get_sample_name() -> None:
    """ Test get_sample_name() """

    assert get_sample_name('tests/inputs/zel_246/') == 'zel_246'


# --------------------------------------------------
def main() -> None:
    """ Main function """

    args = get_args()
    out_dir = args.out_dir

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    bin_files = os.scandir(args.bin_dir)

    bins = []
    contigs = []
    for bin_file in bin_files:
        bin_num = get_bin_name(bin_file.name)
        for contig in SeqIO.parse(bin_file, 'fasta'):
            bins.append(bin_num)
            contigs.append(contig.id)

    out_df = pd.DataFrame({'bin': bins, 'contig': contigs})
    out_df['sample'] = get_sample_name(args.bin_dir)

    out_file = os.path.join(out_dir, 'bin_summary.csv')
    out_df.to_csv(out_file, index=False)

    print(f'Done. Wrote output to {out_file}.')


# --------------------------------------------------
if __name__ == '__main__':
    main()
