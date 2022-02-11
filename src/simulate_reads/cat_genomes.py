#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-02-10
Purpose: Concatenate genomes from profile into single multifasta
"""

import argparse
from glob import glob
import os
import pandas as pd
import re
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    globs: TextIO
    parent: str
    outdir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Concatenate genomes from profile into single multifasta',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('globs',
                        help='File containing genome information',
                        metavar='FILE',
                        type=argparse.FileType('rt'))

    parser.add_argument('-p',
                        '--parent',
                        help='Directory prepended to file globs',
                        metavar='DIR',
                        type=str,
                        default='../../data/refseq')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='DIR',
                        type=str,
                        default='out')

    args = parser.parse_args()

    return Args(args.globs, args.parent, args.outdir)


# --------------------------------------------------
def main() -> None:
    """ Don't worry, be happy """

    args = get_args()
    parent = args.parent
    out_dir = args.outdir
    in_fh = args.globs

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    out_fh = open(make_filename(out_dir, in_fh.name), 'wt')

    genomes = get_matches(parent, parse_globfile(in_fh))

    n_files = 0
    for _, row in genomes.iterrows():
        n_files += 1
        cat_genome(row.filename, row.seq_id, out_fh)

    out_fh.close()

    plu = 's' if n_files != 1 else ''
    print(f'Done. Concatenated {n_files} file{plu} to {out_fh.name}')


# --------------------------------------------------
def make_filename(out_dir: str, in_file: str) -> str:
    """ Make output filename """

    root_name, _ = os.path.splitext(os.path.basename(in_file))

    root_name = root_name.replace('_files', '')

    out_file = os.path.join(out_dir, root_name + '_genomes.fasta')

    return out_file


# --------------------------------------------------
def test_make_filename() -> None:
    """ Test make_filename() """

    assert make_filename('out',
                         'input_1_files.txt') == 'out/input_1_genomes.fasta'
    assert make_filename(
        'out', 'tests/input_1_files.txt') == 'out/input_1_genomes.fasta'


# --------------------------------------------------
def parse_globfile(fh: TextIO) -> pd.DataFrame:
    """ Get filenames that match the globs """

    df = pd.read_csv(fh)

    df.rename(columns={'filename': 'partial_glob'}, inplace=True)

    return df


# --------------------------------------------------
def get_matches(parent: str, df: pd.DataFrame) -> pd.DataFrame:
    """ Get filenames that match the globs """

    df['glob'] = list(
        map(lambda s: os.path.join(parent, s), df['partial_glob']))

    df = df.reset_index()

    for index, row in df.iterrows():
        file_glob = row['glob']
        file_match = glob(file_glob)
        if file_match:
            df.at[index, 'filename'] = file_match[0]
            if len(file_match) > 1:
                print(f'Warning: multiple files match "{file_glob}":')
                print('\t', end='')
                print('\n\t'.join(file_match))
                print(f'Using {file_match[0]}')
        else:
            print(f'Warning: no files match glob "{file_glob}"')

    return df


# --------------------------------------------------
def cat_genome(file_name: str, seq_id: str, out_fh: TextIO) -> None:
    """ Concatenate genome file to output file """

    contents = open(file_name, 'rt').read()

    header_match = re.search(f'^.{seq_id}.*$', contents, re.MULTILINE)

    out_fh.write(header_match[0] + '\n')

    for line in contents.split('\n'):
        if ">" not in line:
            out_fh.write(line + '\n')


# --------------------------------------------------
if __name__ == '__main__':
    main()
