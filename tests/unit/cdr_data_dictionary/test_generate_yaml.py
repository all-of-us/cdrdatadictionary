# Python imports
from datetime import datetime
import unittest

# Third party imports
from mock import ANY, call, patch, mock_open

# Project imports
import cdr_data_dictionary.constants as consts
import cdr_data_dictionary.generate_yaml as gen


class GenerateYAMLTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\n\n**************************************************************')
        print(cls.__name__)
        print('**************************************************************')

    def setUp(self):
        self.today = datetime.now().strftime(consts.DATE_FORMAT)

    def test_append_to_results(self):
        """
        Ensure a value is not appended if it is already in the dictionary
        """
        # pre conditions
        field = 'foo'
        value = 'bar'
        existing = ['baz']
        existing.append(value)
        values_dict = {field: existing}

        # test
        result = gen.append_to_results(field, value, values_dict)

        # post conditions
        expected = ['baz', 'bar', 'bar']
        self.assertEqual(result, expected)

    def test_append_to_results_in(self):
        """
        Ensure a value is not appended if it is already in the dictionary
        """
        # pre conditions
        field = 'foo'
        value = 'bar'
        existing = ['baz']
        existing.append(value)
        values_dict = {field: existing}

        self.assertTrue(value in values_dict.get(field), "pre-condition failed")

        # test
        result = gen.append_to_results(field, value, values_dict, unique=True)

        # post conditions
        expected = ['baz', 'bar']
        self.assertEqual(result, expected)

    def test_append_to_results_not_in(self):
        """
        Ensure a value is appended if it is not already in the dictionary
        """
        # pre conditions
        field = 'foo'
        value = 'bar'
        existing = ['baz']
        values_dict = {field: existing}

        self.assertFalse(value in values_dict.get(field), "pre-condition failed.")

        # test
        result = gen.append_to_results(field, value, values_dict, unique=True)

        # post conditions
        expected = ['baz', 'bar']
        self.assertEqual(result, expected)

    def test_sequentially_process_tab_contents(self):
        # pre-conditions
        values = [
            ['field One', 'field Two', 'Field Three'],
            ['val_one', 'val_two', 'val_three'],
            ['val_four', 'val_five', 'val_six'],
        ]

        #test
        fields, concepts = gen.sequentially_process_tab_contents(values)

        # post conditions
        expected_fields = ['field_one', 'field_two', 'field_three']
        expected_vals = [
            {'field_one': ['val_one'], 'field_two': ['val_two'], 'field_three': ['val_three']},
            {'field_one': ['val_four'], 'field_two': ['val_five'], 'field_three': ['val_six']},

        ]

        self.assertEqual(fields, expected_fields)
        self.assertEqual(concepts, expected_vals)

    def test_process_tab_contents(self):
        # pre-conditions
        values = [
            ['field One', 'field Two', 'Field Three'],
            ['val_one', 'val_two', 'val_three'],
            ['val_four', 'val_five', 'val_six'],
        ]

        #test
        fields, concepts = gen.process_tab_contents(values, 1)

        # post conditions
        expected_fields = ['field_one', 'field_two', 'field_three']
        expected_vals = {
            'val_two': {'field_one': ['val_one'], 'field_three': ['val_three']},
            'val_five': {'field_one': ['val_four'], 'field_three': ['val_six']}
        }

        self.assertEqual(fields, expected_fields)
        self.assertEqual(concepts, expected_vals)

    def test_write_yaml_file_list(self):
        # pre-conditions
        today_time = self.today + " 09:45:33"
        mock_file = mock_open()
        meta_data = {
            consts.CREATED_TIME_FIELD: today_time,
            consts.CONCEPT_ID_FIELD: 80,
            'cdr_version': 'R2019Q8R1'
        }

        fields = [consts.CONCEPT_ID_FIELD, consts.DATE_REQUESTED_FIELD, consts.REGISTERED_TRANSFORM_FIELD, 'name']
        name = 'name'
        none_exc = 'none_exception_trigger'
        int_exc = 'integer_exception_trigger'
        false = 'false_boolean'
        values = [
            {
                consts.CONCEPT_ID_FIELD: ['33'],
                consts.DATE_REQUESTED_FIELD: [self.today],
                consts.REGISTERED_TRANSFORM_FIELD: ['yes'],
                name:  ['phony_field'],
                none_exc: [None],
                int_exc: [20],
                false: ['no']
            }
        ]
        sequence_name = 'change log and concepts'
        index = 3

        # test
        with patch('cdr_data_dictionary.generate_yaml.open', mock_file):
            gen.write_yaml_file(mock_file, meta_data, [fields], [values], [sequence_name], [index])

        # post conditions
        expected_calls = [
             call().write('meta_data:\n  -\n'),
             call().write('    {}: '.format(consts.CREATED_TIME_FIELD)),
             call().write(today_time + '\n'),
             call().write('    {}: '.format(consts.CONCEPT_ID_FIELD)),
             call().write(80),
             call().write('\n'),
             call().write('    cdr_version: '),
             call().write("'R2019Q8R1'\n"),
             call().write('\n'),
             call().write('transformations:\n'),
             call().write('  - \n    change log and concepts:\n'),
             call().write('      - \n'),
             call().write('        {}:  '.format(name)),
             call().write("'phony_field'\n"),
             call().write('        {}:  '.format(consts.REGISTERED_TRANSFORM_FIELD)),
             call().write(True),
             call().write('\n'),
             call().write('        {}:  '.format(none_exc)),
             call().write('\n'),
             call().write('        {}:  '.format(consts.DATE_REQUESTED_FIELD)),
             call().write(self.today + '\n'),
             call().write('        {}:  '.format(int_exc)),
             call().write("'20'\n"),
             call().write('        {}:  '.format(false)),
             call().write('\n'),
             call().write('        {}:  '.format(consts.CONCEPT_ID_FIELD)),
             call().write(u'33'),
             call().write('\n'),
             call().write('\n'),
        ]

        result_calls = mock_file.mock_calls[2:-1]
        self.assertEqual(result_calls, expected_calls)
