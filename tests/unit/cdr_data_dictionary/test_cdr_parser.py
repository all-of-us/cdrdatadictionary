# Python imports
from argparse import ArgumentTypeError
from datetime import datetime
import unittest

# Third party imports

# Project imports
import cdr_data_dictionary.cdr_parser as c_parse
import cdr_data_dictionary.constants as consts


class CDRParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\n\n**************************************************************')
        print(cls.__name__)
        print('**************************************************************')

    def setUp(self):
        self.key = 'bogus/key/file.json'
        self.sheet_id = '123alsdkfjUI8ksld8'
        self.cdr_version = '2010R2Q3'
        self.today = datetime.now().strftime(consts.FILENAME_DATE_FORMAT)
        self.output_file = consts.YAML_OUTPUT_FILENAME.format(cdr_version=self.cdr_version,
                                                              today=self.today)

        self.defaults = {
            'key_file': self.key,
            'spreadsheet_id': self.sheet_id,
            'sheet_name': consts.ALL,
            'range': None,
            'output_file': self.output_file,
            'column_id': None,
            'schema_file': 'cdr_data_dictionary/schema.yaml',
            'log_path': consts.DEFAULT_LOG,
            'console_log': False,
            'cdr_version': self.cdr_version
        }


    def test_parse_all_valid(self):
        # pre-conditions
        args = [
            '-k', self.key, 
            '-i', self.sheet_id, 
            '--cdr-version', self.cdr_version,
            '--sheet-name', "Change Log",
            '--range', 'A1:M30',
            '--group-by', 'c',
            '--schema-file', 'test_schema.yaml',
            '--log-path', 'log.log',
            '--console-log',
        ]
 
        # test
        settings = c_parse.parse_command_line(args)
        
        # post-conditions
        expected = self.defaults
        expected['sheet_name'] = "Change Log"
        expected['range'] = 'A1:M30'
        expected['column_id'] = 2
        expected['schema_file'] = 'test_schema.yaml'
        expected['log_path'] = 'log.log'
        expected['console_log'] = True

        self.assertEqual(expected, vars(settings))

    def test_parse_to_defaults(self):
        # pre-conditions
        args = [
            '-k', self.key, 
            '-i', self.sheet_id, 
            '--cdr-version', self.cdr_version
        ]
 
        # test
        settings = c_parse.parse_command_line(args)
        
        # post-conditions
        expected = self.defaults

        self.assertEqual(expected, vars(settings))
 
    def test_log_filepath(self):
        # pre-conditions
        name = 'path.log'

        # test
        output = c_parse.log_filepath(name)

        # post-conditions
        self.assertEqual(name, output)

    def test_log_filepath_error(self):
        # pre-conditions
        name = 'path.txt'

        # test
        self.assertRaises(
            ArgumentTypeError,
            c_parse.log_filepath,
            name
        )

    def test_output_filename(self):
        # pre-conditions
        version = 'R42019R1Q2'

        # test
        file_path = c_parse.output_filename(version)

        # post-conditions
        expected = consts.YAML_OUTPUT_FILENAME.format(cdr_version=version, 
                                                      today=self.today)

        self.assertEqual(file_path, expected)

    def test_ascii_to_index_none(self):
        # pre-condition
        column = None

        # test
        index = c_parse.ascii_to_index(column)

        # post_condition
        self.assertFalse(index)
        self.assertEqual(index, None)

    def test_ascii_to_index_lower(self):
        # pre-condition
        column = 'c'

        # test
        index = c_parse.ascii_to_index(column)

        # post_condition
        self.assertTrue(index)
        self.assertEqual(index, 2)

    def test_ascii_to_index_upper(self):
        # pre-condition
        column = 'Z'

        # test
        index = c_parse.ascii_to_index(column)

        # post_condition
        self.assertTrue(index)
        self.assertEqual(index, 25)

    def test_ascii_to_index_unknown_col_spec(self):
        # pre-condition
        column = 'ZZZ'

        # test
        self.assertRaises(
            ArgumentTypeError,
            c_parse.ascii_to_index,
            column)
