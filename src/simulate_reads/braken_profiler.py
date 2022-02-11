#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-02-09
Purpose: Create profile from Braken output
"""

import argparse
import os
import pandas as pd
from typing import NamedTuple, TextIO, Tuple

pd.options.mode.chained_assignment = None


class Args(NamedTuple):
    """ Command-line arguments """
    braken: TextIO
    taxonomy: TextIO
    outdir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Create profile from Braken output',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('braken',
                        metavar='FILE',
                        help='Braken output file',
                        type=argparse.FileType('rt'))

    parser.add_argument('-t',
                        '--taxonomy',
                        metavar='FILE',
                        help='Taxonomy mapping file',
                        type=argparse.FileType('rt'),
                        default='../../data/refseq_info/taxonomy.csv')

    parser.add_argument('-o',
                        '--outdir',
                        metavar='DIR',
                        help='Output directory',
                        type=str,
                        default='out')

    args = parser.parse_args()

    return Args(args.braken, args.taxonomy, args.outdir)


# --------------------------------------------------
def main() -> None:
    """ Do the stuff """

    args = get_args()
    out_dir = args.outdir

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    braken_df = clean_braken(pd.read_csv(args.braken, sep='\t'))
    taxonomy_df = clean_taxonomy(pd.read_csv(args.taxonomy))

    joined_df = join_dfs(braken_df, taxonomy_df)

    joined_df['rescaled_abundance'] = rescale_abundances(
        joined_df['fraction_total_reads'])

    files_df = make_files_df(joined_df)
    profile_df = make_profile_df(joined_df)

    files_output, profile_output = make_filenames(args.braken.name, out_dir)

    files_df.to_csv(files_output, sep=",", index=False)
    profile_df.to_csv(profile_output, sep="\t", index=False, header=False)

    print(f'Done. Wrote output files to "{out_dir}".')


# --------------------------------------------------
def clean_braken(df: pd.DataFrame) -> pd.DataFrame:
    """ Clean braken output dataframe """

    df = df[df['fraction_total_reads'] > 0.]

    df.drop([
        'taxonomy_lvl', 'kraken_assigned_reads', 'added_reads', 'new_est_reads'
    ],
            axis='columns',
            inplace=True)

    df.sort_values('fraction_total_reads')

    return df


# --------------------------------------------------
def clean_taxonomy(df: pd.DataFrame) -> pd.DataFrame:
    """ Clean taxonomy dataframe """

    df = df[['kingdom', 'accession', 'taxid', 'seq_id']]

    # There may be multiple reseq files (accession #)
    # for a given tax_id. I need tax_id to be unique,
    # so I will drop duplicate tax id's, keeping only the
    # first accession.
    df = df.drop_duplicates('taxid')

    return df


# --------------------------------------------------
def join_dfs(braken: pd.DataFrame, tax: pd.DataFrame) -> pd.DataFrame:
    """ Join braken and taxonomy dfs """

    joined_df = pd.merge(braken,
                         tax,
                         how='inner',
                         left_on='taxonomy_id',
                         right_on='taxid')

    return joined_df


# --------------------------------------------------
def rescale_abundances(col: pd.Series) -> pd.Series:
    """ Rescale abundances to add to 1 """

    rescale_factor = 1 / col.sum()

    rescaled = rescale_factor * col

    return rescaled


# --------------------------------------------------
def make_files_df(df: pd.DataFrame) -> pd.DataFrame:
    """ Create file names of genomes """

    files_df = df[['kingdom', 'accession', 'seq_id']]

    files_df['filename'] = files_df['kingdom'] + '/' + files_df[
        'accession'] + '*.fna'

    files_df = files_df[['accession', 'filename', 'seq_id']]

    return files_df


# --------------------------------------------------
def make_profile_df(df: pd.DataFrame) -> pd.DataFrame:
    """ Create file of seq IDs and abundances """

    profile_df = df[['seq_id', 'rescaled_abundance']]

    profile_df['rescaled_abundance'] = round(profile_df['rescaled_abundance'],
                                             5)

    return profile_df


# --------------------------------------------------
def make_filenames(infile: str, out_dir: str) -> Tuple[str, str]:
    """ Create names of output files """

    base = os.path.basename(infile)

    root, _ = os.path.splitext(base)

    files_output = os.path.join(out_dir, root + '_files.txt')
    profile_output = os.path.join(out_dir, root + '_profile.txt')

    return files_output, profile_output


# --------------------------------------------------
if __name__ == '__main__':
    main()
