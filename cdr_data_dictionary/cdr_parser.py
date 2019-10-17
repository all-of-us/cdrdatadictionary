"""
Module responsible for reading command line arguments and instructing the package
how to perform.
"""

# Python imports
from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime
from string import ascii_uppercase

# Third party imports

# Project imports
from cdr_data_dictionary import constants as consts

def ascii_to_index(column):
    """
    Helper function to get the proper index associated with lettered column identifiers.

    :param column: A letter used to identify a column.

    :return:  An error if a single letter is not indicated.  None if nothing
        is selected.  Or an integer index value corresponding to where the letter
        is placed in the alphabet.
    """
    if column is None:
        return None

    column = column.upper()

    index = ascii_uppercase.find(column)
    if index == -1:
        message = "Column {} is not an spreadsheet column identifier (upper case ascii letter)."
        raise ArgumentTypeError(message)

    return index


def output_filename(version):
    """
    Sets the output file name.

    :param version:  The version of the CDR this file is generated to interpret.

    :return:  The output filename and filepath.
    """
    out = consts.YAML_OUTPUT_FILENAME
    today = datetime.now().strftime(consts.FILENAME_DATE_FORMAT)
    out = out.format(cdr_version=version, today=today)
    return out


def log_filepath(filepath):
    """
    Verify a log filepath is given.

    filepath must end in .log if specified.

    :param filepath:  string specifying the filepath

    :return:  string filepath

    :raises ArgumentTypeError:  raised if path doesn't end with '.log'
    """
    if filepath.endswith('.log'):
        return filepath
    else:
        raise ArgumentTypeError("Log file names must end with '.log'")


def parse_command_line(raw_args=None):
    """
    Parse the command line arguments.

    :param raw_args:  If None, the raw system arguments. Else a list of
        arguments to be passed to this parser.

    :return:  A namespace object of command line arguments.
    """
    parser = ArgumentParser(
        description=(
            'Automatically generates a yaml file '
            'from the read only version of the cdr data dictionary.  '
            'Output files are saved to cdrdatadictionary/yaml_files/ '
            'with the name CDRDD_<cdr_version>_YYYYMMDD.yaml'
        )
    )
    parser.add_argument('-k', '--key-file', action='store', dest='key_file',
                        required=True,
                        help='Filepath to your service account or client secret key')
    parser.add_argument('-i', '--spreadsheet-id', action='store', dest='spreadsheet_id',
                        required=True,
                        help='Google spreadsheet ID (as seen in URL)')
    parser.add_argument('-s', '--sheet-name', action='store',
                        dest='sheet_name', default=consts.ALL,
                        help=('Name of the sheet in the spreadsheet to parse.  '
                              'Enclose in quotes if the name contains spaces.  '
                              'If not provided, defaults to all sheets.'))
    parser.add_argument('-r', '--range',
                        dest='range',
                        action='store',
                        help=('Range of cells to select in the sheet.  '
                              'If not specified, returns all cell values.')
                       )
    parser.add_argument('-g', '--group-by', action='store', default=None,
                        dest='column_id',
                        type=ascii_to_index,
                        help=('Used to create groupings around fields in a tab.  '
                              'Tabs with \'Field\' in the title '
                              'default to Column B.  Tabs with \'Row\' in the '
                              'title default to Column D.  Tabs with neither in '
                              'the title default to Column A.  Valid choices are letters A-Z.')
                       )
    parser.add_argument('-d', '--schema-file', dest='schema_file', action='store',
                        default='cdr_data_dictionary/schema.yaml',
                        help=('Path to the schema yaml file.  If not provided, '
                              'defaults to \'cdr_data_dictionary/schema.yaml\'.')
                       )
    parser.add_argument('-l', '--log-path', dest='log_path', action='store',
                        default=consts.DEFAULT_LOG, type=log_filepath,
                        help=('Specify the log file path and/or name.  File name '
                              'should end in \'.log\'.  Defaults to '
                              '{}'.format(consts.DEFAULT_LOG))
                       )
    parser.add_argument('-c', '--console-log', dest='console_log', action='store_true',
                        help='Print logs to the console, in addition to the log file.')
    parser.add_argument('--cdr-version', dest='cdr_version', action='store',
                        required=True,
                        help='CDR version number.  Used as part of output file name.')
    args = parser.parse_args(raw_args)

    filename = output_filename(args.cdr_version)
    setattr(args, 'output_file', filename)
    return args


if __name__ == '__main__':
    parse_command_line()
