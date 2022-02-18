""" Tests """

import os
import random
import re
import shutil
import string
from subprocess import getstatusoutput

PRG = './bracken_profiler.py'
INPUT1 = 'tests/inputs/bracken_profiler/input_1.txt'
INPUT2 = 'tests/inputs/bracken_profiler/input_1.txt'
TAX = 'tests/inputs/bracken_profiler/input_1.txt'


# --------------------------------------------------
def test_exists():
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_testing_environment():
    """ Test files are in place """

    assert os.path.isfile(INPUT1)
    assert os.path.isfile(INPUT2)
    assert os.path.isfile(TAX)


# --------------------------------------------------
def test_usage():
    """ Usage """

    for flag in ['-h', '--help']:
        retval, out = getstatusoutput(f'{PRG} {flag}')
        assert retval == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_bad_file():
    """ Bad input file """

    bad = random_string()

    retval, out = getstatusoutput(f'{PRG} -t {TAX} {bad}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('No such file', out)
    assert re.search(bad, out)


# --------------------------------------------------
def test_bad_taxonomy_file():
    """ Bad input file """

    bad = random_string()

    retval, out = getstatusoutput(f'{PRG} -t {bad} {INPUT1}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('No such file', out)
    assert re.search(bad, out)


# --------------------------------------------------
def test_runs_okay():
    """ Run the tool """

    out_dir = random_string()

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{PRG} -o {out_dir} {INPUT1}')

        assert rv == 0
        glob_file = os.path.join(out_dir, 'input_1_files.txt')
        profile_file = os.path.join(out_dir, 'input_1_profile.txt')
        assert re.search(f'Done. Wrote 1 profile to {out_dir}', out)
        assert os.path.isdir(out_dir)
        assert os.path.isfile(glob_file)
        assert os.path.isfile(profile_file)
        header = ('filename,seq_id\n')
        assert open(glob_file).readlines()[0] == header
        profile_lines = open(profile_file).read().count('\n')
        glob_lines = open(glob_file).read().count('\n')
        assert glob_lines == profile_lines + 1

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def random_string() -> str:
    """ Generate a random string """

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
