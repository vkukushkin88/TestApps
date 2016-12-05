
import types
import unittest
from unittest.mock import patch, Mock

import src.data_io as data_io


CSV_FILE_NAME = '/no/existing/file.csv'


class CSVreaderClassTest(unittest.TestCase):

    def setUp(self):
        self.reader = data_io.CSVreader(CSV_FILE_NAME)

    @patch('src.data_io.open')
    @patch('src.data_io.csv')
    def test_read_row(self, csv, open_mock):
        open_mock.__enter__ = Mock()
        open_mock.__exit__ = Mock()
        open_mock.__exit__.return_value = False
        row = self.reader.read_row()
        list(row)
        csv.reader.assert_called_once_with(open_mock().__enter__(), delimiter=',')
        isinstance(row, types.GeneratorType)


if __name__ == '__main__':
    unittest.main()