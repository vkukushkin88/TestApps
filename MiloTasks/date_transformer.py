
"""This module can read from file some dates in fluent format (year, month, day)
separated by '/' and find lowest possible date based on different sequences
of year, month, day given values."""

import argparse
import itertools

from datetime import datetime


def search_min_date(str_date):
    """Try different combinations of year, month, day to find lowest date
    Parameters:
        @str_date: date in format '<year>|<month>|<day>/<year>|<month>|<day>/<year>|<month>|<day>'

    Result:
        Minimal possible date from permutations of given numbers or None
    """
    res = []
    for possible_date in itertools.permutations(str_date.split('/')):
        local_res = try_date(*possible_date)
        res.append(local_res) if local_res else None
    return min(res) if res else None


def try_date(*args):
    """Create data object if combination of year + month + day gives legal date

    Parameters:
        @args: year, month, day

    Result:
        date object or None
    """
    year, month, day = [int(el or 0) for el in args]
    year = 2000 + year if year < 2000 else year
    try:
        return datetime.strptime('/'.join(map(str, [year, month, day])), '%Y/%m/%d').date()
    except ValueError, e:
        pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('datefile')
    return parser.parse_args()


def main(args):
    with open(args.datefile) as datefile:
        for input_date in datefile.readlines():
            min_date = search_min_date(input_date.strip())
            print min_date if min_date else 'is illegal'


if __name__ == '__main__':
    args = parse_args()
    main(args)
