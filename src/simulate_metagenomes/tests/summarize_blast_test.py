""" Tests """

import os
import random
import re
import shutil
import string
from subprocess import getstatusoutput

PRG = './summarize_blast.py'
INPUT = 'tests/inputs/summarize_blast/input_1_blast_out.xml'


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
def run(flag: str) -> None:
    """ Run the tool """

    out_dir = random_string()

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{PRG} -o {out_dir} {INPUT} {flag}')

        assert rv == 0
        out_file = os.path.join(out_dir, 'input_1_parsed_blast.csv')
        assert re.search(f'Done. Wrote output to {out_file}.', out)
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)
        header = (
            'query_id,hit_id,e_val,query_length,alignment_length,start,end\n')
        assert open(out_file).readlines()[0] == header
        out_lines = open(out_file).read().count('\n')
        blast_hits = open(INPUT).read().count('Hit_num') / 2
        assert out_lines == blast_hits

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def test_runs_fast() -> None:
    """ Runs on default mode """

    run('')


# --------------------------------------------------
def test_runs_low_mem() -> None:
    """ Runs on low-memory mode """

    run('--low_mem')


# --------------------------------------------------
def random_string() -> str:
    """ Generate a random string """

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
