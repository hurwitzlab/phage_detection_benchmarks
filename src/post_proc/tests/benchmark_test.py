""" Tests """

import itertools
import os
import re
import shutil
from subprocess import getstatusoutput
from typing import List

PRG = './benchmark.py'
BAD_FMT = 'tests/inputs/benchmarks/bad_format.csv'
BAD_NAME = 'tests/inputs/benchmarks/bad_benchmark_name.txt'
INPUTS = []

kingdoms = ['archaea', 'bacteria', 'fungi', 'viral']
lengths = ['500', '1000', '3000', '5000']

for kingdom, length in itertools.product(kingdoms, lengths):
    INPUTS.append(
        f'tests/inputs/benchmarks/virsorter/{kingdom}_{length}_benchmark.txt')


# --------------------------------------------------
def test_exists():
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage():
    """ Usage """

    for flag in ['-h', '--help']:
        retval, out = getstatusoutput(f'{PRG} {flag}')
        assert retval == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_missing_inputs():
    """ Missing input files """

    retval, out = getstatusoutput(f'{PRG}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('required: FILE', out)


# --------------------------------------------------
def test_bad_file():
    """ Bad input file name """

    retval, out = getstatusoutput(f'{PRG} shimmy.csv')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('No such file', out)


# --------------------------------------------------
def test_bad_file_format():
    """ Bad input file format """

    retval, out = getstatusoutput(f'{PRG} {BAD_FMT}')
    assert retval != 0
    assert re.search('unexpected column names', out)


# --------------------------------------------------
def test_bad_file_name():
    """ Bad input file name """

    retval, out = getstatusoutput(f'{PRG} {BAD_NAME}')
    assert retval != 0
    assert re.search('unexpected file name', out)


# --------------------------------------------------
def run(files: List) -> None:
    """ Run the program with given file(s) """

    out_dir = 'out_test'

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{PRG} -o {out_dir} {" ".join(files)}')

        assert rv == 0
        out_file = os.path.join(out_dir, 'combined_benchmarks.csv')
        assert out == (f'Done. Wrote to {out_file}')
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)

        # Header is retained
        header = ('s,h:m:s,max_rss,max_vms,max_uss,'
                  'max_pss,io_in,io_out,mean_load,cpu_time,'
                  'tool,kingdom,length\n')
        assert open(out_file).readlines()[0] == header

        # Number of rows is retained*
        orig_lines = 0
        if len(files) > 1:
            for file in files:
                orig_lines += open(file).read().count('\n')
        else:
            orig_lines += open("".join(files)).read().count('\n')
        new_lines = open(out_file).read().count('\n')

        # *Headers are dropped from all but 1 file
        assert new_lines == orig_lines - len(files) + 1

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def test_runs_okay() -> None:
    """ Works with good files """

    run(INPUTS)
