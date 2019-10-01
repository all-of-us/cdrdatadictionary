
# Python imports
import logging
from string import ascii_uppercase

# Third party imports
from dateutil import parser as dt_parser
from future.utils import viewitems

# Project imports
import constants as consts
import cdr_parser
import service as service
import validator
import yaml_logging

LOGGER = logging.getLogger(__name__)

def _process_field_names(name_list):
    """
    Read the first row of the tab as a list of field names.

    Processes each column name so that field names are all lower cased letters
    and spaces are replaced with underscores.  These are normalized and used as
    identifiers in the yaml file.

    :param name_list:  a list of string values where each item represents a column
        from the tab and becomes a yaml file field.

    :return:  a list of normalized field names
    """
    normalized_names = []
    for name in name_list:
        name = name.lower()
        name = name.replace(' ', '_')
        normalized_names.append(name)

    return normalized_names


def _process_value(value):
    """
    Process the values to make writing to a yaml file easier.

    Replaces common unicode characters.
    Removes leading and trailing whitespace.
    Replaces new lines with commas and spaces to preserve the yaml file formatting.

    :param value:  The value to process

    :return:  True of False if the value was 'yes' or 'no'.  Otherwise, A string that
        can be written to the output file.
    """
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


def append_to_results(field, value, values_dict, unique=False):
    """
    Helper to add values to fields for specific concepts.

    If the value already exists in the values_dict, it is not added a second
    time.

    :param field:  name of the field
    :param value:  the value to add to a concept
    :param values_dict:  the values that have been processed up to
        this point
    :param unique:  a flag to only append unique results

    :return:  a list of unique values associated with that field
    """
    existing = values_dict.get(field, [])
    if value in existing and unique:
        return existing

    existing.append(value)
    return existing


def sequentially_process_tab_contents(values):
    """
    Helper method to clean and organize tab values.

    :param values:  list of values read from the tab.  each row is a list of
        values where each list item corresponds to a row.

    :return:  A tuple for each tab.  The dictionary of concepts is arranged
        around the field at id_index.  For each unique value in the column
        identified by id_index, it returns a dictionary of all the other
        fields and associated values.
        (A list of fields, A dictionary of concepts)
    """
    fields = _process_field_names(values[0])
    concepts = []
    for value in values[1:]:
        new_dict = {}
        for index, val in enumerate(value):
            new_value = append_to_results(fields[index], val, {})
            new_dict[fields[index]] = new_value
        concepts.append(new_dict)
    return fields, concepts


def process_tab_contents(values, id_index):
    """
    Helper method to clean and organize tab values.

    :param values:  list of values read from the tab.  each row is a list of
        values where each list item corresponds to a row.
    :param id_index:  integer value identifying which column is used to group
        the values as each row is processed.  used to build a dictionary of
        values where the key is based on the value of the items in the
        id_index column

    :return:  A tuple for each tab.  The dictionary of concepts is arranged
        around the field at id_index.  For each unique value in the column
        identified by id_index, it returns a dictionary of all the other
        fields and associated values.
        (A list of fields, A dictionary of concepts)
    """
    fields = _process_field_names(values[0])
    concepts = {}
    for value in values[1:]:
        existing_values = concepts.get(value[id_index], {})
        new_dict = {}
        for index, val in enumerate(value):
            if index == id_index:
                continue
            new_value = append_to_results(fields[index], val, existing_values)
            new_dict[fields[index]] = new_value
        concepts[value[id_index]] = new_dict
    return fields, concepts


def _write_value(yaml_writer, field_name, value):
    """
    Write the value to the yaml file.

    :param yaml_writer:  open file descriptor that is being written to
    :param field_name:  The name of the field the value is associated with.
        It is used to determine how to write the value.
    :param value:  The processed value to write.
    """
    try:
        if field_name in consts.INTEGER_FIELDS or field_name in consts.BOOLEAN_FIELDS:
            yaml_writer.write(value)
            yaml_writer.write('\n')
        elif field_name in consts.TEMPORAL_FIELDS:
            date = dt_parser.parse(value)
            dt_str = date.strftime(consts.DATE_FORMAT)
            yaml_writer.write(dt_str + "\n")
        else:
            yaml_writer.write("'" + value + "'\n")
    except IndexError:
        LOGGER.exception("can't write value for field %s", field_name)
        yaml_writer.write('  IndexError - cant write this value\n')
    except UnicodeEncodeError:
        LOGGER.exception("can't write value for field %s", field_name)
        yaml_writer.write('  UnicodeEncodeError - cant write this value\n')
    except UnicodeDecodeError:
        LOGGER.exception("can't write value for field %s", field_name)
        yaml_writer.write('  UnicodeDecodeError - cant write this value\n')
    except TypeError:
        yaml_writer.write(str(value) + '\n')


def _write_meta_data(yaml_writer, meta_data):
    """
    Helper function to write the meta data dictionary into the yaml output file

    :param yaml_writer:  The yaml file writer object.
    :param meta_data:  a dictionary of meta data values.  Everything in the
        dictionary is written to the meta_data yaml object.
    """
    yaml_writer.write('meta_data:\n  -\n')
    for key, value in viewitems(meta_data):
        yaml_writer.write('    ' + key + ': ')
        if key in consts.INTEGER_FIELDS or key in consts.BOOLEAN_FIELDS:
            yaml_writer.write(value)
            yaml_writer.write('\n')
        elif key in consts.TEMPORAL_FIELDS:
            date = dt_parser.parse(value)
            dt_str = date.strftime(consts.DATETIME_FORMAT)
            yaml_writer.write(dt_str + '\n')
        else:
            yaml_writer.write("'" + value + "'\n")


def write_yaml_file(filepath, meta_data, fields, values_container, sequence_name, index):
    """
    Function responsible for writing the dictionary values into a yaml file.

    :param filepath: name of the generated file, as specified from the command line.
    :param meta_data:  dictionary of meta data describing the spreadsheet
    :param fields: a list of fields for each tab.  each tab has a list of fields.
        this is a list of lists.
    :param value_container: a representation of the values read from the
        spreadsheet in either list or dictionary form.
    :param sequence_name:  the generated sequence name.  used to identify which
        yaml sequence the following values are definitions of.
    :param index:  identifier for the column grouped by. Identifies the first
        field that will be written for each dictionary item.
    """
    with open(filepath, 'w') as yaml:
        # write the meta data
        _write_meta_data(yaml, meta_data)
        yaml.write('\n')

        # start writing actual value data
        yaml.write('transformations:\n')
        for list_index, _ in enumerate(sequence_name):
            LOGGER.info("Writing transformations for: %s", sequence_name[list_index])
            yaml.write('  - \n    ' + sequence_name[list_index] + ':\n')

            if isinstance(values_container[list_index], dict):
                _write_yaml_dict(yaml,
                                 fields[list_index],
                                 values_container[list_index],
                                 index[list_index]
                                )
            elif isinstance(values_container[list_index], list):
                _write_yaml_list(yaml,
                                 fields[list_index],
                                 values_container[list_index],
                                 index[list_index]
                                )


def _write_yaml_list(yaml, fields, value_list, index):
    grouping_field = fields[index]

    for value_dict in value_list:
        yaml.write('      - \n')   # marks this as a sequence
        yaml.write('        ' + grouping_field + ":  ")

        grouping_value = value_dict.get(fields[index])[0]
        if grouping_field in consts.INTEGER_FIELDS or grouping_field in consts.BOOLEAN_FIELDS:
            yaml.write(grouping_value)
            yaml.write('\n')
        else:
            yaml.write("'" + grouping_value + "'\n")

        for key, value in viewitems(value_dict):
            if key == grouping_field:
                continue
            yaml.write('        ' + key + ':  ')
            sub_value = _process_value(value[0])
            if sub_value:
                _write_value(yaml, key, sub_value)
            else:
                yaml.write('\n')

        yaml.write('\n')


def _write_yaml_dict(yaml, fields, value_dict, index):
    for key, value in viewitems(value_dict):
        key = _process_value(key)
        if key is None or key.isspace() or not key:
            continue
        yaml.write('      - \n')   # marks this as a sequence
        yaml.write('        ' + fields[index] + ":  ")
        if fields[index] in consts.INTEGER_FIELDS or fields[index] in consts.BOOLEAN_FIELDS:
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
    """
    Helper function to clean up tab names to become yaml sequence titles.

    Replaces all spaces in the string with underscores.
    Removes '(row)_' and '(column)_' from title names.
    Returns modified string as the yaml sequence title.

    :param title:  The tab name.

    :return:  A modified string for the tab name.  Will be used as the yaml
        sequence identifier.
    """
    sequence_title = title.lower()
    sequence_title = sequence_title.replace(' ', '_')
    sequence_title = sequence_title.replace('(row)_', '')
    sequence_title = sequence_title.replace('(column)_', '')
    return sequence_title


def _create_yaml_file(settings, tab_name, values):
    """
    Helper method to determine how the values for a tab are processed.

    Takes the values and command line arguments and determines what the 'group by'
    column should be.  If a specified sheet name is unrecognized, this is logged.
    The default 'group_by' value depends on the tab that was read.  Generates
    a yaml sequence title based on the tab_name.

    ;param settings:  python namespace values from command line parameters.
    :param tab_name:  name of the tab the values are associated with.
    :param values:  a list of values read from the spreadsheet's tab

    :return:  a tuple of values.  The yaml file sequence title, the fields
        read in the spreadsheet tab, the values dictionary, and the group_by
        column id.  The values dictionary is a dictionary with keys specified
        as the unique values found in the column identified by 'group_by'.  Each
        concept contains a dictionary of the other fields and their associated
        unique values.  These sub-keys may contain list values.
        (sequence_title, fields, values_dict, group_by)
    """
    sequence_title = _get_sequence_title(tab_name)
    group_by = settings.column_id

    fields, values_list = None, None
    if not group_by:
        fields, values_list = sequentially_process_tab_contents(values)

    if tab_name in ['Concept (Row) Generalizations', 'Concept (Row) Suppressions']:
        if group_by is None:
            group_by = 3
    elif tab_name in ['Field (Column) Generalizations', 'Field (Column) Suppressions',
                      'Available Fields']:
        if group_by is None:
            group_by = 1
    elif tab_name in ['Table Suppressions', 'Change Log']:
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

    if not fields:
        fields, values_list = process_tab_contents(values, group_by)

    return (sequence_title, fields, values_list, group_by)


def create_yaml_file(settings, values, meta_data):
    """
    Entry point for creating a yaml file from the given values and settings

    :param settings:  command line settings for generating the yaml file.
        python namespace values.
    :param values:  values read from the google drive spreadsheet.  a list of
        tuples in the form (tab_name, values).
    :param meta_data:  a dictionary of file meta data.  added to the yaml file
        for ease of access
    """
    output_file = settings.output_file

    seq_titles = []
    output_fields = []
    output_values = []
    grouped_by = []
    for item in values:
        seq_title, fields, values_list, grouped = _create_yaml_file(settings, item[0], item[1])
        seq_titles.append(seq_title)
        output_fields.append(fields)
        output_values.append(values_list)
        grouped_by.append(grouped)

    write_yaml_file(output_file, meta_data, output_fields, output_values, seq_titles, grouped_by)

    LOGGER.info("Done.  Read %d tabs.  Created yaml file: %s",
                len(seq_titles), output_file)


def main(raw_args=None):
    """
    Main entry point to generating yaml from a spreadsheet.
    """
    # read command line and set up logging
    args = cdr_parser.parse_command_line(raw_args)
    yaml_logging.setup_logging(args)

    # get the service started up
    credentials = service.create_drive_credentials(args.key_file)
    dd_values_service = service.create_spreadsheets_service(credentials)
    dd_meta_service = service.create_meta_data_service(credentials)
    LOGGER.debug("Successfully set up credentials.")

    # read the values
    values = service.read_sheet_values(dd_values_service, args)

    # read the meta data
    meta_data = service.read_meta_data(dd_meta_service, args)
    # add cdr version to meta data
    meta_data['cdr_version'] = args.cdr_version

    for index, _ in enumerate(values):
        LOGGER.info("Read %d values from: %s", len(values[index][1]), values[index][0])

    # create the yaml file
    create_yaml_file(args, values, meta_data)
    LOGGER.debug("Created the yaml file.")

    # validate the created yaml file
    try:
        validator.validate(args.schema_file, args.output_file)
    except ValueError:
        LOGGER.exception('The generated file does not validate.  Check the '
                         'input source Google spreadsheet and the schema '
                         'definition file for changes.  Update as needed.')
    else:
        LOGGER.info("Successfully validated yaml file: %s", args.output_file)


if __name__ == '__main__':
    main()
