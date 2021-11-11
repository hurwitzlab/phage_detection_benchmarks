#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-11-11
Purpose: Convert from FASTA to GenBank
"""

import argparse
import os
from Bio import SeqIO
from typing import List, NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[TextIO]
    outdir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Convert from FASTA to GenBank',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('files',
                        metavar='FILE',
                        help='FASTA file(s)',
                        type=argparse.FileType('rt'),
                        nargs='+')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='DIR',
                        type=str,
                        default='out')

    args = parser.parse_args()

    return Args(args.files, args.outdir)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    out_dir = args.outdir

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    converted: int = 0
    total_recs: int = 0

    for fh in args.files:
        # Build output file name. Keep old basename, change extension.
        base, _ = os.path.splitext(os.path.basename(fh.name))
        out_name = base + '.gb'
        out_path = os.path.join(out_dir, out_name)

        # Convert the records
        rec_count = SeqIO.convert(fh, 'fasta', out_path, 'genbank', 'DNA')

        # Print message for single file conversion
        plural_rec = 's' if rec_count > 1 else ''
        print(f'Wrote {rec_count} converted record{plural_rec} to {out_path}')

        # Increment counts
        total_recs += rec_count
        converted += 1

    # Give final exit message
    plural_file = 's' if converted > 1 else ''
    print(f'Done. Wrote {converted} file{plural_file} to {out_dir}.')


# --------------------------------------------------
if __name__ == '__main__':
    main()
