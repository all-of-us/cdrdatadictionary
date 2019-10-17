# Python imports
from argparse import Namespace
import logging
import unittest

# Third party imports

# Project imports
import cdr_data_dictionary.yaml_logging as y_log


class YAMLLoggingTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\n\n**************************************************************')
        print(cls.__name__)
        print('**************************************************************')

    def test_setup_logging(self):
        """
        Because logging gets set up once, the test order is important.

        Need to test without the console logger before testing with it.
        """
        # pre-condition
        args = Namespace(console_log=False, log_path='log.log')

        # test
        y_log.setup_logging(args)

        # post-conditions
        expected = 1
        actual = len(logging.getLogger().handlers)
        self.assertEqual(expected, actual)

    def test_setup_logging_to_console(self):
        """
        Because logging gets set up once, the test order is important.

        Need to test without the console logger before testing with it.
        """
        # pre-condition
        args = Namespace(console_log=True, log_path='log.log')

        # test
        y_log.setup_logging(args)

        # post-conditions
        expected = 2
        actual = len(logging.getLogger().handlers)
        self.assertEqual(expected, actual)
