#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2021-09-02
Purpose: Select genomes for analysis
"""

import argparse
import sys
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    config: TextIO
    num: int
    kingdom: list
    seed: bool


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Select genomes for analysis',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('config',
                        help='Config file with genome locations',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default=None)

    parser.add_argument('-n',
                        '--num',
                        help='Number of fragments to select',
                        metavar='int',
                        type=str,
                        default='100')

    parser.add_argument('-k',
                        '--kingdom',
                        help='Which kingdom to select from',
                        metavar='str',
                        type=str,
                        nargs='+',
                        default='all')

    parser.add_argument('-s',
                        '--seed',
                        help='Use seed to fix randomness',
                        action='store_true')

    args = parser.parse_args()

    kingdoms = ['archaea', 'bacteria', 'fungi', 'viral', 'all']

    if args.kingdom == 'all':
        args.kingdom = kingdoms[:-1]

    if not all(elem in kingdoms  for elem in args.kingdom):
        die(f'kingdoms "{args.kingdom}" must be in: {kingdoms}')

    return Args(args.config, args.num, args.kingdom, args.seed)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    config_fh = args.config
    num_frags = args.num
    kingdoms = args.kingdom
    seed_on = args.seed

    print(f'config file = "{config_fh}"')
    print(f'num frags = "{num_frags}"')
    print(f'kingdoms = "{kingdoms}"')
    print(f'seed = "{seed_on}"')


# --------------------------------------------------
def warn(msg) -> None:
    """ Warn with a messsage """
    print(msg, file=sys.stderr)


# --------------------------------------------------
def die(msg='Error') -> None:
    """ Warn with a messsage """
    warn(msg)
    sys.exit(1)


# --------------------------------------------------
if __name__ == '__main__':
    main()
