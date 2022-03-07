""" Tests """

import os
import random
import re
import shutil
import string
from subprocess import getstatusoutput

PRG = './summarize_profile.py'
BRACKEN = 'tests/inputs/summarize_profile/input_1.txt'
PROFILE = 'tests/inputs/summarize_profile/input_1_profile.txt'
TAX = 'tests/inputs/bracken_profiler/taxonomy.csv'


# --------------------------------------------------
def test_exists() -> None:
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_testing_environment() -> None:
    """ Test files are in place """

    in_files = (BRACKEN, PROFILE, TAX)

    for file in in_files:
        assert os.path.isfile(file)


# --------------------------------------------------
def test_usage() -> None:
    """ Usage """

    for flag in ['-h', '--help']:
        retval, out = getstatusoutput(f'{PRG} {flag}')
        assert retval == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def run_bad_file(tax: str, bracken: str, profile: str) -> None:
    """ Run with a bad input file """

    retval, out = getstatusoutput(f'{PRG} -t {tax} -b {bracken} -p {profile}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('No such file', out)


# --------------------------------------------------
def test_bad_taxonomy_file() -> None:
    """ Bad taxonomy file argument """

    run_bad_file(random_string(), BRACKEN, PROFILE)


# --------------------------------------------------
def test_bad_bracken_file() -> None:
    """ Bad Bracken profile argument """

    run_bad_file(TAX, random_string(), PROFILE)


# --------------------------------------------------
def test_bad_profile_file() -> None:
    """ Bad generated profile argument """

    run_bad_file(TAX, BRACKEN, random_string())


# --------------------------------------------------
def test_runs_okay() -> None:
    """ Run the tool """

    out_dir = random_string()

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{PRG} -o {out_dir} -t {TAX} '
                                  f'-b {BRACKEN} -p {PROFILE}')

        assert rv == 0
        out_file = os.path.join(out_dir, 'input_1_profile_comparison.txt')
        assert re.search(f'Done. Wrote output to {out_file}.', out)
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)
        header = ('taxonomy_id\taccession\tfraction_total_reads_bracken'
                  '\tfraction_total_reads\n')
        assert open(out_file).readlines()[0] == header
        out_lines = open(out_file).read().count('\n')
        bracken_lines = open(BRACKEN).read().count('\n')
        assert out_lines == bracken_lines

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def random_string() -> str:
    """ Generate a random string """

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
