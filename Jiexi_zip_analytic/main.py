#! python
# -*- coding: utf-8 -*-

"""This module is main module for launching zip file generator/analyzer application
"""

import os
import time
import argparse

from settings import *
from src.zip_generator import generate_zip_files_in_processes
from src.zip_analizer import analyze_zip_files_in_processes


def generate(args):
    generate_zip_files_in_processes(args)


def analyze(args):
    analyze_zip_files_in_processes(args)


def parse_args():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()
    parser_generate = subparsers.add_parser('generate', help='Generate zips')
    parser_generate.add_argument('-o', '--output-dst', default=DEFAULT_ZIP_PATH,
        help='Destination for storing zip files')
    parser_generate.set_defaults(func=generate)

    analyze_generate = subparsers.add_parser('analyze', help='Analyze zips')
    analyze_generate.add_argument('-i', '--input-src', help='Path to zip files',
        default=DEFAULT_ZIP_PATH)
    analyze_generate.add_argument('-o', '--output-dst', help='Destination where to store csv files',
        default='.')
    analyze_generate.add_argument('-l', '--id-level-csv', help='Name of csv file with `id, level` data',
        default=ID_LEVEL_CSV)
    analyze_generate.add_argument('-n', '--id-name-csv', default=ID_NAME_CSV,
        help='Name of csv file with ` id, object_name` data')
    analyze_generate.set_defaults(func=analyze)
    return parser.parse_args()


if __name__ == '__main__':
    start_time = time.time()
    args = parse_args()
    args.func(args)
    print 'Processing time: %s' % (time.time() - start_time)
