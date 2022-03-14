""" Tests """

import os
import random
import re
import shutil
import string
from subprocess import getstatusoutput

PRG = './summarize_contigs.py'
INPUT = 'tests/inputs/summarize_contigs/final.contigs.fa'


# --------------------------------------------------
def test_exists() -> None:
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_testing_environment() -> None:
    """ Test files are in place """

    assert os.path.isfile(INPUT)


# --------------------------------------------------
def test_usage() -> None:
    """ Usage """

    for flag in ['-h', '--help']:
        retval, out = getstatusoutput(f'{PRG} {flag}')
        assert retval == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_bad_file() -> None:
    """ Run with a bad input file """

    bad = random_string()

    retval, out = getstatusoutput(f'{PRG} {bad}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('No such file', out)


# --------------------------------------------------
def test_runs_okay() -> None:
    """ Run the program """

    out_dir = random_string()

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{PRG} -o {out_dir} {INPUT}')

        assert rv == 0
        out_file = os.path.join(out_dir, 'contig_summary.csv')
        assert re.search(f'Done. Wrote output to {out_file}', out)
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)
        out_contigs = open(out_file).read().count('\n')
        assert out_contigs == 6

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def random_string() -> str:
    """ Generate a random string """

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
