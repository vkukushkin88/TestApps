
"""This file is designed to keep data reader functional"""

import csv


class CSVreader:

    """CSV file reader class"""

    def __init__(self, csv_filepath, delim=','):
        """Initialization of CSV reader

        @param csv_filepath: full path to csv file
        @param delim: csv file delimeter, default `,`

        returns:
            CSVreader object
        """
        self._csv_filepath = csv_filepath
        self._delimeter = delim

    def read_row(self):
        """Generator which returns single row from csv file per each loop"""
        with open(self._csv_filepath, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=self._delimeter)
            for row in spamreader:
                yield row


class ConsolePrint:

    """Simple class for printing to console"""

    def push(self, data):
        print(data)