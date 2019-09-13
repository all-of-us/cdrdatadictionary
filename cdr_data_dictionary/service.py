
# Python imports
import logging
import os.path
import pickle

# Third party imports
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Project imports
import cdr_data_dictionary.constants as consts

LOGGER = logging.getLogger(__name__)

def create_drive_credentials(key_filepath):
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
    if not credentials:
        raise RuntimeError("No credentials provided")

    return build('sheets', 'v4', credentials=credentials, cache_discovery=False)


def read_sheet_values(service, args):
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
            spreadsheetId=args.spreadsheet_id, range=cell_range, majorDimension='ROWS'
        ).execute()

        values = result.get('values', [])
        results.append((cell_range, values))

    return results
