#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2022-03-09
Purpose: parse BLAST output
"""

import argparse
from Bio.Blast import NCBIXML
import io
import os
import pytest
from typing import List, NamedTuple, TextIO, Tuple


class Args(NamedTuple):
    """ Command-line arguments """
    blast_out: TextIO
    outdir: str
    low_mem: bool


class Hit(NamedTuple):
    """ BLAST hit information """
    query_id: str
    hit_id: str
    e_val: str
    query_length: str
    align_length: str
    start: str
    end: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='parse BLAST output',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('blast_out',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        help='BLAST output')

    parser.add_argument('-o',
                        '--outdir',
                        metavar='DIR',
                        help='Output directory',
                        type=str,
                        default='out')

    parser.add_argument('-l',
                        '--low_mem',
                        action='store_true',
                        help='Use low-memory, slower version')

    args = parser.parse_args()

    return Args(args.blast_out, args.outdir, args.low_mem)


# --------------------------------------------------
def main() -> None:
    """ This is how we do iit """

    args = get_args()

    if not os.path.isdir(args.outdir):
        os.mkdir(args.outdir)

    out_file = make_filename(args.outdir, args.blast_out.name)

    hits = get_hits(args.blast_out)
    header = 'query_id,hit_id,e_val,query_length,alignment_length,start,end'

    with open(out_file, 'wt') as out_fh:
        if args.low_mem:
            output_low_mem(header, hits, out_fh)
        else:
            output_fast(header, hits, out_fh)

    print(f'Done. Wrote output to {out_file}.')


# --------------------------------------------------
def make_filename(out_dir: str, infile: str) -> str:
    """ Create output file name """

    root, _ = os.path.splitext(os.path.basename(infile))
    name = root.replace('blast_out', '')

    return os.path.join(out_dir, name + 'parsed_blast.csv')


# --------------------------------------------------
def test_make_filenames() -> None:
    """ Test make_filenames() """

    file_name = 'out/input_1_parsed_blast.csv'
    assert make_filename('out', 'input_1_blast_out.txt') == file_name
    assert make_filename('out', 'tests/input_1_blast_out.txt') == file_name


# --------------------------------------------------
def get_hits(infile: TextIO) -> List[Hit]:
    """ Parse BLAST output for hits """

    hits = []
    for query in NCBIXML.parse(infile):
        query_id = query.query.split(" ")[0]
        query_length = query.query.split(" ")[3].replace('len=', '')

        for alignment in query.alignments:
            hit_id = alignment.hit_def

            for hsp in alignment.hsps:

                hit = Hit(query_id, hit_id, hsp.expect, query_length,
                          hsp.align_length, hsp.query_start, hsp.query_end)

                hits.append(hit)

    return hits


# --------------------------------------------------
def output_low_mem(header: str, hits: List[Hit], fh: TextIO) -> None:
    """ Create output using less memory, but slower """

    fh.write(header)

    for hit in hits:
        print(
            f'\n{hit.query_id},{hit.hit_id},{hit.e_val},{hit.query_length},'
            f'{hit.align_length},{hit.start},{hit.end}',
            file=fh,
            end='')


# --------------------------------------------------
def test_output_low_mem(example_out_data: Tuple[str, List[Hit]],
                        example_out: TextIO) -> None:
    """ Test output_low_mem() """

    header, hits = example_out_data
    out_fh = io.StringIO('')

    output_low_mem(header, hits, out_fh)

    out_fh.seek(0)

    assert out_fh.read() == example_out.read()


# --------------------------------------------------
def output_fast(header: str, hits: List[Hit], fh: TextIO) -> None:
    """ Create output fast, but with more memory usage """

    fh.write(header + '\n')

    hits_str = [
        f'{hit.query_id},{hit.hit_id},{hit.e_val},{hit.query_length},'
        f'{hit.align_length},{hit.start},{hit.end}' for hit in hits
    ]

    fh.write('\n'.join(hits_str))


# --------------------------------------------------
def test_output_fast(example_out_data: Tuple[str, List[Hit]],
                     example_out: TextIO) -> None:
    """ Test output_fast() """

    header, hits = example_out_data
    out_fh = io.StringIO('')

    output_fast(header, hits, out_fh)

    out_fh.seek(0)

    assert out_fh.read() == example_out.read()


# --------------------------------------------------
@pytest.fixture(name='example_out_data')
def fixture_example_out_data() -> Tuple[str, List[Hit]]:
    """ Example data sent to the functions that write output """

    header = 'query_id,hit_id,e_val,query_length,alignment_length,start,end'

    hits = [
        Hit('k141_5989', 'GCF_002148255.1', '8.40553e-160', '306', '306', '1',
            '306'),
        Hit('k141_5989', 'GCF_009834925.2', '2.71137e-55', '306', '208', '70',
            '275')
    ]

    return (header, hits)


# --------------------------------------------------
@pytest.fixture(name='example_out')
def fixture_example_out() -> TextIO:
    """ Example output file handle with contents """
    out_fh = io.StringIO(
        'query_id,hit_id,e_val,query_length,alignment_length,start,end\n'
        'k141_5989,GCF_002148255.1,8.40553e-160,306,306,1,306\n'
        'k141_5989,GCF_009834925.2,2.71137e-55,306,208,70,275')

    return out_fh


# --------------------------------------------------
if __name__ == '__main__':
    main()
