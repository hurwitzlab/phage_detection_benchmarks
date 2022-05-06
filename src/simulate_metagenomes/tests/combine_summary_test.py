""" Tests """

import os
import random
import re
import shutil
import string
from subprocess import getstatusoutput
from typing import List

PRG = './combine_summary.py'
PROFILE = 'tests/inputs/combine_summary/profile_1_profile_comparison.csv'
BLAST = 'tests/inputs/combine_summary/profile_1_model_parsed_blast.csv'
CONTIG1 = 'tests/inputs/combine_summary/profile_1_model_contig_summary.csv'
CONTIG2 = 'tests/inputs/combine_summary/profile_1_model_contig_summary.csv'


# --------------------------------------------------
def test_exists() -> None:
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_testing_environment() -> None:
    """ Test files are in place """

    in_files = [PROFILE, BLAST, CONTIG1, CONTIG2]

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
def test_bad_file() -> None:
    """ Run with a bad input file """

    bad = random_string()

    retval, out = getstatusoutput(f'{PRG} -r "foo" {bad}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('No such file', out)
    assert re.search(bad, out)


# --------------------------------------------------
def test_bad_regex() -> None:
    """ Dies with bad regex """

    bad = random_string()

    retval, out = getstatusoutput(f'{PRG} -r "{bad}" {PROFILE}')
    assert retval != 0
    assert re.search(f'--regex "{bad}" missing "filename" group.', out)


# --------------------------------------------------
def test_no_match() -> None:
    """ Dies when no match found """

    # Good regex, but doesn't match the file
    regex = r'(?P<profile>\w+)_(?P<filename>profile_comparison).csv'

    retval, out = getstatusoutput(f'{PRG} -r "{regex}" {BLAST}')
    assert retval != 0
    assert re.search(re.escape(f'--regex "{regex}" did not match'), out)


# --------------------------------------------------
def run(regex: str, files: List[str], out_name: str, extra_cols: int) -> None:
    """ Run the program """

    out_dir = random_string()

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{PRG} -r "{regex}" -o {out_dir} '
                                  f'{" ".join(files)}')

        assert rv == 0
        out_file = os.path.join(out_dir, out_name)
        assert re.search(f'Done. Wrote output to {out_file}', out)
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)

        # All rows are preserved
        num_files = len(files)
        orig_lines = sum(map(lambda f: open(f).read().count('\n'), files))
        out_lines = open(out_file).read().count('\n')
        assert out_lines == orig_lines - (num_files - 1)

        # Correct number of columns are output
        orig_cols = open(files[0]).readline().count(',') + 1
        new_cols = open(out_file).readline().count(',') + 1
        assert new_cols == orig_cols + extra_cols

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def test_runs_profile() -> None:
    """ Can process profile comparisons """

    regex = r'(?P<profile>\w+)_(?P<filename>profile_comparison).csv'

    run(regex, [PROFILE], 'combined_profile_comparison.csv', 1)


# --------------------------------------------------
def test_runs_blast() -> None:
    """ Can process BLAST summaries """

    regex = (r'(?P<profile>\w+)_'
             r'(?P<model>\w+)_'
             r'(?P<filename>parsed_blast).csv')

    run(regex, [BLAST], 'combined_parsed_blast.csv', 2)


# --------------------------------------------------
def test_runs_contig() -> None:
    """ Can process contig summaries """

    regex = (r'(?P<profile>\w+)_'
             r'(?P<model>\w+)_'
             r'(?P<filename>contig_summary).csv')

    run(regex, [CONTIG1], 'combined_contig_summary.csv', 2)


# --------------------------------------------------
def test_runs_multiple() -> None:
    """ Can concatenate multiple files """

    regex = (r'(?P<profile>\w+)_'
             r'(?P<model>\w+)_'
             r'(?P<filename>contig_summary).csv')

    run(regex, [CONTIG1, CONTIG2], 'combined_contig_summary.csv', 2)


# --------------------------------------------------
def random_string() -> str:
    """ Generate a random string """

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
