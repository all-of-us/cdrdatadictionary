# Python imports
from argparse import ArgumentParser, ArgumentTypeError
import logging
import os.path
import pickle
from string import ascii_uppercase

# Third party imports
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Project imports

LOGGER = logging.getLogger(__name__)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def add_console_logging():
    """

    This config should be done in a separate module, but that can wait
    until later.  Useful for debugging.

    """
    logging.basicConfig(level=logging.INFO,
                        filename='generate_yaml.log',
                        filemode='a')

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)


def create_drive_credentials(key_filepath):
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                key_filepath, SCOPES
            )
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def create_spreadsheets_service(credentials=None):
    if not credentials:
        raise RuntimeError("No credentials provided")

    return build('sheets', 'v4', credentials=credentials, cache_discovery=False)


def read_sheet_values(service, args):
    sheet = service.spreadsheets()

    if args.range is None:
        cell_range = args.sheet_name
    else:
        cell_range = args.sheet_name + '!' + args.range

    result = sheet.values().get(
        spreadsheetId=args.spreadsheet_id, range=cell_range, majorDimension='ROWS'
    ).execute()

    values = result.get('values', [])

    return values


def _process_value(value):
    result = None
    try:
        value = value.replace(u'\u00AD', '-')
        value = value.replace(u'\u2010', '-')
        value = value.replace(u'\u2019', "'")
        value = value.replace(u'\u201c', '"')
        value = value.replace(u'\u201d', '"')
        result = value.encode('utf-8', 'ignore')
    except AttributeError:
        if value is None:
            LOGGER.debug("Value '%s' can not be utf-8 encoded", value)
        elif isinstance(value, int):
            result = str(value)

    result = result.replace('\n', '\n  ')
    result = result.strip()
    return result


def _process_field_names(name_list):
    normalized_names = []
    for name in name_list:
        name = name.lower()
        name = name.replace(' ', '_')
        normalized_names.append(name)

    return normalized_names


def _process_value(value):
    result = None
    try:
        value = value.replace(u'\u00AD', '-')
        value = value.replace(u'\u2010', '-')
        value = value.replace(u'\u2019', "'")
        value = value.replace(u'\u201c', '"')
        value = value.replace(u'\u201d', '"')
        result = value.encode('utf-8', 'ignore')
    except AttributeError:
        if value is None:
            LOGGER.debug("Value '%s' can not be utf-8 encoded", value)
        elif isinstance(value, int):
            result = str(value)

    result = result.replace('\n', ',  ')
    result = result.replace('"', "'")
    result = result.strip()
    return result


def append_to_existing(field, value, values_dict):
    existing = values_dict.get(field, [])
    if value in existing:
        return existing

    existing.append(value)
    return existing


def process_file_contents(values, id_index):
    fields = _process_field_names(values[0])
    concepts = {}
    for value in values[1:]:
        existing_values = concepts.get(value[id_index], {})
        new_dict = {}
        for index, val in enumerate(value):
            if index == id_index:
                continue
            new_value = append_to_existing(fields[index], val, existing_values)
            new_dict[fields[index]] = new_value
        concepts[value[id_index]] = new_dict
    return fields, concepts


def write_yaml_file(filepath, fields, value_dict, sequence_name, index):
    with open(filepath, 'w') as yaml:
        yaml.write('transformations:\n')
        yaml.write('  - \n    ' + sequence_name + ':\n')
        for key, value in value_dict.iteritems():
            key = _process_value(key)
            if key is None or key.isspace() or not key:
                continue
            yaml.write('      - \n')   # marks this as a sequence
            yaml.write('        ' + fields[index] + ':  ' + key + '\n')
            for sub_key, sub_value in value.iteritems():
                yaml.write('        ' + sub_key + ':  ')
                all_vals = ', '.join(sub_value)
                val = _process_value(all_vals)
                try:
                    if ':' in val:
                        yaml.write('"')
                        yaml.write(val + '"\n')
                    else:
                        yaml.write(val + '\n')
                except IndexError:
                    LOGGER.exception("can't write value for field %s", sub_key)
                    yaml.write('  IndexError - cant write this value\n')
                except UnicodeEncodeError:
                    LOGGER.exception("can't write value for field %s", sub_key)
                    yaml.write('  UnicodeEncodeError - cant write this value\n')
                except UnicodeDecodeError:
                    LOGGER.exception("can't write value for field %s", sub_key)
                    yaml.write('  UnicodeDecodeError - cant write this value\n')
            yaml.write('\n')


def _get_sequence_title(title):
    sequence_title = title.lower()
    sequence_title = sequence_title.replace(' ', '_')
    sequence_title = sequence_title.replace('(row)_', '')
    sequence_title = sequence_title.replace('(column)_', '')
    return sequence_title

def create_yaml_file(settings, values):
    group_by = settings.column_id
    output_file = settings.output_file
    if settings.sheet_name in ['Concept (Row) Generalizations', 'Concept (Row) Suppressions']:
        if group_by is None:
            group_by = 3
    elif settings.sheet_name in ['Field (Column) Generalizations', 'Field (Column) Suppressions',
                                 'Available Fields']:
        if group_by is None:
            group_by = 1
    elif settings.sheet_name in ['Table Suppressions', 'Change Log']:
        if group_by is None:
            group_by = 0
    else:
        if group_by is None:
            group_by = 0
        try:
            column = ascii_uppercase[group_by]
        except IndexError:
            LOGGER.exception("Cannot use index greater than 25 (Z)")
            group_by = 0
            column = 'A'

        LOGGER.info("Sheet name unrecognized.  Grouping will be done on Column %s.", column)

    sequence_title = _get_sequence_title(settings.sheet_name)
    fields, values_dict = process_file_contents(values, group_by)
    write_yaml_file(output_file, fields, values_dict, sequence_title, group_by)

    LOGGER.info("Done.  Read %d values.  Created yaml file with %d items.",
                len(values), len(values_dict))


def _ascii_to_index(column):
    if column is None:
        return None
    index = ascii_uppercase.find(column)
    if index == -1:
        message = "Column {} is not an upper case ascii letter"
        raise ArgumentTypeError(message)

    return index


def _parse_command_line():
    parser = ArgumentParser(
        description=(
            'Google drive yaml prototype.  Automatically generates a yaml file '
            'from the read only version of the identified file.  Defaults exist '
            'for choosing the value to group around.  See '
            'https://developers.google.com/sheets/api/quickstart/python and '
            'https://developers.google.com/sheets/api/guides/concepts '
            'for information on configuring required credentials for reading '
            'Google Drive files.'
        )
    )
    parser.add_argument('key_file', type=file, action='store',
                        help='Filepath to your service account or client secret key')
    parser.add_argument('spreadsheet_id', action='store',
                        help='Google spreadsheet ID (as seen in URL)')
    parser.add_argument('sheet_name', action='store',
                        help=('Name of the sheet in the spreadsheet to parse.  '
                              'Enclose in quotes if the name contains spaces.'))
    parser.add_argument('-r', '--range',
                        dest='range',
                        action='store',
                        help=('Range of cells to select in the sheet.  '
                              'If not specified, returns all cell values.')
                       )
    parser.add_argument('-o', '--output_file', action='store', default='out.yaml',
                        dest='output_file',
                        help=('Name to give the produced yaml file.  If not '
                              'provided, defaults to out.yaml')
                       )
    parser.add_argument('-g', '--group_by', action='store', default=None,
                        dest='column_id', choices=ascii_uppercase,
                        help=('Used to create groupings around a different field '
                              'in a sheet.  Sheets with \'Field\' in the title '
                              'default to Column B.  Sheets with \'Row\' in the '
                              'title default to Column D.  Sheets with neither in '
                              'the title default to Column A.')
                       )
    args = parser.parse_args()
    return args

def main():
    add_console_logging()
    args = _parse_command_line()
    args.column_id = _ascii_to_index(args.column_id)
    credentials = create_drive_credentials(args.key_file.name)
    service = create_spreadsheets_service(credentials)
    values = read_sheet_values(service, args)

    create_yaml_file(args, values)

if __name__ == '__main__':
    main()
