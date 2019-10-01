# Python imports
from argparse import ArgumentParser

# Third party imports
import yamale


def validate(schema_path, dict_path):
    schema = yamale.make_schema(schema_path)
    data = yamale.make_data(dict_path)
    yamale.validate(schema, data)


def _parse_command_line():
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
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    ARGS = _parse_command_line()
    validate(ARGS.schema_file, ARGS.yaml_file)
