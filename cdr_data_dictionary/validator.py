"""
A module to validate the generated yaml file.

This modules uses a third party package, yamale, to validate the created
yaml file against a schema defintion file.

This implements a custom URL validator based on regular expressions.
"""
# Python imports
from argparse import ArgumentParser
import re

# Third party imports
import yamale
from yamale.validators import DefaultValidators, Validator

# Project imports
from cdr_data_dictionary import constants as consts


class URL(Validator):
    """ Custom URL validator """
    tag = 'url'

    def _is_valid(self, value):
        try:
            if re.match(consts.URL_REGEX, value):
                return True
            return False
        except TypeError:
            return False


def validate(schema_path, dict_path):
    """
    Perform the yaml file validation.

    :param schema_path:  The path to the schema defintion file.
    :param dict_path:  The path to the file to validate.
    """
    validators = DefaultValidators.copy()  # This is a dictionary
    validators[URL.tag] = URL

    schema = yamale.make_schema(schema_path, validators=validators)
    data = yamale.make_data(dict_path)
    yamale.validate(schema, data)


def _parse_command_line(raw_args=None):
    """
    Parse the command line arguments.

    :param raw_args:  If not None, the arguments to parse.  Otherwise, the
        raw command line arguments are parsed.
    """
    parser = ArgumentParser(
        description=(
            'Yaml file generator validator.  Can be run separately or called from '
            'this module.  Uses the Yamale pacakge to perform the validation.'
        )
    )
    parser.add_argument('-s', '--schema-file', dest='schema_file', action='store',
                        default='schema.yaml',
                        help=('Path to the schema yaml file.  If not provided, '
                              'defaults to \'schema.yaml\' in the current directory.')
                       )
    parser.add_argument('-y', '--yaml-file', dest='yaml_file', action='store',
                        default='out.yaml',
                        help=('Path to the yaml dictionary file.  If not '
                              'provided, defaults to \'out.yaml\' in the '
                              'current directory.')
                       )
    args = parser.parse_args(raw_args)
    return args


if __name__ == '__main__':
    ARGS = _parse_command_line()
    validate(ARGS.schema_file, ARGS.yaml_file)
