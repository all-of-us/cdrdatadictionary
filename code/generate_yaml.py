
# Python imports
from argparse import ArgumentParser, ArgumentTypeError
import logging
import os.path
import pickle
from string import ascii_uppercase

# Third party imports
from dateutil import parser as dt_parser
from future.utils import viewitems
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Project imports
from validator import validate

LOGGER = logging.getLogger(__name__)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
INTEGER_FIELDS = ['concept_id', 'generalized_output_concept_id', 'input_concept_id']
BOOLEAN_FIELDS = ['transformed_by_registered_tier_privacy_methods']
DATE_FIELDS = ['date_requested', 'date_completed']
SHEET_NAMES = [
    'Change Log',
    'Available Fields',
    'Table Suppressions',
    'Field (Column) Suppressions',
    'Concept (Row) Suppressions',
    'Field (Column) Generalizations',
    'Concept (Row) Generalizations'
]
ALL = 'all'
DATE_FORMAT = '%Y-%m-%d'

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

    try:
        # use service account credentials if they exist
        creds = service_account.Credentials.from_service_account_file(
            key_filepath, scopes=SCOPES)
    except ValueError:
        # service account creds aren't being used.  try loading from a stored
        # token file
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # create oauth tokens if credentials are not valid
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # forces a login screen in a web browser
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

    if args.range is None and args.sheet_name is not ALL:
        cell_list = [args.sheet_name]
    elif args.sheet_name is ALL:
        cell_list = SHEET_NAMES
    else:
        cell_list = [args.sheet_name + '!' + args.range]

    results = []
    for cell_range in cell_list:
        result = sheet.values().get(
            spreadsheetId=args.spreadsheet_id, range=cell_range, majorDimension='ROWS'
        ).execute()

        values = result.get('values', [])
        results.append((cell_range, values))

    return results


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
        result = value
    except AttributeError:
        LOGGER.exception("Attribute error encountered for: [%s]", value)
        if value is None:
            LOGGER.debug("Value '%s' can not be utf-8 encoded", value)
        elif isinstance(value, int):
            result = str(value)

    if result:
        result = result.strip()
        result = result.replace('\n', ',  ')
        result = result.replace("'", "''")
        result = result.strip()

        if result.lower() == 'yes':
            return True

        if result.lower() == 'no':
            return False

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


def _write_value(yaml_writer, key, value):
    try:
        if key in INTEGER_FIELDS or key in BOOLEAN_FIELDS:
            yaml_writer.write(value)
            yaml_writer.write('\n')
        elif key in DATE_FIELDS:
            date = dt_parser.parse(value)
            dt_str = date.strftime(DATE_FORMAT)
            yaml_writer.write(dt_str + "\n")
        else:
            yaml_writer.write("'" + value + "'\n")
    except IndexError:
        LOGGER.exception("can't write value for field %s", key)
        yaml_writer.write('  IndexError - cant write this value\n')
    except UnicodeEncodeError:
        LOGGER.exception("can't write value for field %s", key)
        yaml_writer.write('  UnicodeEncodeError - cant write this value\n')
    except UnicodeDecodeError:
        LOGGER.exception("can't write value for field %s", key)
        yaml_writer.write('  UnicodeDecodeError - cant write this value\n')
    except TypeError:
        yaml_writer.write(str(value) + '\n')


def write_yaml_file(filepath, fields, value_dict, sequence_name, index):
    with open(filepath, 'w') as yaml:
        yaml.write('transformations:\n')
        for list_index, _ in enumerate(sequence_name):
            _write_yaml_list(yaml,
                             fields[list_index],
                             value_dict[list_index],
                             sequence_name[list_index],
                             index[list_index]
                            )


def _write_yaml_list(yaml, fields, value_dict, sequence_name, index):
    yaml.write('  - \n    ' + sequence_name + ':\n')
    for key, value in viewitems(value_dict):
        key = _process_value(key)
        if key is None or key.isspace() or not key:
            continue
        yaml.write('      - \n')   # marks this as a sequence
        yaml.write('        ' + fields[index] + ":  ")
        if fields[index] in INTEGER_FIELDS or fields[index] in BOOLEAN_FIELDS:
            yaml.write(key)
            yaml.write('\n')
        else:
            yaml.write("'" + key + "'\n")
        for sub_key, sub_value in viewitems(value):
            yaml.write('        ' + sub_key + ':  ')
            if len(sub_value) > 1:  # more than one item, write an array/seq
                yaml.write('\n')
                for val in sub_value:
                    val = _process_value(val)
                    if val:
                        yaml.write('          - ')
                        _write_value(yaml, sub_key, val)
            else:
                sub_value = _process_value(sub_value[0])
                if sub_value:
                    _write_value(yaml, sub_key, sub_value)
                else:
                    yaml.write('\n')

        yaml.write('\n')


def _get_sequence_title(title):
    sequence_title = title.lower()
    sequence_title = sequence_title.replace(' ', '_')
    sequence_title = sequence_title.replace('(row)_', '')
    sequence_title = sequence_title.replace('(column)_', '')
    return sequence_title


def _create_yaml_file(settings, sheet_name, values):
    group_by = settings.column_id
    if sheet_name in ['Concept (Row) Generalizations', 'Concept (Row) Suppressions']:
        if group_by is None:
            group_by = 3
    elif sheet_name in ['Field (Column) Generalizations', 'Field (Column) Suppressions',
                        'Available Fields']:
        if group_by is None:
            group_by = 1
    elif sheet_name in ['Table Suppressions', 'Change Log']:
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

    sequence_title = _get_sequence_title(sheet_name)
    fields, values_dict = process_file_contents(values, group_by)
    return (sequence_title, fields, values_dict, group_by)


def create_yaml_file(settings, values):
    output_file = settings.output_file

    seq_titles = []
    output_fields = []
    output_values = []
    grouped_by = []
    for item in values:
        seq_title, fields, values_dict, grouped = _create_yaml_file(settings, item[0], item[1])
        seq_titles.append(seq_title)
        output_fields.append(fields)
        output_values.append(values_dict)
        grouped_by.append(grouped)

    write_yaml_file(output_file, output_fields, output_values, seq_titles, grouped_by)

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
    parser.add_argument('key_file', action='store',
                        help='Filepath to your service account or client secret key')
    parser.add_argument('spreadsheet_id', action='store',
                        help='Google spreadsheet ID (as seen in URL)')
    parser.add_argument('-s', '--sheet_name', action='store',
                        dest='sheet_name', default=ALL,
                        help=('Name of the sheet in the spreadsheet to parse.  '
                              'Enclose in quotes if the name contains spaces.  '
                              'If not provided, defaults to all sheets.'))
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
    parser.add_argument('-d', '--schema-file', dest='schema_file', action='store',
                        default='schema.yaml',
                        help=('Path to the schema yaml file.  If not provided, '
                              'defaults to \'schema.yaml\' in the current directory.')
                       )
    args = parser.parse_args()
    return args

def main():
    add_console_logging()
    args = _parse_command_line()
    credentials = create_drive_credentials(args.key_file)
    service = create_spreadsheets_service(credentials)

    args.column_id = _ascii_to_index(args.column_id)
    values = read_sheet_values(service, args)

    create_yaml_file(args, values)

    try:
        validate(args.schema_file, args.output_file)
    except ValueError:
        LOGGER.exception('The generated file does not validate.  Check the '
                         'input source Google spreadsheet and the schema '
                         'definition file for changes.  Update as needed.')


if __name__ == '__main__':
    main()
