#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-04-20
Purpose: Assign taxonomy to BLASTed contigs
"""

import argparse
import multiprocessing as mp
import os
from typing import NamedTuple, TextIO

import pandas as pd

from blast_sorter import assign_tax


class Args(NamedTuple):
    """ Command-line arguments """
    infile: TextIO
    taxonomy: TextIO
    outdir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Assign taxonomy to BLASTed contigs',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('infile',
                        type=argparse.FileType('rt'),
                        metavar='FILE',
                        help='Parsed BLAST output file')

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

    return Args(args.infile, args.taxonomy, args.outdir)


# --------------------------------------------------
def make_filename(infile: str, outdir: str) -> str:
    """ Make output filename from input name """

    in_name, _ = os.path.splitext(os.path.basename(infile))

    out_name = in_name.replace('parsed_blast', 'contig_taxonomy.csv')

    out_name = os.path.join(outdir, out_name)

    return out_name


# --------------------------------------------------
def test_make_filename() -> None:
    """ Test make_filename() """

    assert make_filename('blast/profile_hiseq_parsed_blast.csv',
                         'out') == 'out/profile_hiseq_contig_taxonomy.csv'


# --------------------------------------------------
def main() -> None:
    """ Just go for it """

    n_cpu = mp.cpu_count()
    pool = mp.Pool(n_cpu)
    print(f'Running with {n_cpu} CPUs')

    args = get_args()
    out_dir = args.outdir

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    df = pd.read_csv(args.infile)
    taxonomy_df = pd.read_csv(args.taxonomy)

    assignment_df = pd.DataFrame()
    assignments = pool.map_async(
        assign_tax,
        [query_hits for _, query_hits in df.groupby('query_id')]).get()

    pool.close()

    assignment_df = pd.concat([assignment_df, *assignments])

    assignment_df = assignment_df.reset_index(drop=True)

    out_df = pd.merge(assignment_df,
                      taxonomy_df,
                      how='inner',
                      left_on='hit_id',
                      right_on='accession')

    out_df = out_df.drop_duplicates(
        ['query_id', 'hit_id', 'taxid', 'start', 'end'])

    # Rename and delete duplicate columns

    out_file = make_filename(args.infile.name, out_dir)

    out_df.to_csv(out_file, index=False)

    print(f'Done. Wrote output to {out_file}')


# --------------------------------------------------
if __name__ == '__main__':
    main()
