
"""This module is main module for launching Facebook scraper application
"""

import argparse

from src.data_io import CSVreader, ConsolePrint
from src.fb_data import FBUserCreationProcessor


def run(args):
    file_reader = CSVreader(args.csvfile)
    console_print = ConsolePrint()
    data_processor = FBUserCreationProcessor(
        uaccess_data_keeper=file_reader.read_row(),
        result_data_keeper=console_print
    )
    data_processor.process_all()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('csvfile')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    run(args)