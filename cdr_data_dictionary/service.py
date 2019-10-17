"""
Module responsible for creating a connection to and reading values from google spreadsheets.
"""

# Python imports
import logging
import os.path
import pickle

# Third party imports
from future.utils import viewitems
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Project imports
from cdr_data_dictionary import constants as consts

LOGGER = logging.getLogger(__name__)

def create_drive_credentials(key_filepath):
    """
    Read or create user credentials as needed.

    :param key_filepath:  path to the user keys.  If missing,
        keys may be created.

    :return:  necessary credentials.
    """
    creds = None

    try:
        # use service account credentials if they exist
        creds = service_account.Credentials.from_service_account_file(
            key_filepath, scopes=consts.SCOPES)
    except ValueError:
        # service account creds aren't being used.  try loading from a stored
        # token file
        LOGGER.debug("Could not use service account credentials.")
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        else:
            LOGGER.debug("'token.pickle' does not exist.")

        # create oauth tokens if credentials are not valid
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                LOGGER.debug("Refreshing credentials.")
                creds.refresh(Request())
            else:
                # forces a login screen in a web browser
                flow = InstalledAppFlow.from_client_secrets_file(
                    key_filepath, consts.SCOPES
                )
                creds = flow.run_local_server()
                LOGGER.debug("Created new credentials via web login.")
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                LOGGER.debug("Wrote new token file.  DO NOT SAVE to repository.")

    return creds


def create_spreadsheets_service(credentials=None):
    """
    Use credentials to create a service to read google sheets objects.

    :param credentials:  Credentials to use to build an API reader.  If invalid,
        the user will not get access.

    :return:  the service object.
    """
    if not credentials:
        raise RuntimeError("No credentials provided to read spreadsheet")

    return build('sheets', 'v4', credentials=credentials, cache_discovery=False)


def create_meta_data_service(credentials=None):
    """
    Use credentials to create a service to read google drive file meta data.

    :param credentials:  Credentials to use to build an API reader.  If invalid,
        the user will not get access.

    :return:  the service object.
    """
    if not credentials:
        raise RuntimeError("No credentials provided to read meta data")

    return build('drive', 'v3', credentials=credentials, cache_discovery=False)


def read_sheet_values(service, args, render_option='FORMATTED_VALUE'):
    """
    Read the values of the spreadsheet.

    :param service:  The google sheets service to use for reading
    :param args:  command line arguments describing which sheet to read.  It
        can limit reading values to a range of values or to a tab within a sheet.
    :param render_option:  how to read the spreadsheet values.  May be either
        'FORMATTED_VALUE', 'UNFORMATTED_VALUE', 'FORMULA'.

    :return a list of values read for each defined section of the sheet.  Sections
        are tabs or ranges.
    """
    sheet = service.spreadsheets()

    if args.range is None and args.sheet_name is not consts.ALL:
        cell_list = [args.sheet_name]
    elif args.sheet_name is consts.ALL:
        cell_list = consts.SHEET_NAMES
    else:
        cell_list = [args.sheet_name + '!' + args.range]

    results = []
    for cell_range in cell_list:
        result = sheet.values().get(
            spreadsheetId=args.spreadsheet_id,
            range=cell_range,
            majorDimension='ROWS',
            valueRenderOption=render_option
        ).execute()

        values = result.get('values', [])
        results.append((cell_range, values))

    return results


def _process_key(key):
    """
    Helper function to turn upper camel case names into snake case names

    :param key:  The key to transform to snake_case if applicable

    :return:  an acceptable snake case name
    """
    new_key = ''
    for char in key:
        if char.islower() or char == '_':
            new_key += char
        else:
            new_key = new_key + '_' + char.lower()
    return new_key


def _process_pair(key, value_dict):
    """
    Helper to flatten nested dictionary objects

    :param key:  previous key.  value will be appended to newly generated keys
    :param value_dict:  the dictionary object to iterate

    :return:  the flattened dictionary object
    """
    unnested = {}
    for sub_key, value in viewitems(value_dict):
        new_key = _process_key(key + '_' + sub_key)
        unnested[new_key] = value

    return unnested

def read_meta_data(service, args):
    """
    Read meta data about the data dictionary.

    Return the fields specified below and flatten nested dictionaries into
    a single structure.

    :param service:  The google drive service for reading file meta data
    :param args:  Contains the spread sheet id of the file we want meta data for

    :return:  a flat dictionary of meta data fields we are interested in
    """
    fields = ("id, name, version, createdTime, modifiedTime, "
              "lastModifyingUser/displayName, lastModifyingUser/emailAddress")
    results = service.files().get(fileId=args.spreadsheet_id, fields=fields).execute()

    flat_results = {}
    for key, value in viewitems(results):
        if isinstance(value, dict):
            unnested = _process_pair(key, value)
            flat_results.update(unnested)
        else:
            new_key = _process_key(key)
            flat_results[new_key] = value

    return flat_results
