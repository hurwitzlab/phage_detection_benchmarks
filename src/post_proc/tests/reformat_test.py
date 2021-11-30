""" Tests """

import os
import re
import shutil
from subprocess import getstatusoutput

PRG = './reformat.py'
DVF_RAW = 'tests/inputs/reformat/dvf_raw.txt'


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
def test_bad_file():
    """ Bad input file """

    retval, out = getstatusoutput(f'{PRG} -l 500 -a bacteria shimmy.txt')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('No such file', out)


# --------------------------------------------------
def test_bad_length():
    """ Unexpected length """

    retval, out = getstatusoutput(f'{PRG} -l 600 -a bacteria -t dvf {DVF_RAW}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('--length: invalid choice', out)

    retval, out = getstatusoutput(f'{PRG} -t dvf -a bacteria {DVF_RAW}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('required: -l', out)


# --------------------------------------------------
def test_bad_actual():
    """ Unexpected true classification """

    retval, out = getstatusoutput(f'{PRG} -l 500 -a sponge -t dvf {DVF_RAW}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('--actual: invalid choice', out)

    retval, out = getstatusoutput(f'{PRG} -l 500 -t dvf {DVF_RAW}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('required: -a', out)


# --------------------------------------------------
def test_bad_tool():
    """ Unaccounted tool format """

    retval, out = getstatusoutput(f'{PRG} -l 500 -a bacteria'
                                  f'-t wrench {DVF_RAW}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('--actual: invalid choice', out)

    retval, out = getstatusoutput(f'{PRG} -l 500 -a bacteria {DVF_RAW}')
    assert retval != 0
    assert out.lower().startswith('usage:')
    assert re.search('required: -t', out)


# --------------------------------------------------
def run(tool: str) -> None:
    """ Run the program with given tool """

    out_dir = 'out_test'
    in_file = f'tests/inputs/reformat/{tool}_raw.txt'

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{PRG} -l 500 -a bacteria -t {tool}'
                                  f' -o {out_dir} {in_file}')

        assert rv == 0
        out_file = os.path.join(out_dir, f'{tool}_pred_formatted.csv')
        assert out == (f'Done. Wrote to {out_file}')
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)
        header = ('tool,record,length,actual,prediction,'
                  'lifecycle,value,stat,stat_name\n')
        assert open(out_file).readlines()[0] == header
        orig_lines = open(in_file).read().count('\n')
        new_lines = open(out_file).read().count('\n')
        if tool == 'vibrant':
            assert new_lines == orig_lines + 1
        else:
            assert new_lines == orig_lines

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def test_reformat_breadsticks() -> None:
    """ Reformats Unlimited breadsticks """

    run('breadsticks')


# --------------------------------------------------
def test_reformat_dvf() -> None:
    """ Reformats DeepVirFinder """

    run('dvf')


# --------------------------------------------------
def test_reformat_metaphinder() -> None:
    """ Reformats MetaPhinder """

    run('metaphinder')


# --------------------------------------------------
def test_reformat_seeker() -> None:
    """ Reformats Seeker """

    run('seeker')


# --------------------------------------------------
def test_reformat_vibrant() -> None:
    """ Reformats VIBRANT """

    run('vibrant')


# --------------------------------------------------
def test_reformat_viralverify() -> None:
    """ Reformats viralVerify """

    run('viralverify')


# --------------------------------------------------
def test_reformat_virfinder() -> None:
    """ Reformats VirFinder """

    run('virfinder')


# --------------------------------------------------
def test_reformat_virsorter() -> None:
    """ Reformats VirSorter """

    run('virsorter')


# --------------------------------------------------
def test_reformat_virsorter2() -> None:
    """ Reformats VirSorter2 """

    # Run with typical output
    run('virsorter2')

    # Run with empty virsorter2 output (no viral found)
    tool = 'virsorter2'
    out_dir = 'out_test'
    in_file = f'tests/inputs/reformat/{tool}_raw_empty.txt'

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, out = getstatusoutput(f'{PRG} -l 500 -a bacteria -t {tool}'
                                  f' -o {out_dir} {in_file}')

        assert rv == 0
        out_file = os.path.join(out_dir, f'{tool}_pred_formatted.csv')
        assert out == (f'Done. Wrote to {out_file}')
        assert os.path.isdir(out_dir)
        assert os.path.isfile(out_file)
        header = ('tool,record,length,actual,prediction,'
                  'lifecycle,value,stat,stat_name\n')
        assert open(out_file).readlines()[0] == header
        orig_lines = open(in_file).read().count('\n')
        new_lines = open(out_file).read().count('\n')
        assert new_lines == orig_lines

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
