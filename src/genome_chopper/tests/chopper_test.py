""" Tests """

from subprocess import getstatusoutput
import platform
import os
import re
import shutil

PRG = './chopper.py'
RUN = f'python {PRG}' if platform.system() == 'Windows' else PRG
TEST1 = ('./tests/inputs/input1.fasta')
TEST2 = ('./tests/inputs/input2.fasta')


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
def test_no_args() -> None:
    """ Dies on no args """

    rv, out = getstatusoutput(RUN)
    assert rv != 0
    assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_bad_file() -> None:
    """ Dies with nonexistent file """

    rv, out = getstatusoutput(f'{RUN} foo')
    assert rv != 0
    assert out.lower().startswith('usage:')


# --------------------------------------------------
def test_bad_length() -> None:
    """ Dies with bad length """

    rv, out = getstatusoutput(f'{RUN} {TEST1} -l foo')
    assert rv != 0
    assert out.lower().startswith('usage:')

    rv, out = getstatusoutput(f'{RUN} {TEST1} -l 0')
    assert rv != 0
    assert out.lower().startswith('usage:')

    rv, out = getstatusoutput(f'{RUN} {TEST1} -l 6400')
    assert rv != 0
    assert out.lower().startswith('error:')


# --------------------------------------------------
def test_bad_overlap() -> None:
    """ Dies with bad overlap """

    rv, out = getstatusoutput(f'{RUN} {TEST1} -v foo')
    assert rv != 0
    assert out.lower().startswith('usage:')

    rv, out = getstatusoutput(f'{RUN} {TEST1} -l 200 -v 250')
    assert rv != 0
    assert out.lower().startswith('usage:')

    rv, out = getstatusoutput(f'{RUN} {TEST1} -l 3300 -v 100')
    assert rv != 0
    assert out.lower().startswith('error:')


# --------------------------------------------------
def test_okay() -> None:
    """ Runs on good input """

    out_dir = "out_test"
    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{RUN} {TEST2} -l 6 -v 3 -o {out_dir}')

        assert rv == 0
        assert out == ('Wrote 2 records to "out_test/input2_frags.fasta".\n'
                       'Done. Created fragments from 1 file.')
        assert os.path.isdir(out_dir)
        out_file1 = os.path.join(out_dir, 'input2_frags.fasta')
        out_file2 = os.path.join(out_dir, 'input2_frags.tsv')
        assert os.path.isfile(out_file1)
        assert os.path.isfile(out_file2)
        assert open(out_file1).read().count('>') == 2
        assert open(out_file2).read().count('\n') == 3

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def test_multi_file() -> None:
    """ Runs with multiple inputs """

    out_dir = "out_test"

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{RUN} -l 6 -v 3 -o'
                                  f' {out_dir} {TEST1} {TEST2}')

        assert rv == 0
        assert out == ('Wrote 2130 records to "out_test/input1_frags.fasta".\n'
                       'Wrote 2 records to "out_test/input2_frags.fasta".\n'
                       'Done. Created fragments from 2 files.')
        assert os.path.isdir(out_dir)
        out_file1 = os.path.join(out_dir, 'input1_frags.fasta')
        out_file2 = os.path.join(out_dir, 'input1_frags.tsv')
        out_file3 = os.path.join(out_dir, 'input2_frags.fasta')
        out_file4 = os.path.join(out_dir, 'input2_frags.tsv')
        assert os.path.isfile(out_file1)
        assert os.path.isfile(out_file2)
        assert os.path.isfile(out_file3)
        assert os.path.isfile(out_file4)

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
