""" Tests """

import os
import re
import shutil
from subprocess import getstatusoutput
from typing import List

PRG = './combine.py'
BAD = 'tests/inputs/combine/bad_format.csv'
INPUT1 = 'tests/inputs/combine/dvf_pred_formatted.csv'
INPUT2 = 'tests/inputs/combine/seeker_pred_formatted.csv'


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
def test_bad_file_name():
    """ Bad input file name """

    retval, out = getstatusoutput(f'{PRG} shimmy.csv')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('No such file', out)


# --------------------------------------------------
def test_bad_file_format():
    """ Bad input file format """

    retval, out = getstatusoutput(f'{PRG} {BAD}')
    assert retval != 0
    assert re.search('unexpected column names', out)


# --------------------------------------------------
def run(files: List) -> None:
    """ Run the program with given file(s) """

    out_dir = 'out_test'

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{PRG} -o {out_dir} {" ".join(files)}')

        assert rv == 0
        out_file = os.path.join(out_dir, 'combined.csv')
        assert out == (f'Done. Wrote to {out_file}')
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)

        # Header is retained
        header = ('tool,record,length,actual,prediction,'
                  'lifecycle,value,stat,stat_name\n')
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
def test_runs_single() -> None:
    """ Works with one file """

    run([INPUT1])


# --------------------------------------------------
def test_runs_mulitple() -> None:
    """ Works with multiple files """

    run([INPUT1, INPUT2])
