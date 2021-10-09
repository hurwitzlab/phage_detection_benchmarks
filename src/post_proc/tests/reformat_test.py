""" Tests """

import os
import re
from subprocess import getstatusoutput

PRG = './reformat.py'
DVF_RAW = 'tests/inputs/dvf_raw.txt'


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
