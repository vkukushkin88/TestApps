
import unittest
from unittest.mock import patch, MagicMock

import main


class TestMainModule(unittest.TestCase):

    @patch('main.CSVreader')
    @patch('main.ConsolePrint')
    @patch('main.FBUserCreationProcessor')
    def test_run(self, FBUserCreationProcessor, ConsolePrint, CSVreader):
        args = MagicMock()
        main.run(args)
        FBUserCreationProcessor.assert_called_once()
        ConsolePrint.assert_called_once()
        CSVreader.assert_called_once()

    @patch('main.argparse')
    def test_parse_args(self, argparse):
        result = main.parse_args()
        argparse.ArgumentParser.assert_called_once()


if __name__ == '__main__':
    unittest.main()