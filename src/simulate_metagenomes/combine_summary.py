#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-03-16
Purpose: Combine summary files
"""

import argparse
import os
import pandas as pd
import re
import sys
from typing import List, NamedTuple, Optional, TextIO, Tuple


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[TextIO]
    regex: str
    out_dir: str


class Nameparts(NamedTuple):
    """ Extracted parts of filename """
    filename: str
    profile: str
    model: Optional[str]


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Combine summary files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'files',
        help='Summary files',
        metavar='FILE',
        type=argparse.FileType('rt'),
        nargs='+',
    )

    parser.add_argument('-r',
                        '--regex',
                        help='Filename regular expression',
                        metavar='STR',
                        type=str,
                        required=True)

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='DIR',
                        type=str,
                        default='out')

    args = parser.parse_args()

    return Args(args.files, args.regex, args.outdir)


# --------------------------------------------------
def main() -> None:
    """ Come together, right now, over me """

    args = get_args()
    out_dir = args.out_dir

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    out_df, filename = concat_files(args.regex, args.files)

    out_file = make_filename(out_dir, filename)

    out_df.to_csv(out_file, index=False)

    print(f'Done. Wrote output to {out_file}')


# --------------------------------------------------
def concat_files(regex: str, files: List[TextIO]) -> Tuple[pd.DataFrame, str]:
    """ Concatenate files into single dataframe """

    dfs = []

    for file in files:
        parts = match_regex(regex, file.name)

        df = pd.read_csv(file)

        df['profile'] = parts.profile

        if parts.model:
            df['model'] = parts.model

        dfs.append(df)

    out_df = pd.concat(dfs, ignore_index=True)

    return out_df, parts.filename


# --------------------------------------------------
def match_regex(regex: str, filename: str) -> Nameparts:
    """ Use supplied regex to extract parts of filename """

    compiled_re = re.compile(regex)

    for group in 'filename', 'profile':
        if group not in compiled_re.groupindex:
            sys.exit(f'--regex "{regex}" missing "{group}" group.')

    basename = os.path.basename(filename)
    match = re.match(compiled_re, basename)

    if not match:
        sys.exit(f'--regex "{regex}" did not match filename "{basename}".')

    match_filename = match.group('filename')
    match_profile = match.group('profile')

    if 'model' in compiled_re.groupindex:
        match_model = match.group('model')
    else:
        match_model = None

    return Nameparts(match_filename, match_profile, match_model)


# --------------------------------------------------
def test_match_regex() -> None:
    """ Test match_regex() """

    profile = 'profile_1_profile_comparison.csv'
    profile_re = (r'(?P<profile>\w+)_(?P<filename>profile_comparison).csv')
    profile_exp = Nameparts('profile_comparison', 'profile_1', None)

    assert match_regex(profile_re, profile) == profile_exp

    contigs = 'profile_1_miseq_contig_summary.csv'
    contigs_re = (r'(?P<profile>\w+)_'
                  r'(?P<model>\w+)_'
                  r'(?P<filename>contig_summary).csv')
    contigs_exp = Nameparts('contig_summary', 'profile_1', 'miseq')

    assert match_regex(contigs_re, contigs) == contigs_exp

    blast = 'profile_1_miseq_parsed_blast.csv'
    blast_re = (r'(?P<profile>\w+)_'
                r'(?P<model>\w+)_'
                r'(?P<filename>parsed_blast).csv')
    blast_exp = Nameparts('parsed_blast', 'profile_1', 'miseq')

    assert match_regex(blast_re, blast) == blast_exp


# --------------------------------------------------
def make_filename(out_dir: str, filename: str) -> str:
    """ Make output filename """

    out_file = os.path.join(out_dir, 'combined_' + filename + '.csv')

    return out_file


# --------------------------------------------------
def test_make_filename() -> None:
    """ Test make_filename() """

    assert make_filename('out',
                         'parsed_blast') == 'out/combined_parsed_blast.csv'
    assert make_filename('out',
                         'contig_summary') == 'out/combined_contig_summary.csv'
    assert make_filename(
        'out', 'profile_comparison') == 'out/combined_profile_comparison.csv'


# --------------------------------------------------
if __name__ == '__main__':
    main()
